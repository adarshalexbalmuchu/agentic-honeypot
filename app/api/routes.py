import logging
from fastapi import APIRouter, Depends
from app.api.schemas import IncomingRequest, APIResponse
from app.api.auth import verify_api_key

from app.core import session_store, orchestrator, detection
from app.core.state_machine import FSMState
from app.agent import response_policy, llm_client, persona
from app.metrics import counters
from app.extraction import extractor
from app.extraction import store as extraction_store
from app.core.termination import finalize_intelligence, mark_callback_sent, terminate_session, cleanup_session
from app.callback.payload_builder import build_callback_payload
from app.callback.sender import send_callback
from app.utils.logging import get_logger
from fastapi.responses import JSONResponse


logger = get_logger(__name__)
router = APIRouter()

MIN_TURNS_FOR_FINALIZATION = 6
MIN_INTEL_TYPES = 2


@router.get(
    "/message", 
    summary="API Usage Guide",
    description="Shows how to correctly use the POST /message endpoint"
)
def api_usage_guide():
    """
    Helpful endpoint that explains correct API usage when someone tries GET /message
    (which causes 405 Method Not Allowed error)
    """
    return JSONResponse(
        status_code=405,
        content={
            "error": "Method Not Allowed",
            "message": "This endpoint only accepts POST requests",
            "correct_usage": {
                "method": "POST",
                "url": "/message",
                "headers": {
                    "Content-Type": "application/json",
                    "x-api-key": "test-api-key-123"
                },
                "body_example": {
                    "sessionId": "your-session-id",
                    "message": {
                        "sender": "user",
                        "text": "Your message here",
                        "timestamp": 1738715600
                    }
                }
            },
            "common_mistakes": [
                "Using GET instead of POST method",
                "Missing x-api-key header", 
                "Wrong endpoint URL (/api/message vs /message)",
                "Missing Content-Type: application/json header"
            ]
        },
        headers={"Allow": "POST"}
    )


def extract_signal_types(signals: list) -> set:
    """Extract signal type names from structured detection signals."""
    return {s.get("type") for s in signals if isinstance(s, dict)}


def build_agent_notes(
    session_id: str,
    turn_count: int,
    detection_signals: list,
) -> str:
    intelligence = extraction_store.get_all_intelligence(session_id)
    notes = []
    
    signal_types = extract_signal_types(detection_signals)

    if "urgency_keywords" in signal_types or "urgency_patterns" in signal_types:
        notes.append("Scammer escalated urgency.")

    if "financial_request_patterns" in signal_types or "financial_keywords" in signal_types:
        notes.append("Scammer requested financial action.")
    
    if "credential_request" in signal_types:
        notes.append("Credential request detected.")
    
    if "impersonation_keywords" in signal_types:
        notes.append("Authority impersonation detected.")

    if intelligence.get("upiIds"):
        notes.append("UPI identifier captured.")

    if intelligence.get("phishingLinks"):
        notes.append("Phishing link captured.")

    if intelligence.get("phoneNumbers"):
        notes.append("Phone number captured.")
    
    if intelligence.get("bankAccounts"):
        notes.append("Bank account captured.")
    
    if intelligence.get("ifscCodes"):
        notes.append("IFSC code captured.")

    notes.append(f"Engaged for {turn_count} turns.")
    return " ".join(notes)


@router.post(
    "/message",
    response_model=APIResponse,
    dependencies=[Depends(verify_api_key)],
)
async def handle_message(request: IncomingRequest) -> APIResponse:
    session_id = request.sessionId
    incoming_text = request.message.text

    # 1. Load or create session
    session_store.create_session(session_id)
    current_state = session_store.get_session_state(session_id)
    
    logger.info(f"[{session_id}] Message received, state={current_state.value}")

    # 2. Terminal guard (hard stop, prevents double callback)
    if orchestrator.is_terminal_state(current_state):
        logger.debug(f"[{session_id}] Terminal state, returning no-op")
        return APIResponse(status="success", reply="Thank you.")

    # 3. Increment metrics
    counters.increment_message_counter(session_id)
    turn_count = counters.get_message_count(session_id)

    # 4. Detection (pure analysis with conversation history context)
    history_dicts = [
        {"text": msg.text, "sender": msg.sender}
        for msg in request.conversationHistory
    ]
    detection_result = detection.analyze_with_history(
        current_message=incoming_text,
        conversation_history=history_dicts,
    )

    # 5. FSM transition decision
    next_state = orchestrator.next_state(
        current_state=current_state,
        detection_result=detection_result,
        turn_count=turn_count,
    )

    if next_state != current_state:
        logger.info(f"[{session_id}] State transition: {current_state.value} -> {next_state.value}")
        session_store.set_session_state(session_id, next_state)
        current_state = next_state

    # 6. Agent engaged behavior
    if current_state == FSMState.AGENT_ENGAGED:
        extractor.extract_intelligence_from_message(session_id, incoming_text)

        # ---- Finalization gate (routes-level) ----
        intel = extraction_store.get_all_intelligence(session_id)
        intel_type_count = sum(1 for v in intel.values() if v)

        if (
            turn_count >= MIN_TURNS_FOR_FINALIZATION
            and intel_type_count >= MIN_INTEL_TYPES
        ):
            new_state = finalize_intelligence(current_state)
            if new_state != current_state:
                logger.info(f"[{session_id}] Intelligence finalized, types={intel_type_count}")
                session_store.set_session_state(session_id, new_state)
                current_state = new_state

    # 7. Callback (exactly once)
    if current_state == FSMState.INTEL_READY:
        intelligence = extraction_store.get_all_intelligence(session_id)

        agent_notes = build_agent_notes(
            session_id=session_id,
            turn_count=turn_count,
            detection_signals=detection_result["signals"],
        )

        payload = build_callback_payload(
            session_id=session_id,
            scam_detected=True,
            total_messages_exchanged=turn_count,
            bank_accounts=intelligence.get("bankAccounts", []),
            upi_ids=intelligence.get("upiIds", []),
            phishing_links=intelligence.get("phishingLinks", []),
            phone_numbers=intelligence.get("phoneNumbers", []),
            suspicious_keywords=intelligence.get("suspiciousKeywords", []),
            agent_notes=agent_notes,
        )

        if send_callback(payload):
            logger.info(f"[{session_id}] Callback sent successfully")
            new_state = mark_callback_sent(current_state)
            session_store.set_session_state(session_id, new_state)
            new_state = terminate_session(new_state)
            session_store.set_session_state(session_id, new_state)
            # Clean up session data to prevent memory leaks
            cleanup_session(session_id)
            logger.info(f"[{session_id}] Session terminated and cleaned up")
        else:
            logger.warning(f"[{session_id}] Callback failed")

        return APIResponse(status="success", reply="Thank you.")

    # 8. Persona drift + reply (only if still engaged)
    if current_state == FSMState.AGENT_ENGAGED:
        if turn_count < 3:
            drift_traits = {"emotional_state": "confused"}
        elif turn_count < 6:
            drift_traits = {"emotional_state": "worried"}
        else:
            drift_traits = {"emotional_state": "anxious"}

        signal_types = extract_signal_types(detection_result["signals"])
        scammer_asking_for_data = (
            "financial_request_patterns" in signal_types
            or "credential_request" in signal_types
        )
        scammer_showing_urgency = (
            "urgency_keywords" in signal_types
            or "urgency_patterns" in signal_types
        )
        
        category = response_policy.select_response_category(
            turn_count=turn_count,
            detected_signals=list(signal_types),
            scammer_asking_for_data=scammer_asking_for_data,
            scammer_showing_urgency=scammer_showing_urgency,
        )

        reply_text = await llm_client.generate_response_async(
            category=category,
            persona_traits={**persona.PERSONA_TRAITS, **drift_traits},
        )

        return APIResponse(status="success", reply=reply_text)

    # 9. Fallback
    return APIResponse(status="success", reply="Okay.")

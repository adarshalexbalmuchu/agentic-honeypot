from typing import Dict, Any
from app.core.state_machine import FSMState, TERMINAL_STATES

MIN_TURNS_FOR_FINALIZATION = 6
MIN_INTEL_TYPES = 2

# Detection score thresholds
SUSPICIOUS_SCORE_THRESHOLD = 3
ENGAGEMENT_SCORE_THRESHOLD = 6
MIN_TURNS_FOR_ENGAGEMENT = 1  # Allow single high-threat messages to trigger engagement


class InvalidStateTransition(Exception):
    """Raised when an illegal FSM transition is attempted."""
    pass


def next_state(
    current_state: FSMState,
    detection_result: Dict[str, Any],
    turn_count: int,
) -> FSMState:
    """
    Determine the next FSM state based on detection analysis.
    
    This is the ONLY place where state transition decisions are made.
    Returns the same state if no transition is warranted.
    
    For extremely dangerous messages (score >= 9 with high-value signals),
    this function can progress through multiple states rapidly.
    """
    if current_state in TERMINAL_STATES:
        return current_state
    
    score = detection_result.get("score", 0)
    signals = detection_result.get("signals", [])
    
    # Extract signal types for easier checking
    signal_types = {s.get("type") for s in signals if isinstance(s, dict)}
    
    # High-value signals that indicate definite scam behavior
    has_credential_request = "credential_request" in signal_types
    has_financial_request = "financial_request_patterns" in signal_types
    has_impersonation = "impersonation_keywords" in signal_types
    
    # Check if this is an extremely dangerous message
    is_extreme_threat = (score >= 9 and (has_credential_request or has_financial_request or has_impersonation))
    
    if current_state == FSMState.INIT:
        new_state = transition_to_normal(current_state)
        # For extreme threats, immediately progress further
        if is_extreme_threat:
            new_state = transition_to_suspicious(new_state)
            new_state = transition_to_agent_engaged(new_state)
        return new_state
    
    if current_state == FSMState.NORMAL:
        # For extreme threats, skip to AGENT_ENGAGED immediately  
        if is_extreme_threat:
            new_state = transition_to_suspicious(current_state)
            return transition_to_agent_engaged(new_state)
        # Move to SUSPICIOUS if score exceeds threshold
        if score >= SUSPICIOUS_SCORE_THRESHOLD:
            return transition_to_suspicious(current_state)
        return current_state
    
    if current_state == FSMState.SUSPICIOUS:
        # Move to AGENT_ENGAGED if:
        # - Score is high enough AND
        # - We've seen enough turns AND  
        # - High-value signals present
        # OR for extremely dangerous messages (score >= 9), engage immediately
        if (
            (score >= ENGAGEMENT_SCORE_THRESHOLD
            and turn_count >= MIN_TURNS_FOR_ENGAGEMENT
            and (has_credential_request or has_financial_request or has_impersonation))
            or 
            (score >= 9 and (has_credential_request or has_financial_request or has_impersonation))
        ):
            return transition_to_agent_engaged(current_state)
        return current_state
    
    # AGENT_ENGAGED -> INTEL_READY is handled by termination.finalize_intelligence
    # INTEL_READY -> CALLBACK_SENT is handled by termination.mark_callback_sent
    # CALLBACK_SENT -> TERMINATED is handled by termination.terminate_session
    
    return current_state


def transition_to_normal(current_state: FSMState) -> FSMState:
    if current_state != FSMState.INIT:
        raise InvalidStateTransition(
            f"Cannot transition to NORMAL from {current_state}"
        )
    return FSMState.NORMAL


def transition_to_suspicious(current_state: FSMState) -> FSMState:
    if current_state != FSMState.NORMAL:
        raise InvalidStateTransition(
            f"Cannot transition to SUSPICIOUS from {current_state}"
        )
    return FSMState.SUSPICIOUS


def transition_to_agent_engaged(current_state: FSMState) -> FSMState:
    if current_state != FSMState.SUSPICIOUS:
        raise InvalidStateTransition(
            f"Cannot transition to AGENT_ENGAGED from {current_state}"
        )
    return FSMState.AGENT_ENGAGED


def transition_to_intel_ready(current_state: FSMState) -> FSMState:
    if current_state != FSMState.AGENT_ENGAGED:
        raise InvalidStateTransition(
            f"Cannot transition to INTEL_READY from {current_state}"
        )
    return FSMState.INTEL_READY


def transition_to_callback_sent(current_state: FSMState) -> FSMState:
    if current_state != FSMState.INTEL_READY:
        raise InvalidStateTransition(
            f"Cannot transition to CALLBACK_SENT from {current_state}"
        )
    return FSMState.CALLBACK_SENT


def transition_to_terminated(current_state: FSMState) -> FSMState:
    if current_state != FSMState.CALLBACK_SENT:
        raise InvalidStateTransition(
            f"Cannot transition to TERMINATED from {current_state}"
        )
    return FSMState.TERMINATED


def is_terminal_state(state: FSMState) -> bool:
    return state in TERMINAL_STATES

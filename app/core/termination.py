from app.core.state_machine import FSMState
from app.core.orchestrator import (
    transition_to_intel_ready,
    transition_to_callback_sent,
    transition_to_terminated,
)
from app.core import session_store
from app.extraction import store as extraction_store
from app.metrics import counters
from app.callback import sender


def finalize_intelligence(current_state: FSMState) -> FSMState:
    """
    Explicit finalization step.
    Moves AGENT_ENGAGED → INTEL_READY only.
    """
    if current_state != FSMState.AGENT_ENGAGED:
        return current_state
    return transition_to_intel_ready(current_state)


def mark_callback_sent(current_state: FSMState) -> FSMState:
    """
    Marks that callback has been successfully sent.
    """
    if current_state != FSMState.INTEL_READY:
        return current_state
    return transition_to_callback_sent(current_state)


def terminate_session(current_state: FSMState) -> FSMState:
    """
    Final termination.
    """
    if current_state != FSMState.CALLBACK_SENT:
        return current_state
    return transition_to_terminated(current_state)


def cleanup_session(session_id: str) -> None:
    """
    Clean up all in-memory data for a terminated session.
    Call this after termination to prevent memory leaks.
    """
    session_store.delete_session(session_id)
    extraction_store.delete_session_intelligence(session_id)
    counters.delete_counter(session_id)
    sender.clear_sent_session(session_id)

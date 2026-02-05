from app.core.state_machine import FSMState, TERMINAL_STATES

MIN_TURNS_FOR_FINALIZATION = 6
MIN_INTEL_TYPES = 2

class InvalidStateTransition(Exception):
    """Raised when an illegal FSM transition is attempted."""
    pass


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

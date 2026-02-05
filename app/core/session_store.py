from typing import Dict, Set
from app.core.state_machine import FSMState


# In-memory session state store (opaque)
_sessions: Dict[str, FSMState] = {}

# Lightweight set of terminated session IDs (prevents re-creation)
_terminated_sessions: Set[str] = set()


def create_session(session_id: str) -> None:
    if session_id in _terminated_sessions:
        return  # Don't recreate terminated sessions
    if session_id not in _sessions:
        _sessions[session_id] = FSMState.INIT


def session_exists(session_id: str) -> bool:
    return session_id in _sessions or session_id in _terminated_sessions


def get_session_state(session_id: str) -> FSMState:
    if session_id in _terminated_sessions:
        return FSMState.TERMINATED
    if session_id not in _sessions:
        create_session(session_id)
    return _sessions[session_id]


def set_session_state(session_id: str, state: FSMState) -> None:
    if session_id in _terminated_sessions:
        return  # Can't modify terminated sessions
    if session_id not in _sessions:
        create_session(session_id)
    _sessions[session_id] = state


def delete_session(session_id: str) -> None:
    """Remove session from active store but mark as terminated."""
    if session_id in _sessions:
        del _sessions[session_id]
    _terminated_sessions.add(session_id)


def is_session_terminated(session_id: str) -> bool:
    return session_id in _terminated_sessions

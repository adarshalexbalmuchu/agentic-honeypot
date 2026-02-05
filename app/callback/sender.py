import os
import time
from typing import Dict, Any, Set
import httpx
from app.utils.logging import get_logger


logger = get_logger(__name__)

# GUVI Hackathon evaluation endpoint (MANDATORY)
CALLBACK_URL = os.getenv("CALLBACK_URL", "https://hackathon.guvi.in/api/updateHoneyPotFinalResult")
CALLBACK_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2


# In-memory idempotency guard (session-level)
_sent_sessions: Set[str] = set()


def send_callback(payload: Dict[str, Any]) -> bool:
    session_id = payload.get("sessionId")
    if not session_id:
        logger.warning("Callback payload missing sessionId")
        return False

    if session_id in _sent_sessions:
        logger.debug(f"[{session_id}] Callback already sent (idempotency guard)")
        return True

    success = _attempt_send_with_retry(payload, session_id)
    if success:
        _sent_sessions.add(session_id)

    return success


def _attempt_send_with_retry(payload: Dict[str, Any], session_id: str) -> bool:
    if not CALLBACK_URL:
        logger.error("CALLBACK_URL not configured")
        return False

    for attempt in range(MAX_RETRIES):
        try:
            logger.debug(f"[{session_id}] Callback attempt {attempt + 1}/{MAX_RETRIES}")
            response = httpx.post(
                CALLBACK_URL,
                json=payload,
                timeout=CALLBACK_TIMEOUT,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code in (200, 201, 202):
                return True

            if response.status_code >= 500 and attempt < MAX_RETRIES - 1:
                logger.warning(f"[{session_id}] Server error {response.status_code}, retrying...")
                time.sleep(RETRY_BACKOFF_BASE ** attempt)
                continue

            logger.error(f"[{session_id}] Callback failed with status {response.status_code}")
            return False

        except (httpx.TimeoutException, httpx.RequestError) as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"[{session_id}] Request error: {e}, retrying...")
                time.sleep(RETRY_BACKOFF_BASE ** attempt)
                continue
            logger.error(f"[{session_id}] Callback failed after {MAX_RETRIES} attempts: {e}")
            return False

        except Exception as e:
            logger.error(f"[{session_id}] Unexpected error in callback: {e}")
            return False

    return False


def has_callback_been_sent(session_id: str) -> bool:
    return session_id in _sent_sessions


def clear_sent_session(session_id: str) -> None:
    """Remove session from sent registry (for cleanup)."""
    _sent_sessions.discard(session_id)

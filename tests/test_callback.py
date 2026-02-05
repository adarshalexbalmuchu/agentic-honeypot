from unittest.mock import patch, MagicMock
from app.callback.payload_builder import build_callback_payload
from app.callback.sender import send_callback, has_callback_been_sent


def test_payload_builder_structure():
    payload = build_callback_payload(
        session_id="s1",
        scam_detected=True,
        total_messages_exchanged=5,
        bank_accounts=[],
        upi_ids=["test@upi"],
        phishing_links=[],
        phone_numbers=[],
        suspicious_keywords=["urgent", "verify"],
        agent_notes="done",
    )

    assert payload["sessionId"] == "s1"
    assert "extractedIntelligence" in payload
    assert "upiIds" in payload["extractedIntelligence"]
    assert "suspiciousKeywords" in payload["extractedIntelligence"]


@patch("app.callback.sender.CALLBACK_URL", "http://test-callback.example.com")
@patch("app.callback.sender.httpx.post")
def test_callback_sent_once(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    payload = build_callback_payload(
        session_id="s-idem",
        scam_detected=True,
        total_messages_exchanged=3,
        bank_accounts=[],
        upi_ids=[],
        phishing_links=[],
        phone_numbers=[],
        suspicious_keywords=[],
        agent_notes="",
    )

    assert send_callback(payload) is True
    assert send_callback(payload) is True
    assert mock_post.call_count == 1
    assert has_callback_been_sent("s-idem") is True


@patch("app.callback.sender.CALLBACK_URL", "http://test-callback.example.com")
@patch("app.callback.sender.httpx.post")
def test_callback_failure_does_not_mark_sent(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    payload = build_callback_payload(
        session_id="s-fail",
        scam_detected=True,
        total_messages_exchanged=1,
        bank_accounts=[],
        upi_ids=[],
        phishing_links=[],
        phone_numbers=[],
        suspicious_keywords=[],
        agent_notes="",
    )

    assert send_callback(payload) is False
    assert has_callback_been_sent("s-fail") is False

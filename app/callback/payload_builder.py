from typing import Dict, List, Any


def build_callback_payload(
    session_id: str,
    scam_detected: bool,
    total_messages_exchanged: int,
    bank_accounts: List[str],
    upi_ids: List[str],
    phishing_links: List[str],
    phone_numbers: List[str],
    suspicious_keywords: List[str],
    agent_notes: str,
) -> Dict[str, Any]:
    """
    Build the final callback payload matching GUVI evaluation format.
    This function performs formatting ONLY.
    """

    return {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages_exchanged,
        "extractedIntelligence": {
            "bankAccounts": bank_accounts or [],
            "upiIds": upi_ids or [],
            "phishingLinks": phishing_links or [],
            "phoneNumbers": phone_numbers or [],
            "suspiciousKeywords": suspicious_keywords or [],
        },
        "agentNotes": agent_notes or "",
    }

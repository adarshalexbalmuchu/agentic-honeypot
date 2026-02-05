from typing import Dict, List, Optional
import re


URGENCY_KEYWORDS = {
    "urgent",
    "immediately",
    "today",
    "now",
    "asap",
    "limited time",
    "act now",
    "last chance",
    "expire",
    "expired",
    "expiring",
}

CREDENTIAL_KEYWORDS = {
    "otp",
    "pin",
    "password",
    "cvv",
    "card number",
}

FINANCIAL_KEYWORDS = {
    "upi",
    "bank",
    "account",
    "account number",
    "bank details",
    "transfer",
    "payment",
    "deposit",
    "refund",
}

IMPERSONATION_KEYWORDS = {
    "bank",
    "government",
    "police",
    "court",
    "income tax",
    "customs",
    "officer",
    "official",
    "customer care",
    "support team",
}


URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"\+?\d{10,}", re.IGNORECASE)

URGENCY_PATTERNS = [
    re.compile(r"\bwithin\s+\d+\s+hours?\b", re.IGNORECASE),
    re.compile(r"\bimmediate\s+action\b", re.IGNORECASE),
]

FINANCIAL_REQUEST_PATTERNS = [
    re.compile(r"\bshare\s+(?:upi|account|bank|card)\b", re.IGNORECASE),
    re.compile(r"\bsend\s+(?:money|payment|amount)\b", re.IGNORECASE),
    re.compile(r"\bpay\s+(?:now|immediately|today)\b", re.IGNORECASE),
]


# -----------------------------
# Detection entry point
# -----------------------------

def analyze_message(message_text: str) -> Dict[str, object]:
    """
    Analyze a single message and return scam-related signals.

    This function is PURE:
    - No state
    - No decisions
    - No thresholds
    - No side effects
    """

    text = message_text.lower()

    signals: List[Dict[str, object]] = []
    score = 0

    # ---- Keyword analysis ----

    urgency_hits = [kw for kw in URGENCY_KEYWORDS if kw in text]
    if urgency_hits:
        signals.append({
            "type": "urgency_keywords",
            "matches": urgency_hits,
            "count": len(urgency_hits),
        })
        score += len(urgency_hits)

    credential_hits = [kw for kw in CREDENTIAL_KEYWORDS if kw in text]
    if credential_hits:
        signals.append({
            "type": "credential_request",
            "matches": credential_hits,
            "count": len(credential_hits),
        })
        score += len(credential_hits) * 2

    financial_hits = [kw for kw in FINANCIAL_KEYWORDS if kw in text]
    if financial_hits:
        signals.append({
            "type": "financial_keywords",
            "matches": financial_hits,
            "count": len(financial_hits),
        })
        score += len(financial_hits) * 2

    impersonation_hits = [kw for kw in IMPERSONATION_KEYWORDS if kw in text]
    if impersonation_hits:
        signals.append({
            "type": "impersonation_keywords",
            "matches": impersonation_hits,
            "count": len(impersonation_hits),
        })
        score += len(impersonation_hits) * 2

    # ---- Pattern analysis ----

    urgency_pattern_hits = sum(1 for p in URGENCY_PATTERNS if p.search(text))
    if urgency_pattern_hits:
        signals.append({
            "type": "urgency_patterns",
            "count": urgency_pattern_hits,
        })
        score += urgency_pattern_hits * 2

    financial_request_hits = sum(1 for p in FINANCIAL_REQUEST_PATTERNS if p.search(text))
    if financial_request_hits:
        signals.append({
            "type": "financial_request_patterns",
            "count": financial_request_hits,
        })
        score += financial_request_hits * 3

    if URL_PATTERN.search(text):
        signals.append({
            "type": "contains_url",
            "count": 1,
        })
        score += 2

    if PHONE_PATTERN.search(text):
        signals.append({
            "type": "contains_phone_number",
            "count": 1,
        })
        score += 1

    # ---- Output (data only) ----

    return {
        "score": score,
        "signals": signals,
    }


def analyze_with_history(
    current_message: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, object]:
    """
    Analyze current message with optional conversation history context.
    
    Applies cumulative scoring for pattern escalation across the conversation.
    This function is PURE: no state, no side effects.
    """
    # Analyze current message
    result = analyze_message(current_message)
    
    if not conversation_history:
        return result
    
    # Analyze historical patterns for cumulative scoring
    history_score_bonus = 0
    urgency_count_in_history = 0
    financial_count_in_history = 0
    
    for msg in conversation_history[-10:]:  # Last 10 messages only
        text = msg.get("text", "").lower() if isinstance(msg, dict) else ""
        
        # Count urgency escalation
        if any(kw in text for kw in URGENCY_KEYWORDS):
            urgency_count_in_history += 1
        
        # Count financial pressure
        if any(kw in text for kw in FINANCIAL_KEYWORDS):
            financial_count_in_history += 1
    
    # Bonus for repeated urgency (escalation pattern)
    if urgency_count_in_history >= 3:
        history_score_bonus += 2
        result["signals"].append({
            "type": "urgency_escalation",
            "count": urgency_count_in_history,
        })
    
    # Bonus for persistent financial pressure
    if financial_count_in_history >= 2:
        history_score_bonus += 2
        result["signals"].append({
            "type": "persistent_financial_pressure",
            "count": financial_count_in_history,
        })
    
    result["score"] += history_score_bonus
    result["history_analyzed"] = True
    
    return result

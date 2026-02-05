from app.extraction import patterns, validators, store


# Suspicious keywords to extract (for intelligence reporting)
SUSPICIOUS_KEYWORDS = {
    "urgent", "immediately", "verify", "blocked", "suspended",
    "otp", "pin", "password", "cvv", "card number",
    "transfer", "payment", "deposit", "refund",
    "bank", "account", "upi",
    "police", "arrest", "legal", "court",
    "government", "income tax", "customs",
    "last chance", "act now", "expire", "limited time",
    "click here", "verify now", "account blocked",
    "share", "send money", "pay now",
}


def extract_intelligence_from_message(session_id: str, message_text: str) -> None:
    if not message_text:
        return

    _extract_upi_ids(session_id, message_text)
    _extract_phone_numbers(session_id, message_text)
    _extract_urls(session_id, message_text)
    _extract_bank_accounts(session_id, message_text)
    _extract_suspicious_keywords(session_id, message_text)


def _extract_suspicious_keywords(session_id: str, text: str) -> None:
    text_lower = text.lower()
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text_lower:
            store.add_suspicious_keyword(session_id, keyword)


def _extract_upi_ids(session_id: str, text: str) -> None:
    for candidate in patterns.UPI_ID_PATTERN.findall(text):
        if validators.is_valid_upi_id(candidate):
            store.add_upi_id(session_id, candidate)


def _extract_phone_numbers(session_id: str, text: str) -> None:
    for candidate in patterns.PHONE_NUMBER_PATTERN.findall(text):
        if validators.is_valid_phone_number(candidate):
            normalized = validators.normalize_phone_number(candidate)
            store.add_phone_number(session_id, normalized)


def _extract_urls(session_id: str, text: str) -> None:
    for candidate in patterns.URL_PATTERN.findall(text):
        if validators.is_valid_url(candidate):
            store.add_url(session_id, candidate)


def _extract_bank_accounts(session_id: str, text: str) -> None:
    for candidate in patterns.BANK_ACCOUNT_PATTERN.findall(text):
        if validators.is_valid_bank_account_number(candidate):
            store.add_bank_account(session_id, candidate)

    for candidate in patterns.IFSC_CODE_PATTERN.findall(text):
        if validators.is_valid_ifsc_code(candidate):
            store.add_ifsc_code(session_id, candidate)

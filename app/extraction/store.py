from typing import Dict, Set, List

_intelligence_store: Dict[str, Dict[str, Set[str]]] = {}


def _ensure_session(session_id: str) -> None:
    if session_id not in _intelligence_store:
        _intelligence_store[session_id] = {
            "upi_ids": set(),
            "phone_numbers": set(),
            "urls": set(),
            "bank_accounts": set(),
            "ifsc_codes": set(),
            "suspicious_keywords": set(),
        }


def add_upi_id(session_id: str, value: str) -> None:
    _ensure_session(session_id)
    _intelligence_store[session_id]["upi_ids"].add(value)


def add_phone_number(session_id: str, value: str) -> None:
    _ensure_session(session_id)
    _intelligence_store[session_id]["phone_numbers"].add(value)


def add_url(session_id: str, value: str) -> None:
    _ensure_session(session_id)
    _intelligence_store[session_id]["urls"].add(value)


def add_bank_account(session_id: str, value: str) -> None:
    _ensure_session(session_id)
    _intelligence_store[session_id]["bank_accounts"].add(value)


def add_ifsc_code(session_id: str, value: str) -> None:
    _ensure_session(session_id)
    _intelligence_store[session_id]["ifsc_codes"].add(value)


def add_suspicious_keyword(session_id: str, value: str) -> None:
    _ensure_session(session_id)
    _intelligence_store[session_id]["suspicious_keywords"].add(value.lower())


def get_all_intelligence(session_id: str) -> Dict[str, List[str]]:
    _ensure_session(session_id)
    data = _intelligence_store[session_id]
    return {
        "upiIds": list(data["upi_ids"]),
        "phoneNumbers": list(data["phone_numbers"]),
        "phishingLinks": list(data["urls"]),
        "bankAccounts": list(data["bank_accounts"]),
        "ifscCodes": list(data["ifsc_codes"]),
        "suspiciousKeywords": list(data["suspicious_keywords"]),
    }


def has_any_intelligence(session_id: str) -> bool:
    _ensure_session(session_id)
    data = _intelligence_store[session_id]
    return any(len(values) > 0 for values in data.values())


def delete_session_intelligence(session_id: str) -> None:
    if session_id in _intelligence_store:
        del _intelligence_store[session_id]

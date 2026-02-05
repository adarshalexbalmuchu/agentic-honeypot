import os
from fastapi import HTTPException, Header


def get_api_key() -> str:
    """Get API key from environment, raising if not set."""
    key = os.getenv("API_KEY")
    if not key:
        raise RuntimeError("API_KEY environment variable is not set")
    return key


def verify_api_key(x_api_key: str = Header(...)) -> None:
    expected_key = get_api_key()
    if x_api_key != expected_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

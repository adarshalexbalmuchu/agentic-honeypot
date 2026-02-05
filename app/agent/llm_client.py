import os
from typing import Optional
from app.agent.response_policy import ResponseCategory


def _get_gemini_key():
    return os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-1.5-flash"


FALLBACK_RESPONSES = {
    ResponseCategory.CONFUSION: [
        "I'm not sure I understand what you mean.",
        "Sorry, can you explain that again?",
    ],
    ResponseCategory.CLARIFICATION: [
        "What exactly do I need to do?",
        "Could you explain it more simply?",
    ],
    ResponseCategory.HESITATION: [
        "I'm not sure about this.",
        "This makes me a bit nervous.",
    ],
    ResponseCategory.MILD_CONCERN: [
        "I'm worried something might be wrong.",
    ],
    ResponseCategory.DELAY_TACTIC: [
        "Can I do this later? I'm busy right now.",
    ],
    ResponseCategory.PARTIAL_COMPLIANCE: [
        "Let me check, I might have it somewhere.",
    ],
    ResponseCategory.MISTAKE_ADMISSION: [
        "Sorry, I think I messed that up.",
    ],
    ResponseCategory.ALTERNATIVE_REQUEST: [
        "Is there an easier way to do this?",
    ],
    ResponseCategory.SOFT_FAILURE: [
    "It says something went wrong.",
    "I tried but it didn’t go through.",
    "I might have entered it incorrectly.",
    "It’s asking me to do something else now.",
    ],
}


_fallback_index = {}


def get_fallback_response(category: ResponseCategory) -> str:
    idx = _fallback_index.get(category, 0)
    responses = FALLBACK_RESPONSES.get(category, ["Okay."])
    _fallback_index[category] = idx + 1
    return responses[idx % len(responses)]


def should_use_gemini(category: ResponseCategory) -> bool:
    """Enable Gemini for all response categories when API key is available."""
    return bool(_get_gemini_key())


def build_prompt(category: ResponseCategory, persona_traits: dict) -> str:
    category_name = category.name.lower().replace("_", " ")
    return (
        f"You are a person with {persona_traits['digital_literacy']} digital literacy "
        f"who feels {persona_traits['emotional_state']}.\n\n"
        f"Write ONE short reply (1–2 sentences) that shows {category_name}.\n\n"
        "Rules:\n"
        "- Simple language\n"
        "- No emojis\n"
        "- No markdown\n"
        "- Sound like a real person\n\n"
        "Reply:"
    )


def call_gemini(prompt: str) -> Optional[str]:
    try:
        import google.generativeai as genai
        genai.configure(api_key=_get_gemini_key())
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 50, "temperature": 0.6},
        )
        return response.text.strip() if response and response.text else None
    except Exception:
        return None


async def call_gemini_async(prompt: str) -> Optional[str]:
    """Non-blocking Gemini API call using thread executor."""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, call_gemini, prompt)
        return result
    except Exception:
        return None


def generate_response(
    category: ResponseCategory,
    persona_traits: dict,
) -> str:

    if not should_use_gemini(category):
        return get_fallback_response(category)

    prompt = build_prompt(category, persona_traits)
    gemini_response = call_gemini(prompt)

    return gemini_response or get_fallback_response(category)


async def generate_response_async(
    category: ResponseCategory,
    persona_traits: dict,
) -> str:
    """Async version of generate_response for non-blocking LLM calls."""
    if not should_use_gemini(category):
        return get_fallback_response(category)

    prompt = build_prompt(category, persona_traits)
    gemini_response = await call_gemini_async(prompt)

    return gemini_response or get_fallback_response(category)

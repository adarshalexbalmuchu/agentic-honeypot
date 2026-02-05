import os
from typing import Optional
from app.agent.response_policy import ResponseCategory


def _get_gemini_key():
    return os.getenv("GEMINI_API_KEY")

GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"]


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
        f"You are roleplaying as a person with {persona_traits['digital_literacy']} digital literacy "
        f"who feels {persona_traits['emotional_state']}. A scammer is trying to trick you.\n\n"
        f"Write ONE short reply (1-2 complete sentences) that shows {category_name}.\n\n"
        "Rules:\n"
        "- Use simple everyday language\n"
        "- No emojis, no markdown\n"
        "- Sound like a real confused person talking on the phone\n"
        "- Must be at least 8 words long\n\n"
        "Your reply:"
    )


def call_gemini(prompt: str) -> Optional[str]:
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=_get_gemini_key())
        for model_name in GEMINI_MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=200,
                        temperature=0.7,
                        thinking_config=types.ThinkingConfig(thinking_budget=0),
                    ),
                )
                if response and response.text:
                    return response.text.strip()
            except Exception:
                continue
        return None
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

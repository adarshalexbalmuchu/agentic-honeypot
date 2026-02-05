import os
from typing import Optional
import hashlib
import time
from functools import lru_cache
from app.agent.response_policy import ResponseCategory


def _get_gemini_key():
    return os.getenv("GEMINI_API_KEY")

# Optimized model order - fastest first
GEMINI_MODELS = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash"]

# Simple response cache to avoid duplicate API calls
_response_cache = {}
_cache_ttl = 300  # 5 minutes

# Connection reuse
_client_cache = None


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
    """Optimized prompt builder with shorter, more efficient prompts"""
    category_name = category.name.lower().replace("_", " ")
    return (
        f"You are a {persona_traits['digital_literacy']} tech user who feels {persona_traits['emotional_state']}. "
        f"A scammer contacted you. Reply with {category_name} in 8-20 words. "
        "Sound natural and confused:"
    )


def _get_cached_client():
    """Reuse client connection for better performance"""
    global _client_cache
    if _client_cache is None:
        try:
            from google import genai
            _client_cache = genai.Client(api_key=_get_gemini_key())
        except Exception:
            pass
    return _client_cache

def _cache_key(prompt: str, model: str) -> str:
    """Generate cache key for responses"""
    return hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()

def call_gemini(prompt: str) -> Optional[str]:
    """Optimized Gemini API call with caching and connection reuse"""
    try:
        from google.genai import types
        
        # Check cache first
        cache_key = _cache_key(prompt, GEMINI_MODELS[0])
        if cache_key in _response_cache:
            cached_response, timestamp = _response_cache[cache_key]
            if time.time() - timestamp < _cache_ttl:
                return cached_response
            else:
                del _response_cache[cache_key]
        
        client = _get_cached_client()
        if not client:
            return None
            
        # Try fastest model first
        for model_name in GEMINI_MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=100,  # Reduced for faster response
                        temperature=0.8,         # Slightly more creative
                        thinking_config=types.ThinkingConfig(thinking_budget=0),
                    ),
                )
                if response and response.text:
                    result = response.text.strip()
                    # Cache successful response
                    _response_cache[cache_key] = (result, time.time())
                    # Clean old cache entries
                    if len(_response_cache) > 100:
                        oldest_keys = sorted(_response_cache.keys(), 
                                           key=lambda k: _response_cache[k][1])[:20]
                        for old_key in oldest_keys:
                            del _response_cache[old_key]
                    return result
            except Exception as e:
                # Try next model
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
    """Generate response with optimized caching"""
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

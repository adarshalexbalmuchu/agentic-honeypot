import os
from typing import Optional
import hashlib
import time
from functools import lru_cache
import threading
from collections import defaultdict
from app.agent.response_policy import ResponseCategory


def _get_gemini_key():
    return os.getenv("GEMINI_API_KEY")

# OPTIMIZED: Use fresh quotas first, avoid overused models
GEMINI_MODELS = [
    "gemini-2.5-flash-lite",
    "gemma-2-2b-it",
    "gemini-2.5-flash",
]

# Rate limiting tracking
_request_times = defaultdict(list)
_rate_limit_lock = threading.Lock()

# Model quotas (RPM limits) - increased to maximize API usage
MODEL_LIMITS = {
    "gemini-2.5-flash-lite": 15,
    "gemma-2-2b-it": 45,
    "gemini-2.5-flash": 8,
}

# Simple response cache to avoid duplicate API calls
_response_cache = {}
_cache_ttl = 600

# Connection reuse
_client_cache = None


FALLBACK_RESPONSES = {
    ResponseCategory.CONFUSION: [
        "Wait, are you really from the company? I'm a bit confused.",
        "Sorry, I don't understand. What exactly do you mean?",
        "I'm not sure what you're asking for. Can you explain?",
        "This is confusing. Are you sure this is right?",
        "I don't get it. Why do you need that information?",
    ],
    ResponseCategory.CLARIFICATION: [
        "What exactly do I need to do? I'm not clear on the steps.",
        "Could you explain it more simply? I'm not tech-savvy.",
        "I'm confused about what you're asking. Can you be clearer?",
        "Wait, which account are you talking about? I have several.",
        "Could you repeat that? I didn't catch what you said.",
    ],
    ResponseCategory.HESITATION: [
        "Uh, I'm not sure about this. I think I need to check with someone.",
        "This makes me a bit nervous. Is this really necessary?",
        "I don't know... this doesn't feel right to me.",
        "Hmm, I'm hesitant. Can I call you back later?",
        "I'm not comfortable with this. Are you sure it's safe?",
    ],
    ResponseCategory.MILD_CONCERN: [
        "Oh, that's a bit concerning. I'm not sure I understand.",
        "I'm worried something might be wrong. What's happening?",
        "This is making me nervous. Is my account really at risk?",
        "Wait, is this serious? I'm getting worried now.",
        "I don't like the sound of this. What should I do?",
    ],
    ResponseCategory.DELAY_TACTIC: [
        "Can I do this later? I'm busy with something right now.",
        "I'm at work. Can we do this after I get home?",
        "Uh, could you repeat that? My connection's a bit spotty today.",
        "Hold on, someone's at the door. Can you wait a minute?",
        "Can I call you back in an hour? I'm in the middle of something.",
    ],
    ResponseCategory.PARTIAL_COMPLIANCE: [
        "Let me check, I might have it somewhere. Give me a second.",
        "Okay, I think I have that information. Let me look for it.",
        "I wrote it down somewhere... just trying to find it now.",
        "Let me see... I think I remember where I put that.",
        "Hold on, I'm looking through my papers to find it.",
    ],
    ResponseCategory.MISTAKE_ADMISSION: [
        "Oh no, sorry, I think I messed that up. Wait, what was it again?",
        "Oops, I might have given you the wrong thing. Let me try again.",
        "Sorry, I'm not very good with this tech stuff. Did I do it wrong?",
        "I think I made a mistake. Can you tell me what to do again?",
        "Wait, that didn't work. What am I supposed to do?",
    ],
    ResponseCategory.ALTERNATIVE_REQUEST: [
        "Is there an easier way to do this? This seems complicated.",
        "Can I just come to the branch instead? That would be easier.",
        "Is there a simpler method? I'm not good with phone banking.",
        "Could I do this online instead? I prefer using my computer.",
        "Can my son help me with this? He knows more about these things.",
    ],
    ResponseCategory.SOFT_FAILURE: [
        "Hmm, it says something went wrong. What does that mean?",
        "I tried but it didn't go through. Is there a problem?",
        "It's giving me an error message. Should I try again?",
        "I might have entered it incorrectly. Can you help me?",
        "It's asking me to do something else now. What should I do?",
        "The app isn't working properly. Is this normal?",
    ],
}


_fallback_index = {}


def get_fallback_response(category: ResponseCategory) -> str:
    idx = _fallback_index.get(category, 0)
    responses = FALLBACK_RESPONSES.get(category, ["Okay."])
    _fallback_index[category] = idx + 1
    return responses[idx % len(responses)]


def should_use_gemini(category: ResponseCategory) -> bool:
    return bool(_get_gemini_key())


def _can_make_request(model_name: str) -> bool:
    with _rate_limit_lock:
        now = time.time()
        minute_ago = now - 60
        _request_times[model_name] = [
            t for t in _request_times[model_name] if t > minute_ago
        ]
        limit = MODEL_LIMITS.get(model_name, 5)
        return len(_request_times[model_name]) < limit

def _record_request(model_name: str):
    with _rate_limit_lock:
        _request_times[model_name].append(time.time())

def get_quota_status() -> dict:
    with _rate_limit_lock:
        status = {}
        now = time.time()
        minute_ago = now - 60
        for model, limit in MODEL_LIMITS.items():
            recent_requests = [
                t for t in _request_times[model] if t > minute_ago
            ]
            status[model] = {
                "requests_last_minute": len(recent_requests),
                "rpm_limit": limit,
                "utilization_percent": round((len(recent_requests) / limit) * 100, 1)
            }
        return status

def build_prompt(category: ResponseCategory, persona_traits: dict) -> str:
    category_name = category.name.lower().replace("_", " ")
    return (
        f"You are a {persona_traits['digital_literacy']} tech user who feels {persona_traits['emotional_state']}. "
        f"A scammer contacted you. Reply with {category_name} in 8-20 words. "
        "Sound natural and confused:"
    )


def _get_cached_client():
    global _client_cache
    if _client_cache is None:
        try:
            from google import genai
            _client_cache = genai.Client(api_key=_get_gemini_key())
        except Exception:
            pass
    return _client_cache

def _cache_key(prompt: str, model: str) -> str:
    return hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()

def call_gemini(prompt: str) -> Optional[str]:
    try:
        from google.genai import types
        cache_key = _cache_key(prompt, "cached")
        if cache_key in _response_cache:
            cached_response, timestamp = _response_cache[cache_key]
            if time.time() - timestamp < _cache_ttl:
                return cached_response
            else:
                del _response_cache[cache_key]
        client = _get_cached_client()
        if not client:
            return None
        for model_name in GEMINI_MODELS:
            if not _can_make_request(model_name):
                continue
            try:
                _record_request(model_name)
                config = types.GenerateContentConfig(
                    max_output_tokens=60,
                    temperature=0.95,
                    thinking_config=types.ThinkingConfig(thinking_budget=0) if "gemini" in model_name else None,
                )
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )
                if response and response.text:
                    result = response.text.strip()
                    _response_cache[cache_key] = (result, time.time())
                    return result
            except Exception:
                continue
        return None
    except Exception:
        return None


async def call_gemini_async(prompt: str) -> Optional[str]:
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
    if not should_use_gemini(category):
        return get_fallback_response(category)
    prompt = build_prompt(category, persona_traits)
    gemini_response = await call_gemini_async(prompt)
    return gemini_response or get_fallback_response(category)

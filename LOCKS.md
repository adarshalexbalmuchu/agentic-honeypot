# SYSTEM LOCKS (DO NOT CHANGE)

## API
- Framework: FastAPI
- Response schema: deterministic JSON only
- LLM never controls JSON

## STATE MACHINE
States:
INIT
NORMAL
SUSPICIOUS
AGENT_ENGAGED
INTEL_READY
CALLBACK_SENT
TERMINATED

State transitions are one-way only.

## SCAM DETECTION
- Rule-based scoring
- Minimum turns before detection: __
- Threshold: __

## GPT ROLE
- Persona text generation only
- No extraction
- No decisions
- No state changes

## EXTRACTION
- Regex + validation only
- No LLM authority

## CALLBACK
- Sent once per conversation
- Idempotent
- Retry with backoff

## DEPLOYMENT
- Free tier
- Always-on

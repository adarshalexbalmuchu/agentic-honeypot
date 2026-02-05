# Agentic Honeypot API

This project implements an Agentic Honeypot system for detecting and engaging scam attempts, extracting structured intelligence, and reporting results via a mandatory callback.

## Features
- Finite State Machine–driven lifecycle
- Rule-based scam detection
- Autonomous engagement agent
- Deterministic intelligence extraction
- Idempotent callback mechanism
- Secure API access via API key

## Tech Stack
- FastAPI
- Python 3.10
- Gemini (optional, free tier)
- In-memory state & storage

## Running Locally

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
Install dependencies

pip install -r requirements.txt
Set environment variables

cp .env.example .env
Run server

uvicorn app.main:app --reload
API will be available at:

http://localhost:8000
Health Check
GET /health
Main Endpoint
POST /message
Headers:
  x-api-key: <API_KEY>
Deployment
The project can be deployed on Render or Railway using the provided Dockerfile.

#!/bin/bash
# Production startup script for Agentic Honeypot API
# Ensures environment variables are loaded correctly

cd /workspaces/agentic-honeypot

# Activate virtual environment
source .venv/bin/activate

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "❌ Warning: .env file not found"
fi

# Verify critical environment variables
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ ERROR: GEMINI_API_KEY not set"
    exit 1
fi

if [ -z "$API_KEY" ]; then
    echo "❌ ERROR: API_KEY not set" 
    exit 1
fi

echo "🚀 Starting Agentic Honeypot API server..."
echo "📊 Environment Status:"
echo "   API_KEY: ✅ SET"
echo "   GEMINI_API_KEY: ✅ SET (${GEMINI_API_KEY:0:10}...)"
echo "   CALLBACK_URL: ${CALLBACK_URL:-Not set}"

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from app.api.routes import router

app = FastAPI(
    title="Agentic Honeypot API",
    version="1.0.0",
)

app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agentic Honeypot API</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                   max-width: 800px; margin: 50px auto; padding: 20px; background: #1a1a2e; color: #eee; }
            h1 { color: #00d9ff; }
            a { color: #00d9ff; }
            .endpoint { background: #16213e; padding: 15px; border-radius: 8px; margin: 10px 0; }
            code { background: #0f3460; padding: 2px 8px; border-radius: 4px; }
            .status { color: #00ff88; }
        </style>
    </head>
    <body>
        <h1>🍯 Agentic Honeypot API</h1>
        <p class="status">● Server is running</p>
        
        <h2>Endpoints</h2>
        <div class="endpoint">
            <strong>GET</strong> <code>/health</code> - Health check
        </div>
        <div class="endpoint">
            <strong>POST</strong> <code>/message</code> - Send message (requires <code>x-api-key</code> header)
        </div>
        
        <h2>Documentation</h2>
        <p>
            <a href="/docs">📖 Swagger UI</a> | 
            <a href="/redoc">📚 ReDoc</a>
        </p>
        
        <h2>Quick Test</h2>
        <pre style="background: #16213e; padding: 15px; border-radius: 8px; overflow-x: auto;">
curl -X POST http://localhost:8000/message \\
  -H "Content-Type: application/json" \\
  -H "x-api-key: test-api-key" \\
  -d '{
    "sessionId": "test-session",
    "message": {
      "sender": "test",
      "text": "Your message here",
      "timestamp": 1738771200
    }
  }'
        </pre>
    </body>
    </html>
    """


@app.get("/health")
def health_check():
    return {"status": "healthy"}

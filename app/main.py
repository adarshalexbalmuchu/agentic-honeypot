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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic Honeypot | AI-Powered Scam Detection</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a24;
            --border: #2a2a3a;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.3);
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
        
        /* Header */
        header {
            border-bottom: 1px solid var(--border);
            padding: 20px 0;
            position: sticky;
            top: 0;
            background: rgba(10, 10, 15, 0.9);
            backdrop-filter: blur(10px);
            z-index: 100;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.5rem;
            font-weight: 700;
        }
        
        .logo-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent), #8b5cf6);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .status-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 20px;
            font-size: 0.875rem;
            color: var(--success);
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Hero Section */
        .hero {
            padding: 80px 0;
            text-align: center;
            background: radial-gradient(ellipse at center top, var(--accent-glow), transparent 50%);
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #fff, #a0a0b0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero p {
            font-size: 1.25rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 32px;
        }
        
        .hero-buttons {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover {
            background: #5558e3;
            transform: translateY(-2px);
            box-shadow: 0 10px 40px var(--accent-glow);
        }
        
        .btn-secondary {
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-primary);
        }
        
        .btn-secondary:hover {
            border-color: var(--accent);
        }
        
        /* Stats */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 24px;
            padding: 60px 0;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            transition: all 0.3s;
        }
        
        .stat-card:hover {
            border-color: var(--accent);
            transform: translateY(-4px);
        }
        
        .stat-icon {
            font-size: 2rem;
            margin-bottom: 12px;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            margin-top: 4px;
        }
        
        /* Features */
        .features {
            padding: 60px 0;
        }
        
        .section-title {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 48px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
        }
        
        .feature-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px;
        }
        
        .feature-card h3 {
            font-size: 1.25rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .feature-card p {
            color: var(--text-secondary);
        }
        
        /* API Demo */
        .demo {
            padding: 60px 0;
        }
        
        .demo-container {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
        }
        
        .demo-header {
            background: var(--bg-secondary);
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .demo-dots {
            display: flex;
            gap: 8px;
        }
        
        .demo-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        
        .demo-dot.red { background: #ef4444; }
        .demo-dot.yellow { background: #f59e0b; }
        .demo-dot.green { background: #22c55e; }
        
        .demo-title {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }
        
        .demo-body {
            padding: 24px;
        }
        
        .code-block {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            line-height: 1.8;
        }
        
        .code-block .keyword { color: #c792ea; }
        .code-block .string { color: #c3e88d; }
        .code-block .url { color: #82aaff; }
        .code-block .header { color: #ffcb6b; }
        
        /* Interactive Demo */
        .interactive-demo {
            margin-top: 32px;
            padding: 24px;
            background: var(--bg-secondary);
            border-radius: 12px;
        }
        
        .demo-form {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
        }
        
        .demo-input {
            flex: 1;
            padding: 12px 16px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 1rem;
        }
        
        .demo-input:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        .demo-btn {
            padding: 12px 24px;
            background: var(--accent);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .demo-btn:hover { background: #5558e3; }
        .demo-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        
        .demo-response {
            background: var(--bg-card);
            border-radius: 8px;
            padding: 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.875rem;
            min-height: 100px;
            white-space: pre-wrap;
        }
        
        /* Endpoints */
        .endpoints {
            padding: 60px 0;
        }
        
        .endpoint-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .endpoint {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 24px;
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .method {
            padding: 6px 12px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .method.get { background: rgba(34, 197, 94, 0.2); color: var(--success); }
        .method.post { background: rgba(99, 102, 241, 0.2); color: var(--accent); }
        
        .endpoint-path {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
        }
        
        .endpoint-desc {
            color: var(--text-secondary);
            margin-left: auto;
        }
        
        /* Footer */
        footer {
            border-top: 1px solid var(--border);
            padding: 40px 0;
            text-align: center;
            color: var(--text-secondary);
        }
        
        footer a {
            color: var(--accent);
            text-decoration: none;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .hero p { font-size: 1rem; }
            .endpoint { flex-wrap: wrap; }
            .endpoint-desc { margin-left: 0; width: 100%; margin-top: 8px; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container header-content">
            <div class="logo">
                <div class="logo-icon">🍯</div>
                <span>Agentic Honeypot</span>
            </div>
            <div class="status-badge">
                <div class="status-dot"></div>
                API Online
            </div>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <h1>AI-Powered Scam Detection</h1>
            <p>An intelligent honeypot that engages scammers using AI personas, extracts key intelligence, and protects potential victims.</p>
            <div class="hero-buttons">
                <a href="/docs" class="btn btn-primary">
                    📖 API Docs
                </a>
                <a href="#demo" class="btn btn-secondary">
                    ⚡ Try Demo
                </a>
            </div>
        </div>
    </section>
    
    <section class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-icon">🎭</div>
                <div class="stat-value">7</div>
                <div class="stat-label">FSM States</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🧠</div>
                <div class="stat-value">Gemini</div>
                <div class="stat-label">AI Engine</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔍</div>
                <div class="stat-value">30+</div>
                <div class="stat-label">Scam Patterns</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">Real-time</div>
                <div class="stat-label">Intel Extraction</div>
            </div>
        </div>
    </section>
    
    <section class="features container">
        <h2 class="section-title">How It Works</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🎯 Scam Detection</h3>
                <p>Advanced pattern matching identifies phishing attempts, social engineering, urgency tactics, and financial fraud in real-time.</p>
            </div>
            <div class="feature-card">
                <h3>🤖 AI Personas</h3>
                <p>Gemini AI generates realistic human responses that engage scammers while extracting valuable intelligence.</p>
            </div>
            <div class="feature-card">
                <h3>📤 Intel Extraction</h3>
                <p>Automatically extracts phone numbers, UPI IDs, bank accounts, and suspicious keywords from conversations.</p>
            </div>
            <div class="feature-card">
                <h3>🔄 State Machine</h3>
                <p>7-state FSM tracks conversation flow from initial contact through engagement to intelligence harvesting.</p>
            </div>
            <div class="feature-card">
                <h3>📡 Callback API</h3>
                <p>Sends extracted intelligence to your backend when thresholds are met for further analysis.</p>
            </div>
            <div class="feature-card">
                <h3>🛡️ Production Ready</h3>
                <p>Built with FastAPI, async I/O, proper error handling, and comprehensive test coverage.</p>
            </div>
        </div>
    </section>
    
    <section class="demo container" id="demo">
        <h2 class="section-title">Quick Start</h2>
        <div class="demo-container">
            <div class="demo-header">
                <div class="demo-dots">
                    <div class="demo-dot red"></div>
                    <div class="demo-dot yellow"></div>
                    <div class="demo-dot green"></div>
                </div>
                <span class="demo-title">Terminal</span>
            </div>
            <div class="demo-body">
                <div class="code-block">
<span class="keyword">curl</span> -X POST <span class="url">https://agentic-honeypot-45zq.onrender.com/message</span> \\
  -H <span class="string">"Content-Type: application/json"</span> \\
  -H <span class="header">"x-api-key: YOUR_API_KEY"</span> \\
  -d <span class="string">'{
    "sessionId": "session-123",
    "message": {
      "sender": "unknown",
      "text": "Your message here",
      "timestamp": 1738771200
    }
  }'</span>
                </div>
                
                <div class="interactive-demo">
                    <h4 style="margin-bottom: 16px;">🧪 Live Demo</h4>
                    <div class="demo-form">
                        <input type="text" class="demo-input" id="demoMessage" 
                               placeholder="Enter a scam message to test..." 
                               value="Urgent! Your bank account is blocked. Send OTP now!">
                        <button class="demo-btn" id="demoBtn" onclick="testAPI()">Test API</button>
                    </div>
                    <div class="demo-response" id="demoResponse">Response will appear here...</div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="endpoints container">
        <h2 class="section-title">API Endpoints</h2>
        <div class="endpoint-list">
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/</span>
                <span class="endpoint-desc">This dashboard</span>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/health</span>
                <span class="endpoint-desc">Health check endpoint</span>
            </div>
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/docs</span>
                <span class="endpoint-desc">Swagger UI documentation</span>
            </div>
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="endpoint-path">/message</span>
                <span class="endpoint-desc">Send message for scam analysis (requires x-api-key)</span>
            </div>
        </div>
    </section>
    
    <footer>
        <div class="container">
            <p>Built for GUVI Hackathon 2026 | <a href="/docs">API Documentation</a> | <a href="/redoc">ReDoc</a></p>
        </div>
    </footer>
    
    <script>
        async function testAPI() {
            const btn = document.getElementById('demoBtn');
            const input = document.getElementById('demoMessage');
            const response = document.getElementById('demoResponse');
            
            btn.disabled = true;
            btn.textContent = 'Testing...';
            response.textContent = 'Sending request...';
            
            try {
                const res = await fetch('/message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': 'demo-key'
                    },
                    body: JSON.stringify({
                        sessionId: 'demo-' + Date.now(),
                        message: {
                            sender: 'demo',
                            text: input.value,
                            timestamp: Math.floor(Date.now() / 1000)
                        }
                    })
                });
                
                const data = await res.json();
                response.textContent = JSON.stringify(data, null, 2);
            } catch (err) {
                response.textContent = 'Error: ' + err.message + '\\n\\nNote: Demo requires valid API key configured.';
            }
            
            btn.disabled = false;
            btn.textContent = 'Test API';
        }
    </script>
</body>
</html>
    """


@app.get("/health")
def health_check():
    return {"status": "healthy"}

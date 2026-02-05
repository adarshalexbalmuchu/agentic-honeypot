from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from app.api.routes import router

app = FastAPI(
    title="Agentic Honeypot API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    <title>Agentic Honeypot | Security Operations Center</title>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-darker: #05080a;
            --bg-dark: #0a0e12;
            --bg-panel: #0f1419;
            --bg-elevated: #151b22;
            --border: #1e2730;
            --border-active: #2d3a47;
            --text-primary: #e6edf3;
            --text-secondary: #7d8590;
            --text-muted: #484f58;
            --accent-blue: #58a6ff;
            --accent-purple: #a371f7;
            --accent-green: #3fb950;
            --accent-yellow: #d29922;
            --accent-orange: #db6d28;
            --accent-red: #f85149;
            --accent-cyan: #39c5cf;
            --glow-blue: rgba(88, 166, 255, 0.15);
            --glow-green: rgba(63, 185, 80, 0.15);
            --glow-red: rgba(248, 81, 73, 0.15);
        }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-darker);
            color: var(--text-primary);
            line-height: 1.5;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Header - SOC Style */
        .soc-header {
            background: var(--bg-dark);
            border-bottom: 1px solid var(--border);
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .soc-brand {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        
        .soc-logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .soc-logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        
        .soc-logo-text {
            font-weight: 600;
            font-size: 15px;
            letter-spacing: -0.3px;
        }
        
        .soc-badge {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 10px;
            padding: 3px 8px;
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .soc-status {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 8px var(--accent-green);
            animation: pulse 2s infinite;
        }
        
        .status-dot.warning { background: var(--accent-yellow); box-shadow: 0 0 8px var(--accent-yellow); }
        .status-dot.danger { background: var(--accent-red); box-shadow: 0 0 8px var(--accent-red); }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .nav-links {
            display: flex;
            gap: 8px;
        }
        
        .nav-link {
            font-size: 12px;
            padding: 6px 12px;
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-radius: 4px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.15s;
        }
        
        .nav-link:hover {
            background: var(--bg-panel);
            border-color: var(--border-active);
            color: var(--text-primary);
        }
        
        /* Main Layout */
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 1px;
            background: var(--border);
            min-height: calc(100vh - 57px);
        }
        
        .main-content {
            background: var(--bg-darker);
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .sidebar {
            background: var(--bg-dark);
            display: flex;
            flex-direction: column;
        }
        
        /* Section Headers */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        
        .section-title {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .section-title::before {
            content: '';
            width: 3px;
            height: 12px;
            background: var(--accent-blue);
            border-radius: 2px;
        }
        
        /* Agent Lifecycle Pipeline */
        .pipeline-container {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
        }
        
        .pipeline {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            position: relative;
            padding: 0 10px;
        }
        
        .pipeline::before {
            content: '';
            position: absolute;
            top: 24px;
            left: 50px;
            right: 50px;
            height: 2px;
            background: var(--border);
        }
        
        .pipeline-stage {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            position: relative;
            z-index: 1;
            flex: 1;
            max-width: 140px;
        }
        
        .stage-icon {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--bg-dark);
            border: 2px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            transition: all 0.3s;
        }
        
        .stage-icon.active {
            border-color: var(--accent-blue);
            box-shadow: 0 0 20px var(--glow-blue);
        }
        
        .stage-icon.completed {
            border-color: var(--accent-green);
            background: var(--glow-green);
        }
        
        .stage-icon.warning {
            border-color: var(--accent-yellow);
            animation: pulseWarning 1.5s infinite;
        }
        
        @keyframes pulseWarning {
            0%, 100% { box-shadow: 0 0 10px rgba(210, 153, 34, 0.3); }
            50% { box-shadow: 0 0 25px rgba(210, 153, 34, 0.5); }
        }
        
        .stage-label {
            font-size: 11px;
            font-weight: 500;
            color: var(--text-secondary);
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        
        .stage-sublabel {
            font-size: 10px;
            color: var(--text-muted);
            font-family: 'IBM Plex Mono', monospace;
        }
        
        /* Live Simulation Panel */
        .simulation-panel {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .simulation-header {
            padding: 12px 16px;
            background: var(--bg-dark);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .sim-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            font-weight: 500;
        }
        
        .sim-title .live-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-red);
            border-radius: 50%;
            animation: livePulse 1s infinite;
        }
        
        @keyframes livePulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.2); }
        }
        
        .sim-controls {
            display: flex;
            gap: 8px;
        }
        
        .sim-btn {
            padding: 5px 12px;
            font-size: 11px;
            font-weight: 500;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--bg-elevated);
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.15s;
        }
        
        .sim-btn:hover {
            background: var(--bg-panel);
            border-color: var(--accent-blue);
            color: var(--text-primary);
        }
        
        .sim-btn.primary {
            background: var(--accent-blue);
            border-color: var(--accent-blue);
            color: #fff;
        }
        
        .sim-btn.primary:hover {
            background: #4d9aef;
        }
        
        /* Chat Window */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .chat-message {
            display: flex;
            gap: 10px;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .chat-message.scammer { flex-direction: row; }
        .chat-message.agent { flex-direction: row-reverse; }
        
        .msg-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }
        
        .chat-message.scammer .msg-avatar {
            background: var(--glow-red);
            border: 1px solid var(--accent-red);
        }
        
        .chat-message.agent .msg-avatar {
            background: var(--glow-blue);
            border: 1px solid var(--accent-blue);
        }
        
        .msg-content {
            max-width: 70%;
        }
        
        .msg-bubble {
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .chat-message.scammer .msg-bubble {
            background: var(--bg-elevated);
            border: 1px solid var(--border);
            border-bottom-left-radius: 4px;
        }
        
        .chat-message.agent .msg-bubble {
            background: rgba(88, 166, 255, 0.1);
            border: 1px solid rgba(88, 166, 255, 0.2);
            border-bottom-right-radius: 4px;
        }
        
        .msg-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 4px;
            font-size: 10px;
            color: var(--text-muted);
        }
        
        .msg-tag {
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 9px;
            font-weight: 500;
            text-transform: uppercase;
        }
        
        .msg-tag.threat { background: var(--glow-red); color: var(--accent-red); }
        .msg-tag.intel { background: var(--glow-blue); color: var(--accent-blue); }
        .msg-tag.ai { background: rgba(163, 113, 247, 0.15); color: var(--accent-purple); }
        
        /* Intel Extraction Panel */
        .intel-panel {
            background: var(--bg-panel);
            border-top: 1px solid var(--border);
            padding: 16px;
        }
        
        .intel-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        
        .intel-item {
            background: var(--bg-dark);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px 12px;
            transition: all 0.2s;
        }
        
        .intel-item.found {
            border-color: var(--accent-green);
            background: var(--glow-green);
        }
        
        .intel-item.found .intel-value {
            color: var(--accent-green);
        }
        
        .intel-label {
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        
        .intel-value {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            color: var(--text-secondary);
            word-break: break-all;
        }
        
        /* Sidebar Panels */
        .sidebar-panel {
            padding: 16px;
            border-bottom: 1px solid var(--border);
        }
        
        .sidebar-panel:last-child {
            border-bottom: none;
        }
        
        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        
        .metric-card {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 600;
            color: var(--accent-blue);
            font-family: 'IBM Plex Mono', monospace;
        }
        
        .metric-value.green { color: var(--accent-green); }
        .metric-value.yellow { color: var(--accent-yellow); }
        .metric-value.red { color: var(--accent-red); }
        
        .metric-label {
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        /* FSM State Display */
        .fsm-display {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 6px;
            overflow: hidden;
        }
        
        .fsm-header {
            padding: 10px 12px;
            background: var(--bg-dark);
            border-bottom: 1px solid var(--border);
            font-size: 11px;
            font-weight: 500;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .fsm-states {
            padding: 12px;
        }
        
        .fsm-state {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px solid var(--border);
        }
        
        .fsm-state:last-child { border-bottom: none; }
        
        .fsm-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--bg-elevated);
            border: 2px solid var(--border);
            flex-shrink: 0;
        }
        
        .fsm-state.completed .fsm-dot {
            background: var(--accent-green);
            border-color: var(--accent-green);
        }
        
        .fsm-state.active .fsm-dot {
            background: var(--accent-blue);
            border-color: var(--accent-blue);
            box-shadow: 0 0 10px var(--accent-blue);
        }
        
        .fsm-name {
            font-size: 12px;
            font-family: 'IBM Plex Mono', monospace;
            color: var(--text-secondary);
            flex: 1;
        }
        
        .fsm-state.completed .fsm-name,
        .fsm-state.active .fsm-name { color: var(--text-primary); }
        
        .fsm-icon {
            font-size: 12px;
            opacity: 0.5;
        }
        
        .fsm-state.completed .fsm-icon { opacity: 1; }
        
        /* Evaluation Criteria */
        .eval-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .eval-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 6px;
        }
        
        .eval-check {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--glow-green);
            border: 1px solid var(--accent-green);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: var(--accent-green);
        }
        
        .eval-text {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .eval-score {
            margin-left: auto;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 11px;
            color: var(--accent-green);
        }
        
        /* API Panel */
        .api-panel {
            flex: 1;
            overflow: auto;
            padding: 16px;
        }
        
        .api-endpoint {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 10px;
            overflow: hidden;
        }
        
        .api-header {
            padding: 10px 12px;
            background: var(--bg-dark);
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid var(--border);
        }
        
        .api-method {
            font-size: 10px;
            font-weight: 600;
            font-family: 'IBM Plex Mono', monospace;
            padding: 3px 8px;
            border-radius: 3px;
        }
        
        .api-method.get { background: rgba(63, 185, 80, 0.15); color: var(--accent-green); }
        .api-method.post { background: rgba(88, 166, 255, 0.15); color: var(--accent-blue); }
        
        .api-path {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            color: var(--text-primary);
        }
        
        .api-body {
            padding: 12px;
        }
        
        .api-desc {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        /* Footer */
        .dashboard-footer {
            grid-column: 1 / -1;
            background: var(--bg-dark);
            border-top: 1px solid var(--border);
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text-muted);
        }
        
        .footer-links {
            display: flex;
            gap: 16px;
        }
        
        .footer-links a {
            color: var(--text-secondary);
            text-decoration: none;
        }
        
        .footer-links a:hover { color: var(--accent-blue); }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            .sidebar { display: none; }
            .pipeline { flex-wrap: wrap; gap: 20px; }
            .pipeline::before { display: none; }
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: var(--border-active); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
    </style>
</head>
<body>
    <header class="soc-header">
        <div class="soc-brand">
            <div class="soc-logo">
                <div class="soc-logo-icon">🛡️</div>
                <span class="soc-logo-text">Agentic Honeypot</span>
            </div>
            <span class="soc-badge">SOC Dashboard v1.0</span>
        </div>
        <div class="soc-status">
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>System Online</span>
            </div>
            <div class="status-indicator">
                <div class="status-dot warning" id="agentStatus"></div>
                <span id="agentStatusText">Agent Idle</span>
            </div>
            <div class="nav-links">
                <a href="/docs" class="nav-link">API Docs</a>
                <a href="/redoc" class="nav-link">ReDoc</a>
                <a href="/health" class="nav-link">Health</a>
            </div>
        </div>
    </header>

    <div class="dashboard">
        <div class="main-content">
            <!-- Agent Lifecycle Pipeline -->
            <div class="pipeline-container">
                <div class="section-header">
                    <div class="section-title">Agent Lifecycle Pipeline</div>
                </div>
                <div class="pipeline">
                    <div class="pipeline-stage" id="stage-1">
                        <div class="stage-icon" id="icon-1">📨</div>
                        <div class="stage-label">Incoming</div>
                        <div class="stage-sublabel">Message Received</div>
                    </div>
                    <div class="pipeline-stage" id="stage-2">
                        <div class="stage-icon" id="icon-2">🔍</div>
                        <div class="stage-label">Detection</div>
                        <div class="stage-sublabel">Score: <span id="detectScore">--</span></div>
                    </div>
                    <div class="pipeline-stage" id="stage-3">
                        <div class="stage-icon" id="icon-3">🤖</div>
                        <div class="stage-label">Agent Active</div>
                        <div class="stage-sublabel">Gemini AI</div>
                    </div>
                    <div class="pipeline-stage" id="stage-4">
                        <div class="stage-icon" id="icon-4">💬</div>
                        <div class="stage-label">Engagement</div>
                        <div class="stage-sublabel">Msgs: <span id="msgCount">0</span></div>
                    </div>
                    <div class="pipeline-stage" id="stage-5">
                        <div class="stage-icon" id="icon-5">📊</div>
                        <div class="stage-label">Intel Extract</div>
                        <div class="stage-sublabel">Items: <span id="intelCount">0</span></div>
                    </div>
                    <div class="pipeline-stage" id="stage-6">
                        <div class="stage-icon" id="icon-6">📤</div>
                        <div class="stage-label">Callback</div>
                        <div class="stage-sublabel">GUVI Endpoint</div>
                    </div>
                </div>
            </div>

            <!-- Live API Testing -->
            <div class="simulation-panel">
                <div class="simulation-header">
                    <div class="sim-title">
                        <div class="live-dot" id="liveDot" style="display:none;"></div>
                        <span>Live API Testing</span>
                    </div>
                    <div class="sim-controls">
                        <button class="sim-btn" onclick="clearChat()">Clear</button>
                    </div>
                </div>
                
                <!-- API Key Input -->
                <div style="padding: 12px 16px; background: var(--bg-dark); border-bottom: 1px solid var(--border);">
                    <div style="display: flex; gap: 12px; align-items: center;">
                        <label style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;">API Key:</label>
                        <input type="password" id="apiKeyInput" placeholder="Enter your x-api-key" 
                               style="flex: 1; padding: 8px 12px; background: var(--bg-panel); border: 1px solid var(--border); border-radius: 4px; color: var(--text-primary); font-family: 'IBM Plex Mono', monospace; font-size: 12px;">
                        <button onclick="toggleKeyVisibility()" class="sim-btn" style="padding: 8px 12px;">👁</button>
                    </div>
                </div>
                
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages">
                        <div style="text-align: center; padding: 40px; color: var(--text-muted);" id="emptyState">
                            <div style="font-size: 48px; margin-bottom: 16px;">🛡️</div>
                            <div style="font-size: 14px;">Enter your API key and send a message</div>
                            <div style="font-size: 12px; margin-top: 8px;">Real API calls to your honeypot backend</div>
                        </div>
                    </div>
                </div>
                
                <!-- Message Input -->
                <div style="padding: 16px; background: var(--bg-dark); border-top: 1px solid var(--border);">
                    <div style="display: flex; gap: 12px;">
                        <input type="text" id="messageInput" placeholder="Type a scam message to test..." 
                               value="Urgent! Your bank account is blocked. Send OTP 4589 to verify!"
                               style="flex: 1; padding: 12px 16px; background: var(--bg-panel); border: 1px solid var(--border); border-radius: 6px; color: var(--text-primary); font-size: 13px;"
                               onkeypress="if(event.key==='Enter')sendMessage()">
                        <button onclick="sendMessage()" class="sim-btn primary" id="sendBtn" style="padding: 12px 24px;">
                            Send →
                        </button>
                    </div>
                    <div style="margin-top: 8px; font-size: 10px; color: var(--text-muted);">
                        Session: <span id="sessionDisplay" style="font-family: 'IBM Plex Mono', monospace;">--</span>
                    </div>
                </div>
                
                <!-- Intel Extraction Panel -->
                <div class="intel-panel">
                    <div class="section-header">
                        <div class="section-title">Extracted Intelligence</div>
                    </div>
                    <div class="intel-grid">
                        <div class="intel-item" id="intel-phone">
                            <div class="intel-label">Phone Numbers</div>
                            <div class="intel-value" id="intel-phone-val">--</div>
                        </div>
                        <div class="intel-item" id="intel-upi">
                            <div class="intel-label">UPI IDs</div>
                            <div class="intel-value" id="intel-upi-val">--</div>
                        </div>
                        <div class="intel-item" id="intel-account">
                            <div class="intel-label">Bank Accounts</div>
                            <div class="intel-value" id="intel-account-val">--</div>
                        </div>
                        <div class="intel-item" id="intel-keywords">
                            <div class="intel-label">Keywords</div>
                            <div class="intel-value" id="intel-keywords-val">--</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Sidebar -->
        <div class="sidebar">
            <!-- Engagement Metrics -->
            <div class="sidebar-panel">
                <div class="section-header">
                    <div class="section-title">Engagement Metrics</div>
                </div>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value" id="metricMsgs">0</div>
                        <div class="metric-label">Messages</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value green" id="metricDuration">0s</div>
                        <div class="metric-label">Duration</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value yellow" id="metricScore">0</div>
                        <div class="metric-label">Threat Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value" id="metricIntel">0</div>
                        <div class="metric-label">Intel Items</div>
                    </div>
                </div>
            </div>
            
            <!-- FSM State -->
            <div class="sidebar-panel">
                <div class="section-header">
                    <div class="section-title">FSM State Machine</div>
                </div>
                <div class="fsm-display">
                    <div class="fsm-header">
                        <span>🔄</span> Current State: <strong id="currentState">INIT</strong>
                    </div>
                    <div class="fsm-states" id="fsmStates">
                        <div class="fsm-state active" data-state="INIT">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">INIT</div>
                            <div class="fsm-icon">▶</div>
                        </div>
                        <div class="fsm-state" data-state="NORMAL">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">NORMAL</div>
                            <div class="fsm-icon">→</div>
                        </div>
                        <div class="fsm-state" data-state="SUSPICIOUS">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">SUSPICIOUS</div>
                            <div class="fsm-icon">⚠</div>
                        </div>
                        <div class="fsm-state" data-state="AGENT_ENGAGED">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">AGENT_ENGAGED</div>
                            <div class="fsm-icon">🤖</div>
                        </div>
                        <div class="fsm-state" data-state="INTEL_READY">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">INTEL_READY</div>
                            <div class="fsm-icon">📊</div>
                        </div>
                        <div class="fsm-state" data-state="CALLBACK_SENT">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">CALLBACK_SENT</div>
                            <div class="fsm-icon">📤</div>
                        </div>
                        <div class="fsm-state" data-state="TERMINATED">
                            <div class="fsm-dot"></div>
                            <div class="fsm-name">TERMINATED</div>
                            <div class="fsm-icon">✓</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Evaluation Criteria -->
            <div class="sidebar-panel">
                <div class="section-header">
                    <div class="section-title">Hackathon Criteria</div>
                </div>
                <div class="eval-list">
                    <div class="eval-item">
                        <div class="eval-check">✓</div>
                        <div class="eval-text">Scam Detection Accuracy</div>
                        <div class="eval-score">30+ patterns</div>
                    </div>
                    <div class="eval-item">
                        <div class="eval-check">✓</div>
                        <div class="eval-text">Engagement Depth</div>
                        <div class="eval-score">Multi-turn</div>
                    </div>
                    <div class="eval-item">
                        <div class="eval-check">✓</div>
                        <div class="eval-text">Intel Extraction</div>
                        <div class="eval-score">4 types</div>
                    </div>
                    <div class="eval-item">
                        <div class="eval-check">✓</div>
                        <div class="eval-text">API Compliance</div>
                        <div class="eval-score">GUVI spec</div>
                    </div>
                </div>
            </div>
            
            <!-- API Endpoints -->
            <div class="api-panel">
                <div class="section-header">
                    <div class="section-title">API Endpoints</div>
                </div>
                <div class="api-endpoint">
                    <div class="api-header">
                        <span class="api-method post">POST</span>
                        <span class="api-path">/message</span>
                    </div>
                    <div class="api-body">
                        <div class="api-desc">Send message for scam analysis. Requires x-api-key header.</div>
                    </div>
                </div>
                <div class="api-endpoint">
                    <div class="api-header">
                        <span class="api-method get">GET</span>
                        <span class="api-path">/health</span>
                    </div>
                    <div class="api-body">
                        <div class="api-desc">Health check endpoint for monitoring.</div>
                    </div>
                </div>
                <div class="api-endpoint">
                    <div class="api-header">
                        <span class="api-method get">GET</span>
                        <span class="api-path">/docs</span>
                    </div>
                    <div class="api-body">
                        <div class="api-desc">Interactive Swagger UI documentation.</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="dashboard-footer">
            <div>Built for GUVI Hackathon 2026 | Agentic Honeypot System</div>
            <div class="footer-links">
                <a href="/docs">Swagger</a>
                <a href="/redoc">ReDoc</a>
                <a href="https://github.com/adarshalexbalmuchu/agentic-honeypot" target="_blank">GitHub</a>
            </div>
        </div>
    </div>

    <script>
        // Session state
        let sessionId = 'session-' + Date.now();
        let msgCount = 0;
        let startTime = null;
        let timerInterval = null;
        let conversationHistory = [];
        
        document.getElementById('sessionDisplay').textContent = sessionId;
        
        // Toggle API key visibility
        function toggleKeyVisibility() {
            const input = document.getElementById('apiKeyInput');
            input.type = input.type === 'password' ? 'text' : 'password';
        }
        
        // Clear chat
        function clearChat() {
            sessionId = 'session-' + Date.now();
            msgCount = 0;
            startTime = null;
            if (timerInterval) clearInterval(timerInterval);
            
            document.getElementById('sessionDisplay').textContent = sessionId;
            document.getElementById('chatMessages').innerHTML = 
                '<div style="text-align: center; padding: 40px; color: var(--text-muted);" id="emptyState">' +
                    '<div style="font-size: 48px; margin-bottom: 16px;">🛡️</div>' +
                    '<div style="font-size: 14px;">Enter your API key and send a message</div>' +
                    '<div style="font-size: 12px; margin-top: 8px;">Real API calls to your honeypot backend</div>' +
                '</div>';
            
            // Reset metrics
            document.getElementById('metricMsgs').textContent = '0';
            document.getElementById('metricDuration').textContent = '0s';
            document.getElementById('metricScore').textContent = '0';
            document.getElementById('metricIntel').textContent = '0';
            document.getElementById('msgCount').textContent = '0';
            document.getElementById('intelCount').textContent = '0';
            document.getElementById('detectScore').textContent = '--';
            
            // Reset intel
            ['phone', 'upi', 'account', 'keywords'].forEach(type => {
                document.getElementById('intel-' + type).classList.remove('found');
                document.getElementById('intel-' + type + '-val').textContent = '--';
            });
            
            // Reset FSM
            updateFSM('INIT');
            
            // Reset pipeline
            for (let i = 1; i <= 6; i++) {
                document.getElementById('icon-' + i).classList.remove('active', 'completed', 'warning');
            }
            
            document.getElementById('liveDot').style.display = 'none';
            document.getElementById('agentStatus').className = 'status-dot warning';
            document.getElementById('agentStatusText').textContent = 'Agent Idle';
        }
        
        // Update FSM display
        function updateFSM(newState) {
            const states = document.querySelectorAll('.fsm-state');
            const stateOrder = ['INIT', 'NORMAL', 'SUSPICIOUS', 'AGENT_ENGAGED', 'INTEL_READY', 'CALLBACK_SENT', 'TERMINATED'];
            const newIdx = stateOrder.indexOf(newState);
            
            states.forEach((el, idx) => {
                el.classList.remove('active', 'completed');
                if (idx < newIdx) el.classList.add('completed');
                if (idx === newIdx) el.classList.add('active');
            });
            
            document.getElementById('currentState').textContent = newState;
        }
        
        // Update pipeline stage
        function activateStage(stageNum) {
            for (let i = 1; i <= 6; i++) {
                const icon = document.getElementById('icon-' + i);
                icon.classList.remove('active', 'completed', 'warning');
                if (i < stageNum) icon.classList.add('completed');
                if (i === stageNum) icon.classList.add('active');
            }
        }
        
        // Add chat message
        function addMessage(type, text, tags = []) {
            // Remove empty state
            const emptyState = document.getElementById('emptyState');
            if (emptyState) emptyState.remove();
            
            const chat = document.getElementById('chatMessages');
            const msg = document.createElement('div');
            msg.className = 'chat-message ' + type;
            
            const avatar = type === 'scammer' ? '👤' : '🤖';
            const tagHtml = tags.map(t => '<span class="msg-tag ' + t.type + '">' + t.label + '</span>').join('');
            
            msg.innerHTML = 
                '<div class="msg-avatar">' + avatar + '</div>' +
                '<div class="msg-content">' +
                    '<div class="msg-bubble">' + text + '</div>' +
                    '<div class="msg-meta">' +
                        '<span>' + new Date().toLocaleTimeString() + '</span>' +
                        tagHtml +
                    '</div>' +
                '</div>';
            
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }
        
        // Extract intel from message
        function extractIntel(text) {
            const patterns = {
                phone: /\\b[6-9]\\d{9}\\b|\\b\\d{4}\\b/g,
                upi: /[a-zA-Z0-9.\\-_]+@[a-zA-Z]+/g,
                account: /\\b\\d{10,18}\\b/g
            };
            
            const keywords = ['urgent', 'blocked', 'otp', 'bank', 'kyc', 'verify', 'transfer', 'immediately', 'account'];
            const foundKeywords = keywords.filter(k => text.toLowerCase().includes(k));
            
            if (foundKeywords.length > 0) {
                document.getElementById('intel-keywords').classList.add('found');
                document.getElementById('intel-keywords-val').textContent = foundKeywords.join(', ');
            }
            
            const phones = text.match(patterns.phone);
            if (phones) {
                document.getElementById('intel-phone').classList.add('found');
                document.getElementById('intel-phone-val').textContent = phones.join(', ');
            }
            
            const upis = text.match(patterns.upi);
            if (upis) {
                document.getElementById('intel-upi').classList.add('found');
                document.getElementById('intel-upi-val').textContent = upis.join(', ');
            }
            
            const accounts = text.match(patterns.account);
            if (accounts) {
                document.getElementById('intel-account').classList.add('found');
                document.getElementById('intel-account-val').textContent = accounts[0];
            }
            
            let intelCount = 0;
            if (foundKeywords.length > 0) intelCount++;
            if (phones) intelCount++;
            if (upis) intelCount++;
            if (accounts) intelCount++;
            
            document.getElementById('intelCount').textContent = intelCount;
            document.getElementById('metricIntel').textContent = intelCount;
        }
        
        // Calculate threat score
        function calculateScore(text) {
            const indicators = ['urgent', 'blocked', 'otp', 'bank', 'kyc', 'verify', 'transfer', 'immediately', 'account', 'pin', 'password'];
            let score = 0;
            indicators.forEach(ind => {
                if (text.toLowerCase().includes(ind)) score++;
            });
            return Math.min(score, 10);
        }
        
        // Send message to real API
        async function sendMessage() {
            const apiKey = document.getElementById('apiKeyInput').value;
            const messageText = document.getElementById('messageInput').value;
            
            if (!apiKey) {
                alert('Please enter your API key');
                return;
            }
            
            if (!messageText) {
                alert('Please enter a message');
                return;
            }
            
            // Start timer on first message
            if (!startTime) {
                startTime = Date.now();
                timerInterval = setInterval(() => {
                    const elapsed = Math.floor((Date.now() - startTime) / 1000);
                    document.getElementById('metricDuration').textContent = elapsed + 's';
                }, 1000);
            }
            
            // Show live indicator
            document.getElementById('liveDot').style.display = 'block';
            document.getElementById('agentStatus').className = 'status-dot';
            document.getElementById('agentStatusText').textContent = 'Processing...';
            
            // Activate pipeline stage 1
            activateStage(1);
            
            // Calculate and display threat score
            const score = calculateScore(messageText);
            document.getElementById('detectScore').textContent = score;
            document.getElementById('metricScore').textContent = score;
            
            // Extract intel from sent message
            extractIntel(messageText);
            
            // Add user message to chat
            msgCount++;
            addMessage('scammer', messageText, [{ type: 'threat', label: 'Score: ' + score + '/10' }]);
            document.getElementById('metricMsgs').textContent = msgCount;
            document.getElementById('msgCount').textContent = msgCount;
            
            // Update FSM based on score
            if (score >= 3) {
                activateStage(2);
                updateFSM('SUSPICIOUS');
            }
            if (score >= 5) {
                activateStage(3);
                updateFSM('AGENT_ENGAGED');
            }
            
            // Clear input
            document.getElementById('messageInput').value = '';
            
            // Disable send button
            const sendBtn = document.getElementById('sendBtn');
            sendBtn.disabled = true;
            sendBtn.textContent = 'Sending...';
            
            try {
                const msgPayload = {
                    sender: 'scammer',
                    text: messageText,
                    timestamp: Math.floor(Date.now() / 1000)
                };
                
                const response = await fetch('/message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': apiKey
                    },
                    body: JSON.stringify({
                        sessionId: sessionId,
                        message: msgPayload,
                        conversationHistory: conversationHistory
                    })
                });
                
                // Store in conversation history for future turns
                conversationHistory.push(msgPayload);
                
                const text = await response.text();
                let data;
                try {
                    data = JSON.parse(text);
                } catch (parseErr) {
                    throw new Error('Server returned invalid JSON: ' + text.substring(0, 200));
                }
                
                if (response.ok) {
                    // Store agent reply in history too
                    conversationHistory.push({
                        sender: 'agent',
                        text: data.reply,
                        timestamp: Math.floor(Date.now() / 1000)
                    });
                    
                    // Success - add agent response
                    msgCount++;
                    activateStage(4);
                    addMessage('agent', data.reply, [{ type: 'ai', label: 'Gemini AI' }]);
                    document.getElementById('metricMsgs').textContent = msgCount;
                    document.getElementById('msgCount').textContent = msgCount;
                    
                    document.getElementById('agentStatusText').textContent = 'Agent Active';
                    
                    // Check if we're extracting enough intel
                    const intelCount = parseInt(document.getElementById('metricIntel').textContent);
                    if (intelCount >= 2) {
                        activateStage(5);
                        updateFSM('INTEL_READY');
                    }
                } else {
                    // Error
                    addMessage('agent', 'Error: ' + (data.detail || JSON.stringify(data)), [{ type: 'threat', label: 'API Error ' + response.status }]);
                    document.getElementById('agentStatusText').textContent = 'Error';
                }
            } catch (err) {
                addMessage('agent', 'Network Error: ' + err.message, [{ type: 'threat', label: 'Error' }]);
                document.getElementById('agentStatusText').textContent = 'Error';
            }
            
            // Re-enable send button
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send →';
        }
    </script>
</body>
</html>
    """


@app.get("/health")
def health_check():
    return {"status": "healthy"}

HACKATHON API TESTING GUIDE
============================

🚨 SOLVING 405 "Method Not Allowed" ERRORS

If you're getting 405 errors from the hackathon testing platform, here's why and how to fix it:

## COMMON CAUSES:

1. **Platform Using GET Instead of POST**
   - The testing platform might be set to use GET by default
   - Solution: Change the HTTP method to POST

2. **Platform Using Wrong Endpoint**
   - Trying: /api/message or /messages
   - Correct: /message

3. **Missing Required Headers**
   - Must include: Content-Type: application/json
   - Must include: x-api-key: test-api-key-123

## ✅ CORRECT CONFIGURATION FOR HACKATHON:

**API Endpoint:** https://your-deployment-url.com/message
**Method:** POST
**Headers:**
```
Content-Type: application/json
x-api-key: test-api-key-123
```

**Body (JSON):**
```json
{
  "sessionId": "hackathon-test-123",
  "message": {
    "sender": "user",
    "text": "URGENT! Share your bank PIN 1234 immediately!",
    "timestamp": 1738716000
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "reply": "Wait, who is this and what do you want? I don't understand."
}
```

## 🧪 TESTING COMMANDS:

### Test Local Development:
```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-api-key-123" \
  -d '{
    "sessionId": "test-1",
    "message": {
      "sender": "user",
      "text": "URGENT! Your bank account blocked. Share OTP 1234 now!",
      "timestamp": 1738716000
    }
  }'
```

### Test Production Deployment:
```bash
curl -X POST https://your-deployment.render.com/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-api-key-123" \
  -d '{
    "sessionId": "hackathon-judge-test",
    "message": {
      "sender": "scammer",
      "text": "URGENT ALERT! Your bank account will be blocked. Share OTP 9999 immediately with customer care officer!",
      "timestamp": 1738716000
    }
  }'
```

## 📊 AVAILABLE ENDPOINTS:

1. `GET /` - Dashboard/Homepage
2. `GET /health` - Health check
3. `GET /api/health` - Alternative health check
4. `POST /message` - Main API endpoint (THIS IS WHAT YOU NEED)
5. `GET /message` - Returns helpful usage guide (405 expected)
6. `GET /docs` - FastAPI Swagger documentation

## 🎯 FOR HACKATHON JUDGES:

If the testing platform shows 405 errors:
1. Verify it's using POST method (not GET)
2. Verify endpoint is /message (not /api/message)
3. Verify headers include x-api-key
4. Check the platform's request logs

Contact developer if issues persist: adarshalex.balmuchui23@iimranchi.ac.in

## 🔧 DEBUGGING CHECKLIST:

- [ ] HTTP Method is POST (not GET, PUT, DELETE)
- [ ] URL path is /message (not /api/message, /messages)
- [ ] Content-Type header: application/json
- [ ] x-api-key header: test-api-key-123  
- [ ] Request body is valid JSON with required fields
- [ ] Timestamp is a Unix timestamp (integer)
- [ ] Testing against correct deployment URL

## 💡 WHAT MAKES THE API RESPOND:

**HIGH-THREAT MESSAGES (AI Engages):**
- Contains: "OTP", "PIN", "bank", "urgent", "police", "officer"
- Example: "Share your OTP 1234 now!"
- Response: AI-generated confused reply

**NORMAL MESSAGES (Fallback):**
- Simple greetings or non-threatening content
- Example: "Hello, how are you?"
- Response: "Okay."
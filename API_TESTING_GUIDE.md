🚨 405 ERROR DEBUGGING GUIDE

## ISSUE: External Testing Platform Using Wrong Method/Headers

Your API is working perfectly! The 405 error happens when external testing 
platforms (like Postman, Insomnia, or web testing tools) use incorrect settings.

## ❌ COMMON MISTAKES CAUSING 405:

### 1. Using GET instead of POST
Platform sends: GET /message 
Result: {"detail":"Method Not Allowed"}
Fix: Change method to POST

### 2. Wrong endpoint URL  
Platform sends: POST /api/message
Result: {"detail":"Not Found"} (404)
Fix: Use /message (no /api prefix)

### 3. Missing required headers
Platform sends: POST /message (no headers)
Result: {"detail":[{"type":"missing","loc":["header","x-api-key"]...}]}
Fix: Add both headers below

## ✅ CORRECT CONFIGURATION:

**Method:** POST
**URL:** http://localhost:8000/message
**Headers:**
  Content-Type: application/json
  x-api-key: test-api-key-123

**Body (JSON):**
{
  "sessionId": "your-session-id",
  "message": {
    "sender": "user",
    "text": "Your message here", 
    "timestamp": 1738715600
  }
}

## 🔧 TESTING PLATFORM SETUP:

### Postman:
1. New Request → POST
2. URL: http://localhost:8000/message  
3. Headers Tab:
   - Content-Type: application/json
   - x-api-key: test-api-key-123
4. Body Tab → Raw → JSON → paste body above

### Insomnia:
1. New Request → POST
2. URL: http://localhost:8000/message
3. Header: x-api-key = test-api-key-123
4. Body → JSON → paste body above

### Browser/Website Testing:
```javascript
fetch('http://localhost:8000/message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json', 
    'x-api-key': 'test-api-key-123'
  },
  body: JSON.stringify({
    sessionId: 'web-test',
    message: {
      sender: 'user',
      text: 'Test message',
      timestamp: Date.now()
    }
  })
});
```

## 🧪 WORKING CURL EXAMPLE:
```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: test-api-key-123" \
  -d '{
    "sessionId": "test-session",
    "message": {
      "sender": "user", 
      "text": "Hello API test",
      "timestamp": 1738715600
    }
  }'
```

Expected Response: {"status":"success","reply":"Okay."}

## 🎯 HACKATHON DEMO TIP:
For judges/demos, provide them this exact configuration to avoid 405 errors!
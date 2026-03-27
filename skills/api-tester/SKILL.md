---
name: api-tester
description: Test API endpoints - make HTTP requests, validate responses, debug APIs. Use when user needs to test REST APIs, check endpoints, or debug HTTP requests.
---

# API Tester

## Overview

Helps test REST APIs by making HTTP requests, validating responses, and debugging connectivity issues.

## When to Use

- User needs to test an API endpoint
- User wants to debug HTTP requests
- User needs to validate API responses

## Request Formats

### Using curl
```bash
# GET request
curl -X GET "https://api.example.com/users" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json"

# POST request
curl -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'

# With verbose output
curl -v -X GET "https://api.example.com/users"
```

### Using httpie (if available)
```bash
# GET request
http GET https://api.example.com/users Authorization:"Bearer TOKEN"

# POST request
http POST https://api.example.com/users name=John email=john@example.com
```

## Response Analysis

```markdown
## API Test Results

**Endpoint:** [METHOD] [URL]
**Status:** [code] [status text]
**Time:** [response time]

### Request
- Headers: [list headers]
- Body: [request body if any]

### Response
- Status: [200 OK / 404 Not Found / etc.]
- Headers: [relevant headers]
- Body:
```json
[response body]
```

### Analysis
- ✅ [What's working]
- ❌ [Issues found]
- 💡 [Suggestions]
```

## Common Status Codes

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request body |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Wrong endpoint |
| 500 | Server Error | Backend issue |

## Debugging Tips

1. **Check auth** - Verify token/API key is correct
2. **Validate JSON** - Ensure request body is valid JSON
3. **Check headers** - Content-Type must match body format
4. **URL encoding** - Special chars in URLs need encoding
5. **CORS issues** - Check browser console for CORS errors

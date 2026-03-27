---
name: env-manager
description: Manage environment variables and .env files. Use when user needs help with environment configuration, .env files, or environment variable management.
---

# Environment Manager

## Overview

Helps manage environment variables, .env files, and environment configuration across different contexts.

## When to Use

- User needs to set up environment variables
- User wants to manage .env files
- User needs to debug environment issues
- User wants to secure sensitive configuration

## .env File Format

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db
DB_HOST=localhost
DB_PORT=5432

# API Keys (no quotes needed for simple values)
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key

# With special characters (use quotes)
PASSWORD="p@ss!word#123"

# Multiline (use quotes and \n)
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nMIIE..."

# Boolean/Numbers (still strings in env)
DEBUG=true
PORT=3000
```

## Loading Environment Variables

### Node.js
```javascript
require('dotenv').config();
// or
import 'dotenv/config';

const dbUrl = process.env.DATABASE_URL;
```

### Python
```python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
```

### Shell
```bash
# Load .env in current shell
export $(cat .env | xargs)

# Or source it
set -a; source .env; set +a
```

## Best Practices

### Security
```bash
# .gitignore - NEVER commit .env files
.env
.env.local
.env.*.local
```

### Example File
```bash
# Create .env.example with placeholder values
# .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
API_KEY=your-api-key-here
SECRET_KEY=generate-a-secret-key
```

### Environment-Specific Files
```
.env                # Default/shared
.env.local          # Local overrides (gitignored)
.env.development    # Development
.env.production     # Production
.env.test           # Testing
```

## Debugging

### Check Current Environment
```bash
# Print all env vars
env | sort

# Check specific variable
echo $DATABASE_URL

# Check if variable is set
[ -z "$API_KEY" ] && echo "API_KEY not set"
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Variable not loading | Check file path, ensure dotenv is loaded first |
| Quotes in value | Remove surrounding quotes in .env |
| Newlines in value | Use `\n` or actual newlines in quotes |
| Variable undefined | Check spelling, case sensitivity |
| Wrong environment | Verify which .env file is being loaded |

## Required Variables Checklist

```markdown
## Environment Setup Checklist

### Required
- [ ] DATABASE_URL
- [ ] SECRET_KEY
- [ ] API_KEY

### Optional
- [ ] DEBUG (default: false)
- [ ] PORT (default: 3000)
- [ ] LOG_LEVEL (default: info)
```

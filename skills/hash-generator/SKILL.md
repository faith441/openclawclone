---
name: hash-generator
description: Generate cryptographic hashes - MD5, SHA-1, SHA-256, etc. Use when user needs to hash strings, verify file integrity, or generate checksums.
---

# Hash Generator

## Overview

Generates cryptographic hashes for strings and files, and helps verify data integrity.

## When to Use

- User needs to hash a password or string
- User wants to verify file integrity
- User needs a checksum for data
- User asks about hash algorithms

## Quick Commands

### Hash Strings
```bash
# MD5
echo -n "hello" | md5

# SHA-1
echo -n "hello" | shasum

# SHA-256
echo -n "hello" | shasum -a 256

# SHA-512
echo -n "hello" | shasum -a 512
```

### Hash Files
```bash
# MD5
md5 filename.txt

# SHA-256
shasum -a 256 filename.txt

# All common hashes
openssl dgst -md5 -sha1 -sha256 filename.txt
```

## Output Format

```markdown
## Hash Result

**Input:** [string or filename]
**Type:** [String/File]

### Hashes
| Algorithm | Hash |
|-----------|------|
| MD5 | 5d41402abc4b2a76b9719d911017c592 |
| SHA-1 | aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d |
| SHA-256 | 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c... |
| SHA-512 | 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2... |

### Verification
To verify: `echo -n "[input]" | shasum -a 256`
Expected: `[hash]`
```

## Code Examples

### Python
```python
import hashlib

text = "hello"

# MD5
md5_hash = hashlib.md5(text.encode()).hexdigest()

# SHA-256
sha256_hash = hashlib.sha256(text.encode()).hexdigest()

# SHA-512
sha512_hash = hashlib.sha512(text.encode()).hexdigest()

# Hash file
def hash_file(filepath, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()
```

### JavaScript (Node.js)
```javascript
const crypto = require('crypto');

const text = 'hello';

// SHA-256
const hash = crypto.createHash('sha256')
                   .update(text)
                   .digest('hex');
```

## Algorithm Comparison

| Algorithm | Output Length | Security | Use Case |
|-----------|---------------|----------|----------|
| MD5 | 32 hex (128 bit) | ❌ Broken | Checksums only |
| SHA-1 | 40 hex (160 bit) | ❌ Weak | Legacy systems |
| SHA-256 | 64 hex (256 bit) | ✅ Secure | General purpose |
| SHA-512 | 128 hex (512 bit) | ✅ Secure | High security |
| bcrypt | 60 chars | ✅ Secure | Passwords |
| argon2 | Variable | ✅ Best | Passwords |

## Password Hashing

### DO NOT use MD5/SHA for passwords!

Use proper password hashing:

```python
# Python - bcrypt
import bcrypt

password = "mypassword"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify
bcrypt.checkpw(password.encode(), hashed)
```

```javascript
// Node.js - bcrypt
const bcrypt = require('bcrypt');

const hash = await bcrypt.hash('mypassword', 10);
const valid = await bcrypt.compare('mypassword', hash);
```

## Common Uses

| Use Case | Recommended Algorithm |
|----------|----------------------|
| File integrity | SHA-256 |
| Password storage | bcrypt/argon2 |
| Data deduplication | SHA-256 |
| Quick checksums | MD5 (non-security) |
| Digital signatures | SHA-256/SHA-512 |
| Git commits | SHA-1 (legacy) |

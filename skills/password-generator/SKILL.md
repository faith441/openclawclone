---
name: password-generator
description: Generate secure passwords and passphrases. Use when user needs to create strong passwords, API keys, or secret tokens.
---

# Password Generator

## Overview

Generates cryptographically secure passwords, passphrases, and tokens for various use cases.

## When to Use

- User needs a strong password
- User needs an API key or secret token
- User wants a memorable passphrase
- User needs multiple passwords

## Generation Methods

### Random Password (Recommended)
```bash
# macOS/Linux - 32 character password
openssl rand -base64 32

# URL-safe characters
openssl rand -base64 32 | tr -d '/+=' | head -c 32

# Alphanumeric only
openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 32
```

### Python Generation
```python
import secrets
import string

def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Generate
print(generate_password(20))
```

### Passphrase (Memorable)
```bash
# Using words (requires word list)
shuf -n 4 /usr/share/dict/words | tr '\n' '-' | sed 's/-$//'
# Output: correct-horse-battery-staple
```

## Password Strength Guide

| Type | Length | Characters | Use Case |
|------|--------|------------|----------|
| Basic | 12+ | a-z, A-Z, 0-9, symbols | Personal accounts |
| Strong | 16+ | All printable ASCII | Important accounts |
| Passphrase | 4+ words | Words + separator | Memorable passwords |
| API Key | 32+ | Base64/Hex | API authentication |
| Encryption Key | 32+ bytes | Any | Encryption |

## Output Format

```markdown
## Generated Password

**Type:** [Random/Passphrase/Token]
**Length:** [character count]
**Strength:** [Weak/Medium/Strong/Very Strong]

### Password
```
[generated password here]
```

### Strength Analysis
- ✅ Length: [X] characters
- ✅ Uppercase letters
- ✅ Lowercase letters
- ✅ Numbers
- ✅ Special characters

### Estimated Crack Time
~[X years/centuries] with modern hardware
```

## Common Formats

### UUID (for unique IDs)
```bash
uuidgen
# Output: 550e8400-e29b-41d4-a716-446655440000
```

### Hex Token
```bash
openssl rand -hex 32
# Output: 64 character hex string
```

### JWT Secret
```bash
openssl rand -base64 64
```

## Security Tips

1. **Never reuse** - Each account gets unique password
2. **Use a password manager** - Don't memorize complex passwords
3. **Enable 2FA** - Passwords alone aren't enough
4. **Avoid patterns** - No birthdays, names, or keyboard walks
5. **Longer is better** - Length beats complexity

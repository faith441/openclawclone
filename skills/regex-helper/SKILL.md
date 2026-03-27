---
name: regex-helper
description: Build and explain regular expressions. Use when user needs to create a regex pattern, understand an existing pattern, or test regex matching.
---

# Regex Helper

## Overview

Helps create, explain, and test regular expressions for pattern matching in text.

## When to Use

- User needs to match a specific pattern
- User has a regex they don't understand
- User wants to validate text format
- User needs to extract parts of text

## Output Format

### Building a Regex
```markdown
## Regex Pattern

**Pattern:** `[regex here]`
**Flags:** [g/i/m if needed]

### Explanation
[Part-by-part breakdown]

### Matches
✅ `example1` - [why it matches]
✅ `example2` - [why it matches]

### Does NOT Match
❌ `example3` - [why it doesn't match]
❌ `example4` - [why it doesn't match]

### Usage Example
```python
import re
pattern = r'[regex]'
matches = re.findall(pattern, text)
```
```

### Explaining a Regex
```markdown
## Pattern Breakdown: `[regex]`

| Part | Meaning |
|------|---------|
| `[part]` | [explanation] |
| `[part]` | [explanation] |

### In Plain English
[Human-readable description]
```

## Common Patterns

### Email
```regex
^[\w\.-]+@[\w\.-]+\.\w{2,}$
```

### Phone (US)
```regex
^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$
```

### URL
```regex
https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)
```

### Date (YYYY-MM-DD)
```regex
^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$
```

### IP Address
```regex
^(\d{1,3}\.){3}\d{1,3}$
```

## Regex Cheat Sheet

| Symbol | Meaning |
|--------|---------|
| `.` | Any character |
| `\d` | Digit (0-9) |
| `\w` | Word char (a-z, A-Z, 0-9, _) |
| `\s` | Whitespace |
| `^` | Start of string |
| `$` | End of string |
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `{n}` | Exactly n |
| `{n,m}` | n to m times |
| `[abc]` | Any of a, b, c |
| `[^abc]` | Not a, b, or c |
| `(...)` | Capture group |
| `(?:...)` | Non-capture group |
| `\|` | Or |

## Questions to Ask

- "What text are you trying to match?"
- "Can you give examples of valid and invalid inputs?"
- "What language/tool will you use this in?"

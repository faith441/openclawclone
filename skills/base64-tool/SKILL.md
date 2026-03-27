---
name: base64-tool
description: Encode and decode Base64 strings. Use when user needs to encode/decode Base64, handle binary data, or work with data URLs.
---

# Base64 Tool

## Overview

Encodes and decodes Base64 strings, handles binary data, and creates data URLs.

## When to Use

- User needs to encode text to Base64
- User needs to decode a Base64 string
- User is working with data URLs
- User needs to embed binary data

## Quick Commands

### Encode
```bash
# Encode string
echo -n "Hello World" | base64
# Output: SGVsbG8gV29ybGQ=

# Encode file
base64 -i image.png

# Encode file (one line)
base64 -w 0 image.png  # Linux
base64 -b 0 image.png  # macOS
```

### Decode
```bash
# Decode string
echo "SGVsbG8gV29ybGQ=" | base64 -d
# Output: Hello World

# Decode to file
echo "..." | base64 -d > output.png
```

## Output Format

```markdown
## Base64 Conversion

**Operation:** [Encode/Decode]
**Input length:** [X] characters
**Output length:** [Y] characters

### Result
```
[encoded/decoded result]
```

### Details
- Original: [original string or description]
- Encoding: Base64 (RFC 4648)
```

## Code Examples

### Python
```python
import base64

# Encode string
text = "Hello World"
encoded = base64.b64encode(text.encode()).decode()
# 'SGVsbG8gV29ybGQ='

# Decode string
decoded = base64.b64decode(encoded).decode()
# 'Hello World'

# Encode binary file
with open('image.png', 'rb') as f:
    encoded = base64.b64encode(f.read()).decode()

# URL-safe Base64
encoded = base64.urlsafe_b64encode(text.encode()).decode()
```

### JavaScript
```javascript
// Encode
const encoded = btoa("Hello World");
// 'SGVsbG8gV29ybGQ='

// Decode
const decoded = atob("SGVsbG8gV29ybGQ=");
// 'Hello World'

// For Unicode strings
const encoded = btoa(unescape(encodeURIComponent("Hello 世界")));
const decoded = decodeURIComponent(escape(atob(encoded)));
```

## Data URLs

### Format
```
data:[mediatype][;base64],<data>
```

### Examples
```html
<!-- Image -->
<img src="data:image/png;base64,iVBORw0KGgo..." />

<!-- CSS -->
background-image: url(data:image/svg+xml;base64,PHN2Zy...);

<!-- JSON -->
data:application/json;base64,eyJuYW1lIjogIkpvaG4ifQ==
```

### Create Data URL
```python
import base64

with open('image.png', 'rb') as f:
    data = base64.b64encode(f.read()).decode()
    data_url = f"data:image/png;base64,{data}"
```

## Common MIME Types

| Extension | MIME Type |
|-----------|-----------|
| .png | image/png |
| .jpg/.jpeg | image/jpeg |
| .gif | image/gif |
| .svg | image/svg+xml |
| .pdf | application/pdf |
| .json | application/json |
| .txt | text/plain |

## Notes

- Base64 increases size by ~33%
- Padding (`=`) is required for standard Base64
- URL-safe Base64 uses `-` and `_` instead of `+` and `/`
- Line breaks may be added for readability (76 chars)

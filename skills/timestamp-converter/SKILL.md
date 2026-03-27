---
name: timestamp-converter
description: Convert between timestamps and date formats. Use when user needs to convert Unix timestamps, ISO dates, or parse date strings.
---

# Timestamp Converter

## Overview

Converts between various timestamp and date formats, including Unix timestamps, ISO 8601, and human-readable dates.

## When to Use

- User has a Unix timestamp to convert
- User needs to convert dates between formats
- User asks about time differences
- User needs current timestamp

## Common Formats

### Unix Timestamp
```
Seconds since 1970-01-01 00:00:00 UTC
Example: 1703980800
```

### Unix Milliseconds
```
Milliseconds since epoch
Example: 1703980800000
```

### ISO 8601
```
YYYY-MM-DDTHH:mm:ss.sssZ
Example: 2024-12-31T00:00:00.000Z
```

### RFC 2822
```
Day, DD Mon YYYY HH:mm:ss +0000
Example: Tue, 31 Dec 2024 00:00:00 +0000
```

## Output Format

```markdown
## Timestamp Conversion

**Input:** [original value]
**Type:** [detected format]

### All Formats
| Format | Value |
|--------|-------|
| Unix (seconds) | 1703980800 |
| Unix (milliseconds) | 1703980800000 |
| ISO 8601 | 2024-12-31T00:00:00.000Z |
| RFC 2822 | Tue, 31 Dec 2024 00:00:00 +0000 |
| Human Readable | December 31, 2024 12:00:00 AM UTC |

### In Different Timezones
| Timezone | Local Time |
|----------|------------|
| UTC | 2024-12-31 00:00:00 |
| EST (UTC-5) | 2024-12-30 19:00:00 |
| PST (UTC-8) | 2024-12-30 16:00:00 |
```

## Quick Conversions

### Get Current Timestamp
```bash
# Unix seconds
date +%s

# Unix milliseconds
date +%s%3N

# ISO 8601
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

### Convert in Code

#### Python
```python
from datetime import datetime, timezone

# Unix to datetime
ts = 1703980800
dt = datetime.fromtimestamp(ts, tz=timezone.utc)

# Datetime to Unix
ts = int(dt.timestamp())

# Parse ISO string
dt = datetime.fromisoformat("2024-12-31T00:00:00+00:00")

# Format to ISO
iso_str = dt.isoformat()
```

#### JavaScript
```javascript
// Unix to Date
const ts = 1703980800;
const date = new Date(ts * 1000);

// Date to Unix
const ts = Math.floor(date.getTime() / 1000);

// Parse ISO string
const date = new Date("2024-12-31T00:00:00.000Z");

// Format to ISO
const iso = date.toISOString();
```

## Time Calculations

### Time Ago
| Seconds | Human Readable |
|---------|----------------|
| < 60 | X seconds ago |
| < 3600 | X minutes ago |
| < 86400 | X hours ago |
| < 604800 | X days ago |
| < 2592000 | X weeks ago |
| < 31536000 | X months ago |
| >= 31536000 | X years ago |

### Duration Between Dates
```python
from datetime import datetime

d1 = datetime(2024, 1, 1)
d2 = datetime(2024, 12, 31)
diff = d2 - d1

print(f"{diff.days} days")
print(f"{diff.total_seconds()} seconds")
```

---
name: data-validator
description: Validate data against rules and schemas. Use when user needs to check data quality, validate formats, or ensure data meets requirements.
---

# Data Validator

## Overview

Validates data against defined rules, schemas, or quality requirements. Identifies issues and suggests fixes.

## When to Use

- User needs to check data quality
- User wants to validate data format
- User needs to ensure data meets requirements

## Validation Output

```markdown
## Validation Results

**Status:** ✅ PASSED / ❌ FAILED / ⚠️ WARNINGS
**Records checked:** [count]
**Issues found:** [count]

### Summary
| Check | Status | Issues |
|-------|--------|--------|
| Required fields | ✅ | 0 |
| Data types | ⚠️ | 3 |
| Format validation | ❌ | 12 |
| Business rules | ✅ | 0 |

### Issues Detail

#### ❌ Critical Issues
| Row | Field | Issue | Value |
|-----|-------|-------|-------|
| 5 | email | Invalid format | "not-an-email" |

#### ⚠️ Warnings
| Row | Field | Issue | Value |
|-----|-------|-------|-------|
| 12 | phone | Missing country code | "555-1234" |

### Recommendations
1. [How to fix issue 1]
2. [How to fix issue 2]
```

## Common Validations

### Required Fields
```python
required = ['name', 'email', 'id']
missing = [f for f in required if f not in data or not data[f]]
```

### Email Format
```python
import re
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
valid = bool(re.match(email_pattern, email))
```

### Date Format
```python
from datetime import datetime
try:
    datetime.strptime(date_str, '%Y-%m-%d')
except ValueError:
    print("Invalid date format")
```

### Number Range
```python
valid = min_val <= value <= max_val
```

### Unique Values
```python
duplicates = df[df.duplicated(subset=['id'], keep=False)]
```

## Validation Rules Template

```yaml
fields:
  email:
    required: true
    type: string
    format: email
  age:
    required: true
    type: integer
    min: 0
    max: 150
  status:
    required: true
    enum: [active, inactive, pending]
```

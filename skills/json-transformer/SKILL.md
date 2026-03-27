---
name: json-transformer
description: Transform JSON data structures - flatten, reshape, filter, convert formats. Use when user needs to modify JSON structure or convert between formats.
---

# JSON Transformer

## Overview

Transforms JSON data between different structures, flattens nested objects, filters data, and converts between JSON and other formats.

## When to Use

- User needs to reshape JSON structure
- User wants to flatten nested JSON
- User needs to convert JSON to/from CSV, YAML, etc.
- User wants to filter or extract parts of JSON

## Common Transformations

### Flatten Nested JSON
```python
# Before
{"user": {"name": "John", "address": {"city": "NYC"}}}

# After
{"user.name": "John", "user.address.city": "NYC"}
```

### Extract Fields
```python
# From array of objects, extract specific fields
data = [{"id": 1, "name": "A", "extra": "x"}, ...]
result = [{"id": d["id"], "name": d["name"]} for d in data]
```

### Rename Keys
```python
key_map = {"old_name": "new_name", "oldKey": "newKey"}
result = {key_map.get(k, k): v for k, v in data.items()}
```

### Group By Field
```python
from itertools import groupby
from operator import itemgetter

data.sort(key=itemgetter('category'))
grouped = {k: list(v) for k, v in groupby(data, key=itemgetter('category'))}
```

### JSON to CSV
```python
import pandas as pd
df = pd.json_normalize(data)
df.to_csv('output.csv', index=False)
```

### JSON to YAML
```python
import yaml
yaml_str = yaml.dump(data, default_flow_style=False)
```

## Using jq (Command Line)

```bash
# Extract field
cat data.json | jq '.users[].name'

# Filter
cat data.json | jq '.items | map(select(.price > 100))'

# Transform
cat data.json | jq '{names: [.users[].name]}'
```

## Output Format

When transforming, show:
1. **Input structure** (summarized)
2. **Transformation applied**
3. **Output structure/sample**
4. **Code to reproduce**

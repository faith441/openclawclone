---
name: unit-converter
description: Convert between units of measurement. Use when user needs to convert length, weight, temperature, time, data sizes, or other units.
---

# Unit Converter

## Overview

Converts between various units of measurement including length, weight, temperature, time, and data sizes.

## When to Use

- User asks to convert units
- User needs measurement conversions
- User asks "how many X in Y"

## Quick Conversions

### Length
| From | To | Multiply by |
|------|-----|-------------|
| inches | cm | 2.54 |
| feet | meters | 0.3048 |
| miles | km | 1.60934 |
| cm | inches | 0.393701 |
| meters | feet | 3.28084 |
| km | miles | 0.621371 |

### Weight
| From | To | Multiply by |
|------|-----|-------------|
| pounds | kg | 0.453592 |
| ounces | grams | 28.3495 |
| kg | pounds | 2.20462 |
| grams | ounces | 0.035274 |

### Temperature
```
Celsius to Fahrenheit: (C × 9/5) + 32
Fahrenheit to Celsius: (F - 32) × 5/9
Celsius to Kelvin: C + 273.15
```

### Data Size
| Unit | Bytes |
|------|-------|
| 1 KB | 1,024 |
| 1 MB | 1,048,576 |
| 1 GB | 1,073,741,824 |
| 1 TB | 1,099,511,627,776 |

### Time
| Unit | Seconds |
|------|---------|
| 1 minute | 60 |
| 1 hour | 3,600 |
| 1 day | 86,400 |
| 1 week | 604,800 |
| 1 year | 31,536,000 |

## Output Format

```markdown
## Conversion Result

**Input:** [value] [unit]
**Output:** [converted value] [target unit]

### Calculation
[value] [unit] × [conversion factor] = [result] [target unit]

### Related Conversions
- [value] [unit] = [X] [other unit 1]
- [value] [unit] = [X] [other unit 2]
```

## Common Conversions Reference

### Cooking
- 1 cup = 237 ml = 16 tablespoons
- 1 tablespoon = 15 ml = 3 teaspoons
- 1 teaspoon = 5 ml

### Distance Approximations
- 1 meter ≈ 1 yard (actually 1.094 yards)
- 1 km ≈ 0.6 miles
- 1 inch = 2.54 cm (exact)

### Speed
- 1 mph = 1.60934 km/h
- 1 km/h = 0.621371 mph
- 1 knot = 1.852 km/h

## Programming Helper

```python
def convert_bytes(bytes_val):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"
```

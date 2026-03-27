---
name: color-converter
description: Convert between color formats - HEX, RGB, HSL, etc. Use when user needs to convert colors between different representations.
---

# Color Converter

## Overview

Converts colors between different formats: HEX, RGB, HSL, and provides color information.

## When to Use

- User provides a color and needs it in different format
- User asks about color conversions
- User needs color values for CSS/design

## Color Formats

### HEX
```
#RRGGBB or #RGB
Example: #FF5733, #F53
```

### RGB
```
rgb(red, green, blue)
Values: 0-255
Example: rgb(255, 87, 51)
```

### RGBA
```
rgba(red, green, blue, alpha)
Alpha: 0-1
Example: rgba(255, 87, 51, 0.5)
```

### HSL
```
hsl(hue, saturation%, lightness%)
Hue: 0-360
Saturation/Lightness: 0-100%
Example: hsl(11, 100%, 60%)
```

## Output Format

```markdown
## Color Conversion

**Input:** [original color]

### All Formats
| Format | Value |
|--------|-------|
| HEX | #FF5733 |
| RGB | rgb(255, 87, 51) |
| RGBA | rgba(255, 87, 51, 1) |
| HSL | hsl(11, 100%, 60%) |

### CSS Variables
```css
--color-primary: #FF5733;
--color-primary-rgb: 255, 87, 51;
--color-primary-hsl: 11, 100%, 60%;
```

### Color Preview
██████ [color name if applicable]
```

## Conversion Formulas

### HEX to RGB
```python
hex_color = "#FF5733"
r = int(hex_color[1:3], 16)  # 255
g = int(hex_color[3:5], 16)  # 87
b = int(hex_color[5:7], 16)  # 51
```

### RGB to HEX
```python
r, g, b = 255, 87, 51
hex_color = f"#{r:02x}{g:02x}{b:02x}"  # #ff5733
```

### RGB to HSL
```python
def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2

    if max_c == min_c:
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return round(h * 360), round(s * 100), round(l * 100)
```

## Common Colors Reference

| Name | HEX | RGB |
|------|-----|-----|
| White | #FFFFFF | rgb(255, 255, 255) |
| Black | #000000 | rgb(0, 0, 0) |
| Red | #FF0000 | rgb(255, 0, 0) |
| Green | #00FF00 | rgb(0, 255, 0) |
| Blue | #0000FF | rgb(0, 0, 255) |
| Yellow | #FFFF00 | rgb(255, 255, 0) |
| Cyan | #00FFFF | rgb(0, 255, 255) |
| Magenta | #FF00FF | rgb(255, 0, 255) |

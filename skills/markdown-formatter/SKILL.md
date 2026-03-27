---
name: markdown-formatter
description: Format text as Markdown. Use when user has unformatted text and wants it converted to Markdown, or needs help with Markdown syntax.
---

# Markdown Formatter

## Overview

Converts unformatted text into well-structured Markdown, or helps with Markdown syntax and formatting.

## When to Use

- User has plain text to convert to Markdown
- User needs Markdown syntax help
- User wants to improve document formatting
- User needs tables, lists, or other structures

## Output Format

When formatting text, provide:
1. The formatted Markdown
2. Brief explanation of formatting choices

## Markdown Quick Reference

### Text Formatting
```markdown
**bold** or __bold__
*italic* or _italic_
~~strikethrough~~
`inline code`
[link text](url)
![alt text](image-url)
```

### Headings
```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Lists
```markdown
- Unordered item
- Another item
  - Nested item

1. Ordered item
2. Another item
   1. Nested item

- [ ] Task item
- [x] Completed task
```

### Code Blocks
````markdown
```python
def hello():
    print("Hello, World!")
```
````

### Tables
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Blockquotes
```markdown
> This is a quote
> Multiple lines
```

### Horizontal Rule
```markdown
---
```

## Formatting Guidelines

1. **Use headings** to create hierarchy
2. **Lists for enumeration** - bullets for unordered, numbers for steps
3. **Tables for comparisons** - when data has clear columns
4. **Code blocks** - for any code or commands
5. **Emphasis sparingly** - too much bold loses impact
6. **Consistent style** - pick a convention and stick to it

## Common Conversions

### Plain Text → Structured
```
Before: Meeting notes from Monday. Discussed Q4 goals. John will handle marketing. Sarah owns engineering.

After:
# Meeting Notes - Monday

## Discussion
- Q4 goals review

## Action Items
- **John:** Handle marketing
- **Sarah:** Own engineering
```

---
name: text-translator
description: Translate text between languages. Use when user provides text to translate or asks for translations. Supports common languages and preserves formatting.
---

# Text Translator

## Overview

Translates text between languages while preserving meaning, tone, and formatting.

## When to Use

- User provides text to translate
- User asks for translation to/from a language
- User needs multiple language versions

## Output Format

```markdown
## Translation

**From:** [Source language]
**To:** [Target language]

### Original
[Original text]

### Translation
[Translated text]

### Notes
- [Any cultural context or nuances]
- [Alternative translations for ambiguous phrases]
```

## Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | en | Japanese | ja |
| Spanish | es | Korean | ko |
| French | fr | Arabic | ar |
| German | de | Hindi | hi |
| Italian | it | Portuguese | pt |
| Chinese | zh | Russian | ru |

## Translation Guidelines

1. **Preserve meaning** over literal translation
2. **Maintain tone** - formal stays formal, casual stays casual
3. **Keep formatting** - preserve paragraphs, lists, emphasis
4. **Handle idioms** - use equivalent expressions in target language
5. **Note ambiguity** - when multiple interpretations exist

## Special Cases

### Technical Terms
```
Keep technical terms in original if commonly used:
"API" → "API" (not translated)
"machine learning" → "machine learning" or localized term
```

### Formal vs Informal
```
Spanish: tú (informal) vs usted (formal)
French: tu (informal) vs vous (formal)
German: du (informal) vs Sie (formal)
```

### Proper Nouns
```
Generally keep names unchanged:
"John" → "John" (not "Juan")
Unless user requests localization
```

## Questions to Ask

- "What language should I translate to?"
- "Should I use formal or informal tone?"
- "Should I keep technical terms in English?"

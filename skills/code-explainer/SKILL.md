---
name: code-explainer
description: Explain code snippets in plain language. Use when user pastes code and wants to understand what it does, how it works, or needs documentation.
---

# Code Explainer

## Overview

Explains code in clear, understandable language. Breaks down logic, identifies patterns, and provides context for how code works.

## When to Use

- User pastes code and asks "what does this do?"
- User needs to understand unfamiliar code
- User wants documentation for code

## Output Format

```markdown
## Code Explanation

**Language:** [Detected language]
**Purpose:** [One-line summary of what the code does]

### Overview
[2-3 sentences describing the overall function]

### Step-by-Step Breakdown

1. **[Lines X-Y]:** [What this section does]
   ```[language]
   [relevant code snippet]
   ```
   [Explanation]

2. **[Lines X-Y]:** [What this section does]
   [Explanation]

### Key Concepts Used
- **[Concept 1]:** [Brief explanation]
- **[Concept 2]:** [Brief explanation]

### Input/Output
- **Input:** [What the code expects]
- **Output:** [What the code produces]

### Example Usage
```[language]
[Example of how to use this code]
```

### Potential Issues
- [Any bugs, edge cases, or concerns]
```

## Explanation Levels

### Beginner
- Explain every concept
- Define technical terms
- Use analogies

### Intermediate
- Focus on logic flow
- Explain non-obvious parts
- Skip basic syntax explanation

### Expert
- Focus on architecture decisions
- Discuss performance implications
- Highlight advanced patterns

## What to Look For

1. **Function signatures** - What goes in/out
2. **Control flow** - if/else, loops, recursion
3. **Data transformations** - How data changes
4. **Side effects** - External changes (DB, files, network)
5. **Error handling** - Try/catch, validation
6. **Dependencies** - External libraries used

## Questions to Ask

- "What's your experience level with [language]?"
- "Any specific part you're confused about?"
- "Do you want a high-level overview or detailed breakdown?"

---
name: diff-explainer
description: Explain code diffs and changes. Use when user provides a git diff or code changes and wants to understand what changed and why it matters.
---

# Diff Explainer

## Overview

Explains code diffs in plain language, highlighting what changed, potential impacts, and whether changes look correct.

## When to Use

- User pastes a git diff
- User wants to understand PR changes
- User needs to review code modifications
- User asks "what changed?"

## Output Format

```markdown
## Diff Summary

**Files Changed:** [count]
**Lines Added:** [+count]
**Lines Removed:** [-count]
**Change Type:** [Feature/Bugfix/Refactor/Config/etc.]

### Overview
[1-2 sentence summary of what this diff accomplishes]

### Changes by File

#### `[filename]`
**Purpose of changes:** [What was modified and why]

| Change | Description |
|--------|-------------|
| + Line X | [What was added and why] |
| - Line Y | [What was removed and why] |

### Key Changes

1. **[Change category]**
   - [Specific change]
   - [Impact or reason]

2. **[Change category]**
   - [Specific change]
   - [Impact or reason]

### Potential Concerns
- ⚠️ [Any issues or things to watch]
- ✅ [Positive observations]

### Summary
[Final assessment: Does this look correct? Any suggestions?]
```

## Reading Diff Syntax

```diff
--- a/file.txt    (original)
+++ b/file.txt    (modified)
@@ -1,4 +1,5 @@   (line numbers: old start,count → new start,count)
 unchanged line
-removed line      (prefixed with -)
+added line        (prefixed with +)
 unchanged line
```

## Change Categories

| Type | Indicators |
|------|------------|
| **Feature** | New functions, files, capabilities |
| **Bugfix** | Error handling, edge cases, corrections |
| **Refactor** | Renamed, restructured, no behavior change |
| **Performance** | Optimization, caching, efficiency |
| **Security** | Auth, validation, sanitization |
| **Config** | Settings, environment, dependencies |
| **Docs** | Comments, README, docstrings |
| **Tests** | Test files, assertions |

## What to Look For

1. **Breaking changes** - API modifications, removed features
2. **Security implications** - Input handling, auth changes
3. **Side effects** - Unintended consequences
4. **Missing pieces** - Tests, docs, error handling
5. **Code quality** - Readability, patterns, duplication

## Questions to Ask

- "Is this a PR you're reviewing or your own changes?"
- "Any specific concerns you want me to check for?"
- "Should I focus on correctness or style?"

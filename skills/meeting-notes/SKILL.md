---
name: meeting-notes
description: Generate structured meeting notes from transcripts, recordings, or rough notes. Use when user provides meeting content and wants organized notes with action items.
---

# Meeting Notes

## Overview

Transforms raw meeting transcripts or rough notes into structured, professional meeting notes with clear action items and decisions.

## When to Use

- User pastes a meeting transcript
- User provides rough meeting notes to organize
- User asks to create meeting minutes

## Output Format

```markdown
# Meeting Notes: [Meeting Title]

**Date:** [Date if mentioned]
**Attendees:** [Names if mentioned]
**Duration:** [If mentioned]

## Summary
[2-3 sentence overview]

## Discussion Points

### [Topic 1]
- [Key points discussed]
- [Decisions made]

### [Topic 2]
- [Key points discussed]
- [Decisions made]

## Decisions Made
1. [Decision with rationale if provided]

## Action Items
| Owner | Task | Due Date |
|-------|------|----------|
| [Name] | [Task] | [Date] |

## Next Steps
- [What happens next]

## Parking Lot
- [Items deferred for later discussion]
```

## Guidelines

1. **Extract attendees** from mentions in the transcript
2. **Identify decisions** - look for phrases like "agreed", "decided", "will do"
3. **Find action items** - look for assignments, commitments, "I'll", "we need to"
4. **Note blockers** - any issues preventing progress
5. **Keep it concise** - meeting notes should be scannable

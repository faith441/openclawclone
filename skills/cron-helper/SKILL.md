---
name: cron-helper
description: Help with cron expressions and scheduled tasks. Use when user needs to create, understand, or debug cron schedules.
---

# Cron Helper

## Overview

Helps create, explain, and debug cron expressions for scheduled tasks.

## When to Use

- User needs to create a cron schedule
- User wants to understand a cron expression
- User needs to debug scheduled task timing

## Cron Format

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * * command
```

## Special Characters

| Char | Meaning | Example |
|------|---------|---------|
| `*` | Any value | `* * * * *` = every minute |
| `,` | List | `1,15` = 1st and 15th |
| `-` | Range | `1-5` = 1 through 5 |
| `/` | Step | `*/15` = every 15 |

## Common Examples

| Schedule | Cron Expression |
|----------|-----------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Every day at midnight | `0 0 * * *` |
| Every day at 9 AM | `0 9 * * *` |
| Every Monday at 9 AM | `0 9 * * 1` |
| Every weekday at 9 AM | `0 9 * * 1-5` |
| First of month at midnight | `0 0 1 * *` |
| Every 15 minutes during work hours | `*/15 9-17 * * 1-5` |
| Twice daily (9 AM and 5 PM) | `0 9,17 * * *` |

## Output Format

When explaining a cron expression:

```markdown
## Cron Expression: `[expression]`

**Runs:** [human-readable description]

### Breakdown
| Field | Value | Meaning |
|-------|-------|---------|
| Minute | [val] | [meaning] |
| Hour | [val] | [meaning] |
| Day | [val] | [meaning] |
| Month | [val] | [meaning] |
| Weekday | [val] | [meaning] |

### Next 5 Run Times
1. [datetime]
2. [datetime]
3. [datetime]
4. [datetime]
5. [datetime]
```

## Common Mistakes

1. **Month/Day confusion** - Remember: day-of-month comes before month
2. **Sunday = 0 or 7** - Both work, but 0 is standard
3. **24-hour time** - Use 0-23, not 1-24
4. **Timezone** - Cron uses system timezone
5. **Overlapping conditions** - Day-of-month AND day-of-week are OR'd

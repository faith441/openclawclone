---
name: daily-planner
description: Create daily schedules and time-blocked plans. Use when user wants to plan their day, allocate time for tasks, or create a structured routine.
---

# Daily Planner

## Overview

Creates time-blocked daily schedules that account for energy levels, task types, and realistic time estimates.

## When to Use

- User wants to plan their day
- User has tasks and meetings to fit into a schedule
- User asks for a morning/evening routine

## Output Format

```markdown
# Daily Plan: [Day/Date]

## 🌅 Morning Block (High Energy)
| Time | Activity | Duration |
|------|----------|----------|
| 08:00 | [Deep work task] | 90 min |
| 09:30 | Break | 15 min |
| 09:45 | [Task] | 45 min |

## ☀️ Midday Block
| Time | Activity | Duration |
|------|----------|----------|
| 10:30 | [Meetings/Calls] | 60 min |
| 11:30 | [Task] | 30 min |
| 12:00 | Lunch | 60 min |

## 🌤️ Afternoon Block (Medium Energy)
| Time | Activity | Duration |
|------|----------|----------|
| 13:00 | [Collaborative work] | 90 min |
| 14:30 | Break | 15 min |
| 14:45 | [Task] | 75 min |

## 🌙 Evening Block (Wind Down)
| Time | Activity | Duration |
|------|----------|----------|
| 16:00 | [Admin/Email] | 45 min |
| 16:45 | Plan tomorrow | 15 min |

## Today's Top 3 Priorities
1. [ ] [Most important task]
2. [ ] [Second priority]
3. [ ] [Third priority]
```

## Planning Principles

1. **Deep work first** - Schedule demanding tasks when energy is highest
2. **Buffer time** - Add 15-30% buffer between tasks
3. **Batch similar tasks** - Group emails, calls, admin work
4. **Energy matching** - Creative work AM, routine work PM
5. **Protect breaks** - Short breaks every 90 minutes
6. **Realistic estimates** - Most tasks take longer than expected

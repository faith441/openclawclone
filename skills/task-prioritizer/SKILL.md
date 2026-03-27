---
name: task-prioritizer
description: Prioritize tasks using the Eisenhower matrix (urgent/important). Use when user has a list of tasks and needs help deciding what to focus on first.
---

# Task Prioritizer

## Overview

Helps prioritize tasks using the Eisenhower Matrix, categorizing by urgency and importance to maximize productivity.

## When to Use

- User has a list of tasks and feels overwhelmed
- User asks what to work on first
- User wants to organize their to-do list

## The Eisenhower Matrix

```
                    URGENT              NOT URGENT
              ┌─────────────────┬─────────────────┐
   IMPORTANT  │   DO FIRST      │   SCHEDULE      │
              │   (Quadrant 1)  │   (Quadrant 2)  │
              │   Crisis,       │   Planning,     │
              │   Deadlines     │   Growth        │
              ├─────────────────┼─────────────────┤
NOT IMPORTANT │   DELEGATE      │   ELIMINATE     │
              │   (Quadrant 3)  │   (Quadrant 4)  │
              │   Interruptions │   Time wasters  │
              └─────────────────┴─────────────────┘
```

## Output Format

When prioritizing tasks:

### 🔴 Do First (Urgent + Important)
- [Task] - [Why it's urgent and important]

### 🟡 Schedule (Important, Not Urgent)
- [Task] - [Suggested timeframe]

### 🟠 Delegate (Urgent, Not Important)
- [Task] - [Who could handle this]

### ⚪ Eliminate/Minimize
- [Task] - [Why this is low priority]

### Recommended Order
1. [First task to tackle]
2. [Second task]
3. [etc.]

## Questions to Ask

If task context is unclear, ask:
- "What's the deadline for [task]?"
- "What happens if [task] doesn't get done this week?"
- "Can someone else handle [task]?"

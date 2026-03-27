---
name: log-parser
description: Parse and analyze log files - find errors, extract patterns, summarize events. Use when user has logs to analyze or needs to find specific events in log data.
---

# Log Parser

## Overview

Parses and analyzes log files to find errors, extract patterns, identify trends, and summarize events.

## When to Use

- User pastes log data to analyze
- User needs to find errors in logs
- User wants to understand what happened from logs
- User needs to extract specific information from logs

## Analysis Output

```markdown
## Log Analysis Summary

**Time Range:** [Start] to [End]
**Total Lines:** [count]
**Log Type:** [application/access/system/etc.]

### Event Distribution
| Level | Count | Percentage |
|-------|-------|------------|
| ERROR | [n] | [%] |
| WARN | [n] | [%] |
| INFO | [n] | [%] |
| DEBUG | [n] | [%] |

### Errors Found
| Time | Error | Count | First Occurrence |
|------|-------|-------|------------------|
| [time] | [message] | [n] | [line #] |

### Key Events Timeline
1. [Time] - [Event description]
2. [Time] - [Event description]
3. [Time] - [Event description]

### Patterns Detected
- [Pattern 1 with frequency]
- [Pattern 2 with frequency]

### Recommendations
1. [Suggested action based on findings]
```

## Common Log Formats

### Apache/Nginx Access Log
```
192.168.1.1 - - [10/Oct/2024:13:55:36 -0700] "GET /page HTTP/1.1" 200 2326
```

### Application Log
```
2024-10-10 13:55:36 ERROR [main] com.app.Service - Connection failed: timeout
```

### JSON Log
```json
{"timestamp":"2024-10-10T13:55:36Z","level":"ERROR","message":"Failed"}
```

## Parsing Commands

### Find Errors
```bash
grep -i "error\|exception\|failed" logfile.log
```

### Count by Level
```bash
grep -oP '(ERROR|WARN|INFO|DEBUG)' logfile.log | sort | uniq -c
```

### Extract Timestamps
```bash
grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' logfile.log
```

### Top IPs (Access Log)
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
```

## Questions to Ask

- "What type of log is this?"
- "What time range should I focus on?"
- "Are you looking for specific errors or events?"

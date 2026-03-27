---
name: csv-analyzer
description: Analyze CSV files - show statistics, find patterns, detect issues. Use when user provides CSV data or asks to analyze spreadsheet/tabular data.
---

# CSV Analyzer

## Overview

Analyzes CSV and tabular data to provide statistics, identify patterns, detect data quality issues, and answer questions about the data.

## When to Use

- User pastes CSV data or provides a CSV file
- User asks about data statistics or patterns
- User wants to understand their dataset

## Analysis Output

```markdown
## Dataset Overview
- **Rows:** [count]
- **Columns:** [count]
- **File size:** [if applicable]

## Column Summary

| Column | Type | Non-Null | Unique | Sample Values |
|--------|------|----------|--------|---------------|
| [name] | [type] | [count] | [count] | [examples] |

## Numeric Statistics

| Column | Min | Max | Mean | Median | Std Dev |
|--------|-----|-----|------|--------|---------|
| [name] | [val] | [val] | [val] | [val] | [val] |

## Data Quality Issues
- ⚠️ [Column] has [X] missing values ([Y]%)
- ⚠️ [Column] has [X] duplicate values
- ⚠️ Potential outliers in [Column]

## Key Insights
1. [Insight about the data]
2. [Pattern or trend noticed]
3. [Recommendation]
```

## Common Analysis Tasks

### Quick Stats
```python
import pandas as pd
df = pd.read_csv('file.csv')
print(df.describe())
print(df.info())
```

### Find Missing Values
```python
df.isnull().sum()
```

### Find Duplicates
```python
df.duplicated().sum()
df[df.duplicated()]
```

### Value Counts
```python
df['column'].value_counts()
```

### Correlation
```python
df.corr()
```

## Questions to Ask

- "What questions do you want to answer with this data?"
- "Are there specific columns you're interested in?"
- "Should I look for any particular patterns?"

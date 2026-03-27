---
name: chart-describer
description: Describe data suitable for charts and visualizations. Use when user has data and wants chart recommendations, or needs to prepare data for visualization.
---

# Chart Describer

## Overview

Analyzes data and recommends appropriate chart types, prepares data for visualization, and provides chart specifications.

## When to Use

- User has data and wants to visualize it
- User asks what chart type to use
- User needs chart specifications or descriptions

## Chart Selection Guide

| Data Type | Relationship | Recommended Chart |
|-----------|--------------|-------------------|
| Categories | Comparison | Bar chart |
| Categories | Composition | Pie chart, Stacked bar |
| Time series | Trend | Line chart |
| Two numeric | Correlation | Scatter plot |
| Distribution | Spread | Histogram, Box plot |
| Geographic | Location | Map |
| Hierarchical | Part-to-whole | Treemap, Sunburst |
| Flow | Process | Sankey, Funnel |

## Output Format

```markdown
## Chart Recommendation

**Data Summary:**
- [X] data points
- [Y] categories/series
- Time range: [if applicable]

**Recommended Chart:** [Type]
**Reason:** [Why this chart works best]

### Chart Specification

**Title:** [Descriptive title]
**X-Axis:** [Field] - [Description]
**Y-Axis:** [Field] - [Description]
**Series/Groups:** [If multiple]
**Colors:** [Suggestions]

### Data Preparation

```json
{
  "labels": ["A", "B", "C"],
  "datasets": [{
    "label": "Series 1",
    "data": [10, 20, 30]
  }]
}
```

### Alternative Charts
1. [Alternative 1] - [When to use instead]
2. [Alternative 2] - [When to use instead]
```

## Chart Best Practices

1. **Start Y-axis at zero** for bar charts
2. **Limit pie slices** to 5-7 segments
3. **Use consistent colors** across related charts
4. **Add context** - titles, labels, legends
5. **Avoid 3D effects** - they distort perception

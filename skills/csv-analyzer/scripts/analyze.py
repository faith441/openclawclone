#!/usr/bin/env python3
"""
CSV Analyzer - Analyze CSV files and generate statistics

Usage:
    python analyze.py <csv_file> [--output json|markdown|text]
    python analyze.py data.csv
    python analyze.py data.csv --output markdown

Features:
- Column type detection
- Basic statistics (min, max, mean, median, std)
- Missing value detection
- Duplicate detection
- Value distributions
"""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, median, stdev


def detect_type(values):
    """Detect the type of a column based on its values."""
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return "empty"

    # Try numeric
    numeric_count = 0
    for v in non_empty:
        try:
            float(v.replace(",", ""))
            numeric_count += 1
        except ValueError:
            pass

    if numeric_count == len(non_empty):
        return "numeric"
    elif numeric_count > len(non_empty) * 0.8:
        return "mostly_numeric"

    # Check for boolean
    bool_values = {"true", "false", "yes", "no", "1", "0", "t", "f", "y", "n"}
    if all(v.lower() in bool_values for v in non_empty):
        return "boolean"

    return "string"


def analyze_numeric(values):
    """Analyze numeric column."""
    nums = []
    for v in values:
        try:
            nums.append(float(v.replace(",", "")))
        except (ValueError, AttributeError):
            pass

    if not nums:
        return {}

    stats = {
        "min": min(nums),
        "max": max(nums),
        "mean": round(mean(nums), 2),
        "median": round(median(nums), 2),
    }

    if len(nums) > 1:
        stats["std_dev"] = round(stdev(nums), 2)

    return stats


def analyze_csv(file_path):
    """Analyze a CSV file and return statistics."""
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return {"error": "Empty CSV file"}

    columns = list(rows[0].keys())

    result = {
        "file": str(path.name),
        "rows": len(rows),
        "columns": len(columns),
        "column_details": {},
        "data_quality": {
            "missing_values": {},
            "duplicates": 0,
        }
    }

    # Analyze each column
    for col in columns:
        values = [row.get(col, "") for row in rows]
        col_type = detect_type(values)

        non_empty = [v for v in values if v.strip()]
        missing = len(values) - len(non_empty)
        unique = len(set(non_empty))

        col_info = {
            "type": col_type,
            "non_null": len(non_empty),
            "missing": missing,
            "unique": unique,
            "sample_values": list(set(non_empty))[:5],
        }

        if col_type in ("numeric", "mostly_numeric"):
            col_info["statistics"] = analyze_numeric(values)
        elif col_type == "string" and unique <= 20:
            col_info["value_counts"] = dict(Counter(non_empty).most_common(10))

        result["column_details"][col] = col_info

        if missing > 0:
            result["data_quality"]["missing_values"][col] = {
                "count": missing,
                "percentage": round(missing / len(values) * 100, 1)
            }

    # Check for duplicate rows
    row_tuples = [tuple(row.values()) for row in rows]
    result["data_quality"]["duplicates"] = len(row_tuples) - len(set(row_tuples))

    return result


def format_markdown(analysis):
    """Format analysis as Markdown."""
    if "error" in analysis:
        return f"**Error:** {analysis['error']}"

    lines = [
        f"## CSV Analysis: {analysis['file']}",
        "",
        f"**Rows:** {analysis['rows']}",
        f"**Columns:** {analysis['columns']}",
        "",
        "### Column Summary",
        "",
        "| Column | Type | Non-Null | Missing | Unique |",
        "|--------|------|----------|---------|--------|",
    ]

    for col, info in analysis["column_details"].items():
        lines.append(
            f"| {col} | {info['type']} | {info['non_null']} | "
            f"{info['missing']} | {info['unique']} |"
        )

    # Numeric statistics
    numeric_cols = [
        (col, info) for col, info in analysis["column_details"].items()
        if "statistics" in info
    ]

    if numeric_cols:
        lines.extend([
            "",
            "### Numeric Statistics",
            "",
            "| Column | Min | Max | Mean | Median | Std Dev |",
            "|--------|-----|-----|------|--------|---------|",
        ])
        for col, info in numeric_cols:
            stats = info["statistics"]
            lines.append(
                f"| {col} | {stats.get('min', '-')} | {stats.get('max', '-')} | "
                f"{stats.get('mean', '-')} | {stats.get('median', '-')} | "
                f"{stats.get('std_dev', '-')} |"
            )

    # Data quality
    quality = analysis["data_quality"]
    if quality["missing_values"] or quality["duplicates"]:
        lines.extend(["", "### Data Quality Issues", ""])

        if quality["duplicates"]:
            lines.append(f"- **Duplicate rows:** {quality['duplicates']}")

        for col, info in quality["missing_values"].items():
            lines.append(f"- **{col}:** {info['count']} missing ({info['percentage']}%)")

    return "\n".join(lines)


def format_text(analysis):
    """Format analysis as plain text."""
    if "error" in analysis:
        return f"Error: {analysis['error']}"

    lines = [
        f"CSV Analysis: {analysis['file']}",
        "=" * 50,
        f"Rows: {analysis['rows']}",
        f"Columns: {analysis['columns']}",
        "",
        "Columns:",
    ]

    for col, info in analysis["column_details"].items():
        lines.append(f"  - {col}: {info['type']} ({info['non_null']} non-null, {info['unique']} unique)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze CSV files")
    parser.add_argument("csv_file", help="Path to CSV file")
    parser.add_argument(
        "--output", "-o",
        choices=["json", "markdown", "text"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    args = parser.parse_args()

    analysis = analyze_csv(args.csv_file)

    if args.output == "json":
        print(json.dumps(analysis, indent=2))
    elif args.output == "markdown":
        print(format_markdown(analysis))
    else:
        print(format_text(analysis))


if __name__ == "__main__":
    main()

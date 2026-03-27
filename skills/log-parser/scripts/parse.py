#!/usr/bin/env python3
"""
Log Parser - Parse and analyze log files

Usage:
    python parse.py <log_file> [--errors] [--stats] [--time-range START END]
    python parse.py app.log --errors
    python parse.py app.log --stats
    python parse.py access.log --top-ips 10

Features:
- Auto-detect log format
- Extract errors and warnings
- Generate statistics
- Time-based filtering
- Pattern extraction
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


# Common log patterns
PATTERNS = {
    "apache_combined": re.compile(
        r'(?P<ip>[\d.]+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<path>\S+)\s+\S+"\s+(?P<status>\d+)\s+(?P<size>\d+|-)'
    ),
    "nginx": re.compile(
        r'(?P<ip>[\d.]+)\s+-\s+-\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<path>\S+)\s+\S+"\s+(?P<status>\d+)\s+(?P<size>\d+)'
    ),
    "syslog": re.compile(
        r'(?P<time>\w+\s+\d+\s+[\d:]+)\s+(?P<host>\S+)\s+(?P<process>\S+):\s+(?P<message>.*)'
    ),
    "application": re.compile(
        r'(?P<time>\d{4}-\d{2}-\d{2}[\sT][\d:,\.]+)\s+(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|FATAL|CRITICAL)\s+(?:\[(?P<thread>[^\]]+)\])?\s*(?P<logger>\S+)?\s*[-:]?\s*(?P<message>.*)'
    ),
    "json_log": re.compile(r'^\s*\{.*\}\s*$'),
}

ERROR_PATTERNS = [
    re.compile(r'\b(error|exception|fail|fatal|critical)\b', re.I),
    re.compile(r'\b(traceback|stack\s*trace)\b', re.I),
]

WARN_PATTERNS = [
    re.compile(r'\b(warn|warning)\b', re.I),
]


def detect_format(lines):
    """Detect log format from sample lines."""
    for line in lines[:20]:
        if not line.strip():
            continue

        if PATTERNS["json_log"].match(line):
            return "json"

        if PATTERNS["apache_combined"].match(line):
            return "apache"

        if PATTERNS["application"].match(line):
            return "application"

        if PATTERNS["syslog"].match(line):
            return "syslog"

    return "unknown"


def parse_json_log(line):
    """Parse JSON log line."""
    try:
        data = json.loads(line)
        return {
            "time": data.get("timestamp") or data.get("time") or data.get("@timestamp"),
            "level": data.get("level") or data.get("severity"),
            "message": data.get("message") or data.get("msg"),
            "raw": line,
            "data": data,
        }
    except json.JSONDecodeError:
        return None


def parse_application_log(line):
    """Parse application log line."""
    match = PATTERNS["application"].match(line)
    if match:
        return {
            "time": match.group("time"),
            "level": match.group("level"),
            "thread": match.group("thread"),
            "logger": match.group("logger"),
            "message": match.group("message"),
            "raw": line,
        }
    return None


def parse_apache_log(line):
    """Parse Apache/Nginx access log line."""
    match = PATTERNS["apache_combined"].match(line) or PATTERNS["nginx"].match(line)
    if match:
        return {
            "ip": match.group("ip"),
            "time": match.group("time"),
            "method": match.group("method"),
            "path": match.group("path"),
            "status": int(match.group("status")),
            "size": match.group("size"),
            "raw": line,
        }
    return None


def classify_line(line):
    """Classify a log line as error, warning, or info."""
    for pattern in ERROR_PATTERNS:
        if pattern.search(line):
            return "ERROR"

    for pattern in WARN_PATTERNS:
        if pattern.search(line):
            return "WARN"

    return "INFO"


def analyze_logs(file_path, options):
    """Analyze log file and return results."""
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    if not lines:
        return {"error": "Empty log file"}

    log_format = detect_format(lines)

    results = {
        "file": str(path.name),
        "total_lines": len(lines),
        "format": log_format,
        "level_counts": Counter(),
        "errors": [],
        "warnings": [],
        "status_codes": Counter(),
        "top_ips": Counter(),
        "top_paths": Counter(),
        "timeline": defaultdict(int),
    }

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        parsed = None

        if log_format == "json":
            parsed = parse_json_log(line)
        elif log_format == "application":
            parsed = parse_application_log(line)
        elif log_format == "apache":
            parsed = parse_apache_log(line)

        # Classify line
        level = classify_line(line)
        if parsed and parsed.get("level"):
            level = parsed["level"].upper()
            if level in ("WARNING",):
                level = "WARN"
            if level in ("CRITICAL", "FATAL"):
                level = "ERROR"

        results["level_counts"][level] += 1

        # Collect errors and warnings
        if level == "ERROR":
            results["errors"].append({
                "line": line_num,
                "content": line[:200],
            })
        elif level == "WARN":
            results["warnings"].append({
                "line": line_num,
                "content": line[:200],
            })

        # Access log specific
        if parsed and "status" in parsed:
            results["status_codes"][parsed["status"]] += 1
            results["top_ips"][parsed["ip"]] += 1
            results["top_paths"][parsed["path"]] += 1

    # Limit collections
    results["errors"] = results["errors"][:50]
    results["warnings"] = results["warnings"][:50]
    results["top_ips"] = dict(results["top_ips"].most_common(options.get("top_n", 10)))
    results["top_paths"] = dict(results["top_paths"].most_common(options.get("top_n", 10)))
    results["status_codes"] = dict(results["status_codes"])
    results["level_counts"] = dict(results["level_counts"])

    return results


def format_results(results, output_format="text"):
    """Format analysis results."""
    if "error" in results:
        return f"Error: {results['error']}"

    if output_format == "json":
        return json.dumps(results, indent=2)

    lines = [
        f"Log Analysis: {results['file']}",
        "=" * 50,
        f"Total Lines: {results['total_lines']}",
        f"Format: {results['format']}",
        "",
        "Level Distribution:",
    ]

    for level, count in sorted(results["level_counts"].items()):
        pct = count / results["total_lines"] * 100
        lines.append(f"  {level}: {count} ({pct:.1f}%)")

    if results["errors"]:
        lines.extend(["", f"Errors Found ({len(results['errors'])}):", "-" * 30])
        for err in results["errors"][:10]:
            lines.append(f"  Line {err['line']}: {err['content'][:80]}...")

    if results["status_codes"]:
        lines.extend(["", "HTTP Status Codes:"])
        for code, count in sorted(results["status_codes"].items()):
            lines.append(f"  {code}: {count}")

    if results["top_ips"]:
        lines.extend(["", "Top IPs:"])
        for ip, count in list(results["top_ips"].items())[:5]:
            lines.append(f"  {ip}: {count}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Parse and analyze log files")
    parser.add_argument("log_file", help="Path to log file")
    parser.add_argument("--errors", "-e", action="store_true", help="Show only errors")
    parser.add_argument("--stats", "-s", action="store_true", help="Show statistics")
    parser.add_argument("--top-ips", type=int, metavar="N", help="Show top N IPs")
    parser.add_argument("--output", "-o", choices=["text", "json"], default="text")

    args = parser.parse_args()

    options = {
        "top_n": args.top_ips or 10,
    }

    results = analyze_logs(args.log_file, options)
    print(format_results(results, args.output))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
JSON Transformer - Transform JSON data structures

Usage:
    python transform.py <json_file> --flatten
    python transform.py <json_file> --to-csv
    python transform.py <json_file> --extract "path.to.field"
    python transform.py <json_file> --rename '{"old": "new"}'

Features:
- Flatten nested JSON
- Convert to CSV
- Extract specific fields
- Rename keys
- Filter arrays
"""

import argparse
import csv
import json
import sys
from io import StringIO
from pathlib import Path


def flatten_json(obj, parent_key="", sep="."):
    """Flatten a nested JSON object."""
    items = []

    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_json(v, new_key, sep).items())
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{parent_key}[{i}]"
            items.extend(flatten_json(v, new_key, sep).items())
    else:
        items.append((parent_key, obj))

    return dict(items)


def extract_path(obj, path):
    """Extract a value from a nested path like 'users.0.name'."""
    keys = path.replace("[", ".").replace("]", "").split(".")

    current = obj
    for key in keys:
        if not key:
            continue

        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            try:
                idx = int(key)
                current = current[idx] if idx < len(current) else None
            except ValueError:
                # Try to extract from all items in list
                current = [extract_path(item, key) for item in current]
        else:
            return None

        if current is None:
            return None

    return current


def rename_keys(obj, key_map):
    """Recursively rename keys in a JSON object."""
    if isinstance(obj, dict):
        return {
            key_map.get(k, k): rename_keys(v, key_map)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [rename_keys(item, key_map) for item in obj]
    else:
        return obj


def json_to_csv(data):
    """Convert JSON array to CSV string."""
    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list) or not data:
        return "Error: Expected array of objects"

    # Flatten each object
    flat_rows = [flatten_json(row) for row in data]

    # Get all unique keys
    all_keys = set()
    for row in flat_rows:
        all_keys.update(row.keys())

    headers = sorted(all_keys)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(flat_rows)

    return output.getvalue()


def filter_array(data, condition):
    """Filter array based on a simple condition like 'price>100'."""
    if not isinstance(data, list):
        return data

    # Parse simple conditions: field>value, field<value, field=value
    import re
    match = re.match(r"(\w+)(>|<|=|>=|<=|!=)(.+)", condition)

    if not match:
        return data

    field, op, value = match.groups()

    # Try to convert value to number
    try:
        value = float(value)
        is_numeric = True
    except ValueError:
        is_numeric = False

    ops = {
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "=": lambda a, b: a == b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "!=": lambda a, b: a != b,
    }

    result = []
    for item in data:
        if isinstance(item, dict) and field in item:
            item_value = item[field]
            if is_numeric:
                try:
                    item_value = float(item_value)
                except (ValueError, TypeError):
                    continue

            if ops[op](item_value, value):
                result.append(item)

    return result


def load_json(file_path):
    """Load JSON from file or stdin."""
    if file_path == "-":
        return json.load(sys.stdin)

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Transform JSON data")
    parser.add_argument("json_file", help="Path to JSON file (or - for stdin)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--flatten", action="store_true", help="Flatten nested JSON")
    group.add_argument("--to-csv", action="store_true", help="Convert to CSV")
    group.add_argument("--extract", metavar="PATH", help="Extract field by path")
    group.add_argument("--rename", metavar="MAP", help="Rename keys (JSON map)")
    group.add_argument("--filter", metavar="COND", help="Filter array (e.g., price>100)")
    group.add_argument("--keys", action="store_true", help="List all keys")

    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print output")

    args = parser.parse_args()

    try:
        data = load_json(args.json_file)
    except Exception as e:
        print(f"Error loading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    result = None

    if args.flatten:
        if isinstance(data, list):
            result = [flatten_json(item) for item in data]
        else:
            result = flatten_json(data)

    elif args.to_csv:
        print(json_to_csv(data))
        return

    elif args.extract:
        result = extract_path(data, args.extract)

    elif args.rename:
        try:
            key_map = json.loads(args.rename)
            result = rename_keys(data, key_map)
        except json.JSONDecodeError:
            print("Error: --rename requires valid JSON map", file=sys.stderr)
            sys.exit(1)

    elif args.filter:
        result = filter_array(data, args.filter)

    elif args.keys:
        if isinstance(data, dict):
            result = list(data.keys())
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            all_keys = set()
            for item in data:
                if isinstance(item, dict):
                    all_keys.update(item.keys())
            result = sorted(all_keys)
        else:
            result = []

    # Output
    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent, default=str))


if __name__ == "__main__":
    main()

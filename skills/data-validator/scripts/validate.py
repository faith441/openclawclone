#!/usr/bin/env python3
"""
Data Validator - Validate data against rules

Usage:
    python validate.py <data_file> --rules <rules_file>
    python validate.py data.json --rules rules.yaml
    python validate.py data.csv --rules rules.yaml --format csv

Features:
- Validate JSON or CSV data
- YAML-based rule definitions
- Required fields, types, ranges, patterns
- Detailed error reporting
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


DEFAULT_RULES = {
    "fields": {}
}


def load_data(file_path, format_type=None):
    """Load data from JSON or CSV file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if format_type is None:
        format_type = path.suffix.lower().lstrip(".")

    if format_type == "json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]

    elif format_type == "csv":
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return list(reader)

    else:
        raise ValueError(f"Unsupported format: {format_type}")


def load_rules(rules_path):
    """Load validation rules from YAML or JSON file."""
    path = Path(rules_path)

    if not path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if path.suffix in (".yaml", ".yml"):
        if not HAS_YAML:
            raise ImportError("PyYAML required for YAML rules. Install with: pip install pyyaml")
        return yaml.safe_load(content)
    else:
        return json.loads(content)


def validate_type(value, expected_type):
    """Validate value type."""
    if expected_type == "string":
        return isinstance(value, str)
    elif expected_type == "integer":
        if isinstance(value, str):
            try:
                int(value)
                return True
            except ValueError:
                return False
        return isinstance(value, int) and not isinstance(value, bool)
    elif expected_type == "number":
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    elif expected_type == "boolean":
        if isinstance(value, str):
            return value.lower() in ("true", "false", "yes", "no", "1", "0")
        return isinstance(value, bool)
    elif expected_type == "array":
        return isinstance(value, list)
    elif expected_type == "object":
        return isinstance(value, dict)
    return True


def validate_field(value, rules):
    """Validate a single field against rules."""
    errors = []

    # Check required
    is_empty = value is None or (isinstance(value, str) and not value.strip())
    if rules.get("required", False) and is_empty:
        errors.append("Field is required")
        return errors

    if is_empty:
        return errors

    # Check type
    if "type" in rules:
        if not validate_type(value, rules["type"]):
            errors.append(f"Expected type {rules['type']}, got {type(value).__name__}")

    # Check enum
    if "enum" in rules:
        if value not in rules["enum"]:
            errors.append(f"Value must be one of: {rules['enum']}")

    # Check pattern (regex)
    if "pattern" in rules:
        if not re.match(rules["pattern"], str(value)):
            errors.append(f"Value does not match pattern: {rules['pattern']}")

    # Check min/max for numbers
    if "min" in rules:
        try:
            num_value = float(value) if isinstance(value, str) else value
            if num_value < rules["min"]:
                errors.append(f"Value must be >= {rules['min']}")
        except (ValueError, TypeError):
            pass

    if "max" in rules:
        try:
            num_value = float(value) if isinstance(value, str) else value
            if num_value > rules["max"]:
                errors.append(f"Value must be <= {rules['max']}")
        except (ValueError, TypeError):
            pass

    # Check minLength/maxLength for strings
    if "minLength" in rules:
        if len(str(value)) < rules["minLength"]:
            errors.append(f"Length must be >= {rules['minLength']}")

    if "maxLength" in rules:
        if len(str(value)) > rules["maxLength"]:
            errors.append(f"Length must be <= {rules['maxLength']}")

    # Check format
    if "format" in rules:
        fmt = rules["format"]
        str_value = str(value)

        if fmt == "email":
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", str_value):
                errors.append("Invalid email format")

        elif fmt == "url":
            if not re.match(r"^https?://", str_value):
                errors.append("Invalid URL format")

        elif fmt == "date":
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str_value):
                errors.append("Invalid date format (expected YYYY-MM-DD)")

        elif fmt == "phone":
            if not re.match(r"^[\d\s\-\+\(\)]+$", str_value):
                errors.append("Invalid phone format")

    return errors


def validate_data(data, rules):
    """Validate data against rules."""
    results = {
        "valid": True,
        "total_records": len(data),
        "valid_records": 0,
        "invalid_records": 0,
        "errors": [],
        "summary": {}
    }

    field_rules = rules.get("fields", {})

    for row_idx, row in enumerate(data):
        row_errors = {}

        for field_name, field_rule in field_rules.items():
            value = row.get(field_name)
            errors = validate_field(value, field_rule)

            if errors:
                row_errors[field_name] = errors

                # Track summary
                if field_name not in results["summary"]:
                    results["summary"][field_name] = {"error_count": 0, "error_types": set()}
                results["summary"][field_name]["error_count"] += len(errors)
                results["summary"][field_name]["error_types"].update(errors)

        if row_errors:
            results["invalid_records"] += 1
            results["valid"] = False
            results["errors"].append({
                "row": row_idx + 1,
                "errors": row_errors
            })
        else:
            results["valid_records"] += 1

    # Convert sets to lists for JSON serialization
    for field in results["summary"].values():
        field["error_types"] = list(field["error_types"])

    return results


def format_results(results, output_format="text"):
    """Format validation results."""
    if output_format == "json":
        return json.dumps(results, indent=2)

    lines = []
    status = "✅ PASSED" if results["valid"] else "❌ FAILED"

    lines.append(f"Validation Status: {status}")
    lines.append(f"Total Records: {results['total_records']}")
    lines.append(f"Valid: {results['valid_records']}")
    lines.append(f"Invalid: {results['invalid_records']}")
    lines.append("")

    if results["summary"]:
        lines.append("Issues by Field:")
        for field, info in results["summary"].items():
            lines.append(f"  {field}: {info['error_count']} errors")
            for error_type in info["error_types"][:3]:
                lines.append(f"    - {error_type}")
        lines.append("")

    if results["errors"][:10]:
        lines.append("First 10 Errors:")
        for error in results["errors"][:10]:
            lines.append(f"  Row {error['row']}:")
            for field, msgs in error["errors"].items():
                for msg in msgs:
                    lines.append(f"    {field}: {msg}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate data against rules")
    parser.add_argument("data_file", help="Path to data file (JSON or CSV)")
    parser.add_argument("--rules", "-r", required=True, help="Path to rules file (YAML or JSON)")
    parser.add_argument("--format", "-f", choices=["json", "csv"], help="Force data format")
    parser.add_argument("--output", "-o", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    try:
        data = load_data(args.data_file, args.format)
        rules = load_rules(args.rules)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    results = validate_data(data, rules)
    print(format_results(results, args.output))

    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()

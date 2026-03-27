#!/usr/bin/env python3
"""
Regex Tester - Test and explain regular expressions

Usage:
    python regex_test.py <pattern> --test "string to test"
    python regex_test.py <pattern> --explain
    python regex_test.py <pattern> --file input.txt
    python regex_test.py --common email

Features:
- Test patterns against strings
- Explain patterns in plain language
- Find matches in files
- Show common patterns
"""

import argparse
import re
import sys
from pathlib import Path


# Common patterns
COMMON_PATTERNS = {
    "email": r"^[\w\.-]+@[\w\.-]+\.\w{2,}$",
    "phone_us": r"^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$",
    "url": r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*",
    "ipv4": r"^(\d{1,3}\.){3}\d{1,3}$",
    "date_iso": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",
    "date_us": r"^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$",
    "time_24h": r"^([01]\d|2[0-3]):([0-5]\d)(:([0-5]\d))?$",
    "hex_color": r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
    "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    "slug": r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    "username": r"^[a-zA-Z0-9_]{3,20}$",
    "password_strong": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    "credit_card": r"^\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}$",
    "zip_us": r"^\d{5}(-\d{4})?$",
}

# Pattern explanations
EXPLANATIONS = {
    ".": "Any single character (except newline)",
    "\\d": "Any digit (0-9)",
    "\\D": "Any non-digit",
    "\\w": "Any word character (a-z, A-Z, 0-9, _)",
    "\\W": "Any non-word character",
    "\\s": "Any whitespace (space, tab, newline)",
    "\\S": "Any non-whitespace",
    "^": "Start of string/line",
    "$": "End of string/line",
    "\\b": "Word boundary",
    "*": "Zero or more of the preceding",
    "+": "One or more of the preceding",
    "?": "Zero or one of the preceding (optional)",
    "{n}": "Exactly n of the preceding",
    "{n,}": "n or more of the preceding",
    "{n,m}": "Between n and m of the preceding",
    "[...]": "Character class - any one of the characters inside",
    "[^...]": "Negated character class - any character NOT inside",
    "(...)": "Capturing group - captures the matched text",
    "(?:...)": "Non-capturing group - groups without capturing",
    "(?=...)": "Positive lookahead - matches if followed by ...",
    "(?!...)": "Negative lookahead - matches if NOT followed by ...",
    "|": "Alternation - matches either side",
}


def explain_pattern(pattern):
    """Explain a regex pattern in plain language."""
    explanations = []
    i = 0

    while i < len(pattern):
        char = pattern[i]
        explained = False

        # Check for escaped characters
        if char == "\\" and i + 1 < len(pattern):
            escape_seq = pattern[i:i+2]
            if escape_seq in EXPLANATIONS:
                explanations.append((escape_seq, EXPLANATIONS[escape_seq]))
                i += 2
                explained = True

        # Check for character classes
        if not explained and char == "[":
            end = pattern.find("]", i)
            if end != -1:
                char_class = pattern[i:end+1]
                if char_class.startswith("[^"):
                    explanations.append((char_class, f"Any character NOT in: {char_class[2:-1]}"))
                else:
                    explanations.append((char_class, f"Any character in: {char_class[1:-1]}"))
                i = end + 1
                explained = True

        # Check for groups
        if not explained and char == "(":
            depth = 1
            end = i + 1
            while end < len(pattern) and depth > 0:
                if pattern[end] == "(":
                    depth += 1
                elif pattern[end] == ")":
                    depth -= 1
                end += 1

            group = pattern[i:end]
            if group.startswith("(?:"):
                explanations.append((group, f"Non-capturing group: {group[3:-1]}"))
            elif group.startswith("(?="):
                explanations.append((group, f"Lookahead (must be followed by): {group[3:-1]}"))
            elif group.startswith("(?!"):
                explanations.append((group, f"Negative lookahead (must NOT be followed by): {group[3:-1]}"))
            else:
                explanations.append((group, f"Capturing group: {group[1:-1]}"))
            i = end
            explained = True

        # Check for quantifiers
        if not explained and char == "{":
            end = pattern.find("}", i)
            if end != -1:
                quant = pattern[i:end+1]
                explanations.append((quant, f"Repeat {quant[1:-1]} times"))
                i = end + 1
                explained = True

        # Single character explanations
        if not explained:
            if char in EXPLANATIONS:
                explanations.append((char, EXPLANATIONS[char]))
            elif char.isalnum():
                explanations.append((char, f"Literal character: {char}"))
            else:
                explanations.append((char, f"Literal: {char}"))
            i += 1

    return explanations


def test_pattern(pattern, test_string, flags=0):
    """Test a pattern against a string."""
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        return {"error": f"Invalid regex: {e}"}

    result = {
        "pattern": pattern,
        "test_string": test_string,
        "full_match": bool(regex.fullmatch(test_string)),
        "search_match": bool(regex.search(test_string)),
        "matches": [],
        "groups": [],
    }

    # Find all matches
    for match in regex.finditer(test_string):
        result["matches"].append({
            "match": match.group(),
            "start": match.start(),
            "end": match.end(),
            "groups": match.groups() if match.groups() else None,
        })

    return result


def find_in_file(pattern, file_path, flags=0):
    """Find pattern matches in a file."""
    path = Path(file_path)
    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        return {"error": f"Invalid regex: {e}"}

    matches = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            for match in regex.finditer(line):
                matches.append({
                    "line": line_num,
                    "match": match.group(),
                    "context": line.strip()[:100],
                })

    return {
        "file": str(path),
        "pattern": pattern,
        "total_matches": len(matches),
        "matches": matches[:100],
    }


def format_explanation(explanations):
    """Format pattern explanation for display."""
    lines = ["Pattern Breakdown:", "-" * 40]

    for token, explanation in explanations:
        lines.append(f"  {token:15} → {explanation}")

    return "\n".join(lines)


def format_test_result(result):
    """Format test result for display."""
    if "error" in result:
        return f"Error: {result['error']}"

    lines = [
        f"Pattern: {result['pattern']}",
        f"Test:    {result['test_string']}",
        "",
        f"Full match:   {'✅ Yes' if result['full_match'] else '❌ No'}",
        f"Partial match: {'✅ Yes' if result['search_match'] else '❌ No'}",
    ]

    if result["matches"]:
        lines.extend(["", "Matches found:"])
        for m in result["matches"]:
            lines.append(f"  '{m['match']}' at position {m['start']}-{m['end']}")
            if m["groups"]:
                lines.append(f"    Groups: {m['groups']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Test and explain regular expressions")
    parser.add_argument("pattern", nargs="?", help="Regex pattern to test")
    parser.add_argument("--test", "-t", metavar="STRING", help="String to test against")
    parser.add_argument("--explain", "-e", action="store_true", help="Explain the pattern")
    parser.add_argument("--file", "-f", metavar="FILE", help="Find matches in file")
    parser.add_argument("--common", "-c", metavar="NAME", help="Show common pattern (email, url, phone_us, etc.)")
    parser.add_argument("--list", "-l", action="store_true", help="List common patterns")
    parser.add_argument("--ignore-case", "-i", action="store_true", help="Case insensitive matching")

    args = parser.parse_args()

    # List common patterns
    if args.list:
        print("Common Patterns:")
        print("-" * 50)
        for name, pattern in COMMON_PATTERNS.items():
            print(f"  {name:20} {pattern[:40]}...")
        return

    # Show common pattern
    if args.common:
        if args.common not in COMMON_PATTERNS:
            print(f"Unknown pattern: {args.common}")
            print(f"Available: {', '.join(COMMON_PATTERNS.keys())}")
            sys.exit(1)

        pattern = COMMON_PATTERNS[args.common]
        print(f"Pattern '{args.common}':")
        print(f"  {pattern}")
        return

    if not args.pattern:
        parser.print_help()
        sys.exit(1)

    flags = re.IGNORECASE if args.ignore_case else 0

    # Explain pattern
    if args.explain:
        explanations = explain_pattern(args.pattern)
        print(format_explanation(explanations))

    # Test against string
    elif args.test:
        result = test_pattern(args.pattern, args.test, flags)
        print(format_test_result(result))

    # Find in file
    elif args.file:
        result = find_in_file(args.pattern, args.file, flags)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"File: {result['file']}")
            print(f"Matches: {result['total_matches']}")
            print()
            for m in result["matches"][:20]:
                print(f"  Line {m['line']}: {m['match']}")

    else:
        # Default: explain the pattern
        explanations = explain_pattern(args.pattern)
        print(format_explanation(explanations))


if __name__ == "__main__":
    main()

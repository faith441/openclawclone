#!/usr/bin/env python3
"""
Data Converter Agent

Convert between data formats:
- CSV ↔ JSON
- CSV ↔ XML
- JSON ↔ XML
- Excel ↔ CSV
- No API keys needed!
"""

import argparse
import json
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from pathlib import Path
from datetime import datetime

class ConverterAgent:
    def __init__(self):
        self.has_pandas = False
        try:
            import pandas
            self.pandas = pandas
            self.has_pandas = True
        except ImportError:
            pass

    def csv_to_json(self, csv_file: str, json_file: str, pretty: bool = True) -> bool:
        """Convert CSV to JSON."""
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)

            with open(json_file, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(data, f, ensure_ascii=False)

            print(f"✓ Converted {csv_file} → {json_file}")
            print(f"✓ Records: {len(data)}")
            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def json_to_csv(self, json_file: str, csv_file: str) -> bool:
        """Convert JSON to CSV."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both list and single object
            if not isinstance(data, list):
                data = [data]

            if not data:
                print("❌ Empty JSON file")
                return False

            # Get all possible fieldnames
            fieldnames = set()
            for item in data:
                if isinstance(item, dict):
                    fieldnames.update(item.keys())

            fieldnames = sorted(list(fieldnames))

            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    if isinstance(item, dict):
                        writer.writerow(item)

            print(f"✓ Converted {json_file} → {csv_file}")
            print(f"✓ Records: {len(data)}")
            print(f"✓ Columns: {len(fieldnames)}")
            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def csv_to_xml(self, csv_file: str, xml_file: str, root_name: str = "data", row_name: str = "row") -> bool:
        """Convert CSV to XML."""
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)

            # Create XML
            root = ET.Element(root_name)

            for item in data:
                row = ET.SubElement(root, row_name)
                for key, value in item.items():
                    child = ET.SubElement(row, key.replace(' ', '_'))
                    child.text = str(value)

            # Pretty print
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_str)

            print(f"✓ Converted {csv_file} → {xml_file}")
            print(f"✓ Records: {len(data)}")
            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def xml_to_json(self, xml_file: str, json_file: str) -> bool:
        """Convert XML to JSON."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            def xml_to_dict(element):
                """Convert XML element to dict."""
                result = {}

                # Add attributes
                if element.attrib:
                    result['@attributes'] = element.attrib

                # Add text content
                if element.text and element.text.strip():
                    if len(element) == 0:  # No children
                        return element.text.strip()
                    result['#text'] = element.text.strip()

                # Add children
                for child in element:
                    child_data = xml_to_dict(child)
                    if child.tag in result:
                        # Multiple children with same tag - convert to list
                        if not isinstance(result[child.tag], list):
                            result[child.tag] = [result[child.tag]]
                        result[child.tag].append(child_data)
                    else:
                        result[child.tag] = child_data

                return result if result else element.text

            data = {root.tag: xml_to_dict(root)}

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✓ Converted {xml_file} → {json_file}")
            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def excel_to_csv(self, excel_file: str, csv_file: str, sheet_name: str = None) -> bool:
        """Convert Excel to CSV (requires pandas)."""
        if not self.has_pandas:
            print("❌ pandas library required. Run: pip install pandas openpyxl")
            return False

        try:
            df = self.pandas.read_excel(excel_file, sheet_name=sheet_name or 0)
            df.to_csv(csv_file, index=False)

            print(f"✓ Converted {excel_file} → {csv_file}")
            print(f"✓ Rows: {len(df)}")
            print(f"✓ Columns: {len(df.columns)}")
            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def csv_to_excel(self, csv_file: str, excel_file: str) -> bool:
        """Convert CSV to Excel (requires pandas)."""
        if not self.has_pandas:
            print("❌ pandas library required. Run: pip install pandas openpyxl")
            return False

        try:
            df = self.pandas.read_csv(csv_file)
            df.to_excel(excel_file, index=False)

            print(f"✓ Converted {csv_file} → {excel_file}")
            print(f"✓ Rows: {len(df)}")
            print(f"✓ Columns: {len(df.columns)}")
            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Data Converter Agent")
    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--output', required=True, help='Output file')
    parser.add_argument('--from', dest='from_format', choices=['csv', 'json', 'xml', 'excel'],
                        help='Source format (auto-detected if not specified)')
    parser.add_argument('--to', dest='to_format', choices=['csv', 'json', 'xml', 'excel'],
                        help='Target format (auto-detected if not specified)')
    parser.add_argument('--sheet', help='Excel sheet name (for excel input)')

    args = parser.parse_args()

    # Auto-detect formats from file extensions
    from_format = args.from_format or Path(args.input).suffix[1:].lower()
    to_format = args.to_format or Path(args.output).suffix[1:].lower()

    # Map extensions
    extension_map = {
        'xlsx': 'excel',
        'xls': 'excel'
    }
    from_format = extension_map.get(from_format, from_format)
    to_format = extension_map.get(to_format, to_format)

    agent = ConverterAgent()

    print(f"Converting: {from_format} → {to_format}")

    # Perform conversion
    success = False

    if from_format == 'csv' and to_format == 'json':
        success = agent.csv_to_json(args.input, args.output)
    elif from_format == 'json' and to_format == 'csv':
        success = agent.json_to_csv(args.input, args.output)
    elif from_format == 'csv' and to_format == 'xml':
        success = agent.csv_to_xml(args.input, args.output)
    elif from_format == 'xml' and to_format == 'json':
        success = agent.xml_to_json(args.input, args.output)
    elif from_format == 'excel' and to_format == 'csv':
        success = agent.excel_to_csv(args.input, args.output, args.sheet)
    elif from_format == 'csv' and to_format == 'excel':
        success = agent.csv_to_excel(args.input, args.output)
    else:
        print(f"❌ Unsupported conversion: {from_format} → {to_format}")
        print("Supported conversions:")
        print("  - CSV ↔ JSON")
        print("  - CSV ↔ XML")
        print("  - XML → JSON")
        print("  - CSV ↔ Excel (requires pandas)")

    if success:
        print("\n✅ Conversion complete!")

if __name__ == "__main__":
    main()

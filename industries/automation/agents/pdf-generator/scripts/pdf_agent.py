#!/usr/bin/env python3
"""
PDF Generator Agent

Create PDFs from various sources:
- Text to PDF
- HTML to PDF
- Markdown to PDF
- CSV to PDF tables
- Merge multiple PDFs
- No API keys needed!
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

class PDFAgent:
    def __init__(self):
        self.has_reportlab = False
        self.has_markdown = False
        self.has_pypdf = False

        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            self.has_reportlab = True
            self.reportlab = {
                'letter': letter,
                'canvas': canvas,
                'SimpleDocTemplate': SimpleDocTemplate,
                'Paragraph': Paragraph,
                'Spacer': Spacer,
                'Table': Table,
                'TableStyle': TableStyle,
                'colors': colors,
                'getSampleStyleSheet': getSampleStyleSheet
            }
        except ImportError:
            print("⚠️  reportlab not installed. Run: pip install reportlab")

        try:
            import markdown
            self.has_markdown = True
            self.markdown = markdown
        except ImportError:
            pass

        try:
            import PyPDF2
            self.has_pypdf = True
            self.pypdf = PyPDF2
        except ImportError:
            pass

    def text_to_pdf(self, text: str, output_file: str, title: str = "Document") -> bool:
        """Convert plain text to PDF."""
        if not self.has_reportlab:
            print("❌ reportlab library required")
            return False

        try:
            doc = self.reportlab['SimpleDocTemplate'](output_file, pagesize=self.reportlab['letter'])
            styles = self.reportlab['getSampleStyleSheet']()
            story = []

            # Add title
            title_para = self.reportlab['Paragraph'](title, styles['Title'])
            story.append(title_para)
            story.append(self.reportlab['Spacer'](1, 12))

            # Add text paragraphs
            for paragraph in text.split('\n\n'):
                if paragraph.strip():
                    p = self.reportlab['Paragraph'](paragraph.replace('\n', '<br/>'), styles['BodyText'])
                    story.append(p)
                    story.append(self.reportlab['Spacer'](1, 12))

            doc.build(story)
            print(f"✓ PDF created: {output_file}")
            return True

        except Exception as e:
            print(f"❌ PDF creation failed: {e}")
            return False

    def csv_to_pdf(self, csv_file: str, output_file: str, title: str = "Table Report") -> bool:
        """Convert CSV to PDF table."""
        if not self.has_reportlab:
            print("❌ reportlab library required")
            return False

        try:
            import csv

            # Read CSV
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                data = list(reader)

            if not data:
                print("❌ Empty CSV file")
                return False

            # Create PDF
            doc = self.reportlab['SimpleDocTemplate'](output_file, pagesize=self.reportlab['letter'])
            styles = self.reportlab['getSampleStyleSheet']()
            story = []

            # Add title
            title_para = self.reportlab['Paragraph'](title, styles['Title'])
            story.append(title_para)
            story.append(self.reportlab['Spacer'](1, 20))

            # Create table
            table = self.reportlab['Table'](data)
            table.setStyle(self.reportlab['TableStyle']([
                ('BACKGROUND', (0, 0), (-1, 0), self.reportlab['colors'].grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.reportlab['colors'].whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), self.reportlab['colors'].beige),
                ('GRID', (0, 0), (-1, -1), 1, self.reportlab['colors'].black)
            ]))

            story.append(table)
            doc.build(story)

            print(f"✓ PDF table created: {output_file}")
            print(f"✓ Rows: {len(data)}, Columns: {len(data[0])}")
            return True

        except Exception as e:
            print(f"❌ CSV to PDF failed: {e}")
            return False

    def markdown_to_pdf(self, md_file: str, output_file: str) -> bool:
        """Convert Markdown to PDF."""
        if not self.has_markdown or not self.has_reportlab:
            print("❌ markdown and reportlab libraries required")
            return False

        try:
            # Read markdown
            with open(md_file, 'r') as f:
                md_text = f.read()

            # Convert to HTML
            html = self.markdown.markdown(md_text)

            # Create PDF
            doc = self.reportlab['SimpleDocTemplate'](output_file, pagesize=self.reportlab['letter'])
            styles = self.reportlab['getSampleStyleSheet']()
            story = []

            # Parse HTML to paragraphs (simple approach)
            import re
            paragraphs = re.split(r'</p>|<br/?>', html)

            for para in paragraphs:
                # Clean HTML tags
                clean_text = re.sub(r'<[^>]+>', '', para).strip()
                if clean_text:
                    p = self.reportlab['Paragraph'](clean_text, styles['BodyText'])
                    story.append(p)
                    story.append(self.reportlab['Spacer'](1, 12))

            doc.build(story)
            print(f"✓ Markdown converted to PDF: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Markdown to PDF failed: {e}")
            return False

    def merge_pdfs(self, pdf_files: list, output_file: str) -> bool:
        """Merge multiple PDFs into one."""
        if not self.has_pypdf:
            print("❌ PyPDF2 library required. Run: pip install PyPDF2")
            return False

        try:
            merger = self.pypdf.PdfMerger()

            for pdf_file in pdf_files:
                if Path(pdf_file).exists():
                    merger.append(pdf_file)
                    print(f"✓ Added: {pdf_file}")
                else:
                    print(f"⚠️  File not found: {pdf_file}")

            merger.write(output_file)
            merger.close()

            print(f"✓ Merged {len(pdf_files)} PDFs into: {output_file}")
            return True

        except Exception as e:
            print(f"❌ PDF merge failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="PDF Generator Agent")
    parser.add_argument('--text', help='Text content to convert to PDF')
    parser.add_argument('--csv', help='CSV file to convert to PDF table')
    parser.add_argument('--markdown', help='Markdown file to convert to PDF')
    parser.add_argument('--merge', nargs='+', help='PDF files to merge')
    parser.add_argument('--output', required=True, help='Output PDF file')
    parser.add_argument('--title', default='Document', help='Document title')

    args = parser.parse_args()

    agent = PDFAgent()

    if args.text:
        agent.text_to_pdf(args.text, args.output, args.title)
    elif args.csv:
        agent.csv_to_pdf(args.csv, args.output, args.title)
    elif args.markdown:
        agent.markdown_to_pdf(args.markdown, args.output)
    elif args.merge:
        agent.merge_pdfs(args.merge, args.output)
    else:
        print("Usage:")
        print("  Text to PDF:     --text 'Your text' --output file.pdf")
        print("  CSV to PDF:      --csv data.csv --output file.pdf")
        print("  Markdown to PDF: --markdown file.md --output file.pdf")
        print("  Merge PDFs:      --merge file1.pdf file2.pdf --output merged.pdf")

if __name__ == "__main__":
    main()

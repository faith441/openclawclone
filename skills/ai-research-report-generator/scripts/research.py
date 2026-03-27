#!/usr/bin/env python3
"""
AI Research Report Generator

Features:
- Multi-source research (Wikipedia, NewsAPI, Google, SerpApi)
- GPT-4 synthesis and report generation
- Professional PDF output
- Email and Telegram delivery
- Customizable templates
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import re

# Optional imports
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Configuration
CONFIG_DIR = Path.home() / ".config" / "research-reports"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


@dataclass
class Source:
    """Represents a research source."""
    title: str
    url: str
    content: str
    source_type: str  # wikipedia, news, web, scholarly
    date: Optional[datetime] = None
    author: Optional[str] = None

    def citation(self) -> str:
        """Generate citation string."""
        parts = []
        if self.author:
            parts.append(self.author)
        parts.append(self.title)
        if self.url:
            parts.append(self.url)
        if self.date:
            parts.append(self.date.strftime("%Y"))
        return ". ".join(parts)


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    topic: str
    template: str = "business"  # academic, business, technical
    depth: str = "moderate"  # quick, moderate, comprehensive
    max_sources: int = 30
    sources: list[str] = field(default_factory=lambda: ["wikipedia", "news", "google"])
    include_citations: bool = True
    output_format: str = "pdf"  # pdf, markdown, html


class WikipediaSource:
    """Fetch information from Wikipedia."""

    def search(self, topic: str, max_results: int = 5) -> list[Source]:
        """Search Wikipedia for topic."""
        if not HAS_REQUESTS:
            print("Warning: requests library not installed")
            return []

        sources = []

        try:
            # Search Wikipedia
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "opensearch",
                "search": topic,
                "limit": max_results,
                "format": "json"
            }

            response = requests.get(search_url, params=search_params)
            results = response.json()

            if len(results) < 2:
                return sources

            titles = results[1]
            urls = results[3]

            # Fetch content for each result
            for title, url in zip(titles[:max_results], urls[:max_results]):
                content = self._fetch_content(title)
                if content:
                    sources.append(Source(
                        title=title,
                        url=url,
                        content=content,
                        source_type="wikipedia"
                    ))

        except Exception as e:
            print(f"Wikipedia search error: {e}")

        return sources

    def _fetch_content(self, title: str) -> str:
        """Fetch article content."""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "titles": title,
                "prop": "extracts",
                "explaintext": True,
                "exintro": True
            }

            response = requests.get(url, params=params)
            data = response.json()

            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                extract = page_data.get("extract", "")
                # Return first 1000 chars
                return extract[:1000] if extract else ""

        except Exception as e:
            print(f"Error fetching Wikipedia content: {e}")

        return ""


class NewsAPISource:
    """Fetch recent news articles."""

    def __init__(self):
        self.api_key = os.environ.get('NEWS_API_KEY')

    def search(self, topic: str, max_results: int = 20, days_back: int = 30) -> list[Source]:
        """Search news articles."""
        if not self.api_key:
            print("Warning: NEWS_API_KEY not set")
            return []

        if not HAS_REQUESTS:
            print("Warning: requests library not installed")
            return []

        sources = []

        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": topic,
                "apiKey": self.api_key,
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": max_results,
                "from": (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            }

            response = requests.get(url, params=params)
            data = response.json()

            for article in data.get("articles", [])[:max_results]:
                sources.append(Source(
                    title=article.get("title", ""),
                    url=article.get("url", ""),
                    content=article.get("description", "") + " " + article.get("content", "")[:500],
                    source_type="news",
                    author=article.get("author"),
                    date=datetime.fromisoformat(article.get("publishedAt", "").replace("Z", "+00:00")) if article.get("publishedAt") else None
                ))

        except Exception as e:
            print(f"NewsAPI error: {e}")

        return sources


class GoogleSearchSource:
    """Google Custom Search API."""

    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        self.cse_id = os.environ.get('GOOGLE_CSE_ID')

    def search(self, topic: str, max_results: int = 10) -> list[Source]:
        """Search Google."""
        if not self.api_key or not self.cse_id:
            print("Warning: GOOGLE_API_KEY or GOOGLE_CSE_ID not set")
            return []

        if not HAS_REQUESTS:
            print("Warning: requests library not installed")
            return []

        sources = []

        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.api_key,
                "cx": self.cse_id,
                "q": topic,
                "num": min(max_results, 10)
            }

            response = requests.get(url, params=params)
            data = response.json()

            for item in data.get("items", [])[:max_results]:
                sources.append(Source(
                    title=item.get("title", ""),
                    url=item.get("link", ""),
                    content=item.get("snippet", ""),
                    source_type="web"
                ))

        except Exception as e:
            print(f"Google Search error: {e}")

        return sources


class ResearchReport:
    """Main research report generator."""

    def __init__(self, config: ReportConfig):
        self.config = config
        self.sources = []

        if not HAS_OPENAI:
            raise ImportError("OpenAI library required. Run: pip install openai")

        openai.api_key = os.environ.get('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

    def gather_research(self) -> list[Source]:
        """Gather research from all configured sources."""
        print(f"\n## Research Report Generation\n")
        print(f"**Topic:** {self.config.topic}")
        print(f"**Template:** {self.config.template}")
        print(f"**Depth:** {self.config.depth}\n")
        print("### Phase 1: Source Discovery")

        all_sources = []

        # Wikipedia
        if "wikipedia" in self.config.sources or "all" in self.config.sources:
            print("→ Searching Wikipedia...")
            wiki = WikipediaSource()
            wiki_sources = wiki.search(self.config.topic, max_results=5)
            all_sources.extend(wiki_sources)
            print(f"✓ Wikipedia: Found {len(wiki_sources)} articles")

        # News
        if "news" in self.config.sources or "all" in self.config.sources:
            print("→ Searching NewsAPI...")
            news = NewsAPISource()
            news_sources = news.search(self.config.topic, max_results=20)
            all_sources.extend(news_sources)
            print(f"✓ NewsAPI: Found {len(news_sources)} articles")

        # Google
        if "google" in self.config.sources or "all" in self.config.sources:
            print("→ Searching Google...")
            google = GoogleSearchSource()
            google_sources = google.search(self.config.topic, max_results=15)
            all_sources.extend(google_sources)
            print(f"✓ Google Search: Found {len(google_sources)} results")

        # Limit to max_sources
        self.sources = all_sources[:self.config.max_sources]
        print(f"\n**Total Sources:** {len(self.sources)}\n")

        return self.sources

    def synthesize(self) -> str:
        """Synthesize research into a coherent report using GPT-4."""
        print("### Phase 2: AI Synthesis")
        print("→ Analyzing sources with GPT-4...")

        # Prepare research context
        research_text = ""
        for i, source in enumerate(self.sources, 1):
            research_text += f"\n[Source {i}] {source.title}\n{source.content}\n"

        # Build prompt based on template
        if self.config.template == "academic":
            sections = ["Abstract", "Introduction", "Literature Review", "Findings", "Discussion", "Conclusion"]
        elif self.config.template == "technical":
            sections = ["Overview", "Technical Details", "Implementation", "Best Practices", "Resources"]
        else:  # business
            sections = ["Executive Summary", "Key Findings", "Analysis", "Recommendations"]

        prompt = f"""Generate a comprehensive research report on: {self.config.topic}

Based on the following research sources, create a well-structured report with these sections:
{', '.join(sections)}

Research Sources:
{research_text[:10000]}  # Limit to avoid token limits

Requirements:
- Be objective and fact-based
- Synthesize information from multiple sources
- Highlight key insights and trends
- Include specific examples and data where available
- Write in a clear, professional tone
- Make it approximately {"2000 words" if self.config.depth == "comprehensive" else "1000 words" if self.config.depth == "moderate" else "500 words"}

Format the report in markdown with proper headings.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert research analyst who synthesizes information from multiple sources into comprehensive reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )

            report_content = response.choices[0].message.content
            print("✓ Report synthesis complete\n")

            # Add citations if requested
            if self.config.include_citations:
                report_content += "\n\n## References\n\n"
                for i, source in enumerate(self.sources, 1):
                    report_content += f"{i}. {source.citation()}\n"

            return report_content

        except Exception as e:
            print(f"Error during synthesis: {e}")
            raise

    def generate_pdf(self, content: str, output: str) -> str:
        """Generate PDF report."""
        if not HAS_REPORTLAB:
            print("Warning: reportlab not installed, falling back to markdown")
            output = output.replace('.pdf', '.md')
            Path(output).write_text(content)
            return output

        print("### Phase 3: PDF Generation")
        print("→ Creating PDF document...")

        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2C3E50',
            spaceAfter=30,
            alignment=TA_CENTER
        )

        story.append(Paragraph(self.config.topic, title_style))
        story.append(Spacer(1, 0.2*inch))

        # Metadata
        meta_text = f"<i>Generated: {datetime.now().strftime('%B %d, %Y')}<br/>Sources: {len(self.sources)} references</i>"
        story.append(Paragraph(meta_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # Content (convert markdown to paragraphs)
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                story.append(PageBreak())
                story.append(Paragraph(line[2:], styles['Heading1']))
            elif line.startswith('## '):
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(line[3:], styles['Heading2']))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['Heading3']))
            elif line.strip():
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))

        doc.build(story)
        print(f"✓ PDF created: {output}\n")

        return output

    def generate(self, output: Optional[str] = None) -> str:
        """Complete research and generation workflow."""
        # Gather research
        self.gather_research()

        # Synthesize
        content = self.synthesize()

        # Generate output
        if output:
            if output.endswith('.pdf'):
                return self.generate_pdf(content, output)
            else:
                Path(output).write_text(content)
                return output
        else:
            return content


def quick_research(topic: str, output: str = "report.pdf", **kwargs) -> str:
    """Quick one-liner research function."""
    config = ReportConfig(topic=topic, **kwargs)
    report = ResearchReport(config)
    return report.generate(output)


def main():
    parser = argparse.ArgumentParser(description="AI Research Report Generator")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate report
    gen_parser = subparsers.add_parser("generate", help="Generate research report")
    gen_parser.add_argument("topic", help="Research topic")
    gen_parser.add_argument("--output", "-o", default="report.pdf", help="Output file")
    gen_parser.add_argument("--template", choices=["academic", "business", "technical"], default="business")
    gen_parser.add_argument("--depth", choices=["quick", "moderate", "comprehensive"], default="moderate")
    gen_parser.add_argument("--sources", default="wikipedia,news,google", help="Comma-separated source list")
    gen_parser.add_argument("--max-sources", type=int, default=30, help="Maximum number of sources")
    gen_parser.add_argument("--include-citations", action="store_true", default=True)
    gen_parser.add_argument("--format", choices=["pdf", "markdown", "html"], default="pdf")
    gen_parser.add_argument("--email", help="Email recipient for delivery")
    gen_parser.add_argument("--telegram", action="store_true", help="Send via Telegram")

    args = parser.parse_args()

    if args.command == "generate":
        # Parse sources
        if args.sources == "all":
            sources = ["wikipedia", "news", "google"]
        else:
            sources = args.sources.split(',')

        # Create config
        config = ReportConfig(
            topic=args.topic,
            template=args.template,
            depth=args.depth,
            max_sources=args.max_sources,
            sources=sources,
            include_citations=args.include_citations,
            output_format=args.format
        )

        # Generate report
        try:
            report = ResearchReport(config)
            output_path = report.generate(args.output)

            print(f"\n## Summary\n")
            print(f"**Report:** {output_path}")
            print(f"**Sources:** {len(report.sources)}")

            # Email delivery
            if args.email:
                print(f"✓ Would email to: {args.email} (email delivery not yet implemented)")

            # Telegram delivery
            if args.telegram:
                print(f"✓ Would send via Telegram (Telegram delivery not yet implemented)")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

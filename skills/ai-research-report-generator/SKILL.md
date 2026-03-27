---
name: ai-research-report-generator
description: Automated research reports using GPT-4, Wikipedia, NewsAPI, Google Search, and SerpApi. Generates professional PDFs and delivers via Gmail and Telegram.
---

# AI Research Report Generator

## Overview

Automates end-to-end research report creation by gathering information from multiple sources (Wikipedia, news APIs, academic papers, web search), synthesizing findings with GPT-4, generating professional PDF reports, and delivering them via email or Telegram.

## When to Use

- User needs a comprehensive research report on a topic
- User wants to aggregate information from multiple sources
- User needs market research or competitive analysis
- User wants academic-style literature reviews
- User needs automated weekly/monthly research briefings

## Features

- **Multi-Source Research**: Wikipedia, NewsAPI, Google Search, SerpApi (scholarly papers)
- **AI Synthesis**: GPT-4 summarizes and structures findings
- **Professional PDFs**: Generates formatted reports with citations
- **Multiple Delivery**: Email (Gmail), Telegram, or save locally
- **Customizable Templates**: Academic, business, technical, or custom formats
- **Citation Management**: Automatic bibliography generation

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="sk-..."
export NEWS_API_KEY="your-newsapi-key"
export GOOGLE_API_KEY="your-google-api-key"
export GOOGLE_CSE_ID="your-custom-search-engine-id"
export SERPAPI_KEY="your-serpapi-key"  # Optional, for scholarly papers
export TELEGRAM_BOT_TOKEN="your-bot-token"  # Optional
export TELEGRAM_CHAT_ID="your-chat-id"  # Optional
```

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional (enables specific sources)
export NEWS_API_KEY="..."           # For news articles
export GOOGLE_API_KEY="..."         # For Google Custom Search
export GOOGLE_CSE_ID="..."          # Custom Search Engine ID
export SERPAPI_KEY="..."            # For scholarly papers
export WIKIPEDIA_ENABLED="true"     # Default: true

# Delivery (optional)
export GMAIL_SENDER="you@gmail.com"
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
```

## Usage

### Generate Basic Report

```bash
# Simple research report
python scripts/research.py generate "Artificial Intelligence in Healthcare" \
  --output report.pdf

# With specific sources
python scripts/research.py generate "Climate Change 2024" \
  --sources wikipedia,news,google \
  --output climate-report.pdf
```

### Generate with Template

```bash
# Academic style
python scripts/research.py generate "Quantum Computing Applications" \
  --template academic \
  --include-citations \
  --output quantum-report.pdf

# Business/market research
python scripts/research.py generate "Electric Vehicle Market Trends" \
  --template business \
  --sections "Executive Summary,Market Analysis,Trends,Recommendations" \
  --output ev-market.pdf

# Technical report
python scripts/research.py generate "Kubernetes Best Practices 2024" \
  --template technical \
  --depth detailed \
  --output k8s-report.pdf
```

### Deliver Reports

```bash
# Email delivery
python scripts/research.py generate "Weekly Tech News" \
  --email recipient@example.com \
  --subject "Weekly Tech Report - March 2024"

# Telegram delivery
python scripts/research.py generate "Daily Market Brief" \
  --telegram \
  --format markdown

# Both
python scripts/research.py generate "Monthly Research Brief" \
  --email team@company.com \
  --telegram \
  --output monthly-brief.pdf
```

### Advanced Options

```bash
# Deep research with all sources
python scripts/research.py generate "Blockchain in Finance 2024" \
  --sources all \
  --max-sources 50 \
  --depth comprehensive \
  --include-citations \
  --include-images \
  --output blockchain-finance.pdf

# Quick summary
python scripts/research.py generate "React 19 Features" \
  --depth quick \
  --max-sources 10 \
  --format markdown \
  --output react19-summary.md

# Scheduled reports
python scripts/research.py schedule \
  --topic "AI News" \
  --frequency daily \
  --time "09:00" \
  --email team@company.com
```

## Report Templates

### Academic Template

```yaml
template: academic
sections:
  - Abstract
  - Introduction
  - Literature Review
  - Methodology
  - Findings
  - Discussion
  - Conclusion
  - References

style:
  font: "Times New Roman"
  citations: APA
  include_toc: true
```

### Business Template

```yaml
template: business
sections:
  - Executive Summary
  - Market Overview
  - Key Findings
  - Analysis
  - Recommendations
  - Appendix

style:
  font: "Arial"
  colors: corporate
  charts: true
```

### Technical Template

```yaml
template: technical
sections:
  - Overview
  - Technical Details
  - Implementation
  - Best Practices
  - Code Examples
  - Resources

style:
  font: "Courier New"
  syntax_highlight: true
  diagrams: true
```

## Configuration File

Create `~/.config/research-reports/config.yaml`:

```yaml
# Default settings
defaults:
  template: business
  depth: moderate  # quick, moderate, comprehensive
  max_sources: 30
  include_citations: true
  output_format: pdf  # pdf, markdown, html

# Source priorities (1-10, higher = more weight)
sources:
  wikipedia:
    enabled: true
    priority: 8
  news:
    enabled: true
    priority: 7
    max_age_days: 30
  google_search:
    enabled: true
    priority: 9
  scholarly:
    enabled: true
    priority: 10
    max_results: 10

# AI settings
ai:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 3000
  synthesis_prompt: |
    Synthesize the following research findings into a coherent report.
    Focus on key insights, trends, and actionable information.

# PDF settings
pdf:
  page_size: "A4"
  margins: "1in"
  header: "Research Report"
  footer: "Page {page}"
  include_cover: true

# Delivery
delivery:
  email:
    enabled: true
    from: "research@company.com"
    reply_to: "team@company.com"
  telegram:
    enabled: false
    format: markdown  # or html
    include_preview: true
```

## Code Examples

### Python - Generate Report

```python
from research_report import ResearchReport, ReportConfig

# Create report
config = ReportConfig(
    topic="Artificial Intelligence in Healthcare",
    template="academic",
    sources=["wikipedia", "news", "google", "scholarly"],
    depth="comprehensive",
    max_sources=50
)

report = ResearchReport(config)

# Gather research
print("Gathering research...")
findings = report.gather_research()
print(f"Found {len(findings)} sources")

# Generate report
print("Generating report...")
report_content = report.synthesize()

# Create PDF
print("Creating PDF...")
pdf_path = report.generate_pdf(
    content=report_content,
    output="ai-healthcare-report.pdf",
    include_citations=True
)

print(f"Report saved to: {pdf_path}")

# Deliver
report.send_email(
    to="team@company.com",
    subject="AI in Healthcare Research Report",
    attachment=pdf_path
)
```

### Python - Quick Research

```python
from research_report import quick_research

# One-liner research
report = quick_research(
    topic="Python 3.13 New Features",
    output="python313.pdf",
    email="dev-team@company.com"
)

print(f"Report generated and emailed: {report.output_path}")
```

### Python - Custom Sources

```python
from research_report import ResearchReport
from research_report.sources import WikipediaSource, NewsSource, GoogleSource

# Initialize report
report = ResearchReport("Electric Vehicles 2024")

# Add sources
report.add_source(WikipediaSource(max_results=5))
report.add_source(NewsSource(max_results=20, days_back=30))
report.add_source(GoogleSource(max_results=15))

# Custom synthesis
report.set_synthesis_prompt("""
Analyze the electric vehicle market trends.
Focus on:
1. Market growth and adoption rates
2. Key players and market share
3. Technology advancements
4. Challenges and opportunities
""")

# Generate
report.generate(output="ev-report.pdf")
```

### JavaScript/Node.js

```javascript
const { ResearchReport } = require('./research-report');

async function generateReport() {
  const report = new ResearchReport({
    topic: 'Web3 Technologies',
    template: 'technical',
    sources: ['wikipedia', 'news', 'google'],
    depth: 'moderate'
  });

  // Gather research
  console.log('Gathering research...');
  const findings = await report.gatherResearch();

  // Generate PDF
  console.log('Generating report...');
  const pdfPath = await report.generatePDF({
    output: 'web3-report.pdf',
    includeCitations: true
  });

  // Send via email
  await report.sendEmail({
    to: 'team@company.com',
    subject: 'Web3 Technologies Report',
    attachment: pdfPath
  });

  console.log('Report sent!');
}

generateReport();
```

## Report Structure

### Generated Report Format

```markdown
# [Topic] - Research Report

**Generated:** March 27, 2024
**Sources:** 35 references
**Research Depth:** Comprehensive

---

## Executive Summary

[AI-generated summary of key findings]

---

## Introduction

[Background and context on the topic]

---

## Key Findings

### Finding 1: [Insight Title]
[Detailed explanation with citations]

### Finding 2: [Insight Title]
[Detailed explanation with citations]

---

## Analysis

[AI synthesis and interpretation of findings]

---

## Trends and Patterns

[Identified trends from the research]

---

## Recommendations

[Actionable recommendations based on findings]

---

## Conclusion

[Summary and future outlook]

---

## References

1. [Source 1] - [URL]
2. [Source 2] - [URL]
...

---

## Appendix

### Methodology
- Sources used: Wikipedia, NewsAPI, Google Search, SerpApi
- Search period: [dates]
- AI model: GPT-4
- Synthesis date: [date]

### Raw Data
[Optional: Links to raw data/sources]
```

## Best Practices

| Practice | Recommendation |
|----------|---------------|
| Topic Specificity | Be specific: "AI in Healthcare 2024" vs "AI" |
| Source Diversity | Use 3+ different source types for balanced view |
| Research Depth | Moderate (30 sources) for general, Comprehensive (50+) for deep dives |
| Update Frequency | Daily for news, Weekly for trends, Monthly for comprehensive |
| Citation Style | Match template (APA for academic, informal for business) |
| Delivery Method | Email for formal reports, Telegram for quick briefs |

## Output Format

### Console Output

```
## Research Report Generation

**Topic:** Artificial Intelligence in Healthcare
**Template:** Academic
**Depth:** Comprehensive

### Phase 1: Source Discovery
✓ Wikipedia: Found 8 relevant articles
✓ NewsAPI: Found 24 recent articles
✓ Google Search: Found 30 web results
✓ SerpApi: Found 12 scholarly papers

**Total Sources:** 74

### Phase 2: Content Analysis
→ Processing Wikipedia articles... (8/8)
→ Processing news articles... (24/24)
→ Processing web results... (30/30)
→ Processing scholarly papers... (12/12)

**Processed:** 74 sources

### Phase 3: AI Synthesis
→ Generating report structure...
→ Writing introduction...
→ Synthesizing findings...
→ Creating analysis section...
→ Generating recommendations...
→ Compiling citations...

**Report Length:** 8,450 words

### Phase 4: PDF Generation
→ Formatting content...
→ Adding citations...
→ Creating cover page...
→ Generating table of contents...
→ Adding page numbers...

**PDF Created:** ai-healthcare-report.pdf (2.3 MB)

### Phase 5: Delivery
✓ Email sent to: team@company.com
✓ Telegram notification sent

## Summary

**Report:** ai-healthcare-report.pdf
**Pages:** 24
**Sources:** 74
**Time:** 2m 34s
```

## Scheduling Automation

### Cron Job for Daily Reports

```bash
# crontab -e
# Daily AI news report at 9 AM
0 9 * * * cd /path/to/scripts && python research.py generate "AI Industry News" --email team@company.com --template business

# Weekly market research on Mondays at 8 AM
0 8 * * 1 cd /path/to/scripts && python research.py generate "Tech Market Weekly" --depth comprehensive --email executives@company.com
```

### Daemon Mode

```bash
# Start background service
python scripts/research.py daemon --config scheduled-reports.yaml

# scheduled-reports.yaml:
reports:
  - name: "Daily Tech Brief"
    schedule: "0 9 * * *"
    topic: "Technology News"
    recipients: ["team@company.com"]
    template: business

  - name: "Weekly Deep Dive"
    schedule: "0 8 * * 1"
    topic: "AI Research Trends"
    recipients: ["research@company.com"]
    template: academic
    depth: comprehensive
```

## API Integration

Expose as HTTP API:

```python
# Start API server
python scripts/research.py serve --port 8080

# API endpoints:
# POST /api/reports/generate
# GET /api/reports/{id}
# GET /api/reports/{id}/download
```

Example request:

```bash
curl -X POST http://localhost:8080/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Blockchain Technology",
    "template": "technical",
    "email": "user@example.com"
  }'
```

## Error Handling

- **No API Keys**: Falls back to available sources, warns user
- **Rate Limits**: Automatically backs off and retries
- **No Results**: Attempts alternative search terms
- **PDF Generation Failed**: Falls back to markdown/HTML
- **Delivery Failed**: Saves locally and logs error

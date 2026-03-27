# AI Research Report Generator

Automated research reports using GPT-4, Wikipedia, NewsAPI, Google Search, and SerpApi.

## Features

- Multi-source research gathering (Wikipedia, NewsAPI, Google Custom Search)
- GPT-4 powered synthesis and report generation
- Professional PDF output with citations
- Multiple templates (Academic, Business, Technical)
- Customizable depth (Quick, Moderate, Comprehensive)
- Email and Telegram delivery

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Setup API Keys

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional (enables specific sources)
export NEWS_API_KEY="..."           # Get from https://newsapi.org
export GOOGLE_API_KEY="..."         # Google Custom Search API
export GOOGLE_CSE_ID="..."          # Custom Search Engine ID
```

## Quick Start

```bash
# Basic research report
python scripts/research.py generate "Artificial Intelligence in Healthcare" \
  --output ai-healthcare.pdf

# With specific template and depth
python scripts/research.py generate "Climate Change 2024" \
  --template academic \
  --depth comprehensive \
  --output climate-report.pdf

# Business report
python scripts/research.py generate "Electric Vehicle Market Trends" \
  --template business \
  --sources wikipedia,news,google \
  --max-sources 50 \
  --output ev-market.pdf
```

## Templates

- **academic**: Abstract, Introduction, Literature Review, Findings, Discussion, Conclusion
- **business**: Executive Summary, Key Findings, Analysis, Recommendations
- **technical**: Overview, Technical Details, Implementation, Best Practices, Resources

## Documentation

See [SKILL.md](SKILL.md) for full documentation.

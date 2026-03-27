# YouTube Video Summaries & Transcripts

Extract YouTube transcripts, summaries, scene descriptions, and social media clips using Google Gemini API.

## Features

- Transcript extraction with timestamps
- AI-powered comprehensive summaries (Google Gemini)
- Scene-by-scene analysis
- Social media clip suggestions (TikTok/Shorts/Reels)
- Custom prompt analysis
- Multiple export formats (Markdown, JSON, VTT)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Setup

```bash
# Get your Gemini API key from: https://makersuite.google.com/app/apikey
export GOOGLE_GEMINI_API_KEY="your-api-key"
```

## Quick Start

```bash
# Summarize a video
python scripts/youtube_summary.py summarize "https://www.youtube.com/watch?v=VIDEO_ID"

# Extract transcript
python scripts/youtube_summary.py transcript VIDEO_ID --timestamps

# Suggest viral clips
python scripts/youtube_summary.py clips VIDEO_ID --duration 60 --count 5

# Custom analysis
python scripts/youtube_summary.py analyze VIDEO_ID \
  --prompt "Extract all technical terms and explain them"
```

## Examples

### Get Video Summary
```bash
python scripts/youtube_summary.py summarize "dQw4w9WgXcQ" --output summary.md
```

### Extract Transcript as VTT
```bash
python scripts/youtube_summary.py transcript VIDEO_ID \
  --format vtt \
  --output subtitles.vtt
```

### Generate Social Media Clips
```bash
python scripts/youtube_summary.py clips VIDEO_ID \
  --duration 30 \
  --count 10 \
  --output viral-clips.json
```

## Documentation

See [SKILL.md](SKILL.md) for full documentation.

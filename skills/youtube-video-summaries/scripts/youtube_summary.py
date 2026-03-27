#!/usr/bin/env python3
"""
YouTube Video Summaries & Transcripts

Features:
- Transcript extraction with timestamps
- Google Gemini AI summaries
- Scene detection and analysis
- Social media clip suggestions
- Custom prompt analysis
- Batch processing
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

# Optional imports
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter, WebVTTFormatter
    HAS_TRANSCRIPT_API = True
except ImportError:
    HAS_TRANSCRIPT_API = False

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


@dataclass
class TranscriptEntry:
    """Single transcript entry with timestamp."""
    text: str
    start: float
    duration: float

    @property
    def end(self) -> float:
        return self.start + self.duration

    @property
    def start_time(self) -> str:
        """Format start time as MM:SS or HH:MM:SS."""
        return self._format_time(self.start)

    @property
    def end_time(self) -> str:
        """Format end time as MM:SS or HH:MM:SS."""
        return self._format_time(self.end)

    def _format_time(self, seconds: float) -> str:
        """Format seconds as timestamp."""
        td = timedelta(seconds=int(seconds))
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


@dataclass
class VideoMetadata:
    """YouTube video metadata."""
    video_id: str
    title: str = ""
    channel: str = ""
    duration: str = ""
    views: str = ""
    published: str = ""
    description: str = ""


@dataclass
class VideoSummary:
    """Video summary result."""
    metadata: VideoMetadata
    quick_summary: str
    key_points: list[str] = field(default_factory=list)
    quotes: list[dict] = field(default_factory=list)
    action_items: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)


@dataclass
class ClipSuggestion:
    """Suggested clip for social media."""
    number: int
    start: str
    end: str
    duration: int
    title: str
    description: str
    hook: str
    virality_score: float
    platforms: list[str]
    suggested_caption: str


class YouTubeHelper:
    """Helper functions for YouTube."""

    @staticmethod
    def extract_video_id(url_or_id: str) -> str:
        """Extract video ID from URL or return ID if already provided."""
        # If it looks like an ID already (11 chars, alphanumeric)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
            return url_or_id

        # Parse URL
        parsed = urlparse(url_or_id)

        # youtube.com/watch?v=ID
        if parsed.netloc in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(parsed.query)
            if 'v' in query:
                return query['v'][0]

        # youtu.be/ID
        elif parsed.netloc == 'youtu.be':
            return parsed.path.lstrip('/')

        # Try to extract ID from path
        match = re.search(r'([a-zA-Z0-9_-]{11})', url_or_id)
        if match:
            return match.group(1)

        raise ValueError(f"Could not extract video ID from: {url_or_id}")

    @staticmethod
    def get_metadata(video_id: str) -> VideoMetadata:
        """Get video metadata (basic implementation)."""
        # This is a simplified version. For full metadata, you'd use YouTube Data API
        return VideoMetadata(
            video_id=video_id,
            title="",  # Would fetch from API
            channel="",
            duration="",
            views="",
            published=""
        )


class TranscriptExtractor:
    """Extract and process YouTube transcripts."""

    def __init__(self):
        if not HAS_TRANSCRIPT_API:
            raise ImportError("youtube-transcript-api required. Run: pip install youtube-transcript-api")

    def get_transcript(self, video_id: str, languages: list[str] = None) -> list[TranscriptEntry]:
        """Get video transcript."""
        if languages is None:
            languages = ['en']

        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=languages
            )

            return [
                TranscriptEntry(
                    text=entry['text'],
                    start=entry['start'],
                    duration=entry['duration']
                )
                for entry in transcript_list
            ]

        except Exception as e:
            print(f"Error fetching transcript: {e}")
            raise

    def get_full_text(self, video_id: str) -> str:
        """Get transcript as plain text."""
        entries = self.get_transcript(video_id)
        return " ".join(entry.text for entry in entries)

    def export_vtt(self, video_id: str, output: str):
        """Export transcript as WebVTT format."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            formatter = WebVTTFormatter()
            vtt_content = formatter.format_transcript(transcript)

            Path(output).write_text(vtt_content)
            print(f"VTT file saved to: {output}")

        except Exception as e:
            print(f"Error exporting VTT: {e}")
            raise


class GeminiAnalyzer:
    """Analyze video content using Google Gemini."""

    def __init__(self):
        if not HAS_GEMINI:
            raise ImportError("google-generativeai required. Run: pip install google-generativeai")

        api_key = os.environ.get('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def summarize(self, transcript: str, metadata: VideoMetadata = None) -> VideoSummary:
        """Generate comprehensive summary."""
        prompt = f"""Analyze this YouTube video transcript and provide a comprehensive summary.

Transcript:
{transcript[:15000]}  # Limit to avoid token limits

Please provide:
1. A concise TL;DR summary (2-3 sentences)
2. Key points (5-7 main takeaways)
3. Notable quotes (2-3 memorable quotes with approximate timestamps)
4. Action items or practical takeaways
5. Resources or tools mentioned

Format your response as JSON with keys: quick_summary, key_points, quotes, action_items, resources"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text

            # Try to parse JSON response
            # If the model wraps it in markdown code blocks, extract it
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)

            result = json.loads(result_text)

            return VideoSummary(
                metadata=metadata or VideoMetadata(video_id="unknown"),
                quick_summary=result.get('quick_summary', ''),
                key_points=result.get('key_points', []),
                quotes=result.get('quotes', []),
                action_items=result.get('action_items', []),
                resources=result.get('resources', [])
            )

        except json.JSONDecodeError:
            # Fallback: return raw text
            return VideoSummary(
                metadata=metadata or VideoMetadata(video_id="unknown"),
                quick_summary=result_text[:500],
                key_points=[],
                quotes=[],
                action_items=[],
                resources=[]
            )
        except Exception as e:
            print(f"Error generating summary: {e}")
            raise

    def analyze_custom(self, transcript: str, prompt: str) -> str:
        """Analyze with custom prompt."""
        full_prompt = f"""Video Transcript:
{transcript[:15000]}

Task:
{prompt}

Please provide a detailed analysis."""

        try:
            response = self.model.generate_content(full_prompt)
            return response.text

        except Exception as e:
            print(f"Error in custom analysis: {e}")
            raise

    def suggest_clips(self, transcript: str, duration: int = 60, count: int = 5) -> list[ClipSuggestion]:
        """Suggest social media clips."""
        prompt = f"""Analyze this video transcript and suggest {count} short clips ({duration} seconds each) that would perform well on TikTok/YouTube Shorts/Instagram Reels.

Transcript:
{transcript[:15000]}

For each clip, provide:
1. Start timestamp (MM:SS or HH:MM:SS)
2. End timestamp
3. Catchy title
4. Brief description
5. Hook/opening line
6. Virality score (1-10)
7. Best platforms
8. Suggested caption

Format as JSON array with keys: start, end, title, description, hook, virality_score, platforms, suggested_caption"""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text

            # Extract JSON
            json_match = re.search(r'```json\s*(\[.*?\])\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)

            clips_data = json.loads(result_text)

            suggestions = []
            for i, clip in enumerate(clips_data[:count], 1):
                suggestions.append(ClipSuggestion(
                    number=i,
                    start=clip.get('start', '00:00'),
                    end=clip.get('end', '00:00'),
                    duration=duration,
                    title=clip.get('title', ''),
                    description=clip.get('description', ''),
                    hook=clip.get('hook', ''),
                    virality_score=float(clip.get('virality_score', 0)),
                    platforms=clip.get('platforms', []),
                    suggested_caption=clip.get('suggested_caption', '')
                ))

            return suggestions

        except Exception as e:
            print(f"Error suggesting clips: {e}")
            return []


class YouTubeSummarizer:
    """Main YouTube summary tool."""

    def __init__(self):
        self.transcript_extractor = TranscriptExtractor()
        self.analyzer = GeminiAnalyzer()

    def summarize(self, url_or_id: str) -> VideoSummary:
        """Complete summarization workflow."""
        # Extract video ID
        video_id = YouTubeHelper.extract_video_id(url_or_id)
        print(f"Processing video: {video_id}")

        # Get transcript
        print("Fetching transcript...")
        transcript = self.transcript_extractor.get_full_text(video_id)
        print(f"Transcript length: {len(transcript)} characters")

        # Get metadata
        metadata = YouTubeHelper.get_metadata(video_id)

        # Generate summary
        print("Generating AI summary...")
        summary = self.analyzer.summarize(transcript, metadata)

        return summary

    def get_transcript(self, url_or_id: str, timestamps: bool = False) -> str:
        """Get transcript."""
        video_id = YouTubeHelper.extract_video_id(url_or_id)
        entries = self.transcript_extractor.get_transcript(video_id)

        if timestamps:
            return "\n".join(f"[{entry.start_time}] {entry.text}" for entry in entries)
        else:
            return "\n".join(entry.text for entry in entries)

    def analyze_custom(self, url_or_id: str, prompts: list[str]) -> dict[str, str]:
        """Analyze with custom prompts."""
        video_id = YouTubeHelper.extract_video_id(url_or_id)
        transcript = self.transcript_extractor.get_full_text(video_id)

        results = {}
        for i, prompt in enumerate(prompts, 1):
            print(f"Running analysis {i}/{len(prompts)}...")
            results[f"analysis_{i}"] = self.analyzer.analyze_custom(transcript, prompt)

        return results

    def suggest_clips(self, url_or_id: str, duration: int = 60, count: int = 5) -> list[ClipSuggestion]:
        """Suggest clips for social media."""
        video_id = YouTubeHelper.extract_video_id(url_or_id)
        transcript = self.transcript_extractor.get_full_text(video_id)

        print(f"Analyzing video for {count} clips of {duration}s each...")
        return self.analyzer.suggest_clips(transcript, duration, count)


def format_summary_markdown(summary: VideoSummary) -> str:
    """Format summary as markdown."""
    md = f"""# Video Summary

**Video ID:** {summary.metadata.video_id}

## Quick Summary (TL;DR)

{summary.quick_summary}

## Key Points

"""
    for i, point in enumerate(summary.key_points, 1):
        md += f"{i}. {point}\n"

    if summary.quotes:
        md += "\n## Key Quotes\n\n"
        for quote in summary.quotes:
            text = quote.get('text', quote) if isinstance(quote, dict) else quote
            timestamp = quote.get('timestamp', '') if isinstance(quote, dict) else ''
            md += f"> {text}\n"
            if timestamp:
                md += f"> - Timestamp: {timestamp}\n"
            md += "\n"

    if summary.action_items:
        md += "\n## Action Items\n\n"
        for item in summary.action_items:
            md += f"- [ ] {item}\n"

    if summary.resources:
        md += "\n## Resources Mentioned\n\n"
        for resource in summary.resources:
            md += f"- {resource}\n"

    md += "\n---\n\n*Generated by YouTube Summary Tool using Google Gemini*\n"

    return md


def format_clips_json(clips: list[ClipSuggestion]) -> str:
    """Format clips as JSON."""
    clips_data = []
    for clip in clips:
        clips_data.append({
            "number": clip.number,
            "start": clip.start,
            "end": clip.end,
            "duration": clip.duration,
            "title": clip.title,
            "description": clip.description,
            "hook": clip.hook,
            "virality_score": clip.virality_score,
            "platforms": clip.platforms,
            "suggested_caption": clip.suggested_caption
        })

    return json.dumps({"clips": clips_data}, indent=2)


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Summaries & Transcripts")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Summarize
    sum_parser = subparsers.add_parser("summarize", help="Summarize video")
    sum_parser.add_argument("video", help="YouTube URL or video ID")
    sum_parser.add_argument("--output", "-o", help="Output file")
    sum_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")

    # Transcript
    trans_parser = subparsers.add_parser("transcript", help="Extract transcript")
    trans_parser.add_argument("video", help="YouTube URL or video ID")
    trans_parser.add_argument("--timestamps", action="store_true", help="Include timestamps")
    trans_parser.add_argument("--format", choices=["text", "vtt"], default="text")
    trans_parser.add_argument("--output", "-o", help="Output file")

    # Clips
    clips_parser = subparsers.add_parser("clips", help="Suggest social media clips")
    clips_parser.add_argument("video", help="YouTube URL or video ID")
    clips_parser.add_argument("--duration", type=int, default=60, help="Clip duration in seconds")
    clips_parser.add_argument("--count", type=int, default=5, help="Number of clips")
    clips_parser.add_argument("--output", "-o", help="Output file")

    # Analyze
    analyze_parser = subparsers.add_parser("analyze", help="Custom analysis")
    analyze_parser.add_argument("video", help="YouTube URL or video ID")
    analyze_parser.add_argument("--prompt", action="append", required=True, help="Analysis prompt (can be used multiple times)")
    analyze_parser.add_argument("--output", "-o", help="Output file")

    args = parser.parse_args()

    try:
        summarizer = YouTubeSummarizer()

        if args.command == "summarize":
            summary = summarizer.summarize(args.video)

            if args.format == "markdown":
                output = format_summary_markdown(summary)
            else:
                output = json.dumps({
                    "quick_summary": summary.quick_summary,
                    "key_points": summary.key_points,
                    "quotes": summary.quotes,
                    "action_items": summary.action_items,
                    "resources": summary.resources
                }, indent=2)

            if args.output:
                Path(args.output).write_text(output)
                print(f"Summary saved to: {args.output}")
            else:
                print(output)

        elif args.command == "transcript":
            if args.format == "vtt":
                video_id = YouTubeHelper.extract_video_id(args.video)
                output = args.output or f"{video_id}.vtt"
                summarizer.transcript_extractor.export_vtt(video_id, output)
            else:
                transcript = summarizer.get_transcript(args.video, timestamps=args.timestamps)

                if args.output:
                    Path(args.output).write_text(transcript)
                    print(f"Transcript saved to: {args.output}")
                else:
                    print(transcript)

        elif args.command == "clips":
            clips = summarizer.suggest_clips(args.video, duration=args.duration, count=args.count)
            output = format_clips_json(clips)

            if args.output:
                Path(args.output).write_text(output)
                print(f"Clips saved to: {args.output}")
            else:
                print(output)

        elif args.command == "analyze":
            results = summarizer.analyze_custom(args.video, args.prompts)

            output = ""
            for name, analysis in results.items():
                output += f"\n## {name}\n\n{analysis}\n\n"

            if args.output:
                Path(args.output).write_text(output)
                print(f"Analysis saved to: {args.output}")
            else:
                print(output)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

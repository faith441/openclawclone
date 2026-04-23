#!/usr/bin/env python3
"""
Web Scraper Agent

Simple web scraping with:
- Extract text from any webpage
- Download images
- Save HTML/Markdown
- Extract links
- No API keys needed!
"""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse

class ScraperAgent:
    def __init__(self):
        self.has_requests = False
        self.has_bs4 = False

        try:
            import requests
            self.requests = requests
            self.has_requests = True
        except ImportError:
            print("⚠️  requests library not installed. Run: pip install requests")

        try:
            from bs4 import BeautifulSoup
            self.BeautifulSoup = BeautifulSoup
            self.has_bs4 = True
        except ImportError:
            print("⚠️  beautifulsoup4 not installed. Run: pip install beautifulsoup4")

    def scrape_text(self, url: str) -> dict:
        """Extract all text from a webpage."""
        if not self.has_requests or not self.has_bs4:
            return {"error": "Required libraries not installed"}

        try:
            response = self.requests.get(url, timeout=10)
            response.raise_for_status()

            soup = self.BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            result = {
                "url": url,
                "title": soup.title.string if soup.title else "No title",
                "text": text,
                "length": len(text),
                "timestamp": datetime.now().isoformat()
            }

            print(f"✓ Scraped: {url}")
            print(f"✓ Title: {result['title']}")
            print(f"✓ Text length: {result['length']} characters")

            return result

        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            return {"error": str(e), "url": url}

    def extract_links(self, url: str) -> dict:
        """Extract all links from a webpage."""
        if not self.has_requests or not self.has_bs4:
            return {"error": "Required libraries not installed"}

        try:
            response = self.requests.get(url, timeout=10)
            response.raise_for_status()

            soup = self.BeautifulSoup(response.content, 'html.parser')

            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url, href)
                    links.append({
                        "text": link.get_text().strip(),
                        "url": absolute_url
                    })

            result = {
                "url": url,
                "links_found": len(links),
                "links": links,
                "timestamp": datetime.now().isoformat()
            }

            print(f"✓ Found {len(links)} links on {url}")

            return result

        except Exception as e:
            print(f"❌ Link extraction failed: {e}")
            return {"error": str(e), "url": url}

    def download_images(self, url: str, output_dir: str = "images") -> dict:
        """Download all images from a webpage."""
        if not self.has_requests or not self.has_bs4:
            return {"error": "Required libraries not installed"}

        try:
            response = self.requests.get(url, timeout=10)
            response.raise_for_status()

            soup = self.BeautifulSoup(response.content, 'html.parser')

            # Create output directory
            Path(output_dir).mkdir(exist_ok=True)

            images = []
            for i, img in enumerate(soup.find_all('img')):
                img_url = img.get('src')
                if img_url:
                    img_url = urljoin(url, img_url)

                    # Download image
                    try:
                        img_response = self.requests.get(img_url, timeout=10)
                        img_response.raise_for_status()

                        # Get filename
                        filename = os.path.basename(urlparse(img_url).path) or f"image_{i}.jpg"
                        filepath = os.path.join(output_dir, filename)

                        # Save image
                        with open(filepath, 'wb') as f:
                            f.write(img_response.content)

                        images.append({
                            "url": img_url,
                            "file": filepath,
                            "alt": img.get('alt', '')
                        })

                        print(f"✓ Downloaded: {filename}")

                    except Exception as e:
                        print(f"⚠️  Failed to download {img_url}: {e}")

            result = {
                "url": url,
                "images_downloaded": len(images),
                "output_dir": output_dir,
                "images": images,
                "timestamp": datetime.now().isoformat()
            }

            print(f"\n✓ Downloaded {len(images)} images to {output_dir}/")

            return result

        except Exception as e:
            print(f"❌ Image download failed: {e}")
            return {"error": str(e), "url": url}

    def save_html(self, url: str, output_file: str) -> bool:
        """Save raw HTML from a webpage."""
        if not self.has_requests:
            return False

        try:
            response = self.requests.get(url, timeout=10)
            response.raise_for_status()

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"✓ HTML saved to: {output_file}")
            return True

        except Exception as e:
            print(f"❌ HTML save failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Web Scraper Agent")
    parser.add_argument('--url', required=True, help='URL to scrape')
    parser.add_argument('--mode', choices=['text', 'links', 'images', 'html'], default='text',
                        help='Scraping mode')
    parser.add_argument('--output', help='Output file/directory')

    args = parser.parse_args()

    agent = ScraperAgent()

    if args.mode == 'text':
        result = agent.scrape_text(args.url)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result.get('text', ''))
            print(f"✓ Text saved to: {args.output}")
        else:
            print("\n" + "=" * 70)
            print(result.get('text', '')[:500] + "...")
            print("=" * 70)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.mode == 'links':
        result = agent.extract_links(args.url)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"✓ Links saved to: {args.output}")
        print(json.dumps(result, indent=2))

    elif args.mode == 'images':
        output_dir = args.output or 'images'
        result = agent.download_images(args.url, output_dir)
        print(json.dumps(result, indent=2))

    elif args.mode == 'html':
        output_file = args.output or 'page.html'
        agent.save_html(args.url, output_file)

if __name__ == "__main__":
    main()

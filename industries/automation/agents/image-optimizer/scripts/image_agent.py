#!/usr/bin/env python3
"""
Image Optimizer Agent

Optimize images with:
- Resize images
- Compress/reduce quality
- Convert formats (PNG/JPG/WebP)
- Batch processing
- Create thumbnails
- No API keys needed!
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

class ImageAgent:
    def __init__(self):
        self.has_pillow = False
        try:
            from PIL import Image
            self.Image = Image
            self.has_pillow = True
        except ImportError:
            print("⚠️  Pillow library not installed. Run: pip install Pillow")

    def resize_image(self, input_file: str, output_file: str, width: int = None, height: int = None,
                     keep_aspect: bool = True) -> bool:
        """Resize an image."""
        if not self.has_pillow:
            return False

        try:
            img = self.Image.open(input_file)
            original_size = img.size

            if width and height:
                if keep_aspect:
                    # Calculate size maintaining aspect ratio
                    img.thumbnail((width, height), self.Image.Resampling.LANCZOS)
                    new_size = img.size
                else:
                    img = img.resize((width, height), self.Image.Resampling.LANCZOS)
                    new_size = (width, height)
            elif width:
                # Resize by width only
                aspect_ratio = img.size[1] / img.size[0]
                new_height = int(width * aspect_ratio)
                img = img.resize((width, new_height), self.Image.Resampling.LANCZOS)
                new_size = (width, new_height)
            elif height:
                # Resize by height only
                aspect_ratio = img.size[0] / img.size[1]
                new_width = int(height * aspect_ratio)
                img = img.resize((new_width, height), self.Image.Resampling.LANCZOS)
                new_size = (new_width, height)
            else:
                print("❌ Must specify width and/or height")
                return False

            img.save(output_file)

            print(f"✓ Resized: {input_file}")
            print(f"  Original: {original_size[0]}x{original_size[1]}")
            print(f"  New: {new_size[0]}x{new_size[1]}")
            print(f"  Saved to: {output_file}")

            return True

        except Exception as e:
            print(f"❌ Resize failed: {e}")
            return False

    def compress_image(self, input_file: str, output_file: str, quality: int = 85) -> bool:
        """Compress an image by reducing quality."""
        if not self.has_pillow:
            return False

        try:
            img = self.Image.open(input_file)

            # Convert RGBA to RGB if saving as JPEG
            if output_file.lower().endswith('.jpg') or output_file.lower().endswith('.jpeg'):
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = self.Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

            # Get file sizes
            original_size = os.path.getsize(input_file)

            # Save with compression
            img.save(output_file, quality=quality, optimize=True)

            new_size = os.path.getsize(output_file)
            reduction = ((original_size - new_size) / original_size) * 100

            print(f"✓ Compressed: {input_file}")
            print(f"  Original: {original_size / 1024:.1f} KB")
            print(f"  New: {new_size / 1024:.1f} KB")
            print(f"  Reduction: {reduction:.1f}%")
            print(f"  Quality: {quality}%")

            return True

        except Exception as e:
            print(f"❌ Compression failed: {e}")
            return False

    def convert_format(self, input_file: str, output_file: str, quality: int = 90) -> bool:
        """Convert image format."""
        if not self.has_pillow:
            return False

        try:
            img = self.Image.open(input_file)

            # Handle transparency for JPEG
            if output_file.lower().endswith(('.jpg', '.jpeg')):
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = self.Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background

            img.save(output_file, quality=quality)

            input_ext = Path(input_file).suffix
            output_ext = Path(output_file).suffix

            print(f"✓ Converted: {input_ext} → {output_ext}")
            print(f"  Input: {input_file}")
            print(f"  Output: {output_file}")

            return True

        except Exception as e:
            print(f"❌ Conversion failed: {e}")
            return False

    def create_thumbnail(self, input_file: str, output_file: str, size: int = 150) -> bool:
        """Create a thumbnail."""
        if not self.has_pillow:
            return False

        try:
            img = self.Image.open(input_file)
            img.thumbnail((size, size), self.Image.Resampling.LANCZOS)
            img.save(output_file)

            print(f"✓ Thumbnail created: {size}x{size}")
            print(f"  Saved to: {output_file}")

            return True

        except Exception as e:
            print(f"❌ Thumbnail creation failed: {e}")
            return False

    def batch_optimize(self, input_dir: str, output_dir: str, max_width: int = 1920,
                      quality: int = 85) -> dict:
        """Batch optimize all images in a directory."""
        if not self.has_pillow:
            return {"error": "Pillow not installed"}

        Path(output_dir).mkdir(exist_ok=True)

        results = {"processed": 0, "failed": 0, "total_reduction": 0, "files": []}

        for file_path in Path(input_dir).glob('*'):
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                try:
                    img = self.Image.open(file_path)

                    # Resize if too large
                    if img.size[0] > max_width:
                        aspect_ratio = img.size[1] / img.size[0]
                        new_height = int(max_width * aspect_ratio)
                        img = img.resize((max_width, new_height), self.Image.Resampling.LANCZOS)

                    # Save optimized
                    output_path = Path(output_dir) / file_path.name
                    img.save(output_path, quality=quality, optimize=True)

                    # Calculate reduction
                    original_size = file_path.stat().st_size
                    new_size = output_path.stat().st_size
                    reduction = original_size - new_size

                    results["processed"] += 1
                    results["total_reduction"] += reduction
                    results["files"].append({
                        "file": file_path.name,
                        "original_kb": original_size / 1024,
                        "new_kb": new_size / 1024,
                        "reduction_kb": reduction / 1024
                    })

                    print(f"✓ Optimized: {file_path.name}")

                except Exception as e:
                    print(f"⚠️  Failed: {file_path.name} - {e}")
                    results["failed"] += 1

        print(f"\n✓ Batch optimization complete!")
        print(f"  Processed: {results['processed']}")
        print(f"  Failed: {results['failed']}")
        print(f"  Total space saved: {results['total_reduction'] / 1024 / 1024:.1f} MB")

        return results

def main():
    parser = argparse.ArgumentParser(description="Image Optimizer Agent")
    parser.add_argument('--input', required=True, help='Input file or directory')
    parser.add_argument('--output', required=True, help='Output file or directory')
    parser.add_argument('--mode', choices=['resize', 'compress', 'convert', 'thumbnail', 'batch'],
                        default='compress', help='Optimization mode')
    parser.add_argument('--width', type=int, help='Target width (for resize)')
    parser.add_argument('--height', type=int, help='Target height (for resize)')
    parser.add_argument('--quality', type=int, default=85, help='JPEG quality (1-100)')
    parser.add_argument('--size', type=int, default=150, help='Thumbnail size')

    args = parser.parse_args()

    agent = ImageAgent()

    if args.mode == 'resize':
        agent.resize_image(args.input, args.output, args.width, args.height)
    elif args.mode == 'compress':
        agent.compress_image(args.input, args.output, args.quality)
    elif args.mode == 'convert':
        agent.convert_format(args.input, args.output, args.quality)
    elif args.mode == 'thumbnail':
        agent.create_thumbnail(args.input, args.output, args.size)
    elif args.mode == 'batch':
        result = agent.batch_optimize(args.input, args.output, args.width or 1920, args.quality)
        import json
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

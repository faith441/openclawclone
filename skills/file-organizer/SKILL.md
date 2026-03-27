---
name: file-organizer
description: Organize files by type, date, or project. Use when user wants to sort files, clean up directories, or create folder structures. Provides shell commands or scripts.
---

# File Organizer

## Overview

Helps organize files into logical folder structures based on file type, date, project, or custom criteria. Generates shell commands or Python scripts.

## When to Use

- User wants to organize a messy downloads folder
- User needs to sort files by type or date
- User wants a folder structure recommendation

## Common Organization Patterns

### By File Type
```
organized/
├── documents/    # .pdf, .doc, .docx, .txt
├── images/       # .jpg, .png, .gif, .svg
├── videos/       # .mp4, .mov, .avi
├── audio/        # .mp3, .wav, .flac
├── archives/     # .zip, .tar, .gz
├── code/         # .py, .js, .ts, .go
└── other/        # everything else
```

### By Date
```
organized/
├── 2024/
│   ├── 01-january/
│   ├── 02-february/
│   └── ...
└── 2023/
    └── ...
```

### By Project
```
projects/
├── project-name/
│   ├── docs/
│   ├── assets/
│   └── src/
└── ...
```

## Shell Commands

### Organize by extension (bash)
```bash
# Create directories and move files
for ext in pdf doc docx; do
  mkdir -p documents
  mv *.$ext documents/ 2>/dev/null
done

for ext in jpg jpeg png gif svg; do
  mkdir -p images
  mv *.$ext images/ 2>/dev/null
done
```

### List files by size
```bash
ls -lhS | head -20
```

### Find duplicates by name
```bash
find . -type f | rev | cut -d'/' -f1 | rev | sort | uniq -d
```

## Guidelines

1. **Always preview** before moving - show what will happen first
2. **Handle conflicts** - ask about duplicate filenames
3. **Preserve structure** - don't flatten nested folders without asking
4. **Backup suggestion** - recommend backup for large reorganizations

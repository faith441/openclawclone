---
name: bookmark-manager
description: Organize and categorize bookmarks/links. Use when user has a list of URLs to organize, wants folder structures for bookmarks, or needs to tag and categorize saved links.
---

# Bookmark Manager

## Overview

Helps organize bookmarks and saved links into logical categories with tags and descriptions.

## When to Use

- User has a messy list of bookmarks to organize
- User wants to categorize saved links
- User needs a bookmark folder structure

## Output Format

### Categorized Bookmarks
```markdown
## 📚 Learning & Tutorials
- [Title](url) - Brief description #tag1 #tag2

## 💻 Development Tools
- [Title](url) - Brief description #dev #tools

## 📰 News & Reading
- [Title](url) - Brief description #news

## 🎨 Design Resources
- [Title](url) - Brief description #design

## 🔧 Utilities
- [Title](url) - Brief description #utility
```

### Recommended Folder Structure
```
Bookmarks/
├── Work/
│   ├── Projects/
│   ├── Tools/
│   └── Documentation/
├── Learning/
│   ├── Courses/
│   ├── Tutorials/
│   └── Articles/
├── Personal/
│   ├── Shopping/
│   ├── Entertainment/
│   └── Travel/
└── Reference/
    ├── Cheatsheets/
    └── APIs/
```

## Common Categories

| Category | Examples |
|----------|----------|
| Development | GitHub, Stack Overflow, docs |
| Design | Dribbble, Figma, fonts |
| Productivity | Notion, tools, apps |
| Learning | Courses, tutorials, blogs |
| Reference | Documentation, APIs, specs |
| News | Tech news, newsletters |
| Shopping | Wishlist, stores |
| Entertainment | Streaming, games, media |

## Features

1. **Auto-categorize** based on URL domain
2. **Generate descriptions** from page content
3. **Suggest tags** based on content
4. **Find duplicates** in bookmark list
5. **Export formats** - HTML, JSON, Markdown

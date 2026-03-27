---
name: url-summarizer
description: Summarize web pages and articles. Use when user provides a URL and wants a summary of the content, key points, or specific information extracted.
---

# URL Summarizer

## Overview

Fetches and summarizes web page content, extracting key information, main points, and relevant details.

## When to Use

- User provides a URL to summarize
- User wants key points from an article
- User needs specific information from a web page

## Output Format

```markdown
## Page Summary

**Title:** [Page title]
**Source:** [Domain/Publication]
**Type:** [Article/Documentation/Blog/News/etc.]

### TL;DR
[1-2 sentence summary]

### Key Points
- [Main point 1]
- [Main point 2]
- [Main point 3]
- [Main point 4]
- [Main point 5]

### Detailed Summary
[2-3 paragraph summary covering main content]

### Notable Quotes
> "[Important quote from the article]"

### Related Topics
- [Topic 1]
- [Topic 2]

### Metadata
- **Author:** [If available]
- **Date:** [If available]
- **Reading time:** [Estimated]
```

## Content Types

| Type | Focus On |
|------|----------|
| News Article | Who, what, when, where, why |
| Blog Post | Main argument, key insights |
| Documentation | Purpose, usage, examples |
| Research Paper | Abstract, findings, conclusions |
| Product Page | Features, pricing, comparisons |
| Tutorial | Steps, prerequisites, outcome |

## Guidelines

1. **Preserve accuracy** - Don't add information not in source
2. **Maintain objectivity** - Report what's there, not opinions
3. **Note limitations** - If page is paywalled/inaccessible, say so
4. **Extract structure** - Use headings that match content organization
5. **Link to sections** - Reference specific parts when relevant

## Questions to Ask

- "What specific information are you looking for?"
- "Do you want a brief or detailed summary?"
- "Should I focus on any particular section?"

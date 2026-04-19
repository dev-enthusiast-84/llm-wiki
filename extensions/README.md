# Extensions

Browser extensions and tools for managing your LLM wiki.

## Obsidian Web Clipper

**Purpose**: Clip web content (articles, blog posts, documentation) directly into your wiki from the browser

**Browsers**: Chrome, Firefox, Safari, Edge

**Installation**:

1. Install Obsidian (if not already installed)
   - Download from [obsidian.md](https://obsidian.md)
   - Create a vault or point to your wiki folder

2. Install Web Clipper browser extension
   - **Chrome/Edge**: [Obsidian Web Clipper](https://chrome.google.com/webstore/detail/obsidian-web-clipper/eomnjlefhfokkgboaegkjapghifbjprd)
   - **Firefox**: Available on Firefox Add-ons
   - **Safari**: Available on Safari App Store

3. Configure extension settings
   - Set default save location: `raw/` folder
   - Choose template format (see below)
   - Enable backlink syntax: `[[concept]]`

### Clip Template

Configure Web Clipper to save clips in this format:

```markdown
# [Title of Article]

**URL**: [source-url]  
**Date Clipped**: YYYY-MM-DD

## Content

[clipped content here]

## Related Concepts

- [[concept1]]
- [[concept2]]

## Tags

#clipped #source
```

This preserves the original URL, makes it easy to add related concepts, and keeps clipped material separate from your entity pages.

### Workflow

1. Find relevant article/blog/documentation online
2. Click Obsidian Web Clipper icon in browser toolbar
3. Choose template → "Save"
4. Content is saved to `wiki/` (or specified folder)
5. Later, use `/Sync Wiki from Raw` to extract concepts and create proper entity pages

### Tips

- **Clip before reading**: Save first, organize later
- **Add context**: Before clipping, note which topic/paper it relates to
- **Link to entities**: When reviewing clips, manually link to existing `[[concepts]]`
- **Extract via sync**: Use `/Sync Wiki from Raw` with clipped content to create proper wiki pages

---

## Other Useful Tools

- **Obsidian Sync**: Subscribe to sync vault across devices
- **Git integration**: Use git to version control your wiki (already set up)
- **Markdown preview**: Use VS Code's built-in markdown preview to review pages


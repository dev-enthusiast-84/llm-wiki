# Wiki Format & Conventions

## File Naming

- **Pattern**: `kebab-case-concept.md`
- **Examples**: `self-attention.md`, `masked-language-model.md`, `scaled-dot-product-attention.md`
- **Rules**:
  - Lowercase only
  - Use hyphens to separate words (not underscores)
  - Match the concept name as used in other pages' links

## File Structure

Each entity page should follow this order:

```
# Title

Brief 1-2 sentence definition

## Summary

Quick overview (2-3 sentences)

## Explanation

Detailed breakdown of the concept

## Related Concepts

- [[concept1]]
- [[concept2]]

## Sources

- Paper title (Year) - specific page/section
- Paper title (Year)

## Contradictions

(Only if applicable) Note conflicting definitions or approaches across sources
```

## Link Syntax

**Format**: `[[concept]]` or `[[concept#section]]`

- **Usage**: Use `[[concept]]` to link to another wiki entity
- **Full page link**: `[[self-attention]]`
- **Anchor link**: `[[transformer#attention-mechanism]]`
- **Spacing**: No spaces inside brackets
- **Case**: Match the filename exactly

## Markdown Conventions

- **Headings**: Use `#` for main title, `##` for sections
- **Bold**: Use `**term**` for important vocabulary
- **Formulas**: Use inline `$...$` for simple math, or code blocks for complex
- **Code**: Use backticks for Python/pseudocode snippets
- **Lists**: Bullet lists for related concepts, numbered steps for procedures

## Index Registration

Add your new entity to [wiki/index.md](../../../wiki/index.md) under the appropriate category:

```markdown
## Category Name

- [[new-concept]] - Brief one-sentence description
```

## Quality Checklist

Before committing a new page:

- [ ] Filename matches concept name in kebab-case
- [ ] Summary section is 2-3 sentences max
- [ ] All cross-references use `[[brackets]]` syntax
- [ ] Sources section cites which papers introduced this concept
- [ ] No orphaned pages - add to index.md
- [ ] Check for contradictions between sources, document if found
- [ ] All related concepts are linked

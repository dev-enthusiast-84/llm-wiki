---
name: wiki-compilation
description: 'Extract key concepts from research papers and create entity wiki pages. Use when: processing academic papers, building knowledge bases, creating markdown documentation with cross-references, initializing wiki index, extracting definitions and relationships from sources.'
argument-hint: 'Paste paper content or provide sources'
---

# Wiki Compilation

Transform research papers into a structured wiki by extracting key concepts and creating interconnected entity pages.

## When to Use

- Building an LLM/AI knowledge base from research papers
- Creating entity pages for new concepts
- Setting up initial wiki structure
- Extracting definitions and links between concepts
- Documenting contradictions or variants in literature

## Procedure

### 1. Prepare Source Material

Gather research papers or documentation you want to process. This can be:
- Full paper text
- Paper abstracts
- Multiple papers on related topics
- Technical documentation

### 2. Extract Key Concepts

For each paper source:
- Identify primary concepts and terminology
- Note definitions and explanations
- Record relationships to other concepts
- Flag conflicting definitions or approaches

### 3. Create Entity Pages

For each concept, create a new markdown file in `wiki/` following the [Wiki Format](./references/wiki-format.md):
- **Filename**: kebab-case concept name (e.g., `masked-language-model.md`)
- **Content**: Use the [Entity Template](./assets/entity-template.md)
- **Links**: Connect related concepts using `[[brackets]]` syntax
- **Sources**: Reference which papers introduced or defined this concept

### 4. Update Index

Add the new entity to [wiki/index.md](../../wiki/index.md) in the appropriate category.

### 5. Resolve Contradictions

When multiple sources define a concept differently:
- Note all interpretations in the page
- Cite which papers support each definition
- Use `## Contradictions` section (see template)
- Link to related concepts that clarify distinctions

## Example Workflow

```
Input: Papers on "Transformer" architecture
↓
Extract: self-attention, positional encoding, feed-forward networks
↓
Create: transformer.md, self-attention.md, positional-encoding.md
↓
Link: Each page references the others via [[brackets]]
↓
Update: Add entries to wiki/index.md
```

## Reference Files

- [Wiki Format & Conventions](./references/wiki-format.md) - Structure and style guide
- [Entity Template](./assets/entity-template.md) - Copy-paste starting point

## Tips

- **One concept per file**: Keep pages focused and reusable
- **Cross-link liberally**: Use `[[concept]]` syntax to connect ideas
- **Be precise with links**: Match exact filenames, including hyphens
- **Document sources**: Always trace concepts back to papers
- **Iterative refinement**: Update pages as you find new information

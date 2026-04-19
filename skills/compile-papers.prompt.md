---
description: "Read papers and create entity wiki pages. Extract key concepts, create markdown files with summaries and cross-references, note contradictions."
name: "Compile Papers to Wiki"
argument-hint: "Paste paper content or provide sources"
---

Read these papers and create entity pages in wiki/. For each key concept:

1. **Extract key concepts** from the source material
2. **Create a markdown file** for each concept in `wiki/` with:
   - A clear summary and explanation
   - Related links using `[[brackets]]` syntax
   - Note any contradictions between papers
3. **Update wiki/index.md** to register new entities
4. **Follow the format** in [Entity Template](./skills/wiki-compilation/assets/entity-template.md)

**Key guidelines:**
- Use kebab-case filenames (e.g., `self-attention.md`)
- Link related concepts with `[[concept-name]]`
- Always cite sources with paper title and year
- Document conflicting definitions if found
- Keep summaries to 2-3 sentences

Provide the paper content, abstracts, or sources you want to process.

# LLM Wiki — Personal Knowledge Base

A structured system for building and maintaining a personal wiki of LLM/AI concepts from research papers. Extract key concepts from sources, create interconnected entity pages, and keep your knowledge base organized and up-to-date.

## Quick Start

1. **Add papers** to the `raw/` folder
2. **Run** `/Compile Papers to Wiki` to extract concepts and create entity pages
3. **Add new papers?** Use `/Sync Wiki from Raw` for incremental updates
4. **Reach 20+ pages?** Run `/Audit Wiki` for quality checks

## Folder Structure

```
llm-wiki/
├── raw/                          # Source materials (papers, articles, docs)
├── wiki/                         # Your knowledge base
│   ├── index.md                  # (Auto-generated) Directory of all entities
│   ├── log.md                    # (Auto-generated) Compilation history
│   ├── concept-name.md           # Entity pages for each concept
│   ├── another-concept.md
│   └── ...
├── skills/                       # Copilot skills & commands
│   ├── wiki-compilation/         # Initial wiki setup skill
│   ├── wiki-sync/                # Incremental update skill
│   ├── wiki-audit/               # Quality audit skill
│   ├── compile-papers.prompt.md  # Command: /Compile Papers to Wiki
│   ├── sync-wiki.prompt.md       # Command: /Sync Wiki from Raw
│   └── audit-wiki.prompt.md      # Command: /Audit Wiki
├── extensions/                   # Browser & tool integrations
│   └── README.md                 # Obsidian Web Clipper setup
├── copilot-instructions.md       # Workspace configuration
└── .git/                         # Version control
```

## Three-Step Workflow

### Step 1: Compile Initial Wiki from Papers

When starting the wiki or processing a batch of new research:

**Command**: `/Compile Papers to Wiki`

This workflow:
- Reads papers or research in the `/raw` folder
- Extracts key concepts and terminology
- Creates markdown entity pages for each concept
- Links related concepts using `[[bracket]]` syntax
- Documents contradictions between sources

**Example**:
```
Input: transformer.pdf, bert.pdf in /raw/
↓
Extract: attention, self-attention, positional-encoding, transformer, bert
↓
Create: wiki/transformer.md, wiki/self-attention.md, wiki/bert.md, ...
↓
Link: Each page references related concepts
↓
Update: wiki/index.md with new entries
```

### Step 2: Sync New Sources Incrementally

When new papers are added to `/raw`:

**Command**: `/Sync Wiki from Raw`

This workflow:
- Reads new source alongside existing wiki pages
- Updates affected entity pages with new information
- Creates new pages for novel concepts
- Updates contradictions sections if sources conflict
- Maintains `wiki/log.md` tracking changes

**Example**:
```
New paper: llm-scaling-laws.pdf added to /raw/
↓
Read alongside: transformer.md, pre-training-fine-tuning.md
↓
Update: Add scaling insights to transformer.md, pre-training-fine-tuning.md
↓
Create: wiki/scaling-laws.md (new concept)
↓
Log: "2026-04-20: Added scaling-laws from LLM Scaling Laws paper"
```

**When to sync**:
- After adding new papers to `/raw`
- When you discover new research on a topic
- Regularly (weekly/monthly) to keep wiki current

### Step 3: Audit for Quality (Every ~20 pages)

When wiki reaches approximately 20-30 pages:

**Command**: `/Audit Wiki`

This workflow identifies:
- **Orphan pages** — concepts with no inbound links
- **Missing pages** — concepts referenced but not created
- **Contradictions** — conflicting definitions across pages
- **Stale claims** — outdated information superseded by newer sources

**When to audit**:
- Every ~20-30 new pages (roughly monthly for active projects)
- After major sync batches
- Before sharing or publishing wiki
- When you notice quality issues

## Entity Pages Format

Each concept gets its own markdown file following this template:

```markdown
# Concept Name

One-line definition.

## Summary

2-3 sentence overview of what this is and why it matters.

## Explanation

Detailed breakdown, components, examples, mathematical formulation if applicable.

### Subsection (optional)

More details...

## Related Concepts

- [[concept1]] - How it relates
- [[concept2]] - Connection or distinction
- [[concept3]] - Part of larger architecture

## Sources

- Author(s) - "Paper Title" (Year) - Section/page reference

## Contradictions

(Optional) Note if different sources define this differently

---

**Status**: New / Updated
**Last Updated**: YYYY-MM-DD
```

**Key principles**:
- **One concept per file** — Keep pages focused and reusable
- **Use `[[brackets]]`** for links — Creates a graph of interconnected ideas
- **Always cite sources** — Trace every concept back to papers
- **Document contradictions** — Different sources may define things differently; capture this nuance

## File Organization

### `/raw` folder

Store source materials here:
- PDF papers
- Text articles
- Documentation
- Research notes

No special format required — just add files as you collect them.

### `/wiki` folder

Your knowledge base. Auto-generated files:

**`wiki/index.md`** — Created when you have 30+ pages
Lists every entity with one-line descriptions. Example:
```markdown
# Wiki Index

## Core Concepts
- [[transformer]] - Neural network architecture using self-attention
- [[self-attention]] - Mechanism for computing attention between all token pairs
- [[bert]] - Bidirectional transformer pre-trained on masked language modeling

## Training
- [[pre-training-fine-tuning]] - Two-phase training approach
- [[masked-language-model]] - Self-supervised pre-training objective
```

**`wiki/log.md`** — Created when you have 30+ pages
Tracks compilation history. Example:
```markdown
| Date | Source | New Entities | Updated Entities | Notes |
|------|--------|---|---|---|
| 2026-04-20 | "Attention is All You Need" (2017) | transformer, self-attention | - | Foundational paper |
| 2026-04-21 | "BERT" (2019) | bert, masked-language-model | transformer | Noted contradiction: bidirectional vs causal |
```

## commands in Copilot Chat

All commands appear when you type `/` in Copilot Chat:

| Command | When to Use | Output |
|---------|---|---|
| `/Compile Papers to Wiki` | Initial setup or batch processing | New entity pages + updated index |
| `/Sync Wiki from Raw` | Adding new sources incrementally | Updated + new pages + log entry |
| `/Audit Wiki` | Every ~20-30 pages | Quality report + suggested fixes |

## Best Practices

✓ **Link liberally** — Use `[[concept]]` to create connections. More links = better navigation.

✓ **One concept = one file** — Don't merge related concepts; link them instead.

✓ **Cite everything** — Always include which paper introduced a concept.

✓ **Document contradictions** — If sources disagree, capture both viewpoints and context.

✓ **Commit frequently** — After each compilation/sync, commit with descriptive messages:
  ```bash
  git add wiki/
  git commit -m "Compile wiki: Add 5 concepts from BERT paper"
  ```

✓ **Review before audit** — Skim pages before running audit to catch obvious issues.

✓ **Use descriptive filenames** — Kebab-case: `masked-language-model.md` not `mlm.md`.

✓ **Update sources section** — When syncing, add the new paper to existing pages' sources if relevant.

## Example Workflow

### Day 1: Initialize Wiki

```bash
# Add papers to /raw
cp ~/Papers/transformer-2017.pdf raw/
cp ~/Papers/bert-2019.pdf raw/
cp ~/Papers/gpt-3-2020.pdf raw/

# In Copilot Chat: /Compile Papers to Wiki
# Extracts concepts from all three papers
# Creates wiki/transformer.md, wiki/bert.md, wiki/gpt-3.md, etc.
# Updates wiki/index.md

git add wiki/
git commit -m "Initial wiki: Compile transformer, BERT, GPT-3 papers"
```

### Day 5: Add New Paper

```bash
# Add new paper
cp ~/Papers/llm-scaling-laws-2022.pdf raw/

# In Copilot Chat: /Sync Wiki from Raw
# Reads new paper alongside existing pages
# Updates wiki/pre-training-fine-tuning.md with scaling insights
# Creates wiki/scaling-laws.md
# Updates wiki/log.md

git add wiki/
git commit -m "Sync wiki: Add scaling-laws, update pre-training-fine-tuning"
```

### Day 30: Quality Check

```bash
# Wiki now has ~25 pages

# In Copilot Chat: /Audit Wiki
# Identifies:
# - 2 orphan pages (add backlinks)
# - 3 missing concepts (need new pages)
# - 1 contradiction about "attention" (document it)

# Fix issues, then commit:
git add wiki/
git commit -m "Wiki audit: Fix orphans, link missing concepts, document contradiction"
```

## Navigating Your Wiki

### Via File Links

Most markdown editors support `[[bracket]]` links:
- Click on links to navigate between concepts
- See backlinks (which pages reference this page)
- Build a mental map of concept relationships

### Via `wiki/index.md`

Once you have 30+ pages, the index contains:
- All concepts organized by category
- One-line descriptions for quick lookup
- Links to every entity

### Via `wiki/log.md`

Trace concepts back to their sources:
- Find which paper introduced a concept
- See when pages were last updated
- Track evolution of ideas (see contradictions over time)

## Troubleshooting

**Q: I added a paper to `/raw` but nothing changed**  
A: Run `/Sync Wiki from Raw` command in Copilot Chat to process it.

**Q: How do I fix a broken link?**  
A: Search for the reference in `wiki/*.md`, check the target page name (must match exactly, kebab-case), and update.

**Q: A page wasn't created — concept exists but no file**  
A: Run `/Audit Wiki` to find missing pages, then `/Sync Wiki from Raw` to create them.

**Q: How do I remove a page?**  
A: Delete the file and remove it from `wiki/index.md`. Note all backlinks and decide whether to update or remove them.

**Q: Can I have multiple versions of a concept?**  
A: Better to have one page with a "Contradictions" section noting different definitions. Link to related concepts that clarify distinctions.

## Resources

**Skills & Templates**:
- Entity template: `skills/wiki-compilation/assets/entity-template.md`
- Format guide: `skills/wiki-compilation/references/wiki-format.md`
- Update checklist: `skills/wiki-sync/references/update-checklist.md`
- Audit checklist: `skills/wiki-audit/references/audit-checklist.md`

**Documentation**:
- Wiki compilation: `skills/wiki-compilation/SKILL.md`
- Wiki sync: `skills/wiki-sync/SKILL.md`
- WOptional: Browser Integration

Use **Obsidian Web Clipper** to save web articles directly into your wiki:

1. Install the browser extension (see `extensions/README.md`)
2. Clip relevant articles while browsing
3. Use `/Sync Wiki from Raw` to extract concepts from clipped content
4. Create formal entity pages from the extracted concepts

This workflow lets you capture research on-the-fly without leaving your browser.

## Next Steps

1. ✓ Add first batch of papers to `raw/`
2. Run `/Compile Papers to Wiki` to initialize `wiki/`
3. Review created pages and familiarize yourself with the format
4. Add more papers as you find them, syncing with `/Sync Wiki from Raw`
5. (Optional) Set up Obsidian Web Clipper for browser clipping (see `extensions/README.md`)
6. When wiki reaches ~20 pages, run `/Audit Wiki` for quality checks
7. Add more papers as you find them, syncing with `/Sync Wiki from Raw`
5. When wiki reaches ~20 pages, run `/Audit Wiki` for quality checks
6. Commit progress regularly

## Credit
 Inspired by the concept of LLM Wiki : https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (Andrej Karpathy) 

---

**Created**: 2026-04-19  
**Status**: Ready to use  
**Commands**: 3 (compile, sync, audit)

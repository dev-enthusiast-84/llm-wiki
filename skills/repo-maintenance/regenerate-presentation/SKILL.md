---
name: regenerate-presentation
description: 'Regenerate presentation assets (demo videos and PPTX deck) when code, skills, or UI has changed. Detects what changed via git, decides whether to rebuild videos, the deck, or both, runs the generator scripts, and reports the result.'
argument-hint: 'No argument needed — changes detected via git. Pass "videos" to rebuild videos only, "deck" for deck only, "all" to force full rebuild.'
---

# Regenerate Presentation

Keep `presentation/` assets current whenever code, skills, commands, or the wiki query UI changes. Rebuilds only what is stale — rebuilding videos is skipped when nothing that affects them has changed.

## When to Use

- After modifying `presentation/generate_presentation.py` (slide layout, content, colors, structure)
- After modifying `presentation/generate_demo_videos.py` (terminal or UI demo scenes, timing, narration)
- After adding, renaming, or removing a skill or slash command (terminal demo shows real command names)
- After changing `wiki_query.py` (UI demo screenshots reflect the actual running app)
- Before sharing or presenting — ensures the deck matches the current state of the repo
- After running `/sync-docs` when it flags presentation assets as stale

## What Gets Regenerated

| Asset | Script | When rebuilt |
|-------|--------|-------------|
| `terminal-demo.mp4` | `generate_demo_videos.py --terminal` | `generate_demo_videos.py` changed, or skill commands changed |
| `ui-demo.mp4` | `generate_demo_videos.py --ui` | `generate_demo_videos.py` changed, or `wiki_query.py` changed |
| `llm-wiki-deck.pptx` | `generate_presentation.py --pptx` | Any of the above, or `generate_presentation.py` changed |

## Change-to-Action Mapping

| What changed | What to rebuild |
|---|---|
| `presentation/generate_demo_videos.py` | Both videos + deck |
| `presentation/generate_presentation.py` | Deck only (videos unchanged) |
| `wiki_query.py` | UI demo video + deck |
| `skills/**`, `.claude/commands/**`, `.github/prompts/**` | Terminal demo video + deck |
| Both generator scripts | Both videos + deck |
| Nothing in the above paths | Report "nothing to rebuild" and stop |

## Procedure

### 1. Detect Changes

```bash
git diff --name-only HEAD
git status --short
```

Group changed files:

| Category | Paths |
|----------|-------|
| `video-script` | `presentation/generate_demo_videos.py` |
| `deck-script` | `presentation/generate_presentation.py` |
| `ui-code` | `wiki_query.py` |
| `skill-commands` | `skills/**`, `.claude/commands/**/*.md`, `.github/prompts/**/*.prompt.md` |

If an explicit argument was passed (`videos`, `deck`, or `all`), skip git detection and use that.

If no relevant paths changed, report "Nothing to rebuild" and stop.

### 2. Announce the Plan

Before running anything, state the decision:

```
Changes detected:
  • wiki_query.py               → UI demo video is stale
  • skills/...     → terminal demo video is stale

Plan: rebuild terminal-demo.mp4, ui-demo.mp4, then llm-wiki-deck.pptx
```

### 3. Run Generator Scripts

**Always rebuild videos before the deck.** The deck embeds the video files — rebuilding the deck before the videos embeds stale content.

| Task | Command |
|------|---------|
| Rebuild terminal demo only | `cd presentation && python generate_demo_videos.py --terminal` |
| Rebuild UI demo only | `cd presentation && python generate_demo_videos.py --ui` |
| Rebuild both videos | `cd presentation && python generate_demo_videos.py` |
| Rebuild PPTX deck | `cd presentation && python generate_presentation.py --pptx` |
| Full rebuild (all) | `cd presentation && python generate_demo_videos.py && python generate_presentation.py --pptx` |

If any script exits non-zero: report the error, stop, and do not proceed to the deck step.

### 4. Verify Outputs

Check that each rebuilt file has a non-zero size and a current modification timestamp:

```bash
ls -lh presentation/terminal-demo.mp4 presentation/ui-demo.mp4 presentation/llm-wiki-deck.pptx
```

Verify both videos are embedded in slide 5 of the deck:

```bash
python3 -c "
from pptx import Presentation
p = Presentation('presentation/llm-wiki-deck.pptx')
media = [s.name for sl in p.slides for s in sl.shapes if s.shape_type == 16]
print('Embedded media:', media)
"
```

Expected output: `Embedded media: ['terminal-demo.mp4', 'ui-demo.mp4']`

If the list is missing a video, the deck generator fell back to a placeholder — check that the video file exists at the expected path before re-running.

### 5. Keynote and Google Slides (optional)

If the Keynote format is needed:

```bash
cd presentation && python generate_presentation.py --keynote
```

Then in Keynote: **File → Export To → Keynote** → save as `presentation/llm-wiki-deck.key`.

> macOS Sequoia 15.x blocks programmatic PPTX import via AppleScript. The `--keynote` flag opens Keynote with the file; the export step is manual.

For Google Slides:

```bash
pip install google-api-python-client google-auth-oauthlib  # first time only
# Place OAuth credentials at ~/.llm-wiki-google-credentials.json
cd presentation && python generate_presentation.py --slides
```

Or manually: `slides.google.com → File → Import slides → Upload → llm-wiki-deck.pptx`

### 6. Report

Produce the Results Summary block after completing all steps.

## Results Summary Format

```
✅ Regenerate Presentation — complete  YYYY-MM-DD

🎬 Assets rebuilt:
   terminal-demo.mp4     — rebuilt (N KB) / unchanged
   ui-demo.mp4           — rebuilt (N KB) / unchanged
   llm-wiki-deck.pptx    — rebuilt (N KB)

📊 Deck: 5 slides · both videos embedded · speaker notes on all slides

⚠️  Manual steps for other formats:
   Keynote:  python generate_presentation.py --keynote
             then in Keynote: File → Export To → Keynote
   G Slides: slides.google.com → File → Import slides → Upload llm-wiki-deck.pptx

⚠️  Manual review needed: N items  (or "none")

➡️  Next step: run /sync-docs to update README and copilot-instructions
```

## Relation to Other Skills

| Skill | Relationship |
|-------|-------------|
| `/sync-docs` | Run **after** — keeps README, copilot-instructions, and docs/index.html in sync with any presentation changes |
| `/run-maintenance` | Verifies this skill is registered and all health checks pass |
| `/compile-papers` | Separate — populates wiki entity pages; not related to presentation assets |

## Safety Rules

- Always rebuild videos **before** the deck — the deck embeds them; wrong order = stale content
- If a script fails, stop and report — never produce a partially-built deck
- Never delete `terminal-demo.mp4` or `ui-demo.mp4` without immediately rebuilding them

## Reference Files

- Slide generator: `presentation/generate_presentation.py`
- Video generator: `presentation/generate_demo_videos.py`
- Presentation section in README: `README.md` → `## Presentation`
- Rebuild checklist: `skills/repo-maintenance/regenerate-presentation/references/rebuild-checklist.md`

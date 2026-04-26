---
description: Rebuild demo videos and PPTX deck when code, skills, or the wiki query UI changes. Detects what changed via git, rebuilds only what is stale, and verifies both videos are embedded in the deck.
---

## Usage

**Invoke:** type `/regenerate-presentation` in Claude Code CLI  
**When to run:** after modifying `generate_presentation.py`, `generate_demo_videos.py`, `wiki_query.py`, or any skill/command file  
**Arguments:** none (auto-detects via git) · `videos` · `deck` · `all`

---

## Step 1: Detect what changed

```bash
git diff --name-only HEAD
git status --short
```

Group changed paths:

| Category | Paths |
|----------|-------|
| `video-script` | `presentation/generate_demo_videos.py` |
| `deck-script` | `presentation/generate_presentation.py` |
| `ui-code` | `wiki_query.py` |
| `skill-commands` | `skills/**`, `.claude/commands/**`, `.github/prompts/**` |

If an explicit argument was passed (`videos`, `deck`, or `all`), skip git detection and use that.

Announce the decision before running anything. If no relevant paths changed, report **"Nothing to rebuild"** and stop.

---

## Step 2: Rebuild assets

Decision table:

| What changed | What to rebuild |
|---|---|
| `generate_demo_videos.py` | Both videos + deck |
| `generate_presentation.py` | Deck only |
| `wiki_query.py` | UI demo video + deck |
| `skills/**` or commands | Terminal demo video + deck |

Commands (run from repo root):

| Task | Command |
|------|---------|
| Terminal demo only | `cd presentation && python generate_demo_videos.py --terminal` |
| UI demo only | `cd presentation && python generate_demo_videos.py --ui` |
| Both videos | `cd presentation && python generate_demo_videos.py` |
| Deck only | `cd presentation && python generate_presentation.py --pptx` |
| Full rebuild | `cd presentation && python generate_demo_videos.py && python generate_presentation.py --pptx` |

**Always rebuild videos before the deck** — the deck embeds them. Stop and report any non-zero exit code.

---

## Step 3: Verify outputs

```bash
ls -lh presentation/terminal-demo.mp4 presentation/ui-demo.mp4 presentation/llm-wiki-deck.pptx
```

Confirm both videos are embedded in the deck:
```bash
python3 -c "
from pptx import Presentation
p = Presentation('presentation/llm-wiki-deck.pptx')
media = [s.name for sl in p.slides for s in sl.shapes if s.shape_type == 16]
print('Embedded media:', media)
"
```

Expected: `Embedded media: ['terminal-demo.mp4', 'ui-demo.mp4']`

If a video is missing from the list, check the file exists at the expected path, then rerun the deck generator.

---

## Results Summary

```
✅ Regenerate Presentation — complete  YYYY-MM-DD

🎬 Assets rebuilt:
   terminal-demo.mp4     — rebuilt (N KB) / unchanged
   ui-demo.mp4           — rebuilt (N KB) / unchanged
   llm-wiki-deck.pptx    — rebuilt (N KB)

📊 Deck: 5 slides · both videos embedded · speaker notes on all slides

⚠️  Manual steps for other formats:
   Keynote:  cd presentation && python generate_presentation.py --keynote
             then in Keynote: File → Export To → Keynote
   G Slides: slides.google.com → File → Import slides → Upload llm-wiki-deck.pptx

➡️  Next step: run /sync-docs to update README and copilot-instructions
```

See `skills/repo-maintenance/regenerate-presentation/SKILL.md` for full guidance.

$ARGUMENTS

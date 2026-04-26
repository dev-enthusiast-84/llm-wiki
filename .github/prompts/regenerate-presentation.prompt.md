---
mode: agent
description: Rebuild demo videos and PPTX deck when code, skills, or the wiki query UI changes. Detects what changed via git, rebuilds only what is stale, and verifies both videos are embedded in the deck.
---

## Step 1: Detect what changed

Run:
```
git diff --name-only HEAD
git status --short
```

Group changed paths into:

| Category | Paths |
|----------|-------|
| `video-script` | `presentation/generate_demo_videos.py` |
| `deck-script` | `presentation/generate_presentation.py` |
| `ui-code` | `wiki_query.py` |
| `skill-commands` | `skills/**`, `.claude/commands/**`, `.github/prompts/**` |

Announce what will be rebuilt before running anything. If no relevant paths changed, report **"Nothing to rebuild"** and stop.

---

## Step 2: Rebuild assets

**Always rebuild videos before the deck** — the deck embeds the video files.

Decision:

| What changed | Rebuild |
|---|---|
| `generate_demo_videos.py` | Both videos + deck |
| `generate_presentation.py` | Deck only |
| `wiki_query.py` | UI demo video + deck |
| `skills/**` or commands | Terminal demo video + deck |

Commands (run from repo root):

| Task | Command |
|------|---------|
| Both videos | `cd presentation && python generate_demo_videos.py` |
| Terminal only | `cd presentation && python generate_demo_videos.py --terminal` |
| UI only | `cd presentation && python generate_demo_videos.py --ui` |
| Deck only | `cd presentation && python generate_presentation.py --pptx` |
| Everything | `cd presentation && python generate_demo_videos.py && python generate_presentation.py --pptx` |

Stop and report any non-zero exit code.

---

## Step 3: Verify

```
ls -lh presentation/terminal-demo.mp4 presentation/ui-demo.mp4 presentation/llm-wiki-deck.pptx
```

Confirm both videos are embedded in the deck:
```
python3 -c "
from pptx import Presentation
p = Presentation('presentation/llm-wiki-deck.pptx')
media = [s.name for sl in p.slides for s in sl.shapes if s.shape_type == 16]
print('Embedded media:', media)
"
```

Expected: `Embedded media: ['terminal-demo.mp4', 'ui-demo.mp4']`

---

## Output

Report what was rebuilt (file sizes, slide count, embedded media), list any manual steps remaining for Keynote/Google Slides, and remind the user to run **Sync Docs** to update README and copilot-instructions.

See `skills/repo-maintenance/regenerate-presentation/SKILL.md` for full guidance and `skills/repo-maintenance/regenerate-presentation/references/rebuild-checklist.md` for verification steps.

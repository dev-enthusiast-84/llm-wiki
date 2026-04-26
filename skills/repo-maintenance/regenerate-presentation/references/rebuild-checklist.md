# Rebuild Checklist

Step-by-step verification for `/regenerate-presentation`.

---

## Pre-run

- [ ] Running from the repo root (check: `ls presentation/generate_presentation.py`)
- [ ] `python-pptx` is installed: `python3 -c "from pptx import Presentation"`
- [ ] `moviepy` and `Pillow` are installed: `python3 -c "from moviepy import ImageClip; from PIL import Image"`
- [ ] `presentation/generate_demo_videos.py` and `presentation/generate_presentation.py` exist

---

## Step 1 — Change Detection

- [ ] `git diff --name-only HEAD` and `git status --short` both run
- [ ] Changed paths grouped into: `video-script`, `deck-script`, `ui-code`, `skill-commands`
- [ ] Decision announced before any script runs
- [ ] If no relevant paths changed: reported "Nothing to rebuild" and stopped

---

## Step 2 — Video Rebuild (if needed)

- [ ] Video scripts run **before** the deck script
- [ ] Terminal demo rebuilt when: `generate_demo_videos.py` changed OR skill/command files changed
- [ ] UI demo rebuilt when: `generate_demo_videos.py` changed OR `wiki_query.py` changed
- [ ] Script exited with code 0 — no errors
- [ ] File size > 0 for each rebuilt video

---

## Step 3 — Deck Rebuild

- [ ] `generate_presentation.py --pptx` ran after videos (if videos were rebuilt)
- [ ] Script exited with code 0
- [ ] `presentation/llm-wiki-deck.pptx` has a current modification timestamp

---

## Step 4 — Verification

- [ ] `ls -lh presentation/*.mp4 presentation/*.pptx` shows non-zero sizes
- [ ] Embedded media check passes:
  ```
  python3 -c "
  from pptx import Presentation
  p = Presentation('presentation/llm-wiki-deck.pptx')
  media = [s.name for sl in p.slides for s in sl.shapes if s.shape_type == 16]
  print('Embedded media:', media)
  "
  ```
  Expected: `Embedded media: ['terminal-demo.mp4', 'ui-demo.mp4']`
- [ ] If a video is missing from the embedded list: verify the file exists, then rerun deck generator

---

## Step 5 — Optional Formats

- [ ] Keynote: `python generate_presentation.py --keynote` run (opens Keynote)
  - [ ] Manual export done: Keynote → File → Export To → Keynote → `llm-wiki-deck.key`
- [ ] Google Slides: `python generate_presentation.py --slides` run (or manual upload)

---

## Post-run

- [ ] Results Summary block emitted with correct file sizes
- [ ] Next step reminder issued: run `/sync-docs`
- [ ] No stale `.pptx` or `.mp4` files left from a previous version (check `ls -lh presentation/`)

---

## Common Issues

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: moviepy` | moviepy not installed | `pip install moviepy` |
| `ModuleNotFoundError: pptx` | python-pptx not installed | `pip install python-pptx` |
| Embedded media list is empty | Videos not found at expected path when deck was built | Rebuild videos first, then deck |
| Video file size is 0 KB | Script failed silently | Re-run script with `python generate_demo_videos.py --terminal` and check stderr |
| Keynote shows 0 documents | macOS Sequoia AppleScript restriction | Use manual File → Export To → Keynote in the Keynote UI |

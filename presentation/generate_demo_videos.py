"""
LLM Wiki Demo Video Generator
Generates terminal-demo.mp4 and ui-demo.mp4.

terminal-demo.mp4:
  · Claude Code CLI: /compile-papers, /sync-wiki, /audit-wiki
  · GitHub Copilot Chat equivalent workflow

ui-demo.mp4:
  · Settings → Wiki confirmation → Happy-path query → Error scenarios

Run:
    python generate_demo_videos.py             # both videos
    python generate_demo_videos.py --terminal  # terminal only
    python generate_demo_videos.py --ui        # UI only

Requirements: pip install moviepy pillow numpy
"""

from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips

HERE        = Path(__file__).parent
TERM_OUT    = HERE / "terminal-demo.mp4"
UI_OUT      = HERE / "ui-demo.mp4"

W, H = 1280, 720
FPS  = 24

MONO_FONT  = "/System/Library/Fonts/Menlo.ttc"
SANS_FONT  = "/System/Library/Fonts/Helvetica.ttc"


# ── Color palettes ─────────────────────────────────────────────────────────────

T = SimpleNamespace(
    BG       = (26,  27,  38),
    TITLE_BG = (20,  20,  30),
    BORDER   = (50,  50,  70),
    WHITE    = (220, 220, 230),
    DIM      = ( 90,  90, 120),
    GREEN    = ( 80, 200, 100),
    CYAN     = ( 60, 190, 210),
    BLUE     = ( 90, 160, 255),
    YELLOW   = (250, 200,  60),
    ORANGE   = (200, 110,  80),
    PURPLE   = (155, 105, 235),
    RED      = (230,  80,  80),
    GREY     = (120, 120, 150),
)

U = SimpleNamespace(
    BG       = (248, 249, 252),
    SIDEBAR  = (240, 242, 248),
    WHITE    = (255, 255, 255),
    ACCENT   = (255,  75,  75),
    BLUE     = ( 14, 105, 218),
    TEXT     = ( 14,  17,  23),
    DIM      = (100, 108, 120),
    BORDER   = (210, 215, 225),
    SUCCESS  = ( 21, 153,  87),
    WARNING  = (200, 120,   0),
    ERROR    = (185,  40,  40),
    INFO     = ( 14, 100, 195),
)

# Obsidian dark theme
OBS = SimpleNamespace(
    BG       = ( 30,  30,  46),   # canvas background
    SIDEBAR  = ( 22,  22,  34),   # left file pane
    CHROME   = ( 18,  18,  28),   # title bar
    BORDER   = ( 55,  55,  85),
    NODE     = (124, 106, 245),   # default node (purple)
    NODE_HI  = (167, 139, 250),   # selected/highlighted node
    EDGE     = ( 75,  75, 115),   # link line
    TEXT     = (220, 220, 230),
    DIM      = ( 95,  95, 135),
    GREEN    = ( 52, 211, 153),
    CYAN     = ( 56, 189, 248),
    YELLOW   = (250, 200,  60),
)


# ── Font helpers ───────────────────────────────────────────────────────────────

def _mono(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(MONO_FONT, size)
    except Exception:
        return ImageFont.load_default()


def _sans(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    try:
        idx = 1 if bold else 0
        return ImageFont.truetype(SANS_FONT, size, index=idx)
    except Exception:
        return ImageFont.load_default()


# ── Low-level drawing helpers ──────────────────────────────────────────────────

def _rrect(draw: ImageDraw.Draw, x, y, w, h, fill, radius=8, outline=None, outline_w=1):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill,
                           outline=outline, width=outline_w)


def _text(draw: ImageDraw.Draw, text: str, x, y, font, color):
    draw.text((x, y), text, font=font, fill=color)


def _clip(img: Image.Image, duration: float) -> ImageClip:
    return ImageClip(np.array(img), duration=duration)


# ── Terminal screen builder ───────────────────────────────────────────────────

CHROME_H   = 38
PAD_X      = 22
PAD_Y      = CHROME_H + 16
LINE_H     = 22
MONO_SIZE  = 15

MONO_S  = _mono(MONO_SIZE)
MONO_SM = _mono(13)


def _term_base() -> tuple[Image.Image, ImageDraw.Draw]:
    img  = Image.new("RGB", (W, H), T.BG)
    draw = ImageDraw.Draw(img)
    # window chrome
    draw.rectangle([0, 0, W, CHROME_H], fill=T.TITLE_BG)
    draw.rectangle([0, CHROME_H, W, CHROME_H + 1], fill=T.BORDER)
    for cx, col in [(16, (255,  95,  86)),
                    (36, (255, 189,  46)),
                    (56, ( 39, 201,  63))]:
        draw.ellipse([cx - 7, CHROME_H // 2 - 7, cx + 7, CHROME_H // 2 + 7], fill=col)
    _text(draw, "llm-wiki — zsh — 120×35",
          W // 2 - 90, 10, _mono(13), T.GREY)
    return img, draw


def _render_terminal(lines: list[list[tuple[str, tuple]]]) -> Image.Image:
    """
    Render a list of lines onto the terminal background.
    Each line is [(text_segment, color), ...].
    """
    img, draw = _term_base()
    y = PAD_Y
    for line_parts in lines:
        x = PAD_X
        for seg, color in line_parts:
            _text(draw, seg, x, y, MONO_S, color)
            bbox = MONO_S.getbbox(seg) or (0, 0, 0, 0)
            x += bbox[2] - bbox[0]
        y += LINE_H
    return img


def _term_clip(lines, duration=3.0):
    return _clip(_render_terminal(lines), duration)


def _PROMPT():
    return [("user", T.GREEN), ("@", T.DIM), ("llm-wiki", T.CYAN),
            ("  ~/llm-wiki  ", T.DIM), ("% ", T.WHITE)]


# ── Terminal scene builders ────────────────────────────────────────────────────

def _title_card(title: str, subtitle: str, color, duration=2.5) -> ImageClip:
    img  = Image.new("RGB", (W, H), T.BG)
    draw = ImageDraw.Draw(img)
    BIG  = _sans(52, bold=True)
    MED  = _sans(26)
    draw.rectangle([0, H // 2 - 4, W, H // 2 + 4], fill=color)
    w1 = BIG.getbbox(title)[2] if BIG.getbbox(title) else len(title) * 30
    w2 = MED.getbbox(subtitle)[2] if MED.getbbox(subtitle) else len(subtitle) * 15
    draw.text((W // 2 - w1 // 2, H // 2 - 70), title,  font=BIG, fill=T.WHITE)
    draw.text((W // 2 - w2 // 2, H // 2 + 28), subtitle, font=MED, fill=color)
    return _clip(img, duration)


def _scene_startup() -> ImageClip:
    lines = [
        _PROMPT() + [("claude", T.WHITE)],
        [],
        [("  ╭─────────────────────────────────────────────────────╮", T.BORDER)],
        [("  │  ", T.BORDER), ("✻  Welcome to Claude Code", T.ORANGE), ("                        │", T.BORDER)],
        [("  │  ", T.BORDER), ("   Type /help for available commands", T.GREY), ("        │", T.BORDER)],
        [("  │  ", T.BORDER), ("   Model: claude-sonnet-4-6", T.DIM), ("                  │", T.BORDER)],
        [("  ╰─────────────────────────────────────────────────────╯", T.BORDER)],
        [],
        [("  > ", T.PURPLE)],
    ]
    return _term_clip(lines, duration=2.5)


def _scene_compile() -> ImageClip:
    lines = [
        _PROMPT() + [("claude", T.WHITE)],
        [],
        [("  > ", T.PURPLE), ("/compile-papers", T.ORANGE)],
        [],
        [("  ● ", T.CYAN), ("Reading 9 sources and extracting concepts...", T.WHITE)],
        [],
        [("  ✓  Compile Papers", T.GREEN), (" — complete  ", T.WHITE), ("2026-04-25", T.DIM)],
        [],
        [("  ● ", T.CYAN), ("Sources processed: ", T.WHITE), ("9", T.GREEN)],
        [("     ✓ ", T.GREEN), ("Attention.pdf  FMs.pdf  gpt3.pdf  SLL.pdf  bert-overview.txt", T.WHITE)],
        [("     ✓ ", T.GREEN), ("rlhf-overview.docx  transformer-architecture.html  RNN and LSTM Basics.pptx", T.WHITE)],
        [("     ⊘ ", T.DIM), ("llm-spreadsheet-tasks.xlsx", T.WHITE), ("  (benchmark data — no entities)", T.DIM)],
        [],
        [("  ● ", T.CYAN), ("Entity pages created: ", T.WHITE), ("37", T.GREEN)],
        [("     ", T.DIM), ("wiki/transformer.md  wiki/self-attention.md  wiki/bert.md  wiki/gpt-3.md", T.DIM)],
        [("     ", T.DIM), ("wiki/rlhf.md  wiki/foundation-model.md  wiki/scaling-laws.md  wiki/lstm.md", T.DIM)],
        [("     ", T.DIM), ("wiki/small-language-model.md  ...  (28 more)", T.DIM)],
        [],
        [("  ● ", T.CYAN), ("wiki/index.md", T.WHITE), ("  — updated ", T.DIM), ("(37 new entries)", T.GREEN)],
        [("  ● ", T.CYAN), ("wiki/log.md", T.WHITE), ("    — updated ", T.DIM), ("(9 new rows)", T.GREEN)],
        [],
        [("  ⚠ ", T.YELLOW), ("Issues: ", T.WHITE), ("none", T.GREEN)],
        [("  → ", T.DIM), ('Next step:  git add wiki/ && git commit -m "Compile wiki: 9 sources, 37 pages"', T.DIM)],
    ]
    return _term_clip(lines, duration=7.0)


def _scene_sync() -> ImageClip:
    lines = [
        [],
        [("  > ", T.PURPLE), ("/sync-wiki", T.ORANGE)],
        [],
        [("  ● ", T.CYAN), ("Checking /raw for new sources...", T.WHITE)],
        [],
        [("  ✓  Sync Wiki", T.GREEN), (" — complete  ", T.WHITE), ("2026-04-25", T.DIM)],
        [],
        [("  ● ", T.CYAN), ("New sources processed: ", T.WHITE), ("0", T.GREEN)],
        [("     ⊘ ", T.DIM), ("Attention.pdf  FMs.pdf  gpt3.pdf  SLL.pdf", T.DIM), ("  (skipped — already in log.md)", T.DIM)],
        [("     ⊘ ", T.DIM), ("bert-overview.txt  rlhf-overview.docx  transformer-architecture.html", T.DIM)],
        [("     ⊘ ", T.DIM), ("RNN and LSTM Basics.pptx  llm-spreadsheet-tasks.xlsx", T.DIM)],
        [],
        [("  ● ", T.CYAN), ("Entity pages created: ", T.WHITE), ("0", T.GREEN)],
        [("  ● ", T.CYAN), ("Entity pages updated: ", T.WHITE), ("0", T.GREEN)],
        [],
        [("  ● ", T.CYAN), ("wiki/index.md", T.WHITE), ("  — no changes", T.DIM)],
        [("  ● ", T.CYAN), ("wiki/log.md", T.WHITE), ("    — no changes", T.DIM)],
        [],
        [("  → ", T.DIM), ("Next step: drop new files into /raw and re-run /sync-wiki", T.DIM)],
    ]
    return _term_clip(lines, duration=5.5)


def _scene_audit() -> ImageClip:
    lines = [
        [],
        [("  > ", T.PURPLE), ("/audit-wiki", T.ORANGE)],
        [],
        [("  ● ", T.CYAN), ("Auditing 37 wiki pages...", T.WHITE)],
        [],
        [("  ✓  Audit Wiki", T.GREEN), (" — complete  ", T.WHITE), ("2026-04-25", T.DIM)],
        [],
        [("  ● ", T.CYAN), ("Findings:", T.WHITE)],
        [("     Orphan pages:   ", T.DIM), ("0", T.GREEN), ("  (every page has inbound links)", T.DIM)],
        [("     Missing pages:  ", T.DIM), ("0", T.GREEN), ("  (all [[links]] resolve correctly)", T.DIM)],
        [("     Contradictions: ", T.DIM), ("0", T.GREEN)],
        [("     Stale claims:   ", T.DIM), ("0", T.GREEN)],
        [],
        [("  ● ", T.CYAN), ("Auto-fixed: ", T.WHITE), ("0 issues", T.GREEN)],
        [("  ! ", T.YELLOW), ("Needs manual review: ", T.WHITE), ("0 issues", T.GREEN)],
        [],
        [("  ● ", T.CYAN), ("wiki/index.md", T.WHITE), ("  — no changes", T.DIM)],
        [("  ● ", T.CYAN), ("wiki/log.md", T.WHITE), ("    — unchanged (audit adds no log rows)", T.DIM)],
        [],
        [("  → ", T.DIM), ("Next step: wiki is healthy — commit and continue", T.DIM)],
    ]
    return _term_clip(lines, duration=6.5)


def _scene_copilot() -> ImageClip:
    img  = Image.new("RGB", (W, H), (30, 30, 40))
    draw = ImageDraw.Draw(img)

    # VS Code-like header
    draw.rectangle([0, 0, W, 36], fill=(37, 37, 38))
    draw.rectangle([0, 36, W, 37], fill=(0, 122, 204))
    TITLE = _sans(13)
    draw.text((W // 2 - 80, 10), "llm-wiki — VS Code", font=TITLE, fill=(204, 204, 204))

    # Copilot panel
    panel_x, panel_y = 320, 37
    panel_w = W - panel_x - 4
    draw.rectangle([panel_x, panel_y, W - 4, H - 4], fill=(37, 37, 38))
    draw.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + 40], fill=(45, 45, 50))

    HDR = _sans(14, bold=True)
    draw.text((panel_x + 14, panel_y + 12), "GitHub Copilot Chat", font=HDR, fill=(200, 200, 210))
    draw.rectangle([panel_x + panel_w - 90, panel_y + 10, panel_x + panel_w - 14, panel_y + 30],
                   fill=(0, 122, 204), outline=None)
    draw.text((panel_x + panel_w - 84, panel_y + 13), "New Chat", font=_sans(12), fill=(255, 255, 255))

    CHAT_FONT  = _sans(14)
    CHAT_BOLD  = _sans(14, bold=True)
    CODE_FONT  = _mono(13)

    lines = [
        (panel_x + 14, panel_y + 50,  "You",         CHAT_BOLD,  (0, 122, 204)),
        (panel_x + 14, panel_y + 68,  "@workspace /Compile Papers to Wiki", CODE_FONT, (200, 200, 210)),
        (panel_x + 14, panel_y + 100, "GitHub Copilot", CHAT_BOLD, (16, 185, 129)),
        (panel_x + 14, panel_y + 118, "● Scanning /raw for source files...", CHAT_FONT, (100, 100, 120)),
        (panel_x + 14, panel_y + 136, "  Found 9 source files", CHAT_FONT, (140, 140, 160)),
        (panel_x + 14, panel_y + 158, "  ✓ wiki/transformer.md  ✓ wiki/bert.md  ✓ wiki/lstm.md", CHAT_FONT, (80, 200, 100)),
        (panel_x + 14, panel_y + 176, "  ✓ wiki/gpt-3.md  ... (33 more pages)", CHAT_FONT, (80, 200, 100)),
        (panel_x + 14, panel_y + 200, "✓ Compiled 37 entity pages", CHAT_BOLD, (80, 200, 100)),
        # Second exchange: Launch Wiki UI
        (panel_x + 14, panel_y + 234, "You",         CHAT_BOLD,  (0, 122, 204)),
        (panel_x + 14, panel_y + 252, "@workspace /Launch Wiki UI", CODE_FONT, (200, 200, 210)),
        (panel_x + 14, panel_y + 284, "GitHub Copilot", CHAT_BOLD, (16, 185, 129)),
        (panel_x + 14, panel_y + 302, "● Checking dependencies (streamlit, anthropic)...", CHAT_FONT, (100, 100, 120)),
        (panel_x + 14, panel_y + 320, "  ✓ All dependencies present", CHAT_FONT, (80, 200, 100)),
        (panel_x + 14, panel_y + 342, "  ✓ Wiki: 37 pages available", CHAT_FONT, (80, 200, 100)),
        (panel_x + 14, panel_y + 366, "✓ Streamlit app running → http://localhost:8501", CHAT_BOLD, (80, 200, 100)),
    ]
    for x, y, text, font, color in lines:
        draw.text((x, y), text, font=font, fill=color)

    # Sidebar (file explorer hint)
    draw.rectangle([0, 37, 320, H], fill=(37, 37, 38))
    draw.rectangle([0, 37, 320, 77], fill=(45, 45, 50))
    draw.text((14, 53), "EXPLORER", font=_sans(11, bold=True), fill=(187, 187, 187))
    for i, fname in enumerate(["wiki/", "  transformer.md", "  self-attention.md",
                                "  bert.md", "  gpt-3.md", "  rlhf.md",
                                "  scaling-laws.md", "  index.md", "  log.md"]):
        draw.text((14, 84 + i * 22), fname, font=_mono(12), fill=(140, 140, 160))

    return _clip(img, duration=6.0)


# ── Obsidian graph data ───────────────────────────────────────────────────────
# Each node: (x_offset, y_offset, radius, color_key, short_label)
# Colour keys: "hi"=selected-purple, "def"=default-purple, "acc"=cyan, "grn"=green, "dim"=muted
_OBS_NODES: dict[str, tuple[int, int, int, str, str]] = {
    # Core transformer architecture
    "transformer":              (390, 300, 16, "hi",  "transformer"),
    "self-attention":           (280, 220, 12, "def", "self-attention"),
    "multi-head-attention":     (295, 148, 11, "def", "multi-head"),
    "positional-encoding":      (185, 280, 10, "dim", "pos-encoding"),
    "feed-forward-network":     (250, 390, 10, "dim", "feed-forward"),
    "layer-normalization":      (170, 378,  9, "dim", "layer-norm"),
    # BERT family
    "bert":                     (110, 235, 13, "acc", "bert"),
    "masked-language-model":    ( 42, 185, 10, "dim", "mask-lm"),
    "next-sentence-prediction": ( 30, 305,  9, "dim", "nsp"),
    "wordpiece":                ( 78, 395,  9, "dim", "wordpiece"),
    "pre-training":             (220, 128,  9, "dim", "pre-training"),
    "self-supervised":          (110, 110,  8, "dim", "self-supervised"),
    # GPT / language models
    "gpt-3":                    (570, 210, 13, "acc", "gpt-3"),
    "in-context-learning":      (655, 148, 10, "grn", "in-context"),
    "autoregressive":           (640, 298,  9, "dim", "autoregressive"),
    # Scaling & emergence
    "scaling-laws":             (490, 130, 12, "grn", "scaling-laws"),
    "emergence":                (585, 105,  9, "grn", "emergence"),
    "foundation-model":         (390, 115, 11, "def", "foundation-model"),
    # RLHF / safety
    "rlhf":                     (548, 415, 12, "def", "rlhf"),
    "reward-model":             (632, 490, 10, "dim", "reward-model"),
    "hallucination":            (490, 495,  9, "dim", "hallucination"),
    "instructgpt":              (638, 385,  9, "dim", "instructgpt"),
    # Pre-transformer (RNN/LSTM cluster)
    "recurrent-neural-network": ( 90, 430, 11, "dim", "rnn"),
    "lstm":                     (185, 470, 12, "acc", "lstm"),
    "vanishing-gradient":       ( 78, 510,  8, "dim", "vanishing-grad"),
    # Agentic / small models
    "small-language-model":     (730, 340,  9, "grn", "small-LM"),
}

_OBS_EDGES: list[tuple[str, str]] = [
    ("transformer", "self-attention"),
    ("transformer", "multi-head-attention"),
    ("transformer", "positional-encoding"),
    ("transformer", "feed-forward-network"),
    ("transformer", "layer-normalization"),
    ("self-attention", "multi-head-attention"),
    ("bert", "transformer"),
    ("bert", "masked-language-model"),
    ("bert", "next-sentence-prediction"),
    ("bert", "wordpiece"),
    ("bert", "pre-training"),
    ("pre-training", "self-supervised"),
    ("masked-language-model", "self-supervised"),
    ("gpt-3", "transformer"),
    ("gpt-3", "in-context-learning"),
    ("gpt-3", "autoregressive"),
    ("gpt-3", "scaling-laws"),
    ("scaling-laws", "emergence"),
    ("scaling-laws", "foundation-model"),
    ("foundation-model", "bert"),
    ("foundation-model", "gpt-3"),
    ("foundation-model", "pre-training"),
    ("rlhf", "reward-model"),
    ("rlhf", "hallucination"),
    ("rlhf", "instructgpt"),
    ("instructgpt", "gpt-3"),
    ("reward-model", "gpt-3"),
    ("recurrent-neural-network", "transformer"),
    ("recurrent-neural-network", "lstm"),
    ("lstm", "vanishing-gradient"),
    ("foundation-model", "hallucination"),
    ("scaling-laws", "small-language-model"),
]

_OBS_SIDEBAR_W = 228
_OBS_CHROME_H  = 36


def _obsidian_base() -> tuple[Image.Image, ImageDraw.Draw]:
    img  = Image.new("RGB", (W, H), OBS.BG)
    draw = ImageDraw.Draw(img)

    # title bar
    draw.rectangle([0, 0, W, _OBS_CHROME_H], fill=OBS.CHROME)
    draw.rectangle([0, _OBS_CHROME_H, W, _OBS_CHROME_H + 1], fill=OBS.BORDER)
    _text(draw, "◇  llm-wiki  —  Obsidian", 14, 10, _mono(13), OBS.DIM)
    _text(draw, "Graph View", W - 115, 10, _sans(12, bold=True), OBS.NODE_HI)

    # left sidebar
    draw.rectangle([0, _OBS_CHROME_H + 1, _OBS_SIDEBAR_W, H], fill=OBS.SIDEBAR)
    draw.rectangle([_OBS_SIDEBAR_W, _OBS_CHROME_H + 1, _OBS_SIDEBAR_W + 1, H], fill=OBS.BORDER)

    _text(draw, "VAULT",    12, _OBS_CHROME_H + 14, _sans(10, bold=True), OBS.DIM)
    _text(draw, "llm-wiki", 12, _OBS_CHROME_H + 30, _sans(13, bold=True), OBS.TEXT)

    files = [
        ("wiki/",                     OBS.DIM),
        ("  transformer.md",          OBS.NODE_HI),
        ("  self-attention.md",       OBS.TEXT),
        ("  multi-head-attention.md", OBS.TEXT),
        ("  bert.md",                 OBS.CYAN),
        ("  gpt-3.md",                OBS.CYAN),
        ("  rlhf.md",                 OBS.TEXT),
        ("  scaling-laws.md",         OBS.GREEN),
        ("  positional-encoding.md",  OBS.DIM),
        ("  feed-forward-network.md", OBS.DIM),
        ("  layer-normalization.md",  OBS.DIM),
        ("  reward-model.md",         OBS.DIM),
        ("  in-context-learning.md",  OBS.DIM),
        ("  masked-language-model.md",OBS.DIM),
        ("  ... (21 more)",           OBS.DIM),
    ]
    for i, (fname, color) in enumerate(files):
        fy = _OBS_CHROME_H + 58 + i * 21
        if fy > H - 24:
            break
        if fname.strip().endswith(".md") and i == 1:
            draw.rectangle([0, fy - 2, _OBS_SIDEBAR_W, fy + 17], fill=(50, 38, 92))
        _text(draw, fname, 10, fy, _mono(11), color)

    return img, draw


def _scene_obsidian_app() -> ImageClip:
    """Obsidian desktop app window — vault open, transformer.md in the editor."""
    img  = Image.new("RGB", (W, H), OBS.BG)
    draw = ImageDraw.Draw(img)

    SIDE_W   = 222
    CHROME_H = 38
    RIBBON_W = 46
    STATUS_H = 26
    TAB_H    = 30

    # ── macOS window chrome ──────────────────────────────────────────
    draw.rectangle([0, 0, W, CHROME_H], fill=OBS.CHROME)
    for cx, col in [(18, (255, 95, 86)), (38, (255, 189, 46)), (58, (39, 201, 63))]:
        draw.ellipse([cx - 7, CHROME_H // 2 - 7, cx + 7, CHROME_H // 2 + 7], fill=col)
    title = "llm-wiki — Obsidian"
    tw = (_mono(13).getbbox(title) or (0, 0, 160, 0))[2]
    _text(draw, title, W // 2 - tw // 2, CHROME_H // 2 - 7, _mono(13), OBS.DIM)
    draw.rectangle([0, CHROME_H, W, CHROME_H + 1], fill=OBS.BORDER)

    # ── left sidebar ─────────────────────────────────────────────────
    draw.rectangle([0, CHROME_H + 1, SIDE_W, H - STATUS_H], fill=OBS.SIDEBAR)
    draw.rectangle([SIDE_W, CHROME_H + 1, SIDE_W + 1, H - STATUS_H], fill=OBS.BORDER)

    _text(draw, "VAULT", 12, CHROME_H + 14, _sans(10, bold=True), OBS.DIM)
    _text(draw, "◇  llm-wiki", 10, CHROME_H + 30, _sans(13, bold=True), OBS.NODE_HI)
    draw.rectangle([10, CHROME_H + 50, SIDE_W - 10, CHROME_H + 51], fill=OBS.BORDER)

    tree = [
        ("▾ wiki/",                  OBS.DIM,     False),
        ("    transformer.md",        OBS.NODE_HI, True),   # active
        ("    self-attention.md",     OBS.TEXT,    False),
        ("    multi-head-attention.md", OBS.TEXT,  False),
        ("    bert.md",               OBS.CYAN,    False),
        ("    gpt-3.md",              OBS.CYAN,    False),
        ("    rlhf.md",               OBS.TEXT,    False),
        ("    scaling-laws.md",       OBS.GREEN,   False),
        ("    positional-encoding.md",OBS.DIM,     False),
        ("    feed-forward-network.md", OBS.DIM,   False),
        ("    layer-normalization.md",OBS.DIM,     False),
        ("    reward-model.md",       OBS.DIM,     False),
        ("    in-context-learning.md",OBS.DIM,     False),
        ("    masked-language-model.md", OBS.DIM,  False),
        ("    … 20 more pages",       OBS.DIM,     False),
    ]
    for i, (fname, color, active) in enumerate(tree):
        fy = CHROME_H + 58 + i * 22
        if fy > H - STATUS_H - 16:
            break
        if active:
            draw.rectangle([0, fy - 2, SIDE_W, fy + 18], fill=(50, 36, 92))
        _text(draw, fname, 10, fy, _mono(11), color)

    # ── tab bar ───────────────────────────────────────────────────────
    EX = SIDE_W + 1
    EW = W - SIDE_W - RIBBON_W - 1
    draw.rectangle([EX, CHROME_H + 1, W - RIBBON_W, CHROME_H + TAB_H + 1], fill=OBS.CHROME)
    # active tab
    draw.rectangle([EX, CHROME_H + 1, EX + 176, CHROME_H + TAB_H + 1], fill=OBS.BG)
    _text(draw, "transformer.md  ✕", EX + 12, CHROME_H + 8, _sans(12), OBS.NODE_HI)
    draw.rectangle([EX, CHROME_H + TAB_H, EX + 176, CHROME_H + TAB_H + 2], fill=OBS.NODE_HI)
    draw.rectangle([EX, CHROME_H + TAB_H + 1, W - RIBBON_W, CHROME_H + TAB_H + 2], fill=OBS.BORDER)

    # ── editor content ────────────────────────────────────────────────
    CX = EX + 52          # left margin of prose
    cy = CHROME_H + TAB_H + 32

    # H1
    _text(draw, "# Transformer", CX, cy, _sans(22, bold=True), OBS.TEXT)
    cy += 36
    _text(draw, "Neural architecture based entirely on self-attention,", CX, cy, _sans(13), OBS.DIM)
    cy += 19
    _text(draw, "without recurrence or convolution.", CX, cy, _sans(13), OBS.DIM)
    cy += 34

    # H2 Summary
    _text(draw, "## Summary", CX, cy, _sans(16, bold=True), OBS.TEXT)
    cy += 26
    summary_lines = [
        "Introduced by Vaswani et al. (2017), the Transformer replaced recurrent",
        "networks with multi-head self-attention, enabling massively parallel training",
        "and forming the foundation of every modern large language model.",
    ]
    for line in summary_lines:
        _text(draw, line, CX, cy, _sans(13), OBS.TEXT)
        cy += 19
    cy += 18

    # H2 Related Concepts
    _text(draw, "## Related Concepts", CX, cy, _sans(16, bold=True), OBS.TEXT)
    cy += 26
    links = [
        ("[[self-attention]]",        " — core scaled dot-product mechanism"),
        ("[[multi-head-attention]]",  " — parallel attention heads"),
        ("[[positional-encoding]]",   " — injects sequence order"),
        ("[[feed-forward-network]]",  " — per-token MLP sublayer"),
        ("[[layer-normalization]]",   " — stabilises deep residual stacks"),
        ("[[bert]]",                  " — encoder-only descendant"),
        ("[[gpt-3]]",                 " — decoder-only descendant"),
    ]
    for bracket, rest in links:
        _text(draw, "–  ", CX, cy, _sans(13), OBS.DIM)
        _text(draw, bracket, CX + 18, cy, _sans(13), OBS.NODE_HI)
        bw = (_sans(13).getbbox(bracket) or (0, 0, 0, 0))[2]
        _text(draw, rest, CX + 18 + bw, cy, _sans(13), OBS.DIM)
        cy += 21
    cy += 16

    # H2 Sources
    _text(draw, "## Sources", CX, cy, _sans(16, bold=True), OBS.TEXT)
    cy += 24
    _text(draw, 'Vaswani et al. — "Attention Is All You Need" (NeurIPS 2017)',
          CX, cy, _sans(13), OBS.DIM)

    # ── right ribbon ──────────────────────────────────────────────────
    RX = W - RIBBON_W
    draw.rectangle([RX, CHROME_H + 1, W, H - STATUS_H], fill=OBS.CHROME)
    draw.rectangle([RX, CHROME_H + 1, RX + 1, H - STATUS_H], fill=OBS.BORDER)
    ribbon = [("📁", OBS.DIM), ("🔍", OBS.DIM), ("◎", OBS.NODE_HI), ("≡", OBS.DIM)]
    for i, (icon, color) in enumerate(ribbon):
        _text(draw, icon, RX + 10, CHROME_H + 18 + i * 44, _sans(15), color)
    # "graph" label under the graph icon
    _text(draw, "graph", RX + 4, CHROME_H + 18 + 2 * 44 + 18, _sans(9), OBS.NODE_HI)

    # ── status bar ────────────────────────────────────────────────────
    draw.rectangle([0, H - STATUS_H, W, H], fill=OBS.CHROME)
    draw.rectangle([0, H - STATUS_H, W, H - STATUS_H + 1], fill=OBS.BORDER)
    _text(draw, "  37 notes  ·  252 links resolved  ·  llm-wiki",
          12, H - STATUS_H + 6, _sans(11), OBS.DIM)
    _text(draw, "Reading mode  ·  transformer.md",
          W - 240, H - STATUS_H + 6, _sans(11), OBS.DIM)

    return _clip(img, duration=7.0)


def _scene_obsidian_graph() -> ImageClip:
    """Rendered Obsidian graph view showing the wiki knowledge graph."""
    img, draw = _obsidian_base()

    GX = _OBS_SIDEBAR_W + 28   # graph canvas left edge
    GY = _OBS_CHROME_H + 18    # graph canvas top edge

    node_colors = {
        "hi":  OBS.NODE_HI,
        "def": OBS.NODE,
        "acc": OBS.CYAN,
        "grn": OBS.GREEN,
        "dim": OBS.DIM,
    }

    # resolve absolute positions
    pos: dict[str, tuple[int, int]] = {
        k: (GX + ox, GY + oy)
        for k, (ox, oy, *_) in _OBS_NODES.items()
    }

    # draw edges first (behind nodes)
    for src, dst in _OBS_EDGES:
        if src in pos and dst in pos:
            draw.line([*pos[src], *pos[dst]], fill=OBS.EDGE, width=1)

    # draw nodes with glow layers
    label_font = _mono(10)
    for key, (ox, oy, r, ck, label) in _OBS_NODES.items():
        nx, ny = pos[key]
        color   = node_colors[ck]

        # outer glow
        gc = tuple(max(0, min(255, int(c * 0.22))) for c in color)
        draw.ellipse([nx - r*2 - 2, ny - r*2 - 2, nx + r*2 + 2, ny + r*2 + 2], fill=gc)
        # mid glow
        mc = tuple(max(0, min(255, int(c * 0.48))) for c in color)
        draw.ellipse([nx - r - 4, ny - r - 4, nx + r + 4, ny + r + 4], fill=mc)
        # core
        draw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=color)

        # label below node
        bb = label_font.getbbox(label)
        lw = (bb[2] - bb[0]) if bb else len(label) * 7
        _text(draw, label, nx - lw // 2, ny + r + 3, label_font, OBS.TEXT)

    # stats badge (bottom-left of graph area)
    bx, by = GX, H - 68
    _rrect(draw, bx, by, 260, 50, OBS.CHROME, radius=8, outline=OBS.BORDER)
    _text(draw, "37 nodes  ·  252 links", bx + 12, by + 8,  _sans(12, bold=True), OBS.NODE_HI)
    _text(draw, "Graph view  ·  scroll to zoom  ·  drag to pan",
          bx + 12, by + 28, _sans(11), OBS.DIM)

    # "selected node" info panel (top-right of graph area)
    px, py, pw = W - 230, _OBS_CHROME_H + 10, 218
    _rrect(draw, px, py, pw, 148, OBS.CHROME, radius=8, outline=OBS.BORDER)
    _text(draw, "transformer.md",   px + 12, py + 10, _sans(13, bold=True), OBS.NODE_HI)
    _text(draw, "18 backlinks  ·  7 outlinks", px + 12, py + 30, _sans(11), OBS.DIM)
    draw.rectangle([px + 12, py + 48, px + pw - 12, py + 49], fill=OBS.BORDER)
    _text(draw, "Linked from:", px + 12, py + 57, _sans(11, bold=True), OBS.DIM)
    for i, lk in enumerate(["bert.md", "gpt-3.md", "foundation-model.md",
                             "scaling-laws.md", "... (14 more)"]):
        _text(draw, "  · " + lk, px + 12, py + 74 + i * 15, _mono(10), OBS.TEXT)

    return _clip(img, duration=8.0)


def generate_terminal_demo(output: Path = TERM_OUT) -> Path:
    """Generate the terminal skills demo video."""
    print("  Generating terminal demo...")
    clips = [
        _title_card("Terminal Skills Demo",
                    "Claude Code CLI  ·  GitHub Copilot", T.ORANGE),
        _scene_startup(),
        _scene_compile(),
        _scene_sync(),
        _scene_audit(),
        _title_card("GitHub Copilot Chat",
                    "Same workflow, different tool", T.BLUE, duration=1.8),
        _scene_copilot(),
        _title_card("Obsidian Vault",
                    "Open wiki as a vault  ·  explore the knowledge graph", T.PURPLE, duration=2.2),
        _scene_obsidian_app(),
        _title_card("Graph View",
                    "37 nodes  ·  252 links  ·  fully interconnected", T.PURPLE, duration=1.8),
        _scene_obsidian_graph(),
    ]
    video = concatenate_videoclips(clips)
    video.write_videofile(str(output), fps=FPS, codec="libx264",
                          audio=False, logger=None,
                          ffmpeg_params=["-crf", "23", "-preset", "fast"])
    print(f"  ✓ terminal-demo.mp4 ({output.stat().st_size // 1024} KB)")
    return output


# ── UI screen builder ─────────────────────────────────────────────────────────

SIDEBAR_W = 240
MAIN_X    = SIDEBAR_W + 1
MAIN_W    = W - MAIN_X
HEADER_H  = 44


def _ui_base(title="LLM Wiki Query") -> tuple[Image.Image, ImageDraw.Draw]:
    img  = Image.new("RGB", (W, H), U.BG)
    draw = ImageDraw.Draw(img)
    # header
    draw.rectangle([0, 0, W, HEADER_H], fill=U.WHITE)
    draw.rectangle([0, HEADER_H, W, HEADER_H + 1], fill=U.BORDER)
    draw.text((16, 12), title, font=_sans(18, bold=True), fill=U.TEXT)
    draw.text((W - 120, 14), "streamlit", font=_sans(13), fill=(255, 75, 75))
    # sidebar
    draw.rectangle([0, HEADER_H + 1, SIDEBAR_W, H], fill=U.SIDEBAR)
    draw.rectangle([SIDEBAR_W, HEADER_H + 1, SIDEBAR_W + 1, H], fill=U.BORDER)
    # sidebar content
    draw.text((14, HEADER_H + 16), "Navigation", font=_sans(12, bold=True), fill=U.DIM)
    for i, (label, active) in enumerate([("Settings", False), ("Wiki", False), ("Chat", False)]):
        y = HEADER_H + 42 + i * 32
        color = U.ACCENT if active else U.DIM
        draw.text((14, y), f"  {label}", font=_sans(13), fill=color)
    return img, draw


def _input_field(draw, x, y, w, value, placeholder="", masked=False):
    _rrect(draw, x, y, w, 38, U.WHITE, radius=6, outline=U.BORDER, outline_w=1)
    txt = "•" * len(value) if masked and value else (value or placeholder)
    color = U.TEXT if value else U.DIM
    font = _sans(14)
    draw.text((x + 10, y + 10), txt[:48], font=font, fill=color)


def _button(draw, x, y, w, label, primary=True):
    bg = U.ACCENT if primary else U.SIDEBAR
    fg = U.WHITE if primary else U.TEXT
    _rrect(draw, x, y, w, 40, bg, radius=6)
    bw = _sans(14, bold=True).getbbox(label)[2] if _sans(14, bold=True).getbbox(label) else len(label) * 9
    draw.text((x + w // 2 - bw // 2, y + 11), label, font=_sans(14, bold=True), fill=fg)


def _alert(draw, x, y, w, text, kind="info"):
    colors = {"info": (U.INFO, (230, 240, 255)),
              "success": (U.SUCCESS, (225, 250, 235)),
              "warning": (U.WARNING, (255, 245, 220)),
              "error": (U.ERROR, (255, 230, 230))}
    fg, bg = colors.get(kind, colors["info"])
    _rrect(draw, x, y, w, 56, bg, radius=6, outline=fg, outline_w=1)
    icon = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✕"}.get(kind, "ℹ")
    draw.text((x + 12, y + 18), icon, font=_sans(16, bold=True), fill=fg)
    draw.text((x + 36, y + 16), text, font=_sans(13), fill=fg)


def _label(draw, x, y, text, bold=False, color=None):
    draw.text((x, y), text, font=_sans(13, bold=bold), fill=color or U.TEXT)


def _scene_settings() -> ImageClip:
    img, draw = _ui_base()
    MX = MAIN_X + 30
    MY = HEADER_H + 30

    draw.text((MX, MY), "Step 1 of 3 — Settings", font=_sans(12), fill=U.DIM)
    draw.text((MX, MY + 24), "Configure your session", font=_sans(22, bold=True), fill=U.TEXT)
    draw.rectangle([MX, MY + 56, MX + MAIN_W - 60, MY + 57], fill=U.BORDER)

    _label(draw, MX, MY + 70, "Claude Model ID", bold=True)
    _label(draw, MX, MY + 90, "Supported: claude-opus-4-7, claude-sonnet-4-6, claude-haiku-4-5", color=U.DIM)
    _input_field(draw, MX, MY + 112, MAIN_W - 60, "claude-sonnet-4-6")

    _label(draw, MX, MY + 172, "Anthropic API Key", bold=True)
    _label(draw, MX, MY + 192, "Starts with sk-ant-  ·  Never saved to disk", color=U.DIM)
    _input_field(draw, MX, MY + 214, MAIN_W - 60, "sk-ant-api03-aBcDeFg...", masked=True)

    _button(draw, MX, MY + 272, 200, "Save & Continue  →")

    return _clip(img, duration=5.0)


def _scene_settings_error() -> ImageClip:
    img, draw = _ui_base()
    MX = MAIN_X + 30
    MY = HEADER_H + 30

    draw.text((MX, MY + 24), "Configure your session", font=_sans(22, bold=True), fill=U.TEXT)
    _label(draw, MX, MY + 70, "Claude Model ID", bold=True)
    _input_field(draw, MX, MY + 92, MAIN_W - 60, "claude-sonnet-4-6")
    _label(draw, MX, MY + 150, "Anthropic API Key", bold=True)
    _input_field(draw, MX, MY + 172, MAIN_W - 60, "invalid-key-xyz", masked=False)
    _alert(draw, MX, MY + 230, MAIN_W - 60,
           "Invalid API key format. Key must start with sk-ant-", kind="error")
    _button(draw, MX, MY + 306, 200, "Save & Continue  →")

    return _clip(img, duration=4.5)


def _scene_empty_wiki() -> ImageClip:
    img, draw = _ui_base()
    MX = MAIN_X + 30
    MY = HEADER_H + 30

    draw.text((MX, MY + 24), "Step 2 of 3 — Wiki Overview", font=_sans(22, bold=True), fill=U.TEXT)
    _alert(draw, MX, MY + 80, MAIN_W - 60,
           "Wiki is empty — no entity pages found in wiki/", kind="warning")

    draw.text((MX, MY + 160), "To populate the wiki, run one of:", font=_sans(14), fill=U.TEXT)

    steps = [
        ("Claude Code CLI",   "/compile-papers"),
        ("GitHub Copilot",    "/Compile Papers to Wiki"),
    ]
    for i, (tool, cmd) in enumerate(steps):
        sy = MY + 195 + i * 48
        _rrect(draw, MX, sy, MAIN_W - 60, 40, U.WHITE, radius=6, outline=U.BORDER)
        draw.text((MX + 12, sy + 11), tool + ": ", font=_sans(13, bold=True), fill=U.DIM)
        w = _sans(13, bold=True).getbbox(tool + ": ")[2]
        draw.text((MX + 12 + w, sy + 11), cmd, font=_mono(13), fill=U.INFO)

    draw.text((MX, MY + 308), "Then reload this app.", font=_sans(13), fill=U.DIM)

    return _clip(img, duration=5.0)


def _scene_wiki_confirmation() -> ImageClip:
    img, draw = _ui_base()
    MX = MAIN_X + 30
    MY = HEADER_H + 30

    draw.text((MX, MY + 24), "Step 2 of 3 — Wiki Overview", font=_sans(22, bold=True), fill=U.TEXT)
    _alert(draw, MX, MY + 80, MAIN_W - 60,
           "Wiki ready — 34 entity pages available", kind="success")

    draw.text((MX, MY + 160), "Available pages:", font=_sans(13, bold=True), fill=U.TEXT)

    pages = ["transformer", "self-attention", "multi-head-attention",
             "bert", "gpt-3", "rlhf", "scaling-laws", "positional-encoding",
             "feed-forward-network", "layer-normalization", "reward-model",
             "in-context-learning", "... (22 more)"]

    cols = 3
    col_w = (MAIN_W - 60) // cols
    for i, page in enumerate(pages):
        col = i % cols
        row = i // cols
        px = MX + col * col_w
        py = MY + 188 + row * 26
        draw.text((px, py), "· " + page, font=_mono(12), fill=U.DIM)

    _button(draw, MX, MY + 360, 180, "Start Querying  →")

    return _clip(img, duration=4.5)


def _scene_happy_query() -> ImageClip:
    img, draw = _ui_base()
    MX = MAIN_X + 12
    MY = HEADER_H + 1
    CW = MAIN_W - 24

    # Chat area header
    draw.rectangle([MX, MY, MX + CW, MY + 44], fill=U.WHITE)
    draw.text((MX + 14, MY + 13), "Wiki Chat", font=_sans(15, bold=True), fill=U.TEXT)
    draw.rectangle([MX, MY + 44, MX + CW, MY + 45], fill=U.BORDER)

    # Session sidebar info
    draw.text((14, HEADER_H + 16), "Session", font=_sans(12, bold=True), fill=U.DIM)
    for i, (k, v, vc) in enumerate([
        ("Model:", "claude-sonnet-4-6", U.TEXT),
        ("Pages:", "34 available", U.SUCCESS),
        ("Tokens in:", "1,247", U.TEXT),
        ("Cache read:", "892", U.INFO),
        ("Cache write:", "355", U.DIM),
    ]):
        y = HEADER_H + 42 + i * 26
        draw.text((14, y), k, font=_sans(12), fill=U.DIM)
        draw.text((14, y + 14), v, font=_sans(12, bold=True), fill=vc)

    # User message
    CY = MY + 60
    _rrect(draw, MX + CW - 320, CY, 310, 44, (230, 240, 255), radius=10)
    draw.text((MX + CW - 308, CY + 13), "What is self-attention?", font=_sans(14), fill=U.TEXT)

    # Assistant message
    CY += 64
    _rrect(draw, MX + 8, CY, CW - 28, 220, U.WHITE, radius=10, outline=U.BORDER)
    lines = [
        "Self-attention is a mechanism that allows each position in a sequence to",
        "attend to all other positions, computing a weighted sum of value vectors.",
        "",
        "For each position, three vectors are computed — Query (Q), Key (K), and",
        "Value (V) — via learned linear projections. Attention weights are:",
        "",
        "    Attention(Q, K, V) = softmax(QKᵀ / √dₖ) · V",
        "",
        "The √dₖ scaling prevents vanishing gradients in high-dimensional spaces.",
    ]
    for i, line in enumerate(lines):
        font = _mono(12) if line.startswith("    ") else _sans(13)
        color = U.INFO if line.startswith("    ") else U.TEXT
        draw.text((MX + 20, CY + 12 + i * 19), line, font=font, fill=color)

    draw.text((MX + 20, CY + 194), "Source: wiki/self-attention.md  ·  Attention.pdf §3.2",
              font=_sans(11), fill=U.SUCCESS)

    # Input bar
    IY = H - 56
    _rrect(draw, MX, IY, CW, 42, U.WHITE, radius=8, outline=U.BORDER)
    draw.text((MX + 14, IY + 12), "Ask another question...", font=_sans(13), fill=U.DIM)

    return _clip(img, duration=7.5)


def _scene_not_found() -> ImageClip:
    img, draw = _ui_base()
    MX = MAIN_X + 12
    MY = HEADER_H + 1
    CW = MAIN_W - 24

    draw.rectangle([MX, MY, MX + CW, MY + 44], fill=U.WHITE)
    draw.text((MX + 14, MY + 13), "Wiki Chat", font=_sans(15, bold=True), fill=U.TEXT)
    draw.rectangle([MX, MY + 44, MX + CW, MY + 45], fill=U.BORDER)

    CY = MY + 60
    _rrect(draw, MX + CW - 290, CY, 280, 44, (230, 240, 255), radius=10)
    draw.text((MX + CW - 278, CY + 13), "What is a diffusion model?", font=_sans(14), fill=U.TEXT)

    CY += 64
    _rrect(draw, MX + 8, CY, CW - 28, 188, (255, 248, 240), radius=10, outline=(255, 200, 150))
    draw.text((MX + 20, CY + 14), "No information found in the wiki for this query.",
              font=_sans(14, bold=True), fill=U.WARNING)
    draw.text((MX + 20, CY + 44),
              "The wiki covers topics from 8 sources (Attention.pdf, FMs.pdf,",
              font=_sans(13), fill=U.TEXT)
    draw.text((MX + 20, CY + 64), "gpt3.pdf, SLL.pdf, and 4 others).",
              font=_sans(13), fill=U.TEXT)
    draw.text((MX + 20, CY + 100), "To add diffusion model coverage:",
              font=_sans(13, bold=True), fill=U.TEXT)
    draw.text((MX + 20, CY + 122), "  1.  Add relevant papers to /raw/",
              font=_sans(13), fill=U.DIM)
    draw.text((MX + 20, CY + 142), "  2.  Run /sync-wiki  (Claude) or /Sync Wiki from Raw  (Copilot)",
              font=_sans(13), fill=U.DIM)
    draw.text((MX + 20, CY + 162), "  3.  Query again in this UI",
              font=_sans(13), fill=U.DIM)

    IY = H - 56
    _rrect(draw, MX, IY, CW, 42, U.WHITE, radius=8, outline=U.BORDER)
    draw.text((MX + 14, IY + 12), "Ask another question...", font=_sans(13), fill=U.DIM)

    return _clip(img, duration=6.0)


def generate_ui_demo(output: Path = UI_OUT) -> Path:
    """Generate the wiki query UI demo video using real Streamlit screenshots."""
    print("  Generating UI demo (launching real Streamlit UI via Playwright)...")
    from capture_ui_demo import capture
    result = capture(output)
    print(f"  ✓ ui-demo.mp4 ({result.stat().st_size // 1024} KB)")
    return result


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Generate LLM Wiki demo videos")
    ap.add_argument("--terminal", action="store_true", help="Terminal demo only")
    ap.add_argument("--ui",       action="store_true", help="UI demo only")
    args = ap.parse_args()

    both = not args.terminal and not args.ui

    if both or args.terminal:
        generate_terminal_demo()
    if both or args.ui:
        generate_ui_demo()


if __name__ == "__main__":
    main()

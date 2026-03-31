# Shared config: colors, fonts, constants
from manim import *

# ── Background ──────────────────────────────────────────────────────────────
BG = BLACK

# ── Palette ─────────────────────────────────────────────────────────────────
WHITE_TEXT   = "#F2F2F2"
GRAY_TEXT    = "#AAAAAA"
DIM_GRAY     = "#555555"

BLUE_LIGHT   = "#5BC4F5"   # treatment / highlight
GREEN_LIGHT  = "#6FD18A"   # true effects / NES
RED_LIGHT    = "#F47C7C"   # paradox / wrong / baselines
YELLOW_LIGHT = "#F5C842"   # emphasis / paradox label
PURPLE_LIGHT = "#C39BD3"   # SAE / latent space

# ── Typography ───────────────────────────────────────────────────────────────
TITLE_SCALE  = 0.72
BODY_SCALE   = 0.48
SMALL_SCALE  = 0.38
LABEL_SCALE  = 0.36

# ── Layout helpers ───────────────────────────────────────────────────────────
def slide_title(text, color=WHITE_TEXT):
    return Text(text, color=color).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

def subtitle(text, color=GRAY_TEXT):
    return Text(text, color=color).scale(BODY_SCALE)

def label(text, color=GRAY_TEXT):
    return Text(text, color=color).scale(LABEL_SCALE)

# White-background theme: mirrors config.py with an inverted palette.
# Same constant names so scenes can swap `from config import *`
# for `from config_white import *` with no other changes.
from manim import *

# ── Background ──────────────────────────────────────────────────────────────
BG = WHITE

# ── Palette (inverted / deepened for contrast on white) ──────────────────────
WHITE_TEXT   = "#1A1A1A"   # primary text (was near-white)
GRAY_TEXT    = "#555555"
DIM_GRAY     = "#AAAAAA"

BLUE_LIGHT   = "#1F7FB5"   # treatment / highlight
GREEN_LIGHT  = "#2E9E5B"   # true effects / NES
RED_LIGHT    = "#D14343"   # paradox / wrong / baselines
YELLOW_LIGHT = "#C08A00"   # emphasis / paradox label
PURPLE_LIGHT = "#8E44AD"   # SAE / latent space
TEAL_LIGHT   = "#1FA391"   # second dataset / interpretation

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

#!/bin/bash
# Render scenes as interactive HTML slides.
# Usage:
#   ./build.sh              → render all scenes + open presentation.html
#   ./build.sh s01          → render single scene + open in browser
#   ./build.sh s01 low      → render with custom quality (low/medium/high/production/4k)
#   ./build.sh html         → convert-only (skip rendering), open presentation.html
#   ./build.sh clean        → remove all build artifacts (media/, slides/, output/)

set -e
CONDA_ENV="${CONDA_ENV:-visualize}"
OUT_DIR="output"

SCENES=(
  "scenes/s01_title.py            S01Title           s01"
  "scenes/s02_causality_primer.py S02CausalityPrimer s02"
  "scenes/s03_eci.py              S03ECI             s03"
  "scenes/s04_dictionary.py       S04Dictionary      s04"
  "scenes/s05_pipeline.py         S05Pipeline        s05"
  "scenes/s06_paradox.py          S06Paradox         s06"
  "scenes/s07_nes.py              S07NES             s07"
  "scenes/s08_experiments.py      S08Experiments     s08"
  "scenes/s09_realworld.py        S09RealWorld       s09"
  "scenes/s10_conclusion.py       S10Conclusion      s10"
  "scenes/s11_thankyou.py         S11ThankYou        s11"
)

resolve_quality() {
  case "$1" in
    low)    echo l ;;
    medium) echo m ;;
    high|"") echo h ;;
    prod|production) echo p ;;
    4k|k)   echo k ;;
    *)      echo "$1" ;;
  esac
}

run_manim() { conda run -n $CONDA_ENV --live-stream "$@"; }

needs_render() {
  local file=$1 cls=$2
  local json="slides/${cls}.json"
  [ ! -f "$json" ] && return 0
  [ "$file" -nt "$json" ] && return 0
  return 1
}

render_scene() {
  local file=$1 cls=$2 quality=$3
  run_manim manim-slides render --quality "$quality" "$file" "$cls"
}

# ── clean ────────────────────────────────────────────────────────────────────
if [ "$1" = "clean" ]; then
  echo "Removing build artifacts..."
  rm -rf media/ slides/ output/
  echo "Done."
  exit 0
fi

# ── html only (convert, no render) ──────────────────────────────────────────
if [ "$1" = "html" ]; then
  ALL_CLASSES=""
  for entry in "${SCENES[@]}"; do
    read -r file cls tag <<< "$entry"
    if [ -f "slides/${cls}.json" ]; then
      ALL_CLASSES="$ALL_CLASSES $cls"
    else
      echo "  ⚠ Skipping $cls (not yet rendered)"
    fi
  done
  if [ -z "$ALL_CLASSES" ]; then
    echo "ERROR: No rendered scenes found in slides/. Run ./build.sh first to render."
    exit 1
  fi
  echo "Converting to $OUT_DIR/presentation.html..."
  mkdir -p "$OUT_DIR"
  run_manim manim-slides convert $ALL_CLASSES "$OUT_DIR/presentation.html"
  open "$OUT_DIR/presentation.html"
  exit 0
fi

mkdir -p "$OUT_DIR"
quality=$(resolve_quality "$2")

# ── single scene ─────────────────────────────────────────────────────────────
for entry in "${SCENES[@]}"; do
  read -r file cls tag <<< "$entry"
  if [ "$1" = "$tag" ]; then
    render_scene "$file" "$cls" "$quality"
    run_manim manim-slides convert "$cls" "$OUT_DIR/${tag}.html"
    open "$OUT_DIR/${tag}.html"
    exit 0
  fi
done

# ── all scenes ───────────────────────────────────────────────────────────────
if [ -n "$1" ]; then
  echo "Unknown scene '$1'. Available: s01..s12, clean"
  exit 1
fi

quality=$(resolve_quality "$1")  # no arg → high
ALL_CLASSES=""
echo "Rendering scenes (skipping unchanged)..."
for entry in "${SCENES[@]}"; do
  read -r file cls tag <<< "$entry"
  if needs_render "$file" "$cls"; then
    echo "  → $cls (rendering)"
    render_scene "$file" "$cls" "$quality"
  else
    echo "  → $cls (up to date)"
  fi
  ALL_CLASSES="$ALL_CLASSES $cls"
done

echo "Converting to $OUT_DIR/presentation.html..."
run_manim manim-slides convert $ALL_CLASSES "$OUT_DIR/presentation.html"
open "$OUT_DIR/presentation.html"

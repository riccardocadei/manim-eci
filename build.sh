#!/bin/bash
# Render a scene and preview as HTML.
# Usage:
#   ./build.sh s01    → render s01_title + open in browser
#   ./build.sh        → render all + open full presentation.html

set -e
CONDA_ENV="visualize"
OUT_DIR="output"
mkdir -p "$OUT_DIR"

render_and_open() {
  local file=$1 cls=$2 out=$OUT_DIR/$3
  case "$4" in
    low)    quality=l ;;
    medium) quality=m ;;
    high)   quality=h ;;
    prod|production) quality=p ;;
    4k|k)   quality=k ;;
    "")     quality=h ;;
    *)      quality=$4 ;;
  esac
  conda run -n $CONDA_ENV manim-slides render --quality $quality $file $cls
  conda run -n $CONDA_ENV manim-slides convert $cls $out
  open $out
}

case "$1" in
  s01) render_and_open scenes/s01_title.py            S01Title           s01.html "$2" ;;
  s02) render_and_open scenes/s02_causality_primer.py S02CausalityPrimer s02.html "$2" ;;
  s03) render_and_open scenes/s03_eci.py              S03ECI             s03.html "$2" ;;
  s04) render_and_open scenes/s04_mi.py               S04MI              s04.html "$2" ;;
  s05) render_and_open scenes/s05_pipeline.py         S05Pipeline        s05.html "$2" ;;
  s06) render_and_open scenes/s06_paradox.py          S06Paradox         s06.html "$2" ;;
  s07) render_and_open scenes/s07_nes.py              S07NES             s07.html "$2" ;;
  s08) render_and_open scenes/s08_full_pipeline.py    S08FullPipeline    s08.html "$2" ;;
  s09) render_and_open scenes/s09_experiments.py      S09Experiments     s09.html "$2" ;;
  s10) render_and_open scenes/s10_realworld.py        S10RealWorld       s10.html "$2" ;;
  s11) render_and_open scenes/s11_conclusion.py       S11Conclusion      s11.html "$2" ;;
  s12) render_and_open scenes/s12_thankyou.py         S12ThankYou        s12.html "$2" ;;
  *)
    echo "Rendering all scenes..."
    for pair in \
      "scenes/s01_title.py S01Title" \
      "scenes/s02_causality_primer.py S02CausalityPrimer" \
      "scenes/s03_eci.py S03ECI" \
      "scenes/s04_mi.py S04MI" \
      "scenes/s05_pipeline.py S05Pipeline" \
      "scenes/s06_paradox.py S06Paradox" \
      "scenes/s07_nes.py S07NES" \
      "scenes/s08_full_pipeline.py S08FullPipeline" \
      "scenes/s09_experiments.py S09Experiments" \
      "scenes/s10_realworld.py S10RealWorld" \
      "scenes/s11_conclusion.py S11Conclusion" \
      "scenes/s12_thankyou.py S12ThankYou"
    do
      f=$(echo $pair | cut -d' ' -f1)
      c=$(echo $pair | cut -d' ' -f2)
      echo "  → $c"
      conda run -n $CONDA_ENV manim-slides render --quality h $f $c
    done
    echo "Converting to $OUT_DIR/presentation.html..."
    conda run -n $CONDA_ENV manim-slides convert \
      S01Title S02CausalityPrimer S03ECI S04MI \
      S05Pipeline S06Paradox S07NES S08FullPipeline S09Experiments \
      S10RealWorld S11Conclusion S12ThankYou \
      $OUT_DIR/presentation.html
    open $OUT_DIR/presentation.html
    ;;
esac

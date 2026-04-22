from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


FRAMES_DIR = os.path.join(os.path.dirname(__file__), "..",
                          "assets", "data", "nems", "frames")


class S18Experiments(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title (exactly as s09) ────────────────────────────────────────
        title = Text(
            "Results: semi-synthetic (CelebA+)",
            color=WHITE_TEXT,
            t2s={"semi-synthetic (CelebA+)": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        self.play(Write(title), run_time=0.7)
        self.wait(0.3)
        self.next_slide()

        FIG_H = 5.2
        N_FRAMES = 15
        STEP = 1 / 15  # seconds per frame

        def _sweep(frames):
            """Single Succession that stacks fade-ins through a frame sequence.
            Each new opaque frame covers the previous one — no blink gap."""
            return Succession(*[
                FadeIn(frames[i], run_time=STEP)
                for i in range(1, len(frames))
            ])

        # ── Phase 1: baselines (t-test + Bonferroni) bars grow ────────────
        base_frames = [
            ImageMobject(os.path.join(FRAMES_DIR, f"grow_base_{i:02d}.png"))
                .set_height(FIG_H).next_to(title, DOWN, buff=0.3)
            for i in range(N_FRAMES)
        ]
        self.add(base_frames[0])
        self.play(_sweep(base_frames))
        fig_current = base_frames[-1]
        self.wait(0.4)
        self.next_slide()

        # ── Phase 2: trend line appears → ECI paradox ─────────────────────
        fig_trend = ImageMobject(os.path.join(FRAMES_DIR, "trend.png"))
        fig_trend.set_height(FIG_H).move_to(fig_current.get_center())
        fig_trend.set_opacity(0)

        self.add(fig_trend)
        self.play(fig_trend.animate.set_opacity(1), run_time=0.8)
        self.remove(fig_current)
        fig_current = fig_trend

        self.wait(0.4)
        self.next_slide()

        # ── Phase 2b: ECI paradox label ───────────────────────────────────
        paradox_text = Text(
            "Exploratory Causal Inference Paradox",
            color=RED_LIGHT,
            t2s={"Exploratory Causal Inference Paradox": ITALIC},
        ).scale(BODY_SCALE * 1.1)
        paradox_text.next_to(fig_current, DOWN, buff=0.25)

        self.play(Write(paradox_text), run_time=0.7)
        self.wait(0.3)
        self.next_slide()

        # ── Phase 3: baselines dim, NEMS (ours) grows in ──────────────────
        self.play(FadeOut(paradox_text), run_time=0.3)

        nems_frames = [
            ImageMobject(os.path.join(FRAMES_DIR, f"add_nems_{i:02d}.png"))
                .set_height(FIG_H).move_to(fig_current.get_center())
            for i in range(N_FRAMES)
        ]
        self.remove(fig_current)
        self.add(nems_frames[0])
        self.play(_sweep(nems_frames))
        self.wait(0.6)
        self.next_slide()

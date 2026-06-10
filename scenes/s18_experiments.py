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

        # ── Phase 2b: ECI paradox label (line 1 only) ─────────────────────
        PAR_SCALE = BODY_SCALE

        lbl1  = Text("Multiple Testing:", color=WHITE_TEXT).scale(PAR_SCALE)
        lbl2  = Text("NEMS (ours):",      color=WHITE_TEXT).scale(PAR_SCALE)
        tail1 = Text(
            "precision collapse",
            color=WHITE_TEXT,
            t2s={"precision collapse": ITALIC},
        ).scale(PAR_SCALE)
        tail2 = Text(
            "precision collapse",
            color=WHITE_TEXT,
            t2s={"precision collapse": ITALIC},
        ).scale(PAR_SCALE)

        # Stack labels right-aligned so colons line up; tails share a left edge.
        lbl2.next_to(lbl1, DOWN, buff=0.15, aligned_edge=RIGHT)
        tail1.next_to(lbl1, RIGHT, buff=0.22)
        tail2.next_to(lbl2, RIGHT, buff=0.22)
        tail2.align_to(tail1, LEFT)

        strike = Line(
            tail2.get_left()  + LEFT  * 0.05,
            tail2.get_right() + RIGHT * 0.05,
            color=WHITE_TEXT, stroke_width=2.5,
        )

        line1_group = VGroup(lbl1, tail1)
        line2_group = VGroup(lbl2, tail2, strike)
        paradox_block = VGroup(line1_group, line2_group)
        paradox_block.next_to(fig_current, DOWN, buff=0.22)

        self.play(Write(line1_group), run_time=0.8)
        self.wait(0.3)
        self.next_slide()

        # ── Phase 3: NEMS grows in (frame sequence), then line 2 writes in ─
        nems_frames = [
            ImageMobject(os.path.join(FRAMES_DIR, f"add_nems_{i:02d}.png"))
                .set_height(FIG_H).move_to(fig_current.get_center())
            for i in range(N_FRAMES)
        ]
        self.remove(fig_current)
        self.add(nems_frames[0])
        self.play(_sweep(nems_frames))

        self.play(Write(line2_group), run_time=0.9)
        self.wait(0.4)
        self.next_slide()

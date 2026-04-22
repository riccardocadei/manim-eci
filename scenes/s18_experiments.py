from manim import *
from manim_slides import Slide
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


# ── Data (pre-aggregated means from assets/data/nems/*.parquet) ─────────────

# Effect sweep, fixed n=500
ETA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
EFFECT_IOU = {
    "Marginal":       [0.0022, 0.0020, 0.0015, 0.0012, 0.0010,
                       0.0009, 0.0009, 0.0008, 0.0008, 0.0008],
    "Marginal (Bon)": [0.0000, 0.1751, 0.1742, 0.0698, 0.0369,
                       0.0229, 0.0174, 0.0143, 0.0122, 0.0111],
    "NEMS (auto)":    [0.0000, 0.2500, 0.6833, 0.8500, 0.8458,
                       0.8750, 0.8917, 0.8875, 0.9042, 0.9083],
}

# n sweep, fixed eta=5
N_VALS = [50, 100, 250, 500, 1000, 2000, 5000, 10000]
N_LOG  = [np.log10(v) for v in N_VALS]  # 1.70 … 4.00
N_IOU = {
    "Marginal":       [0.0014, 0.0024, 0.0015, 0.0010, 0.0006,
                       0.0005, 0.0003, 0.0003],
    "Marginal (Bon)": [0.0250, 0.1066, 0.1811, 0.0369, 0.0083,
                       0.0020, 0.0008, 0.0005],
    "NEMS (auto)":    [0.0250, 0.1667, 0.5183, 0.8458, 0.9000,
                       0.9750, 1.0000, 1.0000],
}

# Display metadata for the three methods
METHODS = [
    {"key": "Marginal",       "label": "t-test (marginal)",    "color": RED_LIGHT,    "dashed": False},
    {"key": "Marginal (Bon)", "label": "Bonferroni (marginal)","color": YELLOW_LIGHT, "dashed": False},
    {"key": "NEMS (auto)",    "label": "NEMS (ours)",          "color": GREEN_LIGHT,  "dashed": False},
]


# ── Helpers ────────────────────────────────────────────────────────────────

def _make_axes(x_range, y_range, x_length, y_length,
               x_tick, y_tick):
    """Create clean, minimal axes."""
    ax = Axes(
        x_range=[*x_range, x_tick],
        y_range=[*y_range, y_tick],
        x_length=x_length,
        y_length=y_length,
        tips=False,
        axis_config={
            "color": GRAY_TEXT,
            "stroke_width": 1.8,
            "include_ticks": True,
            "tick_size": 0.05,
        },
    )
    return ax


def _line_through(ax, xs, ys, color, stroke_width=3.0, dashed=False):
    """Poly-line through (xs,ys) on given axes."""
    points = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    line = VMobject(color=color, stroke_width=stroke_width)
    line.set_points_as_corners(points)
    if dashed:
        line = DashedVMobject(line, num_dashes=20, dashed_ratio=0.55)
    return line


def _dots(ax, xs, ys, color, radius=0.045):
    return VGroup(*[
        Dot(ax.c2p(x, y), color=color, radius=radius)
        for x, y in zip(xs, ys)
    ])


# ── Scene ──────────────────────────────────────────────────────────────────

class S18Experiments(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ──────────────────────────────────────────────────────────
        title = Text(
            "Results: simulations",
            color=WHITE_TEXT,
            t2s={"simulations": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)
        self.wait(0.2)
        self.next_slide()

        # ── Layout constants ───────────────────────────────────────────────
        PANEL_Y  = -0.15
        LEFT_X   = -3.55
        RIGHT_X  =  3.55
        AX_W     =  4.4
        AX_H     =  3.2

        # ── LEFT: IoU vs effect size η (n=500) ─────────────────────────────
        ax_L = _make_axes(
            x_range=[1, 10], y_range=[0, 1.0],
            x_length=AX_W, y_length=AX_H,
            x_tick=1, y_tick=0.25,
        ).move_to([LEFT_X, PANEL_Y, 0])

        # Custom x-tick labels: integer η values
        x_lbls_L = VGroup()
        for v in [1, 3, 5, 7, 10]:
            t = Text(str(v), color=GRAY_TEXT).scale(0.28)
            t.next_to(ax_L.c2p(v, 0), DOWN, buff=0.10)
            x_lbls_L.add(t)

        y_lbls_L = VGroup()
        for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
            t = Text(f"{v:.2f}", color=GRAY_TEXT).scale(0.28)
            t.next_to(ax_L.c2p(1, v), LEFT, buff=0.10)
            y_lbls_L.add(t)

        x_title_L = MathTex(r"\text{effect size } \eta", color=WHITE_TEXT).scale(0.45)
        x_title_L.next_to(ax_L, DOWN, buff=0.40)
        y_title_L = Text("IoU", color=WHITE_TEXT).scale(0.42)
        y_title_L.rotate(PI / 2).next_to(ax_L, LEFT, buff=0.55)

        sub_L = Text("n = 500", color=GRAY_TEXT, slant=ITALIC).scale(0.38)
        sub_L.next_to(ax_L, UP, buff=0.15)

        # ── RIGHT: IoU vs sample size n (η=5), log-scale x ─────────────────
        ax_R = _make_axes(
            x_range=[np.log10(50), np.log10(10000)], y_range=[0, 1.0],
            x_length=AX_W, y_length=AX_H,
            x_tick=1, y_tick=0.25,
        ).move_to([RIGHT_X, PANEL_Y, 0])

        x_lbls_R = VGroup()
        for v in [50, 100, 500, 1000, 10000]:
            t = Text(str(v), color=GRAY_TEXT).scale(0.28)
            t.next_to(ax_R.c2p(np.log10(v), 0), DOWN, buff=0.10)
            x_lbls_R.add(t)

        y_lbls_R = VGroup()
        for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
            t = Text(f"{v:.2f}", color=GRAY_TEXT).scale(0.28)
            t.next_to(ax_R.c2p(np.log10(50), v), LEFT, buff=0.10)
            y_lbls_R.add(t)

        x_title_R = MathTex(r"\text{sample size } n \text{ (log)}", color=WHITE_TEXT).scale(0.45)
        x_title_R.next_to(ax_R, DOWN, buff=0.40)
        y_title_R = Text("IoU", color=WHITE_TEXT).scale(0.42)
        y_title_R.rotate(PI / 2).next_to(ax_R, LEFT, buff=0.55)

        sub_R = Text("η = 5", color=GRAY_TEXT, slant=ITALIC).scale(0.38)
        sub_R.next_to(ax_R, UP, buff=0.15)

        # ── Draw axes + labels ─────────────────────────────────────────────
        self.play(
            Create(ax_L), Create(ax_R),
            FadeIn(x_title_L), FadeIn(y_title_L),
            FadeIn(x_title_R), FadeIn(y_title_R),
            FadeIn(sub_L), FadeIn(sub_R),
            FadeIn(x_lbls_L), FadeIn(y_lbls_L),
            FadeIn(x_lbls_R), FadeIn(y_lbls_R),
            run_time=0.9,
        )
        self.wait(0.2)
        self.next_slide()

        # ── Legend (below both panels) ─────────────────────────────────────
        LEG_Y = -2.85

        def _legend_entry(color, label):
            seg = Line(ORIGIN, RIGHT * 0.32, color=color, stroke_width=3.5)
            dot = Dot(seg.get_center(), color=color, radius=0.05)
            txt = Text(label, color=WHITE_TEXT).scale(0.36)
            txt.next_to(seg, RIGHT, buff=0.12)
            return VGroup(seg, dot, txt)

        leg_entries = [_legend_entry(m["color"], m["label"]) for m in METHODS]
        legend = VGroup(*leg_entries).arrange(RIGHT, buff=0.65)
        legend.move_to([0, LEG_Y, 0])

        # ── Animate each method in sequence (left + right together) ────────
        lines_L, lines_R, dots_L, dots_R = {}, {}, {}, {}

        for i, m in enumerate(METHODS):
            key = m["key"]
            color = m["color"]

            lnL = _line_through(ax_L, ETA,   EFFECT_IOU[key], color)
            lnR = _line_through(ax_R, N_LOG, N_IOU[key],      color)
            dtL = _dots(ax_L, ETA,   EFFECT_IOU[key], color)
            dtR = _dots(ax_R, N_LOG, N_IOU[key],      color)
            lines_L[key] = lnL; lines_R[key] = lnR
            dots_L[key]  = dtL; dots_R[key]  = dtR

            is_last = (i == len(METHODS) - 1)
            run_t = 1.1 if is_last else 0.9

            self.play(
                Create(lnL), Create(lnR),
                FadeIn(leg_entries[i]),
                run_time=run_t,
            )
            self.play(
                FadeIn(dtL), FadeIn(dtR),
                run_time=0.35,
            )

            if not is_last:
                self.wait(0.25)
                self.next_slide()
            else:
                # Emphasise NEMS (ours): thicken + small pulse
                self.play(
                    lnL.animate.set_stroke(width=4.6),
                    lnR.animate.set_stroke(width=4.6),
                    run_time=0.35,
                )

        self.wait(0.5)
        self.next_slide()

        # ── Closing callout: NEMS dominates ────────────────────────────────
        takeaway = Text(
            "NEMS recovers the true effect modifiers",
            color=GREEN_LIGHT,
            t2s={"NEMS": ITALIC},
        ).scale(BODY_SCALE * 0.95)
        takeaway.next_to(legend, DOWN, buff=0.28)

        self.play(FadeIn(takeaway, shift=UP * 0.08), run_time=0.6)
        self.wait(0.5)
        self.next_slide()

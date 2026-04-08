from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np


# ── Helpers ───────────────────────────────────────────────────────────────────

_NODE_R   = 0.30
_STROKE_W = 2.5
_LBL_SC   = 0.50


def _node(tex, color=WHITE_TEXT):
    circ = Circle(radius=_NODE_R, color=color, stroke_width=_STROKE_W,
                  fill_color=color, fill_opacity=0.0)
    lbl  = MathTex(tex, color=color).scale(_LBL_SC)
    return VGroup(circ, lbl)


def _causal_arrow(start_mob, end_mob, color=WHITE_TEXT):
    return Arrow(
        start_mob.get_center(), end_mob.get_center(),
        color=color, buff=_NODE_R + 0.05, stroke_width=2.0,
        max_tip_length_to_length_ratio=0.08,
    )


def _sankey_band(src, dst, color, width=0.10, opacity=0.35):
    """Curved filled band from src center-right to dst center-left."""
    s = src.get_right() + RIGHT * 0.02
    d = dst.get_left()  + LEFT  * 0.02
    mid_x = (s[0] + d[0]) / 2.0
    hw = width / 2.0

    top_pts = [
        s + UP * hw,
        np.array([mid_x, s[1] + hw, 0]),
        np.array([mid_x, d[1] + hw, 0]),
        d + UP * hw,
    ]
    bot_pts = [
        d + DOWN * hw,
        np.array([mid_x, d[1] - hw, 0]),
        np.array([mid_x, s[1] - hw, 0]),
        s + DOWN * hw,
    ]

    band = VMobject()
    band.start_new_path(s + UP * hw)
    band.add_cubic_bezier_curve_to(top_pts[1], top_pts[2], top_pts[3])
    band.add_line_to(d + DOWN * hw)
    band.add_cubic_bezier_curve_to(bot_pts[1], bot_pts[2], bot_pts[3])
    band.add_line_to(s + UP * hw)

    band.set_fill(color, opacity=opacity)
    band.set_stroke(color, width=0.8, opacity=opacity * 0.8)
    return band


def _cross_on(mob, color=RED_LIGHT, size=0.22):
    """Big × centred on a mobject."""
    c = mob.get_center()
    l1 = Line(c + UP * size + LEFT * size, c + DOWN * size + RIGHT * size,
              color=color, stroke_width=4.0)
    l2 = Line(c + UP * size + RIGHT * size, c + DOWN * size + LEFT * size,
              color=color, stroke_width=4.0)
    return VGroup(l1, l2)


# ── Scene ─────────────────────────────────────────────────────────────────────

class S07NES(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ─────────────────────────────────────────────────────────────
        title = Text(
            "Mitigation: Neural Effect Search", color=WHITE_TEXT,
            t2s={"Neural Effect Search": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ==================================================================
        # DAG — centred
        # ==================================================================

        # Nodes
        T  = _node("T",   WHITE_TEXT)
        Y1 = _node("Y_1", WHITE_TEXT)
        Y2 = _node("Y_2", WHITE_TEXT)
        Z1 = _node("Z_1", WHITE_TEXT)
        Z2 = _node("Z_2", WHITE_TEXT)
        Z3 = _node("Z_3", WHITE_TEXT)

        # Centred positions
        col_T = -2.8;  col_Y = -0.4;  col_Z = 2.0
        vert_off = -0.05

        T.move_to( [col_T, 0 + vert_off, 0])
        Y1.move_to([col_Y, 1.05 + vert_off, 0])
        Y2.move_to([col_Y, -1.05 + vert_off, 0])
        Z1.move_to([col_Z, 1.8 + vert_off, 0])
        Z2.move_to([col_Z, 0 + vert_off, 0])
        Z3.move_to([col_Z, -1.8 + vert_off, 0])

        # Causal arrows T → Y
        a_T_Y1 = _causal_arrow(T, Y1)
        a_T_Y2 = _causal_arrow(T, Y2)

        # Sankey bands Y → Z
        bnd_Y1_Z1 = _sankey_band(Y1, Z1, BLUE_LIGHT,  width=0.14, opacity=0.40)
        bnd_Y1_Z2 = _sankey_band(Y1, Z2, BLUE_LIGHT,  width=0.06, opacity=0.18)
        bnd_Y2_Z3 = _sankey_band(Y2, Z3, PURPLE_LIGHT, width=0.14, opacity=0.40)
        bnd_Y2_Z2 = _sankey_band(Y2, Z2, PURPLE_LIGHT, width=0.06, opacity=0.18)

        bands_Y1 = VGroup(bnd_Y1_Z1, bnd_Y1_Z2)
        bands_Y2 = VGroup(bnd_Y2_Z3, bnd_Y2_Z2)

        # Column labels – smaller, lower (below title with gap)
        lbl_sc = LABEL_SCALE * 0.85
        top_y = 2.45 + vert_off

        lbl_T = Text("treatment", color=GRAY_TEXT).scale(lbl_sc)
        lbl_T.move_to([col_T, top_y, 0])

        lbl_Y1 = Text("affected outcomes", color=GRAY_TEXT).scale(lbl_sc)
        lbl_Y2 = Text("(ground truth)", color=GRAY_TEXT).scale(lbl_sc * 0.9)
        lbl_Y_grp = VGroup(lbl_Y1, lbl_Y2).arrange(DOWN, buff=0.04)
        lbl_Y_grp.move_to([col_Y, top_y, 0])

        lbl_Z1 = Text("sparse representation", color=GRAY_TEXT).scale(lbl_sc)
        lbl_Z2 = Text("(learned)", color=GRAY_TEXT).scale(lbl_sc * 0.9)
        lbl_Z_grp = VGroup(lbl_Z1, lbl_Z2).arrange(DOWN, buff=0.04)
        lbl_Z_grp.move_to([col_Z, top_y, 0])

        # ── Build DAG gradually ──────────────────────────────────────────────

        # 1) T appears
        self.play(FadeIn(T), FadeIn(lbl_T), run_time=0.5)

        # 2) arrows to Ys, Ys appear
        self.play(
            FadeIn(Y1), FadeIn(Y2),
            Create(a_T_Y1), Create(a_T_Y2),
            FadeIn(lbl_Y_grp),
            run_time=0.7,
        )

        # 3) bands to Zs, Zs appear
        self.play(
            FadeIn(Z1), FadeIn(Z2), FadeIn(Z3),
            LaggedStart(
                FadeIn(bnd_Y1_Z1), FadeIn(bnd_Y1_Z2),
                FadeIn(bnd_Y2_Z3), FadeIn(bnd_Y2_Z2),
                lag_ratio=0.08,
            ),
            FadeIn(lbl_Z_grp),
            run_time=0.8,
        )
        self.wait(0.4)
        self.next_slide()

        # ==================================================================
        # Persistent bottom bar: "Step N:    S = {...}"
        # ==================================================================

        BOT_Y = -3.3

        def _bottom_bar(step_num, s_tex):
            """Create a bottom bar with step label and S on the same line."""
            st = Text(f"Step {step_num}:", color=WHITE_TEXT, weight=BOLD).scale(SMALL_SCALE)
            sv = MathTex(s_tex, color=GREEN_LIGHT).scale(0.48)
            bar = VGroup(st, sv).arrange(RIGHT, buff=0.35)
            bar.move_to([0, BOT_Y, 0])
            return bar, st, sv

        # ==================================================================
        # STEP 1 — Estimate APO difference for each neuron, select max → Z₁
        # ==================================================================

        bar1, step1_txt, s1_val = _bottom_bar(1, r"\mathtt{S} = \varnothing")

        # Per-neuron formulas (estimand only, no value yet)
        form_z1 = MathTex(
            r"\mathbb{E}[Z_1 | \mathrm{do}(1)] - \mathbb{E}[Z_1 | \mathrm{do}(0)]",
            color=WHITE_TEXT,
        ).scale(0.30)
        form_z2 = MathTex(
            r"\mathbb{E}[Z_2 | \mathrm{do}(1)] - \mathbb{E}[Z_2 | \mathrm{do}(0)]",
            color=WHITE_TEXT,
        ).scale(0.30)
        form_z3 = MathTex(
            r"\mathbb{E}[Z_3 | \mathrm{do}(1)] - \mathbb{E}[Z_3 | \mathrm{do}(0)]",
            color=WHITE_TEXT,
        ).scale(0.30)
        form_z1.next_to(Z1, RIGHT, buff=0.40)
        form_z2.next_to(Z2, RIGHT, buff=0.40)
        form_z3.next_to(Z3, RIGHT, buff=0.40)

        # Estimates (appear separately)
        val_z1 = MathTex(r"\approx 0.82", color=WHITE_TEXT).scale(0.30)
        val_z2 = MathTex(r"\approx 0.45", color=WHITE_TEXT).scale(0.30)
        val_z3 = MathTex(r"\approx 0.51", color=WHITE_TEXT).scale(0.30)
        val_z1.next_to(form_z1, RIGHT, buff=0.08)
        val_z2.next_to(form_z2, RIGHT, buff=0.08)
        val_z3.next_to(form_z3, RIGHT, buff=0.08)

        # Show bottom bar + formulas
        self.play(
            FadeIn(bar1),
            LaggedStart(
                FadeIn(form_z1, shift=LEFT * 0.1),
                FadeIn(form_z2, shift=LEFT * 0.1),
                FadeIn(form_z3, shift=LEFT * 0.1),
                lag_ratio=0.15,
            ),
            run_time=0.7,
        )
        self.wait(0.3)

        # Then show estimated values
        self.play(
            LaggedStart(
                FadeIn(val_z1, shift=LEFT * 0.06),
                FadeIn(val_z2, shift=LEFT * 0.06),
                FadeIn(val_z3, shift=LEFT * 0.06),
                lag_ratio=0.15,
            ),
            run_time=0.6,
        )
        self.wait(0.3)

        # Highlight largest → Z₁: scale up then back down
        est1_grp = VGroup(form_z1, val_z1)
        self.play(
            est1_grp.animate.scale(1.3).set_color(GREEN_LIGHT),
            Z1[0].animate.set_stroke(GREEN_LIGHT, width=3.5),
            Z1[1].animate.set_color(GREEN_LIGHT),
            run_time=0.4,
        )
        self.play(est1_grp.animate.scale(1 / 1.3), run_time=0.3)
        self.wait(0.2)

        # Update S: ∅ → {Z₁} with ghost flying down
        bar1_new, _, _ = _bottom_bar(1, r"\mathtt{S} = \{Z_1\}")
        z1_ghost = MathTex("Z_1", color=GREEN_LIGHT).scale(0.40).move_to(Z1)
        self.play(
            z1_ghost.animate.move_to(bar1_new[1].get_center()).set_opacity(0),
            Transform(bar1, bar1_new),
            run_time=0.6,
        )
        self.remove(z1_ghost)
        self.wait(0.4)
        self.next_slide()

        # ==================================================================
        # STEP 2 — Control for Z₁ → dim Y₁ + × on Y₁, re-estimate
        # ==================================================================

        step1_ui = VGroup(form_z1, form_z2, form_z3, val_z1, val_z2, val_z3)

        bar2, _, _ = _bottom_bar(2, r"\mathtt{S} = \{Z_1\}")
        x_Y1 = _cross_on(Y1)

        # Per-neuron formulas conditioned on Z₁
        form2_z2 = MathTex(
            r"\mathbb{E}[Z_2 | \mathrm{do}(1), Z_1] - \mathbb{E}[Z_2 | \mathrm{do}(0), Z_1]",
            color=WHITE_TEXT,
        ).scale(0.28)
        form2_z3 = MathTex(
            r"\mathbb{E}[Z_3 | \mathrm{do}(1), Z_1] - \mathbb{E}[Z_3 | \mathrm{do}(0), Z_1]",
            color=WHITE_TEXT,
        ).scale(0.28)
        form2_z2.next_to(Z2, RIGHT, buff=0.40)
        form2_z3.next_to(Z3, RIGHT, buff=0.40)

        self.play(
            FadeOut(step1_ui),
            Transform(bar1, bar2),
            Y1[0].animate.set_stroke(opacity=0.20),
            Y1[1].animate.set_opacity(0.20),
            bnd_Y1_Z1.animate.set_fill(opacity=0.08).set_stroke(opacity=0.06),
            bnd_Y1_Z2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.03),
            FadeIn(x_Y1),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                FadeIn(form2_z2, shift=LEFT * 0.1),
                FadeIn(form2_z3, shift=LEFT * 0.1),
                lag_ratio=0.15,
            ),
            run_time=0.5,
        )
        self.wait(0.3)

        # Then show estimates
        val2_z2 = MathTex(r"\approx 0.08", color=WHITE_TEXT).scale(0.28)
        val2_z3 = MathTex(r"\approx 0.51", color=WHITE_TEXT).scale(0.28)
        val2_z2.next_to(form2_z2, RIGHT, buff=0.08)
        val2_z3.next_to(form2_z3, RIGHT, buff=0.08)

        self.play(
            LaggedStart(
                FadeIn(val2_z2, shift=LEFT * 0.06),
                FadeIn(val2_z3, shift=LEFT * 0.06),
                lag_ratio=0.15,
            ),
            run_time=0.5,
        )
        self.wait(0.3)

        # Highlight largest → Z₃: scale up then back down
        est2_grp = VGroup(form2_z3, val2_z3)
        self.play(
            est2_grp.animate.scale(1.3).set_color(GREEN_LIGHT),
            Z3[0].animate.set_stroke(GREEN_LIGHT, width=3.5),
            Z3[1].animate.set_color(GREEN_LIGHT),
            run_time=0.4,
        )
        self.play(est2_grp.animate.scale(1 / 1.3), run_time=0.3)
        self.wait(0.2)

        # Update S: {Z₁} → {Z₁, Z₃}
        bar2_new, _, _ = _bottom_bar(2, r"\mathtt{S} = \{Z_1, Z_3\}")
        z3_ghost = MathTex("Z_3", color=GREEN_LIGHT).scale(0.40).move_to(Z3)
        self.play(
            z3_ghost.animate.move_to(bar2_new[1].get_center()).set_opacity(0),
            Transform(bar1, bar2_new),
            run_time=0.6,
        )
        self.remove(z3_ghost)
        self.wait(0.4)
        self.next_slide()

        # ==================================================================
        # STEP 3 — Control for Z₁, Z₃ → dim Y₂ + × on Y₂ → no sig → stop
        # ==================================================================

        step2_ui = VGroup(form2_z2, form2_z3, val2_z2, val2_z3)

        bar3, _, _ = _bottom_bar(3, r"\mathtt{S} = \{Z_1, Z_3\}")
        x_Y2 = _cross_on(Y2)

        form3_z2 = MathTex(
            r"\mathbb{E}[Z_2 | \mathrm{do}(1), Z_1, Z_3] - \mathbb{E}[Z_2 | \mathrm{do}(0), Z_1, Z_3]",
            color=WHITE_TEXT,
        ).scale(0.26)
        form3_z2.next_to(Z2, RIGHT, buff=0.40)

        self.play(
            FadeOut(step2_ui),
            Transform(bar1, bar3),
            Y2[0].animate.set_stroke(opacity=0.20),
            Y2[1].animate.set_opacity(0.20),
            bnd_Y2_Z3.animate.set_fill(opacity=0.08).set_stroke(opacity=0.06),
            bnd_Y2_Z2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.03),
            FadeIn(x_Y2),
            run_time=0.8,
        )
        self.play(FadeIn(form3_z2, shift=LEFT * 0.1), run_time=0.5)
        self.wait(0.3)

        # Show estimate ≈ 0 — first in white, then dim
        val3_z2 = MathTex(r"\approx 0.02", color=WHITE_TEXT).scale(0.26)
        val3_z2.next_to(form3_z2, RIGHT, buff=0.08)

        self.play(FadeIn(val3_z2, shift=LEFT * 0.06), run_time=0.5)
        self.wait(0.6)

        # Now dim everything: formula, value, and Z₂ node
        self.play(
            val3_z2.animate.set_color(DIM_GRAY),
            form3_z2.animate.set_color(DIM_GRAY),
            Z2[0].animate.set_stroke(DIM_GRAY, width=2.0),
            Z2[1].animate.set_color(DIM_GRAY),
            run_time=0.6,
        )
        self.wait(0.3)

        # Final S
        bar_final, _, _ = _bottom_bar(3, r"\mathtt{S}_{\mathrm{final}} = \{Z_1, Z_3\}")
        self.play(Transform(bar1, bar_final), run_time=0.6)
        self.wait(1)
        self.next_slide()

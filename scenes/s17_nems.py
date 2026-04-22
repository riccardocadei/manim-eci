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

class S17NEMS(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ─────────────────────────────────────────────────────────────
        title = Text(
            "Mitigation: Neural Effect Modifiers Search", color=WHITE_TEXT,
            t2s={"Neural Effect Modifiers Search": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ==================================================================
        # DAG — Z (left, 3 nodes) → W (middle, 2 nodes) → Y (right);
        #        T (below W_1, W_2) → Y
        # ==================================================================

        # Nodes
        Z1 = _node("Z_1", WHITE_TEXT)
        Z2 = _node("Z_2", WHITE_TEXT)
        Z3 = _node("Z_3", WHITE_TEXT)
        W1 = _node("W_1", WHITE_TEXT)
        W2 = _node("W_2", WHITE_TEXT)
        T  = _node("T",   WHITE_TEXT)
        Y  = _node("Y",   WHITE_TEXT)

        # Centred positions
        col_Z = -2.8; col_W = -0.1; col_Y = 2.8
        vert_off = -0.05

        Z1.move_to([col_Z,  1.55 + vert_off, 0])
        Z2.move_to([col_Z,  0.00 + vert_off, 0])
        Z3.move_to([col_Z, -1.55 + vert_off, 0])
        W1.move_to([col_W,  0.95 + vert_off, 0])
        W2.move_to([col_W, -0.55 + vert_off, 0])
        T.move_to( [(col_W + col_Y) / 2, -1.55 + vert_off, 0])
        Y.move_to( [col_Y,  0.20 + vert_off, 0])

        # Causal arrows: T → Y, W_1 → Y, W_2 → Y
        a_T_Y  = _causal_arrow(T,  Y)
        a_W1_Y = _causal_arrow(W1, Y)
        a_W2_Y = _causal_arrow(W2, Y)

        # Sankey bands Z → W
        bnd_Z1_W1 = _sankey_band(Z1, W1, BLUE_LIGHT,   width=0.14, opacity=0.40)
        bnd_Z1_W2 = _sankey_band(Z1, W2, BLUE_LIGHT,   width=0.06, opacity=0.18)
        bnd_Z3_W2 = _sankey_band(Z3, W2, PURPLE_LIGHT, width=0.14, opacity=0.40)
        bnd_Z3_W1 = _sankey_band(Z3, W1, PURPLE_LIGHT, width=0.06, opacity=0.18)
        bnd_Z2_W1 = _sankey_band(Z2, W1, GRAY_TEXT,    width=0.06, opacity=0.18)
        bnd_Z2_W2 = _sankey_band(Z2, W2, GRAY_TEXT,    width=0.06, opacity=0.18)

        bands_Z1 = VGroup(bnd_Z1_W1, bnd_Z1_W2)
        bands_Z2 = VGroup(bnd_Z2_W1, bnd_Z2_W2)
        bands_Z3 = VGroup(bnd_Z3_W2, bnd_Z3_W1)

        # Column labels (at top) + T label (near T)
        lbl_sc = LABEL_SCALE * 0.85
        top_y = 2.45 + vert_off

        lbl_Z1 = Text("sparse representation", color=GRAY_TEXT).scale(lbl_sc)
        lbl_Z2 = Text("(learned)", color=GRAY_TEXT).scale(lbl_sc * 0.9)
        lbl_Z_grp = VGroup(lbl_Z1, lbl_Z2).arrange(DOWN, buff=0.04)
        lbl_Z_grp.move_to([col_Z, top_y, 0])

        lbl_W1 = Text("effect modifiers", color=GRAY_TEXT).scale(lbl_sc)
        lbl_W2 = Text("(ground truth)", color=GRAY_TEXT).scale(lbl_sc * 0.9)
        lbl_W_grp = VGroup(lbl_W1, lbl_W2).arrange(DOWN, buff=0.04)
        lbl_W_grp.move_to([col_W, top_y, 0])

        lbl_Y = Text("affected outcome", color=GRAY_TEXT).scale(lbl_sc)
        lbl_Y.move_to([col_Y, top_y, 0])

        lbl_T = Text("treatment", color=GRAY_TEXT).scale(lbl_sc)
        lbl_T.next_to(T, DOWN, buff=0.14)

        # ── Build DAG gradually ──────────────────────────────────────────────

        # 1) T and Y appear, T → Y
        self.play(
            FadeIn(T), FadeIn(lbl_T),
            FadeIn(Y), FadeIn(lbl_Y),
            Create(a_T_Y),
            run_time=0.6,
        )

        # 2) W_1, W_2 appear with arrows into Y
        self.play(
            FadeIn(W1), FadeIn(W2),
            Create(a_W1_Y), Create(a_W2_Y),
            FadeIn(lbl_W_grp),
            run_time=0.7,
        )

        # 3) Z's appear with sankey bands into W's
        self.play(
            FadeIn(Z1), FadeIn(Z2), FadeIn(Z3),
            LaggedStart(
                FadeIn(bnd_Z1_W1), FadeIn(bnd_Z1_W2),
                FadeIn(bnd_Z3_W2), FadeIn(bnd_Z3_W1),
                FadeIn(bnd_Z2_W1), FadeIn(bnd_Z2_W2),
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

        BOT_Y   = -3.3
        FORM_Y  = -2.75   # score-definition line (above bottom bar)

        def _bottom_bar(step_num, s_tex):
            st = Text(f"Step {step_num}:", color=WHITE_TEXT, weight=BOLD).scale(SMALL_SCALE)
            sv = MathTex(s_tex, color=GREEN_LIGHT).scale(0.48)
            bar = VGroup(st, sv).arrange(RIGHT, buff=0.35)
            bar.move_to([0, BOT_Y, 0])
            return bar, st, sv

        # ==================================================================
        # STEP 1 — Null test for each neuron → select smallest p-value (Z_1)
        # ==================================================================

        bar1, _, _ = _bottom_bar(1, r"\mathtt{S} = \varnothing")

        # Null-hypothesis test (centred, below DAG)
        null_test = MathTex(
            r"H_0(j\mid S):\;"
            r"\mathbb{E}[\tau_i\mid Z_i^{\,j},\mathbf{Z}_i^{\,S}]"
            r"\;\overset{a.s.}{=}\;"
            r"\mathbb{E}[\tau_i\mid \mathbf{Z}_i^{\,S}]",
            color=WHITE_TEXT,
        ).scale(0.50)
        null_test.move_to([0, FORM_Y, 0])

        # Per-neuron p-values (next to each Z, on the LEFT)
        val_z1 = MathTex(r"p\text{-value}(Z_1) \approx 0.001", color=WHITE_TEXT).scale(0.34)
        val_z2 = MathTex(r"p\text{-value}(Z_2) \approx 0.011", color=WHITE_TEXT).scale(0.34)
        val_z3 = MathTex(r"p\text{-value}(Z_3) \approx 0.008", color=WHITE_TEXT).scale(0.34)
        val_z1.next_to(Z1, LEFT, buff=0.25)
        val_z2.next_to(Z2, LEFT, buff=0.25)
        val_z3.next_to(Z3, LEFT, buff=0.25)

        # Show bottom bar + null-test definition
        self.play(
            FadeIn(bar1),
            FadeIn(null_test, shift=UP * 0.08),
            run_time=0.7,
        )
        self.wait(0.2)

        # Show per-neuron p-values
        self.play(
            LaggedStart(
                FadeIn(val_z1, shift=RIGHT * 0.08),
                FadeIn(val_z2, shift=RIGHT * 0.08),
                FadeIn(val_z3, shift=RIGHT * 0.08),
                lag_ratio=0.15,
            ),
            run_time=0.7,
        )
        self.wait(0.3)

        # Highlight smallest p-value → Z_1: scale up then back down
        self.play(
            val_z1.animate.scale(1.30).set_color(GREEN_LIGHT),
            Z1[0].animate.set_stroke(GREEN_LIGHT, width=3.5),
            Z1[1].animate.set_color(GREEN_LIGHT),
            run_time=0.4,
        )
        self.play(val_z1.animate.scale(1 / 1.30), run_time=0.3)
        self.wait(0.2)

        # Update S: ∅ → {Z_1} with ghost flying down
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
        # STEP 2 — Control for Z_1 → dim W_1 + × on W_1, re-score
        # ==================================================================

        step1_vals = VGroup(val_z1, val_z2, val_z3)

        bar2, _, _ = _bottom_bar(2, r"\mathtt{S} = \{Z_1\}")
        x_W1 = _cross_on(W1)

        val2_z2 = MathTex(r"p\text{-value}(Z_2\mid Z_1) \approx 0.038", color=WHITE_TEXT).scale(0.32)
        val2_z3 = MathTex(r"p\text{-value}(Z_3\mid Z_1) \approx 0.012", color=WHITE_TEXT).scale(0.32)
        val2_z2.next_to(Z2, LEFT, buff=0.25)
        val2_z3.next_to(Z3, LEFT, buff=0.25)

        # Transition: clear step-1 values, dim W_1 and its bands, update bar
        self.play(
            FadeOut(step1_vals),
            Transform(bar1, bar2),
            W1[0].animate.set_stroke(opacity=0.20),
            W1[1].animate.set_opacity(0.20),
            bnd_Z1_W1.animate.set_fill(opacity=0.08).set_stroke(opacity=0.06),
            bnd_Z1_W2.animate.set_fill(opacity=0.05).set_stroke(opacity=0.03),
            FadeIn(x_W1),
            run_time=0.9,
        )

        # Show new p-values
        self.play(
            LaggedStart(
                FadeIn(val2_z2, shift=RIGHT * 0.08),
                FadeIn(val2_z3, shift=RIGHT * 0.08),
                lag_ratio=0.15,
            ),
            run_time=0.6,
        )
        self.wait(0.3)

        # Highlight smallest p-value → Z_3
        self.play(
            val2_z3.animate.scale(1.30).set_color(GREEN_LIGHT),
            Z3[0].animate.set_stroke(GREEN_LIGHT, width=3.5),
            Z3[1].animate.set_color(GREEN_LIGHT),
            run_time=0.4,
        )
        self.play(val2_z3.animate.scale(1 / 1.30), run_time=0.3)
        self.wait(0.2)

        # Update S: {Z_1} → {Z_1, Z_3}
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
        # STEP 3 — Control for Z_1, Z_3 → dim W_2 + × on W_2 → ≈0 → stop
        # ==================================================================

        step2_vals = VGroup(val2_z2, val2_z3)

        bar3, _, _ = _bottom_bar(3, r"\mathtt{S} = \{Z_1, Z_3\}")
        x_W2 = _cross_on(W2)

        val3_z2 = MathTex(r"p\text{-value}(Z_2\mid Z_1, Z_3) \approx 0.214", color=WHITE_TEXT).scale(0.30)
        val3_z2.next_to(Z2, LEFT, buff=0.25)

        self.play(
            FadeOut(step2_vals),
            Transform(bar1, bar3),
            W2[0].animate.set_stroke(opacity=0.20),
            W2[1].animate.set_opacity(0.20),
            bnd_Z3_W2.animate.set_fill(opacity=0.08).set_stroke(opacity=0.06),
            bnd_Z3_W1.animate.set_fill(opacity=0.05).set_stroke(opacity=0.03),
            FadeIn(x_W2),
            run_time=0.9,
        )
        self.play(FadeIn(val3_z2, shift=RIGHT * 0.08), run_time=0.5)
        self.wait(0.6)

        # p-value > 0.05: cannot reject H_0 → dim Z_2 (no effect modification info)
        self.play(
            val3_z2.animate.set_color(DIM_GRAY),
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

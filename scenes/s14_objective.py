from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np


class S14Objective(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = slide_title("Direct Effect Modifiers Identification", color=WHITE_TEXT)

        # ── 3x3 grid positions ───────────────────────────────────────────────
        #   1 2 3
        #   4 5 6
        #   7 8 9
        dx, dy = 3.0, 2.1
        y_mid = -0.3
        pos = {
            2: np.array([0.0, y_mid + dy, 0]),
            3: np.array([ dx, y_mid + dy, 0]),
            4: np.array([-dx, y_mid,      0]),
            5: np.array([0.0, y_mid,      0]),
            6: np.array([ dx, y_mid,      0]),
            8: np.array([0.0, y_mid - dy, 0]),
        }

        r = 0.6
        fs_single = 0.72
        fs_sub    = 0.58

        def node(label_tex, p, fs):
            c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(p)
            l = MathTex(label_tex, color=WHITE_TEXT).scale(fs).move_to(c)
            return c, l

        T_c,     T_l     = node(r"T",                pos[2], fs_single)
        Y_c,     Y_l     = node(r"Y",                pos[3], fs_single)
        Wind_c,  Wind_l  = node(r"W_{\mathrm{ind}}", pos[4], fs_sub)
        Wdir_c,  Wdir_l  = node(r"W_{\mathrm{dir}}", pos[5], fs_sub)
        Wprox_c, Wprox_l = node(r"W_{\mathrm{prox}}",pos[6], fs_sub)
        Wcc_c,   Wcc_l   = node(r"W_{\mathrm{cc}}",  pos[8], fs_sub)

        def arr(a_c, b_c):
            a_p, b_p = a_c.get_center(), b_c.get_center()
            d = (b_p - a_p) / np.linalg.norm(b_p - a_p)
            return Arrow(
                a_p + d * (r + 0.08),
                b_p - d * (r + 0.08),
                color=WHITE_TEXT, buff=0, stroke_width=5,
                max_tip_length_to_length_ratio=0.18,
            )

        arr_TY        = arr(T_c,    Y_c)
        arr_WdirY     = arr(Wdir_c, Y_c)
        arr_WindWdir  = arr(Wind_c, Wdir_c)
        arr_WindWcc   = arr(Wind_c, Wcc_c)
        arr_WdirWprox = arr(Wdir_c, Wprox_c)

        # ── Reveal ───────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.7)
        self.play(
            LaggedStart(
                *[AnimationGroup(GrowFromCenter(c), FadeIn(l))
                  for c, l in [(T_c, T_l), (Y_c, Y_l),
                               (Wind_c, Wind_l), (Wdir_c, Wdir_l),
                               (Wprox_c, Wprox_l), (Wcc_c, Wcc_l)]],
                lag_ratio=0.12,
            ),
            run_time=1.6,
        )
        self.play(
            LaggedStart(
                Create(arr_TY),
                Create(arr_WindWdir),
                Create(arr_WdirWprox),
                Create(arr_WdirY),
                Create(arr_WindWcc),
                lag_ratio=0.15,
            ),
            run_time=1.2,
        )
        self.wait(0.4)
        self.next_slide()

        # ── Emphasize W_dir (bold + larger), dim other W nodes ──────────────
        dim = 0.18
        scale_up = 1.28
        self.play(
            Wdir_c.animate.scale(scale_up).set_stroke(width=6.0),
            Wdir_l.animate.scale(scale_up).set_stroke(width=1.2, opacity=1.0),
            Wind_c.animate.set_opacity(dim),
            Wind_l.animate.set_opacity(dim),
            Wprox_c.animate.set_opacity(dim),
            Wprox_l.animate.set_opacity(dim),
            Wcc_c.animate.set_opacity(dim),
            Wcc_l.animate.set_opacity(dim),
            arr_WindWdir.animate.set_opacity(dim),
            arr_WindWcc.animate.set_opacity(dim),
            arr_WdirWprox.animate.set_opacity(dim),
            run_time=0.9,
        )
        self.wait(0.4)
        self.next_slide()

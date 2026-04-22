from manim import *
from manim_slides import Slide
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np
from PIL import Image as PILImage

GHANA_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "ghana")


def _square_image(path):
    """Center-crop image to a square, save to temp PNG, return the temp path."""
    img = PILImage.open(path).convert("RGBA")
    arr = np.array(img)
    h, w = arr.shape[:2]
    s = min(h, w)
    y0, x0 = (h - s) // 2, (w - s) // 2
    cropped = arr[y0:y0 + s, x0:x0 + s]
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    PILImage.fromarray(cropped).save(tmp.name)
    return tmp.name


class S13DAG(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ─────────────────────────────────────────────────────────────────────
        # Recreate s12 end state statically (title + chat + prompt + images)
        # ─────────────────────────────────────────────────────────────────────
        motiv_title = Text("Motivation: Humanitarian Program",
                           t2s={"Humanitarian Program": ITALIC},
                           color=WHITE_TEXT).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        # ── ChatGPT box — dark mode (same dims as s12) ───────────────────────
        _BXW  = 9.0
        _BXH  = _BXW / 5.41
        _BXCR = _BXH * 0.18
        _SEP  = 0.667

        _CTXT = "#E8E8E8"
        _CGRY = "#9A9A9A"
        _CBLU = "#8AB4F8"
        _CBDR = "#4A4A4A"
        _CSEP = "#4A4A4A"
        _CBGF = "#303030"

        chat_box = RoundedRectangle(
            width=_BXW, height=_BXH, corner_radius=_BXCR,
            fill_color=_CBGF, fill_opacity=1,
            stroke_color=_CBDR, stroke_width=1.2,
        ).move_to([0, 1.85, 0])

        _BXL = chat_box.get_left()[0]
        _BXR = chat_box.get_right()[0]
        _BXT = chat_box.get_top()[1]
        _BXB = chat_box.get_bottom()[1]

        _sy = _BXT - _SEP * _BXH
        chat_sep = Line(
            [_BXL + 0.06, _sy, 0], [_BXR - 0.06, _sy, 0],
            color=_CSEP, stroke_width=0.7,
        )
        _by = (_sy + _BXB) / 2

        _pl = 0.09
        chat_plus = VGroup(
            Line([0, -_pl, 0], [0, _pl, 0], color=_CGRY, stroke_width=1.6),
            Line([-_pl, 0, 0], [_pl, 0, 0], color=_CGRY, stroke_width=1.6),
        ).move_to([_BXL + 0.043 * _BXW, _by, 0])

        _er = _BXH * 0.055
        _ex = _BXL + 0.100 * _BXW
        et_circ = Circle(radius=_er, color=_CBLU, stroke_width=1.4, fill_opacity=0
                         ).move_to([_ex, _by, 0])
        et_hand1 = Line([_ex, _by, 0], [_ex, _by + _er * 0.60, 0],
                        color=_CBLU, stroke_width=1.4)
        _h2x = _ex + _er * 0.42 * np.sin(np.radians(60))
        _h2y = _by + _er * 0.42 * np.cos(np.radians(60))
        et_hand2 = Line([_ex, _by, 0], [_h2x, _h2y, 0],
                        color=_CBLU, stroke_width=1.4)
        et_clock = VGroup(et_circ, et_hand1, et_hand2)
        et_lbl = Text("Extended thinking", color=_CBLU, font="Helvetica Neue").scale(0.22)
        et_lbl.next_to(et_clock, RIGHT, buff=_BXW * 0.010).set_y(_by)
        _chev_h = et_lbl.height * 0.38
        _chev_w = _chev_h * 0.9
        et_chev = VGroup(
            Line([-_chev_w, _chev_h * 0.5, 0], ORIGIN, color=_CBLU, stroke_width=1.2),
            Line([_chev_w, _chev_h * 0.5, 0],  ORIGIN, color=_CBLU, stroke_width=1.2),
        )
        et_chev.next_to(et_lbl, RIGHT, buff=_BXW * 0.005).set_y(_by)
        et_pill = VGroup(et_clock, et_lbl, et_chev)

        _mx = _BXL + 0.900 * _BXW
        _mr = _BXH * 0.035
        mic_body = RoundedRectangle(
            width=_mr * 2, height=_mr * 3.4, corner_radius=_mr,
            stroke_color=_CGRY, stroke_width=1.2, fill_opacity=0,
        ).move_to([_mx, _by + _mr * 0.7, 0])
        mic_arc = Arc(
            radius=_mr * 1.65,
            start_angle=-PI * 0.17, angle=-(PI * 0.66),
            color=_CGRY, stroke_width=1.2,
        ).move_to([_mx, mic_body.get_bottom()[1] - _mr * 0.10, 0])
        _mbot = mic_arc.get_bottom()[1]
        mic_stem = Line([_mx, _mbot, 0], [_mx, _mbot - _mr * 0.85, 0],
                        color=_CGRY, stroke_width=1.2)
        mic_base = Line(
            [_mx - _mr * 0.9, mic_stem.get_end()[1], 0],
            [_mx + _mr * 0.9, mic_stem.get_end()[1], 0],
            color=_CGRY, stroke_width=1.2,
        )
        mic_icon = VGroup(mic_body, mic_arc, mic_stem, mic_base)

        _snx = _BXL + 0.963 * _BXW
        _snr = _BXH * 0.088
        snd_bg = Circle(radius=_snr, fill_color="#FFFFFF", fill_opacity=1, stroke_opacity=0
                        ).move_to([_snx, _by, 0])
        _aw = _snr * 0.34
        _atop = _by + _snr * 0.45
        _abot = _by - _snr * 0.45
        _amid = _by + _snr * 0.05
        snd_shaft = Line([_snx, _abot, 0], [_snx, _atop, 0],
                         color=_CBGF, stroke_width=2.2)
        snd_head = VGroup(
            Line([_snx - _aw, _amid, 0], [_snx, _atop, 0], color=_CBGF, stroke_width=2.2),
            Line([_snx + _aw, _amid, 0], [_snx, _atop, 0], color=_CBGF, stroke_width=2.2),
        )
        snd_btn = VGroup(snd_bg, snd_shaft, snd_head)

        chat_toolbar = VGroup(chat_sep, chat_plus, et_pill, mic_icon, snd_btn)
        chat_shell = VGroup(chat_box, chat_toolbar)

        PROMPT = (
            "How is the impact of a cash transfers program varying between recipients?\n"
            "I have some hypotheses but unsure if exhaustive. See data in attachment."
        )
        prompt_mob = Text(PROMPT, color=_CTXT, font="Helvetica Neue",
                          font_size=30, line_spacing=1.20)
        _max_w = 0.909 * _BXW
        if prompt_mob.width > _max_w:
            prompt_mob.set_width(_max_w)
        prompt_mob.align_to([_BXL + 0.031 * _BXW, 0, 0], LEFT)
        prompt_mob.align_to([0, _BXT - 0.153 * _BXH, 0], UP)

        # ── Three square images with captions ────────────────────────────────
        _IMG_H = 2.6
        img_pre = ImageMobject(_square_image(
            os.path.join(GHANA_DIR, "pre-treatment.jpg"))).scale_to_fit_height(_IMG_H)
        img_trt = ImageMobject(_square_image(
            os.path.join(GHANA_DIR, "treatment.jpg"))).scale_to_fit_height(_IMG_H)
        img_eff = ImageMobject(_square_image(
            os.path.join(GHANA_DIR, "effect.png"))).scale_to_fit_height(_IMG_H)

        lbl_pre = Text("pre-treatment observation", color=GRAY_TEXT).scale(0.28)
        lbl_trt = Text("treatment",                  color=GRAY_TEXT).scale(0.28)
        lbl_eff = Text("affected outcome",           color=GRAY_TEXT).scale(0.28)

        col_pre = Group(img_pre, lbl_pre).arrange(DOWN, buff=0.14)
        col_trt = Group(img_trt, lbl_trt).arrange(DOWN, buff=0.14)
        col_eff = Group(img_eff, lbl_eff).arrange(DOWN, buff=0.14)
        imgs = Group(col_pre, col_trt, col_eff).arrange(RIGHT, buff=0.6).move_to([0, -1.3, 0])
        col_trt.align_to(col_pre, UP)
        col_eff.align_to(col_pre, UP)

        self.add(motiv_title, chat_shell, prompt_mob, imgs)

        # ─────────────────────────────────────────────────────────────────────
        # Animation 1: transition to DAG (T→Y, X→Y)
        # ─────────────────────────────────────────────────────────────────────
        r, fs = 0.48, 0.62
        # Positions match s14 3x3 grid: T=pos2, Y=pos3, X initial=pos5 (future W_dir)
        T_pos = np.array([ 0.0,  1.8, 0])   # s14 pos 2
        Y_pos = np.array([ 3.0,  1.8, 0])   # s14 pos 3
        X_pos = np.array([ 0.0, -0.3, 0])   # s14 pos 5 (future W_dir)

        # Title with "Exploratory" dimmed (matching s04 pattern)
        eci_title = Text("Exploratory Causal Inference",
                         color=WHITE_TEXT).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        eci_title[:11].set_opacity(0.25)

        T_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(T_pos)
        Y_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(Y_pos)
        X_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(X_pos)
        T_l = MathTex("T", color=WHITE_TEXT).scale(fs).move_to(T_c)
        Y_l = MathTex("Y", color=WHITE_TEXT).scale(fs).move_to(Y_c)
        X_l = MathTex("X", color=WHITE_TEXT).scale(fs).move_to(X_c)

        arr_TY = Arrow(
            T_c.get_right() + RIGHT * 0.08,
            Y_c.get_left()  + LEFT  * 0.08,
            color=WHITE_TEXT, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        _dir_xy = (Y_pos - X_pos) / np.linalg.norm(Y_pos - X_pos)
        arr_XY = Arrow(
            X_pos + _dir_xy * (r + 0.08),
            Y_pos - _dir_xy * (r + 0.08),
            color=WHITE_TEXT, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )

        # Step 1: fade out chat + prompt + captions, transform title
        self.play(
            FadeOut(chat_shell), FadeOut(prompt_mob),
            FadeOut(lbl_pre), FadeOut(lbl_trt), FadeOut(lbl_eff),
            ReplacementTransform(motiv_title, eci_title),
            run_time=0.6,
        )

        # Step 2: shrink images to DAG node positions
        _NODE_IMG_H = 1.5
        self.play(
            img_pre.animate.scale_to_fit_height(_NODE_IMG_H).move_to(X_pos),
            img_trt.animate.scale_to_fit_height(_NODE_IMG_H).move_to(T_pos),
            img_eff.animate.scale_to_fit_height(_NODE_IMG_H).move_to(Y_pos),
            run_time=0.9,
        )

        # Step 3: dim images with BG overlay, grow DAG nodes on top
        _ghost_op = 0.18
        _ov_op    = 1 - _ghost_op

        rect_x = Rectangle(width=_NODE_IMG_H, height=_NODE_IMG_H,
                           fill_color=BG, fill_opacity=0, stroke_width=0).move_to(X_pos)
        rect_t = Rectangle(width=_NODE_IMG_H, height=_NODE_IMG_H,
                           fill_color=BG, fill_opacity=0, stroke_width=0).move_to(T_pos)
        rect_y = Rectangle(width=_NODE_IMG_H, height=_NODE_IMG_H,
                           fill_color=BG, fill_opacity=0, stroke_width=0).move_to(Y_pos)
        self.add(rect_x, rect_t, rect_y)

        self.play(
            rect_x.animate.set_fill(opacity=_ov_op),
            rect_t.animate.set_fill(opacity=_ov_op),
            rect_y.animate.set_fill(opacity=_ov_op),
            LaggedStart(
                AnimationGroup(GrowFromCenter(T_c), FadeIn(T_l)),
                AnimationGroup(GrowFromCenter(Y_c), FadeIn(Y_l)),
                AnimationGroup(GrowFromCenter(X_c), FadeIn(X_l)),
                lag_ratio=0.25,
            ),
            run_time=1.5,
        )
        self.play(Create(arr_TY), Create(arr_XY), run_time=0.7)
        self.wait(0.4)
        self.next_slide()

        # ─────────────────────────────────────────────────────────────────────
        # Animation 2: reveal "Exploratory" + subtitle,
        #              relabel X → ?, add new X above, arrow ? → X
        # ─────────────────────────────────────────────────────────────────────
        eci_subtitle = Text("Direct Effect Modifiers Identification",
                            color=GRAY_TEXT).scale(BODY_SCALE * 0.9
                            ).next_to(eci_title, DOWN, buff=0.2)
        eci_subtitle.set_opacity(0)
        self.add(eci_subtitle)

        # New X node below at s14 pos 8, arrow ? → X
        X_new_pos = np.array([0.0, -2.4, 0])
        X_new_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(X_new_pos)
        X_new_l = MathTex("X", color=WHITE_TEXT).scale(fs).move_to(X_new_c)

        _dir_qx = (X_new_pos - X_pos) / np.linalg.norm(X_new_pos - X_pos)
        arr_QX = Arrow(
            X_pos + _dir_qx * (r + 0.08),
            X_new_pos - _dir_qx * (r + 0.08),
            color=WHITE_TEXT, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )

        # "?" label replaces "X" at the current X_pos (in gray, matching s04)
        q_X = MathTex("?", color=GRAY_TEXT).scale(fs).move_to(X_c)

        self.play(
            eci_title[:11].animate.set_opacity(1),
            eci_subtitle.animate.set_opacity(1),
            img_pre.animate.move_to(X_new_pos),
            rect_x.animate.move_to(X_new_pos),
            ReplacementTransform(X_l, q_X),
            AnimationGroup(GrowFromCenter(X_new_c), FadeIn(X_new_l)),
            Create(arr_QX),
            run_time=1.4,
        )
        self.wait(0.5)
        self.next_slide()

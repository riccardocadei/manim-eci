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


class S12Motivation(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Slide: title + ChatGPT prompt + images ────────────────────────────

        motiv_title = Text("Motivation: Humanitarian Program",
                           t2s={"Humanitarian Program": ITALIC},
                           color=WHITE_TEXT).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        self.play(Write(motiv_title), run_time=0.8)
        self.wait(0.3)
        self.next_slide()

        # ── ChatGPT box — dark mode ──────────────────────────────────────────
        _BXW  = 9.0
        _BXH  = _BXW / 5.41
        _BXCR = _BXH * 0.18
        _SEP  = 0.667

        _CTXT = "#E8E8E8"       # light text on dark bg
        _CGRY = "#9A9A9A"       # toolbar icon gray
        _CBLU = "#8AB4F8"       # "Extended thinking" blue
        _CBDR = "#4A4A4A"       # subtle border
        _CSEP = "#4A4A4A"       # separator line
        _CBGF = "#303030"       # box fill

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

        # "+" icon — two thin crossed lines
        _pl = 0.09
        chat_plus = VGroup(
            Line([0, -_pl, 0], [0, _pl, 0], color=_CGRY, stroke_width=1.6),
            Line([-_pl, 0, 0], [_pl, 0, 0], color=_CGRY, stroke_width=1.6),
        ).move_to([_BXL + 0.043 * _BXW, _by, 0])

        # Extended thinking icon — clock face (circle + two hands)
        _er = _BXH * 0.055
        _ex = _BXL + 0.100 * _BXW
        et_circ = Circle(
            radius=_er, color=_CBLU, stroke_width=1.4, fill_opacity=0,
        ).move_to([_ex, _by, 0])
        et_hand1 = Line(
            [_ex, _by, 0], [_ex, _by + _er * 0.60, 0],
            color=_CBLU, stroke_width=1.4,
        )
        _h2x = _ex + _er * 0.42 * np.sin(np.radians(60))
        _h2y = _by + _er * 0.42 * np.cos(np.radians(60))
        et_hand2 = Line(
            [_ex, _by, 0], [_h2x, _h2y, 0],
            color=_CBLU, stroke_width=1.4,
        )
        et_clock = VGroup(et_circ, et_hand1, et_hand2)
        et_lbl = Text(
            "Extended thinking", color=_CBLU, font="Helvetica Neue",
        ).scale(0.22)
        et_lbl.next_to(et_clock, RIGHT, buff=_BXW * 0.010).set_y(_by)
        _chev_h = et_lbl.height * 0.38
        _chev_w = _chev_h * 0.9
        et_chev = VGroup(
            Line([-_chev_w, _chev_h * 0.5, 0], ORIGIN, color=_CBLU, stroke_width=1.2),
            Line([_chev_w, _chev_h * 0.5, 0],  ORIGIN, color=_CBLU, stroke_width=1.2),
        )
        et_chev.next_to(et_lbl, RIGHT, buff=_BXW * 0.005).set_y(_by)
        et_pill = VGroup(et_clock, et_lbl, et_chev)

        # Microphone icon
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
        mic_stem = Line(
            [_mx, _mbot, 0], [_mx, _mbot - _mr * 0.85, 0],
            color=_CGRY, stroke_width=1.2,
        )
        mic_base = Line(
            [_mx - _mr * 0.9, mic_stem.get_end()[1], 0],
            [_mx + _mr * 0.9, mic_stem.get_end()[1], 0],
            color=_CGRY, stroke_width=1.2,
        )
        mic_icon = VGroup(mic_body, mic_arc, mic_stem, mic_base)

        # Send button — white circle with up-arrow (↑)
        _snx = _BXL + 0.963 * _BXW
        _snr = _BXH * 0.088
        snd_bg = Circle(
            radius=_snr, fill_color="#FFFFFF", fill_opacity=1, stroke_opacity=0,
        ).move_to([_snx, _by, 0])
        _aw = _snr * 0.34
        _atop = _by + _snr * 0.45
        _abot = _by - _snr * 0.45
        _amid = _by + _snr * 0.05
        snd_shaft = Line(
            [_snx, _abot, 0], [_snx, _atop, 0],
            color=_CBGF, stroke_width=2.2,
        )
        snd_head = VGroup(
            Line([_snx - _aw, _amid, 0],
                 [_snx, _atop, 0], color=_CBGF, stroke_width=2.2),
            Line([_snx + _aw, _amid, 0],
                 [_snx, _atop, 0], color=_CBGF, stroke_width=2.2),
        )
        snd_btn = VGroup(snd_bg, snd_shaft, snd_head)

        chat_toolbar = VGroup(chat_sep, chat_plus, et_pill, mic_icon, snd_btn)

        PROMPT = (
            "How is the impact of a cash transfers program varying between recipients?\n"
            "I have some hypotheses but unsure if exhaustive. See data in attachment."
        )
        prompt_mob = Text(
            PROMPT, color=_CTXT,
            font="Helvetica Neue", font_size=30,
            line_spacing=1.20,
        )
        _max_w = 0.909 * _BXW
        if prompt_mob.width > _max_w:
            prompt_mob.set_width(_max_w)
        prompt_mob.align_to([_BXL + 0.031 * _BXW, 0, 0], LEFT)
        prompt_mob.align_to([0, _BXT - 0.153 * _BXH, 0], UP)

        chat_shell = VGroup(chat_box, chat_toolbar)

        # Box appears + typing animation
        self.play(FadeIn(chat_shell), run_time=0.7)
        self.wait(0.3)
        self.play(AddTextLetterByLetter(prompt_mob, time_per_char=0.035),
                  run_time=3.5)
        self.wait(0.5)
        self.next_slide()

        # ── Three square images appear below the ChatGPT box ─────────────────
        _IMG_H = 2.6

        img_pre = ImageMobject(_square_image(
            os.path.join(GHANA_DIR, "pre-treatment.jpg")
        )).scale_to_fit_height(_IMG_H)
        img_trt = ImageMobject(_square_image(
            os.path.join(GHANA_DIR, "treatment.jpg")
        )).scale_to_fit_height(_IMG_H)
        img_eff = ImageMobject(_square_image(
            os.path.join(GHANA_DIR, "effect.png")
        )).scale_to_fit_height(_IMG_H)

        lbl_pre = Text("pre-treatment observation", color=GRAY_TEXT).scale(0.28)
        lbl_trt = Text("treatment",                  color=GRAY_TEXT).scale(0.28)
        lbl_eff = Text("affected outcome",           color=GRAY_TEXT).scale(0.28)

        col_pre = Group(img_pre, lbl_pre).arrange(DOWN, buff=0.14)
        col_trt = Group(img_trt, lbl_trt).arrange(DOWN, buff=0.14)
        col_eff = Group(img_eff, lbl_eff).arrange(DOWN, buff=0.14)
        imgs = Group(col_pre, col_trt, col_eff).arrange(RIGHT, buff=0.6).move_to([0, -1.3, 0])
        # Force top-alignment across the three image columns
        col_trt.align_to(col_pre, UP)
        col_eff.align_to(col_pre, UP)

        self.play(FadeIn(imgs), run_time=0.9)
        self.wait(0.6)
        self.next_slide()

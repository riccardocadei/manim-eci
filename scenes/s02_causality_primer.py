from manim import *
from manim_slides import Slide
import sys, os, glob as _glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np
from PIL import Image as PILImage

ANTS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "ants")
TFRAMES  = os.path.join(ANTS_DIR, "treatment_frames")
EFRAMES  = os.path.join(ANTS_DIR, "effect_frames")

_W  = WHITE_TEXT
_Q  = GRAY_TEXT    # colour for unobserved "?"
_S  = 0.48         # math header scale
_CW = 1.30         # column width
_RH = 0.46         # row height

xs6 = [(j - 2.5) * _CW for j in range(6)]

YTBL      = 1.90
SEP_HDR_Y = 1.55
SEP_BOT_Y = -1.25

X_LEFT = xs6[0] - 0.55
X_R5   = xs6[4] + 0.55
X_R6   = xs6[5] + 0.55

COMMENT_Y = 2.83


# ── Emoji ──────────────────────────────────────────────────────────────────────

def _emoji(char, height=0.5):
    import AppKit
    path = f"/tmp/_manim_emoji_{ord(char[0])}_hq.png"
    if not os.path.exists(path):
        SZ   = 300
        font = AppKit.NSFont.systemFontOfSize_(SZ * 0.80)
        attrs = {AppKit.NSFontAttributeName: font}
        astr = AppKit.NSAttributedString.alloc().initWithString_attributes_(char, attrs)
        img  = AppKit.NSImage.alloc().initWithSize_((SZ + 30, SZ + 30))
        img.lockFocus(); astr.drawAtPoint_((15, 15)); img.unlockFocus()
        tiff = img.TIFFRepresentation()
        bmp  = AppKit.NSBitmapImageRep.imageRepWithData_(tiff)
        png  = bmp.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, None)
        png.writeToFile_atomically_(path, True)
    return ImageMobject(path).scale_to_fit_height(height)


# ── VideoPlayer ────────────────────────────────────────────────────────────────

class VideoPlayer(ImageMobject):
    def __init__(self, frames_dir, fps=10, **kwargs):
        paths = sorted(_glob.glob(os.path.join(frames_dir, "frame_*.png")))
        self._arrays = [np.array(PILImage.open(p).convert("RGBA")) for p in paths]
        self._fps = fps
        self._nf  = len(self._arrays)
        super().__init__(paths[0], **kwargs)

    def set_time(self, t):
        self.pixel_array = self._arrays[int(t * self._fps) % self._nf]
        return self


# ── Table helpers ──────────────────────────────────────────────────────────────

def _hdr(tex, col_idx, color=None):
    return MathTex(tex, color=color or _W).scale(_S).move_to([xs6[col_idx], YTBL, 0])

def _sep_h(y, x_l=X_LEFT, x_r=X_R5):
    return Line([x_l, y, 0], [x_r, y, 0], color=DIM_GRAY, stroke_width=1)

def _cell(tex, col_idx, row_idx, color=None):
    y = SEP_HDR_Y - (row_idx + 0.5) * _RH
    return MathTex(tex, color=color or _W).scale(_S * 0.86).move_to([xs6[col_idx], y, 0])

def _row_y(ri):
    return SEP_HDR_Y - (ri + 0.5) * _RH


# ── DAG helper ─────────────────────────────────────────────────────────────────

def _make_dag(r=0.48, fs=0.62):
    T_c = Circle(radius=r, color=_W, stroke_width=3.5).move_to(LEFT * 2.1)
    Y_c = Circle(radius=r, color=_W, stroke_width=3.5).move_to(RIGHT * 2.1)
    T_l = MathTex("T", color=_W).scale(fs).move_to(T_c)
    Y_l = MathTex("Y", color=_W).scale(fs).move_to(Y_c)
    arr = Arrow(
        T_c.get_right() + RIGHT * 0.08,
        Y_c.get_left()  + LEFT  * 0.08,
        color=_W, buff=0, stroke_width=5,
        max_tip_length_to_length_ratio=0.18,
    )
    q = MathTex("?", color=_W).scale(fs * 1.10).next_to(arr, UP, buff=0.12)
    return VGroup(T_c, T_l, Y_c, Y_l, arr, q)


# ── Scene ──────────────────────────────────────────────────────────────────────

class S02CausalityPrimer(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Slide 2: title + ChatGPT prompt + GIFs ──────────────────────────────

        motiv_title = Text("Motivation: Social Immunity",
                           t2s={"Social Immunity": ITALIC},
                           color=_W).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        self.play(Write(motiv_title), run_time=0.8)
        self.wait(0.3)

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
        # minute hand: center → 12 o'clock
        et_hand1 = Line(
            [_ex, _by, 0], [_ex, _by + _er * 0.60, 0],
            color=_CBLU, stroke_width=1.4,
        )
        # hour hand: center → ~2 o'clock
        et_hand2 = Line(
            [_ex, _by, 0],
            [_ex + _er * 0.42 * np.cos(np.radians(60)),
             _by + _er * 0.42 * np.sin(np.radians(60)) * (-1) + _er * 0.42 * np.sin(np.radians(30)),
             0],
            color=_CBLU, stroke_width=1.4,
        )
        # simpler: hand pointing to ~2 o'clock = 60° from 12 = angle 30° from horizontal-right
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
        # "v" chevron — match x-height of "Extended thinking" text
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
        _aw = _snr * 0.34   # arrowhead half-width
        _atop = _by + _snr * 0.45   # arrow tip
        _abot = _by - _snr * 0.45   # shaft bottom
        _amid = _by + _snr * 0.05   # arrowhead base
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
            "What is the social effect of a pathogen exposure? "
            "I have some hypotheses but unsure if exhaustive.\n"
            "See experiment in attachment."
        )
        prompt_mob = Text(
            PROMPT, color=_CTXT,
            font="Helvetica Neue", font_size=30,
            line_spacing=1.20,
        )
        prompt_mob.set_width(0.909 * _BXW)
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

        # ── GIFs appear below the ChatGPT box ────────────────────────────────
        fps, n_frames = 10, 40
        duration = n_frames / fps
        n_loops  = 4

        vid_t = VideoPlayer(TFRAMES, fps=fps).scale_to_fit_height(2.8)
        vid_e = VideoPlayer(EFRAMES, fps=fps).scale_to_fit_height(2.8)
        lbl_t = Text("treatment",                  color=GRAY_TEXT).scale(0.28)
        lbl_e = Text("post-treatment observation", color=GRAY_TEXT).scale(0.28)
        col_t = Group(vid_t, lbl_t).arrange(DOWN, buff=0.14)
        col_e = Group(vid_e, lbl_e).arrange(DOWN, buff=0.14)
        vids  = Group(col_t, col_e).arrange(RIGHT, buff=0.8).move_to([0, -1.2, 0])

        tracker = ValueTracker(0)
        upd_t = lambda m: m.set_time(tracker.get_value())
        upd_e = lambda m: m.set_time(tracker.get_value())
        vid_t.add_updater(upd_t)
        vid_e.add_updater(upd_e)

        self.play(FadeIn(vids), run_time=0.8)
        self.play(tracker.animate.set_value(n_loops * duration),
                  run_time=n_loops * duration, rate_func=linear)
        vid_t.clear_updaters()
        vid_e.clear_updaters()
        self.next_slide()

        # ── Slide 3: GIFs replaced by DAG at same position (ChatGPT stays) ──
        dag = _make_dag()
        dag.move_to(vids)
        self.play(
            FadeOut(vids),
            FadeIn(dag),
            run_time=1.0,
        )
        self.wait(0.8)
        self.next_slide()

        # ── Slide 4: ChatGPT removed, title → "Primer: Causal Inference",
        #             DAG → top-right + table/equations ───────────────────────
        h_i  = _hdr(r"i",       0)
        h_Ti = _hdr(r"T_i",     1)
        h_Yi = _hdr(r"Y_i",     2)
        h_Y1 = _hdr(r"Y_i(1)", 3)
        h_Y0 = _hdr(r"Y_i(0)", 4)
        hdr3 = VGroup(h_i, h_Ti, h_Yi)

        X_R3 = xs6[2] + 0.55   # right edge after Y_i column

        # separators: start narrow (3 cols), extend to 5 when pot. outcomes appear
        sep_top   = _sep_h(YTBL + 0.32, X_LEFT, X_R3)
        sep_mid   = _sep_h(SEP_HDR_Y,   X_LEFT, X_R3)
        sep_top_5 = _sep_h(YTBL + 0.32, X_LEFT, X_R5)
        sep_mid_5 = _sep_h(SEP_HDR_Y,   X_LEFT, X_R5)

        pot_out_lbl = Text("potential outcomes", color=GRAY_TEXT).scale(0.24)
        pot_out_lbl.move_to([(xs6[3] + xs6[4]) / 2, YTBL + 0.62, 0])

        sep_top_full = _sep_h(YTBL + 0.32, X_LEFT, X_R5)
        exp_lbl = Text("Experiment:", color=GRAY_TEXT).scale(0.36)
        exp_lbl.next_to(sep_top_full, UP, buff=0.10).align_to(sep_top_full, LEFT)

        # New title
        title = Text("Primer: Causal Inference",
                     t2s={"Causal Inference": ITALIC},
                     color=_W).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        self.play(
            FadeOut(chat_shell), FadeOut(prompt_mob),
            ReplacementTransform(motiv_title, title),
            dag.animate.scale(0.52).move_to([5.6, 3.3, 0]),
            run_time=0.8,
        )

        # Step 1 ── "Experiment:" label alone
        self.play(FadeIn(exp_lbl, shift=UP * 0.06), run_time=0.4)
        self.wait(0.2)

        # Step 2 ── core headers (i, T_i, Y_i) + narrow separators
        self.play(FadeIn(hdr3), FadeIn(sep_top), FadeIn(sep_mid), run_time=0.5)
        self.wait(0.2)

        # rows_data: (T_i, Y_i, (Y_i(1)_val, Y_i(1)_col), (Y_i(0)_val, Y_i(0)_col))
        rows_data = [
            ("1", "1", ("1",  _W), (r"?", _Q)),   # treated, Y=1
            ("0", "1", (r"?", _Q), ("1",  _W)),   # control,  Y=1 (recovered without treatment)
            ("1", "0", ("0",  _W), (r"?", _Q)),   # treated, Y=0 (treatment didn't help)
            ("0", "0", (r"?", _Q), ("0",  _W)),   # control,  Y=0
            ("0", "1", (r"?", _Q), ("1",  _W)),   # control,  Y=1
        ]

        # original colour per (row, col) for later restoration
        def orig_col(col_idx, ri):
            if col_idx in (0, 1, 2):
                return _W
            elif col_idx == 3:
                return rows_data[ri][2][1]
            else:
                return rows_data[ri][3][1]

        row_mobs  = []
        sep_rows  = []   # narrow (3-col) versions live in scene
        sep_rows5 = []   # full (5-col) targets for later Transform
        dots_5 = VGroup(*[
            MathTex(r"\vdots", color=_W).scale(_S * 0.75).move_to([xs6[j], _row_y(5), 0])
            for j in range(5)
        ])

        # Step 3 ── rows appear one by one, core columns only
        for ri, (ti, yi, (y1v, y1c), (y0v, y0c)) in enumerate(rows_data):
            row = VGroup(
                _cell(str(ri + 1), 0, ri),
                _cell(ti,          1, ri),
                _cell(yi,          2, ri),
                _cell(y1v,         3, ri, y1c),
                _cell(y0v,         4, ri, y0c),
            )
            sr3 = _sep_h(_row_y(ri) - _RH / 2, X_LEFT, X_R3)
            sr5 = _sep_h(_row_y(ri) - _RH / 2, X_LEFT, X_R5)
            row_mobs.append(row)
            sep_rows.append(sr3)
            sep_rows5.append(sr5)

            core = VGroup(row[0], row[1], row[2])
            self.play(FadeIn(core), FadeIn(sr3), run_time=0.4)
            self.wait(0.35)

        # dots appear on their own after all rows
        self.play(FadeIn(VGroup(dots_5[0], dots_5[1], dots_5[2])), run_time=0.4)
        self.wait(0.35)

        self.next_slide()

        # Step 4 ── potential outcomes columns + extend separators
        self.play(
            Transform(sep_top, sep_top_5),
            Transform(sep_mid, sep_mid_5),
            *[Transform(sep_rows[ri], sep_rows5[ri]) for ri in range(5)],
            FadeIn(h_Y1), FadeIn(h_Y0),
            FadeIn(pot_out_lbl, shift=DOWN * 0.06),
            *[FadeIn(VGroup(row[3], row[4])) for row in row_mobs],
            FadeIn(VGroup(dots_5[3], dots_5[4])),
            run_time=0.7,
        )
        self.wait(0.4)

        self.next_slide()

        # ── τ_i column: PO names then entries move into ITE ──────────────────────
        h_tau = MathTex(r"\tau_i = Y_i(1) - Y_i(0)", color=_W).scale(_S)
        h_tau.move_to([xs6[5], YTBL, 0])

        sep_top_6  = _sep_h(YTBL + 0.32, X_LEFT, X_R6)
        sep_mid_6  = _sep_h(SEP_HDR_Y,   X_LEFT, X_R6)
        sep_rows_6 = [_sep_h(_row_y(ri) - _RH / 2, X_LEFT, X_R6) for ri in range(5)]

        causal_eff_lbl = Text("causal effect", color=GRAY_TEXT).scale(0.24)
        causal_eff_lbl.move_to([xs6[5], YTBL + 0.62, 0])

        _HDR_EM = 1.35   # header emphasis scale
        _CEL_EM = 1.30   # cell emphasis scale

        # Step A: seps extend
        self.play(
            Transform(sep_top, sep_top_6),
            Transform(sep_mid, sep_mid_6),
            *[Transform(sep_rows[ri], sep_rows_6[ri]) for ri in range(5)],
            run_time=0.5,
        )

        # Step B: column names scale up in place
        self.play(
            h_Y1.animate.scale(_HDR_EM),
            h_Y0.animate.scale(_HDR_EM),
            run_time=0.3,
        )
        # Step C: column names scale back to normal
        self.play(
            h_Y1.animate.scale(1 / _HDR_EM),
            h_Y0.animate.scale(1 / _HDR_EM),
            run_time=0.25,
        )

        # Step D: copies fly to τ_i, h_tau appears
        hdr_Y1_copy = h_Y1.copy()
        hdr_Y0_copy = h_Y0.copy()
        self.add(hdr_Y1_copy, hdr_Y0_copy)
        tgt_hdr = np.array([xs6[5], YTBL, 0])

        self.play(
            hdr_Y1_copy.animate.move_to(tgt_hdr).set_opacity(0),
            hdr_Y0_copy.animate.move_to(tgt_hdr).set_opacity(0),
            FadeIn(h_tau),
            FadeIn(causal_eff_lbl, shift=DOWN * 0.06),
            run_time=0.7,
        )
        self.wait(0.4)

        # Step D: entries scale up in place
        self.play(
            *[row_mobs[ri][3].animate.scale(_CEL_EM) for ri in range(5)],
            *[row_mobs[ri][4].animate.scale(_CEL_EM) for ri in range(5)],
            run_time=0.35,
        )

        # Step F: entries scale back to normal
        self.play(
            *[row_mobs[ri][3].animate.scale(1 / _CEL_EM) for ri in range(5)],
            *[row_mobs[ri][4].animate.scale(1 / _CEL_EM) for ri in range(5)],
            run_time=0.25,
        )

        # Step G: copies fly to τ_i rows, "?" appears
        tau_cells = VGroup(*[_cell(r"?", 5, ri, _Q) for ri in range(5)])
        tau_dots  = MathTex(r"\vdots", color=_Q).scale(_S * 0.75).move_to([xs6[5], _row_y(5), 0])

        col3_copies = VGroup(*[row_mobs[ri][3].copy() for ri in range(5)])
        col4_copies = VGroup(*[row_mobs[ri][4].copy() for ri in range(5)])
        self.add(col3_copies, col4_copies)

        fly_anims = []
        for ri in range(5):
            tgt = tau_cells[ri].get_center()
            fly_anims.append(col3_copies[ri].animate.move_to(tgt).set_opacity(0))
            fly_anims.append(col4_copies[ri].animate.move_to(tgt).set_opacity(0))

        self.play(
            *fly_anims,
            FadeIn(tau_cells),
            FadeIn(tau_dots, shift=LEFT * 0.2),
            run_time=0.9,
        )
        self.wait(0.4)
        self.next_slide()

        # ── ITE "?" entries converge into single big "?" ─────────────────────
        _q_center = np.array([xs6[5], _row_y(2), 0])   # vertical midpoint of rows
        big_q = MathTex(r"?", color=_Q).scale(_S * 4.5).move_to(_q_center)
        fpci_lbl = Text(
            "Foundamental Problem of Causal Inference",
            color=GRAY_TEXT,
        ).scale(0.44)
        fpci_lbl.move_to([0, SEP_BOT_Y - 0.70, 0])

        tau_copies = VGroup(*[tau_cells[ri].copy() for ri in range(5)])
        self.add(tau_copies)
        self.play(
            *[tau_copies[ri].animate.move_to(_q_center).set_opacity(0) for ri in range(5)],
            *[tau_cells[ri].animate.set_opacity(0) for ri in range(5)],
            tau_dots.animate.set_opacity(0),
            FadeIn(big_q),
            run_time=0.7,
        )
        self.play(FadeIn(fpci_lbl, shift=UP * 0.06), run_time=0.5)
        self.wait(0.5)
        self.next_slide()

        # restore: big "?" dissolves, individual cells return
        self.play(
            FadeOut(big_q), FadeOut(fpci_lbl),
            *[tau_cells[ri].animate.set_opacity(1) for ri in range(5)],
            tau_dots.animate.set_opacity(1),
            run_time=0.6,
        )

        # ── Define all three equation rows + labels upfront ──────────────────
        t1_rows = [ri for ri, (ti, *_) in enumerate(rows_data) if ti == "1"]
        t0_rows = [ri for ri, (ti, *_) in enumerate(rows_data) if ti == "0"]

        ate = MathTex(
            r"\tau", r"\;=\;",
            r"\mathbb{E}[Y_i(1)]", r"-", r"\mathbb{E}[Y_i(0)]",
            color=_W,
        ).scale(0.52)
        ate.move_to([0, -2.05, 0])
        ate.align_to([X_LEFT, 0, 0], LEFT)

        idt = MathTex(
            r"\phantom{\tau}", r"\;=\;",
            r"\mathbb{E}[Y_i \mid T_i=1]", r"-", r"\mathbb{E}[Y_i \mid T_i=0]",
            color=_W,
        ).scale(0.52)
        idt.next_to(ate, DOWN, buff=0.45)
        idt.shift(RIGHT * (ate[1].get_center()[0] - idt[1].get_center()[0]))

        est = MathTex(
            r"\phantom{\tau}", r"\;\approx\;",
            r"0.50", r"-", r"0.66", r"\;=\;", r"-0.16",
            color=_W,
        ).scale(0.52)
        est.next_to(idt, DOWN, buff=0.35)
        est.shift(RIGHT * (ate[1].get_center()[0] - est[1].get_center()[0]))

        # all equations start ghosted; only the final result is pre-coloured red
        _GHOST = 0.25
        ate.set_opacity(_GHOST)
        idt.set_opacity(_GHOST)
        est.set_opacity(_GHOST)
        # est[6] stays white – no special pre-colour

        # labels – same scale, aligned to the same x
        _LSCALE = 0.26
        causal_lbl = Text("(causal estimand)",      color=DIM_GRAY).scale(_LSCALE)
        stat_lbl   = Text("(statistical estimand)", color=DIM_GRAY).scale(_LSCALE)
        est_lbl    = Text("(statistical estimate)", color=DIM_GRAY).scale(_LSCALE)
        causal_lbl.next_to(ate, RIGHT, buff=0.28)
        stat_lbl.next_to(idt,   RIGHT, buff=0.28)
        est_lbl.next_to(est,    RIGHT, buff=0.28)
        lbl_x = max(causal_lbl.get_left()[0],
                    stat_lbl.get_left()[0],
                    est_lbl.get_left()[0]) + 0.4
        for lbl in [causal_lbl, stat_lbl, est_lbl]:
            lbl.align_to([lbl_x, 0, 0], LEFT)

        idt_section_lbl = Text("Average Treatment Effect:", color=GRAY_TEXT).scale(0.36)
        idt_section_lbl.next_to(ate, UP, buff=0.22).align_to(exp_lbl, LEFT)

        # ── All equations ghosted + labels ────────────────────────────────────
        self.play(
            FadeIn(ate), FadeIn(idt), FadeIn(est),
            FadeIn(causal_lbl), FadeIn(stat_lbl), FadeIn(est_lbl),
            FadeIn(idt_section_lbl),
            run_time=0.7,
        )
        self.wait(0.4)
        self.next_slide()

        # ── Step 1: row 1 white → E[Y_i(1)] blue → white ─────────────────────
        col_Y1_grp  = VGroup(*[row_mobs[ri][3] for ri in range(5)], dots_5[3])
        rect_col_E1 = SurroundingRectangle(col_Y1_grp, color=BLUE_LIGHT, buff=0.10, stroke_width=1.2)

        # 1a: ate → full white
        self.play(ate.animate.set_opacity(1), run_time=0.4)
        self.wait(0.15)

        # 1b: ate[2] → blue + term rect + column highlight
        rect_E1 = SurroundingRectangle(ate[2], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        self.play(
            ate[2].animate.set_color(BLUE_LIGHT),
            Create(rect_E1), Create(rect_col_E1),
            *[row_mobs[ri][3].animate.set_color(BLUE_LIGHT) for ri in range(5)],
            dots_5[3].animate.set_color(BLUE_LIGHT),
            run_time=0.4,
        )
        self.wait(0.3)

        # 1c: ate[2] → white, restore column
        self.play(
            ate[2].animate.set_color(_W),
            FadeOut(rect_E1), FadeOut(rect_col_E1),
            *[row_mobs[ri][3].animate.set_color(orig_col(3, ri)) for ri in range(5)],
            dots_5[3].animate.set_color(_W),
            run_time=0.45,
        )
        self.wait(0.35)

        # ── Step 2 (same slide): E[Y_i(0)] blue → white ──────────────────────
        col_Y0_grp  = VGroup(*[row_mobs[ri][4] for ri in range(5)], dots_5[4])
        rect_col_E0 = SurroundingRectangle(col_Y0_grp, color=BLUE_LIGHT, buff=0.10, stroke_width=1.2)

        # 2a: ate[4] → blue + term rect + column highlight
        rect_E0 = SurroundingRectangle(ate[4], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        self.play(
            ate[4].animate.set_color(BLUE_LIGHT),
            Create(rect_E0), Create(rect_col_E0),
            *[row_mobs[ri][4].animate.set_color(BLUE_LIGHT) for ri in range(5)],
            dots_5[4].animate.set_color(BLUE_LIGHT),
            run_time=0.5,
        )
        self.wait(0.35)

        # 2b: ate[4] → white, restore column
        self.play(
            ate[4].animate.set_color(_W),
            FadeOut(rect_E0), FadeOut(rect_col_E0),
            *[row_mobs[ri][4].animate.set_color(orig_col(4, ri)) for ri in range(5)],
            dots_5[4].animate.set_color(_W),
            run_time=0.45,
        )
        self.wait(0.25)
        self.next_slide()

        # ── Step 3: rows 2+3 white first, then E[Y|T=1] blue + box + aggregate ─

        # 3a: idt + est[0:5] → full white (est[5:7] stay ghosted)
        self.play(
            idt.animate.set_opacity(1),
            *[est[i].animate.set_opacity(1) for i in range(5)],
            run_time=0.5,
        )
        self.wait(0.3)

        # 3b: idt[2] → blue (start highlighting)
        self.play(
            idt[2].animate.set_color(BLUE_LIGHT),
            run_time=0.3,
        )
        self.wait(0.2)

        # 3c: box idt[2] term + box T=1 table cells
        rect_idt2 = SurroundingRectangle(idt[2], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        cell_rects_I1 = VGroup(*[
            SurroundingRectangle(row_mobs[ri][3], color=BLUE_LIGHT,
                                 buff=0.08, stroke_width=1.2)
            for ri in t1_rows
        ])
        self.play(
            Create(rect_idt2),
            *[row_mobs[ri][3].animate.set_color(BLUE_LIGHT) for ri in t1_rows],
            *[row_mobs[ri][3].animate.set_color(DIM_GRAY)   for ri in t0_rows],
            *[Create(r) for r in cell_rects_I1],
            run_time=0.35,
        )
        self.wait(0.1)

        # 3c: copies fly → est[2] blue; boxes out
        copies_T1 = VGroup(*[row_mobs[ri][3].copy() for ri in t1_rows])
        self.add(copies_T1)
        tgt_T1 = est[2].get_center()
        self.play(
            *[copies_T1[i].animate.move_to(tgt_T1).scale(0.4).set_opacity(0)
              for i in range(len(t1_rows))],
            est[2].animate.set_color(BLUE_LIGHT),
            FadeOut(rect_idt2), FadeOut(cell_rects_I1),
            run_time=0.5,
        )
        self.wait(0.15)

        # 3d: idt[2] → white, est[2] → white, cells restore
        self.play(
            idt[2].animate.set_color(_W),
            est[2].animate.set_color(_W),
            *[row_mobs[ri][3].animate.set_color(orig_col(3, ri)) for ri in t1_rows],
            *[row_mobs[ri][3].animate.set_color(orig_col(3, ri)) for ri in t0_rows],
            run_time=0.45,
        )
        self.wait(0.4)

        # ── Step 4 (same slide): E[Y|T=0] blue + box term + box cells
        #           → aggregate → est[4] blue → all white ─────────────────────

        # 4a: idt[4] → blue + box term
        rect_idt4 = SurroundingRectangle(idt[4], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        self.play(
            idt[4].animate.set_color(BLUE_LIGHT),
            Create(rect_idt4),
            run_time=0.3,
        )
        self.wait(0.2)

        # 4b: box T=0 table cells
        cell_rects_I0 = VGroup(*[
            SurroundingRectangle(row_mobs[ri][4], color=BLUE_LIGHT,
                                 buff=0.08, stroke_width=1.2)
            for ri in t0_rows
        ])
        self.play(
            *[row_mobs[ri][4].animate.set_color(BLUE_LIGHT) for ri in t0_rows],
            *[row_mobs[ri][4].animate.set_color(DIM_GRAY)   for ri in t1_rows],
            *[Create(r) for r in cell_rects_I0],
            run_time=0.35,
        )
        self.wait(0.1)

        # 4c: copies fly → est[4] blue + est[1,3] → white; boxes out
        copies_T0 = VGroup(*[row_mobs[ri][4].copy() for ri in t0_rows])
        self.add(copies_T0)
        tgt_T0 = est[4].get_center()
        self.play(
            *[copies_T0[i].animate.move_to(tgt_T0).scale(0.4).set_opacity(0)
              for i in range(len(t0_rows))],
            est[4].animate.set_color(BLUE_LIGHT),
            FadeOut(rect_idt4), FadeOut(cell_rects_I0),
            run_time=0.5,
        )
        self.wait(0.15)

        # 4d: idt[4] → white, est[4] → white, cells restore
        self.play(
            idt[4].animate.set_color(_W),
            est[4].animate.set_color(_W),
            *[row_mobs[ri][4].animate.set_color(orig_col(4, ri)) for ri in t0_rows],
            *[row_mobs[ri][4].animate.set_color(orig_col(4, ri)) for ri in t1_rows],
            run_time=0.35,
        )
        self.wait(0.3)
        self.next_slide()

        # ── Step 5: combine est[2]+est[4] → reveal -0.16 in red → white ──────

        # 5a: flash est[2] and est[4] blue (showing they are the inputs)
        self.play(
            est[2].animate.set_color(BLUE_LIGHT),
            est[4].animate.set_color(BLUE_LIGHT),
            run_time=0.3,
        )
        self.wait(0.2)

        # 5b: copies fly to -0.16 position; = and -0.16 emerge in BLUE
        copies_combine = VGroup(est[2].copy(), est[4].copy())
        self.add(copies_combine)
        tgt_diff = est[6].get_center()
        self.play(
            copies_combine[0].animate.move_to(tgt_diff).scale(0.4).set_opacity(0),
            copies_combine[1].animate.move_to(tgt_diff).scale(0.4).set_opacity(0),
            est[5].animate.set_opacity(1),
            est[6].animate.set_opacity(1).set_color(BLUE_LIGHT),
            run_time=0.5,
        )
        self.wait(0.3)

        # 5c: all settle to white
        self.play(
            est[2].animate.set_color(_W),
            est[4].animate.set_color(_W),
            est[6].animate.set_color(_W),
            run_time=0.45,
        )
        self.wait(0.4)
        self.next_slide()

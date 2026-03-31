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

        # ── Slide 1: title + definition ───────────────────────────────────────
        title = slide_title("Causal Inference — Primer")
        emoji = _emoji("🎯", height=0.38)
        defn_txt = Text("modelling the effect of real-world interventions",
                        color=_W).scale(0.36)
        defn = Group(emoji, defn_txt).arrange(RIGHT, buff=0.18)
        defn.next_to(title, DOWN, buff=0.28)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(defn, shift=UP * 0.08), run_time=0.6)
        self.wait(0.5)
        self.next_slide()

        # ── Slide 2: two gifs looping 4× ─────────────────────────────────────
        fps, n_frames = 10, 40
        duration = n_frames / fps
        n_loops  = 4

        vid_t = VideoPlayer(TFRAMES, fps=fps).scale_to_fit_height(3.2)
        vid_e = VideoPlayer(EFRAMES, fps=fps).scale_to_fit_height(3.2)
        lbl_t = Text("treatment",                  color=GRAY_TEXT).scale(0.30)
        lbl_e = Text("post-treatment observation", color=GRAY_TEXT).scale(0.30)
        col_t = Group(vid_t, lbl_t).arrange(DOWN, buff=0.18)
        col_e = Group(vid_e, lbl_e).arrange(DOWN, buff=0.18)
        vids  = Group(col_t, col_e).arrange(RIGHT, buff=1.0).center().shift(DOWN * 0.4)

        example_title = Text(
            "Motivating Example: social immunity in ants",
            t2s={"social immunity in ants": ITALIC},
            color=_W,
        ).scale(BODY_SCALE)
        example_title.next_to(vids, UP, buff=0.35).align_to(vids, LEFT)

        tracker = ValueTracker(0)
        upd_t = lambda m: m.set_time(tracker.get_value())
        upd_e = lambda m: m.set_time(tracker.get_value())
        vid_t.add_updater(upd_t)
        vid_e.add_updater(upd_e)

        # both clips enter together with a slow fade
        self.play(FadeIn(vids), FadeIn(example_title, shift=DOWN * 0.06), run_time=1.2)
        self.play(tracker.animate.set_value(n_loops * duration),
                  run_time=n_loops * duration, rate_func=linear)
        vid_t.clear_updaters()
        vid_e.clear_updaters()
        self.next_slide()

        # ── Slide 3: replace gifs with T→Y DAG centred ───────────────────────
        dag = _make_dag()
        dag.center()
        self.play(FadeOut(vids), FadeOut(example_title), FadeIn(dag), run_time=1.4)
        self.wait(0.8)
        self.next_slide()

        # ── Slide 4: DAG squeezes to top-right + table enters simultaneously ───
        # scale 0.52: rightmost point ≈ (2.1+0.48)*0.52 ≈ 1.34; at x=5.4 → 6.74 (safe)
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

        self.play(
            dag.animate.scale(0.52).move_to([5.6, 3.3, 0]),
            FadeOut(defn),
            run_time=0.7,
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
            "Foundational Problem\nof Causal Inference",
            color=GRAY_TEXT,
        ).scale(0.34)
        fpci_lbl.move_to([0, big_q.get_bottom()[1] - 0.48, 0])

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

        # ── ATE formula ───────────────────────────────────────────────────────
        ate = MathTex(
            r"\tau", r"\;=\;",
            r"\mathbb{E}[Y_i(1)]", r"-", r"\mathbb{E}[Y_i(0)]",
            color=_W,
        ).scale(0.52)
        ate.move_to([0, -2.05, 0])
        ate.align_to([X_LEFT, 0, 0], LEFT)   # left-align with table

        causal_lbl = Text("(causal estimand)", color=DIM_GRAY).scale(0.22)
        causal_lbl.next_to(ate, RIGHT, buff=0.28)

        idt_section_lbl = Text("Identify:", color=GRAY_TEXT).scale(0.36)
        idt_section_lbl.next_to(ate, UP, buff=0.22).align_to(exp_lbl, LEFT)

        self.play(FadeIn(ate), FadeIn(causal_lbl), FadeIn(idt_section_lbl), run_time=0.6)
        self.wait(0.4)
        self.next_slide()

        # ── Emphasise E[Y_i(1)] + Y_i(1) column ──────────────────────────────
        rect_E1      = SurroundingRectangle(ate[2], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        col_Y1_grp   = VGroup(*[row_mobs[ri][3] for ri in range(5)], dots_5[3])
        rect_col_E1  = SurroundingRectangle(col_Y1_grp, color=BLUE_LIGHT, buff=0.10, stroke_width=1.2)
        self.play(
            ate[2].animate.set_color(BLUE_LIGHT),
            Create(rect_E1),
            h_Y1.animate.set_color(BLUE_LIGHT),
            *[row_mobs[ri][3].animate.set_color(BLUE_LIGHT) for ri in range(5)],
            dots_5[3].animate.set_color(BLUE_LIGHT),
            Create(rect_col_E1),
            run_time=0.4,
        )
        self.wait(0.4)
        self.next_slide()

        # ── Restore + emphasise E[Y_i(0)] + Y_i(0) column ───────────────────
        rect_E0      = SurroundingRectangle(ate[4], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        col_Y0_grp   = VGroup(*[row_mobs[ri][4] for ri in range(5)], dots_5[4])
        rect_col_E0  = SurroundingRectangle(col_Y0_grp, color=BLUE_LIGHT, buff=0.10, stroke_width=1.2)
        self.play(
            ate[2].animate.set_color(_W),
            FadeOut(rect_E1), FadeOut(rect_col_E1),
            h_Y1.animate.set_color(_W),
            *[row_mobs[ri][3].animate.set_color(orig_col(3, ri)) for ri in range(5)],
            dots_5[3].animate.set_color(_W),
            ate[4].animate.set_color(BLUE_LIGHT),
            Create(rect_E0),
            h_Y0.animate.set_color(BLUE_LIGHT),
            *[row_mobs[ri][4].animate.set_color(BLUE_LIGHT) for ri in range(5)],
            dots_5[4].animate.set_color(BLUE_LIGHT),
            Create(rect_col_E0),
            run_time=0.4,
        )
        self.wait(0.4)
        self.next_slide()

        # ── Restore + identification ──────────────────────────────────────────
        self.play(
            ate[4].animate.set_color(_W),
            FadeOut(rect_E0), FadeOut(rect_col_E0),
            h_Y0.animate.set_color(_W),
            *[row_mobs[ri][4].animate.set_color(orig_col(4, ri)) for ri in range(5)],
            dots_5[4].animate.set_color(_W),
            run_time=0.3,
        )

        idt = MathTex(
            r"\phantom{\tau}", r"\;=\;",
            r"\mathbb{E}[Y_i \mid T_i=1]", r"-", r"\mathbb{E}[Y_i \mid T_i=0]",
            color=_W,
        ).scale(0.52)
        idt.next_to(ate, DOWN, buff=0.45)
        # align "=" signs explicitly so they stack vertically
        shift_x = ate[1].get_center()[0] - idt[1].get_center()[0]
        idt.shift(RIGHT * shift_x)

        stat_lbl = Text("(statistical estimand)", color=DIM_GRAY).scale(0.22)
        stat_lbl.next_to(idt, RIGHT, buff=0.28)

        self.play(
            FadeIn(idt), FadeIn(stat_lbl),
            run_time=0.6,
        )
        self.wait(0.4)
        self.next_slide()

        # ── Emphasise E[Y_i|T=1] + Y_i(1) entries for T=1 rows ──────────────
        t1_rows = [ri for ri, (ti, *_) in enumerate(rows_data) if ti == "1"]
        t0_rows = [ri for ri, (ti, *_) in enumerate(rows_data) if ti == "0"]

        rect_I1       = SurroundingRectangle(idt[2], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        cell_rects_I1 = VGroup(*[
            SurroundingRectangle(row_mobs[ri][3], color=BLUE_LIGHT, buff=0.08, stroke_width=1.2)
            for ri in t1_rows
        ])
        self.play(
            idt[2].animate.set_color(BLUE_LIGHT),
            Create(rect_I1),
            *[row_mobs[ri][3].animate.set_color(BLUE_LIGHT) for ri in t1_rows],
            *[row_mobs[ri][3].animate.set_color(DIM_GRAY)   for ri in t0_rows],
            *[Create(r) for r in cell_rects_I1],
            run_time=0.4,
        )
        self.wait(0.4)
        self.next_slide()

        # ── Restore + emphasise E[Y_i|T=0] + Y_i(0) entries for T=0 rows ────
        rect_I0       = SurroundingRectangle(idt[4], color=BLUE_LIGHT, buff=0.06, stroke_width=1.5)
        cell_rects_I0 = VGroup(*[
            SurroundingRectangle(row_mobs[ri][4], color=BLUE_LIGHT, buff=0.08, stroke_width=1.2)
            for ri in t0_rows
        ])
        self.play(
            idt[2].animate.set_color(_W),
            FadeOut(rect_I1),
            *[row_mobs[ri][3].animate.set_color(orig_col(3, ri)) for ri in t1_rows],
            *[row_mobs[ri][3].animate.set_color(orig_col(3, ri)) for ri in t0_rows],
            idt[4].animate.set_color(BLUE_LIGHT),
            Create(rect_I0),
            *[row_mobs[ri][4].animate.set_color(BLUE_LIGHT) for ri in t0_rows],
            *[row_mobs[ri][4].animate.set_color(DIM_GRAY)   for ri in t1_rows],
            *[FadeOut(r) for r in cell_rects_I1],
            *[Create(r) for r in cell_rects_I0],
            run_time=0.4,
        )
        self.wait(1)
        self.next_slide()

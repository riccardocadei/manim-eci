from manim import *
from manim_slides import Slide
import sys, os, glob as _glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np
from PIL import Image as PILImage

ANTS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "ants")
TFRAMES  = os.path.join(ANTS_DIR, "treatment_frames")
DFRAMES  = os.path.join(ANTS_DIR, "demo_frames")
EFRAMES  = os.path.join(ANTS_DIR, "effect_frames")



# ── VideoPlayer ────────────────────────────────────────────────────────────────

class VideoPlayer(ImageMobject):
    def __init__(self, frames_dir, fps=10, frame_start=None, frame_end=None,
                 square_crop=False, **kwargs):
        paths = sorted(_glob.glob(os.path.join(frames_dir, "frame_*.png")))
        if frame_start is not None or frame_end is not None:
            s = frame_start if frame_start is not None else 0
            e = frame_end if frame_end is not None else len(paths)
            paths = paths[s:e]
        arrays = [np.array(PILImage.open(p).convert("RGBA")) for p in paths]
        if square_crop:
            arrays = [self._crop_square(a) for a in arrays]
            # Write first cropped frame to a temp file so ImageMobject
            # initialises with the correct dimensions (orig_alpha_pixel_array).
            import tempfile
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            PILImage.fromarray(arrays[0]).save(tmp.name)
            init_path = tmp.name
        else:
            init_path = paths[0]
        self._arrays = arrays
        self._fps = fps
        self._nf  = len(self._arrays)
        super().__init__(init_path, **kwargs)

    @staticmethod
    def _crop_square(arr):
        h, w = arr.shape[:2]
        s = min(h, w)
        y0, x0 = (h - s) // 2, (w - s) // 2
        return arr[y0:y0 + s, x0:x0 + s]

    def set_time(self, t):
        self.pixel_array = self._arrays[int(t * self._fps) % self._nf]
        return self



# ── Scene ──────────────────────────────────────────────────────────────────────

class S02Motivation(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Slide: title + ChatGPT prompt + GIFs ───────────────────────────────

        motiv_title = Text("Motivation: Social Immunity",
                           t2s={"Social Immunity": ITALIC},
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

        _GIF_H = 2.8   # forced height for all GIFs

        vid_t = VideoPlayer(TFRAMES, fps=fps).scale_to_fit_height(_GIF_H)
        vid_e = VideoPlayer(EFRAMES, fps=fps).scale_to_fit_height(_GIF_H)
        lbl_t = Text("treatment",                  color=GRAY_TEXT).scale(0.28)
        lbl_e = Text("post-treatment observation", color=GRAY_TEXT).scale(0.28)
        col_t = Group(vid_t, lbl_t).arrange(DOWN, buff=0.14)
        col_e = Group(vid_e, lbl_e).arrange(DOWN, buff=0.14)
        vids  = Group(col_t, col_e).arrange(RIGHT, buff=0.8).move_to([0, -1.2, 0])
        # Force top-alignment between the two video columns
        col_e.align_to(col_t, UP)

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

        # ── Swap right GIF: effect → demo (square-cropped) ──────────────────
        d_fps, d_nf = 10, 331
        vid_d = VideoPlayer(DFRAMES, fps=d_fps, square_crop=True
                            ).scale_to_fit_height(_GIF_H)
        # Exact same position as effect GIF: same centre, top-aligned
        vid_d.move_to(vid_e.get_center())
        vid_d.align_to(vid_t, UP)

        self.play(FadeOut(vid_e), FadeIn(vid_d), run_time=0.6)

        tracker2 = ValueTracker(0)
        vid_t.add_updater(lambda m: m.set_time(tracker2.get_value()))
        vid_d.add_updater(lambda m: m.set_time(tracker2.get_value()))

        demo_duration = d_nf / d_fps
        self.play(
            tracker2.animate.set_value(demo_duration),
            run_time=demo_duration,
            rate_func=linear,
        )
        vid_t.clear_updaters()
        vid_d.clear_updaters()
        self.next_slide()

        # ── Transition: GIFs → T→Y DAG ──────────────────────────────────────
        # Use final T→Y→X positions from the start so T/Y stay consistent
        # when s03 later adds X below.
        r, fs = 0.48, 0.62
        T_pos = np.array([-2.5,  0.5, 0])
        Y_pos = np.array([ 2.0,  0.5, 0])

        T_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(T_pos)
        Y_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(Y_pos)
        T_l = MathTex("T", color=WHITE_TEXT).scale(fs).move_to(T_c)
        Y_l = MathTex("Y", color=WHITE_TEXT).scale(fs).move_to(Y_c)

        arr_TY = Arrow(
            T_c.get_right() + RIGHT * 0.08,
            Y_c.get_left()  + LEFT  * 0.08,
            color=WHITE_TEXT, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )
        q_TY = MathTex("?", color=WHITE_TEXT).scale(fs * 1.10).next_to(arr_TY, UP, buff=0.12)

        # Title: "Exploratory Causal Inference" with "Exploratory" dimmed
        eci_title = Text(
            "Exploratory Causal Inference",
            color=WHITE_TEXT,
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        # Dim "Exploratory" (first word, chars 0–10)
        eci_title[:11].set_opacity(0.25)

        # Center the full dag group (T, Y, arrows) accounting for future X
        # so positions stay consistent when s03 extends the graph
        X_pos = np.array([ 0.0, -1.6, 0])
        dag_full = VGroup(T_c, T_l, Y_c, Y_l, arr_TY, q_TY,
                          # invisible X anchor for consistent centering
                          Circle(radius=r, stroke_opacity=0, fill_opacity=0).move_to(X_pos))
        dag_full.center().shift(DOWN * 0.3)

        # Step 1: fade out ChatGPT box, prompt, labels; transform title
        self.play(
            FadeOut(chat_shell), FadeOut(prompt_mob),
            FadeOut(lbl_t), FadeOut(lbl_e),
            ReplacementTransform(motiv_title, eci_title),
            run_time=0.6,
        )

        # Step 2: shrink GIFs toward DAG node positions
        self.play(
            vid_t.animate.scale_to_fit_height(1.8).move_to(T_c),
            vid_d.animate.scale_to_fit_height(1.8).move_to(Y_c),
            run_time=0.9,
        )

        # Step 3: swap for looping overlays, dim, grow DAG nodes
        _ghost_op = 0.18
        _ov_op    = 1 - _ghost_op

        ov_t = VideoPlayer(TFRAMES, fps=fps).scale_to_fit_height(1.8).move_to(T_c)
        ov_d = VideoPlayer(DFRAMES, fps=d_fps, frame_start=71, frame_end=211,
                           square_crop=True).scale_to_fit_height(1.8).move_to(Y_c)

        ov_tracker = ValueTracker(0)
        ov_t.add_updater(lambda m: m.set_time(ov_tracker.get_value()))
        ov_d.add_updater(lambda m: m.set_time(ov_tracker.get_value()))

        rect_t = Rectangle(width=ov_t.width, height=ov_t.height,
                           fill_color=BG, fill_opacity=0, stroke_width=0).move_to(T_c)
        rect_d = Rectangle(width=ov_d.width, height=ov_d.height,
                           fill_color=BG, fill_opacity=0, stroke_width=0).move_to(Y_c)

        self.remove(vid_t, vid_d)
        self.add(ov_t, ov_d)
        self.bring_to_back(ov_t, ov_d)
        self.add(rect_t, rect_d)

        self.play(
            rect_t.animate.set_fill(opacity=_ov_op),
            rect_d.animate.set_fill(opacity=_ov_op),
            LaggedStart(
                AnimationGroup(GrowFromCenter(T_c), FadeIn(T_l)),
                AnimationGroup(GrowFromCenter(Y_c), FadeIn(Y_l)),
                lag_ratio=0.35,
            ),
            run_time=1.5,
        )
        self.play(Create(arr_TY), FadeIn(q_TY), run_time=0.7)
        self.play(
            ov_tracker.animate.set_value(8.0),
            run_time=8.0,
            rate_func=linear,
        )
        ov_t.clear_updaters()
        ov_d.clear_updaters()
        self.next_slide()

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
    def __init__(self, frames_dir, fps=10, frame_start=None, frame_end=None, **kwargs):
        paths = sorted(_glob.glob(os.path.join(frames_dir, "frame_*.png")))
        if frame_start is not None or frame_end is not None:
            s = frame_start if frame_start is not None else 0
            e = frame_end if frame_end is not None else len(paths)
            paths = paths[s:e]
        self._arrays = [np.array(PILImage.open(p).convert("RGBA")) for p in paths]
        self._fps = fps
        self._nf  = len(self._arrays)
        super().__init__(paths[0], **kwargs)

    def set_time(self, t):
        self.pixel_array = self._arrays[int(t * self._fps) % self._nf]
        return self


# ── Scene ──────────────────────────────────────────────────────────────────────

class S03ECI(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = slide_title("Exploratory Causal Inference")
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ── Gifs: treatment (loops) + demo (plays once) ───────────────────────
        t_fps,  t_nf = 10, 40    # treatment: 40 frames → 4 s loop
        d_fps,  d_nf = 10, 331   # demo: 331 frames → 33.1 s

        vid_t = VideoPlayer(TFRAMES, fps=t_fps).scale_to_fit_height(3.2)
        vid_d = VideoPlayer(DFRAMES, fps=d_fps).scale_to_fit_height(3.2)

        lbl_t = Text("treatment",                  color=GRAY_TEXT).scale(0.30)
        lbl_d = Text("post-treatment observation", color=GRAY_TEXT).scale(0.30)

        col_t = Group(vid_t, lbl_t).arrange(DOWN, buff=0.18)
        col_d = Group(vid_d, lbl_d).arrange(DOWN, buff=0.18)
        vids  = Group(col_t, col_d).arrange(RIGHT, buff=1.0).center().shift(DOWN * 0.4)

        example_title = Text(
            "Motivating Example: social immunity in ants",
            t2s={"social immunity in ants": ITALIC},
            color=WHITE_TEXT,
        ).scale(BODY_SCALE)
        example_title.next_to(vids, UP, buff=0.35).align_to(vids, LEFT)

        tracker = ValueTracker(0)
        vid_t.add_updater(lambda m: m.set_time(tracker.get_value()))
        vid_d.add_updater(lambda m: m.set_time(tracker.get_value()))

        demo_duration = d_nf / d_fps   # 33.1 s — demo plays once, treatment loops ~8×

        self.play(FadeIn(vids), FadeIn(example_title, shift=DOWN * 0.06), run_time=1.2)
        self.play(
            tracker.animate.set_value(demo_duration),
            run_time=demo_duration,
            rate_func=linear,
        )
        vid_t.clear_updaters()
        vid_d.clear_updaters()
        self.next_slide()

        # ── Build DAG (positions computed for full T→Y→X layout) ─────────────
        r, fs = 0.48, 0.62
        T_pos = np.array([-2.5,  0.5, 0])
        Y_pos = np.array([ 2.0,  0.5, 0])
        X_pos = np.array([ 0.0, -1.6, 0])

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
        _dv = X_pos - Y_pos
        _dv = _dv / np.linalg.norm(_dv)
        arr_YX = Arrow(
            Y_pos + _dv * (r + 0.08),
            X_pos - _dv * (r + 0.08),
            color=WHITE_TEXT, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )

        # Center full dag so T/Y/X positions are consistent across both slides
        dag = VGroup(T_c, T_l, Y_c, Y_l, X_c, X_l, arr_TY, arr_YX)
        dag.center().shift(DOWN * 0.3)

        # ── Gif underlays (full opacity; dimmed later via dark overlay) ─────────
        _ghost_op = 0.18          # final gif visibility
        _ov_op    = 1 - _ghost_op  # overlay opacity that achieves ghost effect

        ov_t = VideoPlayer(TFRAMES, fps=t_fps).scale_to_fit_height(1.8).move_to(T_c)
        ov_y = VideoPlayer(DFRAMES, fps=d_fps, frame_start=71, frame_end=211).scale_to_fit_height(1.8).move_to(Y_c)
        ov_e = VideoPlayer(EFRAMES, fps=t_fps).scale_to_fit_height(1.8).move_to(X_c)

        ov_tracker = ValueTracker(0)
        ov_t.add_updater(lambda m: m.set_time(ov_tracker.get_value()))
        ov_y.add_updater(lambda m: m.set_time(ov_tracker.get_value()))
        ov_e.add_updater(lambda m: m.set_time(ov_tracker.get_value()))

        # Dark rectangles that animate from transparent → opaque to ghost the gifs
        rect_t = Rectangle(width=ov_t.width, height=ov_t.height,
                            fill_color=BG, fill_opacity=0, stroke_width=0).move_to(T_c)
        rect_y = Rectangle(width=ov_y.width, height=ov_y.height,
                            fill_color=BG, fill_opacity=0, stroke_width=0).move_to(Y_c)
        rect_e = Rectangle(width=ov_e.width, height=ov_e.height,
                            fill_color=BG, fill_opacity=0, stroke_width=0).move_to(X_c)

        # ── Slide: gifs → T→Y DAG, emphasize "Causal Inference" in title ──────
        # title[:11] = "Exploratory", title[11:] = " Causal Inference"
        self.play(FadeOut(vids), FadeOut(example_title), run_time=0.8)

        # ghost gifs behind T and Y are already added before DAG builds
        self.add(ov_t, ov_y)
        self.bring_to_back(ov_t, ov_y)
        self.add(rect_t, rect_y)

        # ghost gifs + build T→Y nodes + arrow
        self.play(
            rect_t.animate.set_fill(opacity=_ov_op),
            rect_y.animate.set_fill(opacity=_ov_op),
            LaggedStart(
                AnimationGroup(GrowFromCenter(T_c), FadeIn(T_l)),
                AnimationGroup(GrowFromCenter(Y_c), FadeIn(Y_l)),
                lag_ratio=0.35,
            ),
            run_time=1.5,
        )
        self.play(Create(arr_TY), run_time=0.7)
        self.play(
            ov_tracker.animate.set_value(8.0),
            run_time=8.0,
            rate_func=linear,
        )
        self.next_slide()

        # ── Slide: add X, emphasize "Exploratory", Y → "?" ──────────────────
        q_Y = MathTex("?", color=GRAY_TEXT).scale(fs).move_to(Y_c)

        self.add(ov_e)
        self.bring_to_back(ov_e)
        self.add(rect_e)

        # ghost X gif + add X node + arrow + swap Y→?  + remove Y ghost gif
        self.play(
            rect_e.animate.set_fill(opacity=_ov_op),
            FadeOut(ov_y), FadeOut(rect_y),
            ReplacementTransform(Y_l, q_Y),
            AnimationGroup(GrowFromCenter(X_c), FadeIn(X_l)),
            Create(arr_YX),
            run_time=1.4,
        )
        self.play(
            ov_tracker.animate.set_value(ov_tracker.get_value() + 8.0),
            run_time=8.0,
            rate_func=linear,
        )
        ov_t.clear_updaters()
        ov_y.clear_updaters()
        ov_e.clear_updaters()
        self.next_slide()

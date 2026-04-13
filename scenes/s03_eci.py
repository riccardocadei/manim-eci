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

class S03ECI(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Recreate s02 end state ───────────────────────────────────────────
        # Title with "Exploratory" dimmed, T→Y DAG, ghost GIF underlays
        r, fs = 0.48, 0.62
        t_fps = 10

        T_pos = np.array([-2.5,  0.5, 0])
        Y_pos = np.array([ 2.0,  0.5, 0])
        X_pos = np.array([ 0.0, -1.6, 0])

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

        # Invisible X anchor for consistent centering (matches s02)
        _x_anchor = Circle(radius=r, stroke_opacity=0, fill_opacity=0).move_to(X_pos)
        dag_full = VGroup(T_c, T_l, Y_c, Y_l, arr_TY, q_TY, _x_anchor)
        dag_full.center().shift(DOWN * 0.3)

        # Title with "Exploratory" dimmed (matching s02 end state)
        eci_title = Text(
            "Exploratory Causal Inference",
            color=WHITE_TEXT,
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        eci_title[:11].set_opacity(0.25)

        # Ghost GIF underlays
        _ghost_op = 0.18
        _ov_op    = 1 - _ghost_op

        ov_t = VideoPlayer(TFRAMES, fps=t_fps).scale_to_fit_height(1.8).move_to(T_c)
        ov_d = VideoPlayer(DFRAMES, fps=t_fps, frame_start=71, frame_end=211,
                           square_crop=True).scale_to_fit_height(1.8).move_to(Y_c)

        rect_t = Rectangle(width=ov_t.width, height=ov_t.height,
                           fill_color=BG, fill_opacity=_ov_op, stroke_width=0).move_to(T_c)
        rect_d = Rectangle(width=ov_d.width, height=ov_d.height,
                           fill_color=BG, fill_opacity=_ov_op, stroke_width=0).move_to(Y_c)

        self.add(ov_t, ov_d, rect_t, rect_d)
        self.add(T_c, T_l, Y_c, Y_l, arr_TY, q_TY, eci_title)

        # ── Slide: reveal "Exploratory", Y → "?", add X with effect GIF ─────

        # Prepare new elements
        X_c = Circle(radius=r, color=WHITE_TEXT, stroke_width=3.5).move_to(X_pos)
        X_l = MathTex("X", color=WHITE_TEXT).scale(fs).move_to(X_c)

        # X position is already consistent — _x_anchor was part of dag_full
        # when it was centered, so it absorbed the same transform.
        X_c.move_to(_x_anchor)
        X_l.move_to(X_c)

        _dv = X_c.get_center() - Y_c.get_center()
        _dv = _dv / np.linalg.norm(_dv)
        arr_YX = Arrow(
            Y_c.get_center() + _dv * (r + 0.08),
            X_c.get_center() - _dv * (r + 0.08),
            color=WHITE_TEXT, buff=0, stroke_width=5,
            max_tip_length_to_length_ratio=0.18,
        )

        q_Y = MathTex("?", color=GRAY_TEXT).scale(fs).move_to(Y_c)

        # Effect GIF overlay for X node
        ov_e = VideoPlayer(EFRAMES, fps=t_fps).scale_to_fit_height(1.8).move_to(X_c)
        rect_e = Rectangle(width=ov_e.width, height=ov_e.height,
                           fill_color=BG, fill_opacity=0, stroke_width=0).move_to(X_c)

        ov_tracker = ValueTracker(0)
        ov_t.add_updater(lambda m: m.set_time(ov_tracker.get_value()))
        ov_d.add_updater(lambda m: m.set_time(ov_tracker.get_value()))
        ov_e.add_updater(lambda m: m.set_time(ov_tracker.get_value()))

        # Step 1: reveal "Exploratory" to full white
        self.play(
            eci_title[:11].animate.set_opacity(1),
            run_time=0.6,
        )
        self.wait(0.3)

        # Step 2: Y → "?", remove Y ghost gif, add effect gif at X,
        #         grow X node + arrow (the old routine from git history)
        self.add(ov_e)
        self.bring_to_back(ov_e)
        self.add(rect_e)

        self.play(
            rect_e.animate.set_fill(opacity=_ov_op),
            FadeOut(ov_d), FadeOut(rect_d),
            FadeOut(q_TY),
            ReplacementTransform(Y_l, q_Y),
            AnimationGroup(GrowFromCenter(X_c), FadeIn(X_l)),
            Create(arr_YX),
            run_time=1.4,
        )

        # Let GIFs loop for a bit
        self.play(
            ov_tracker.animate.set_value(8.0),
            run_time=8.0,
            rate_func=linear,
        )
        ov_t.clear_updaters()
        ov_d.clear_updaters()
        ov_e.clear_updaters()
        self.next_slide()

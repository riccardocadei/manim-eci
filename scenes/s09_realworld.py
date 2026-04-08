from manim import *
from manim_slides import Slide
import sys, os, random, tempfile
import numpy as np
from PIL import Image as PILImage

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *

ANTS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "ants", "results")


def _extract_gif_frames(gif_path):
    """Return list of RGBA numpy arrays and per-frame duration in seconds."""
    pil_img = PILImage.open(gif_path)
    duration = pil_img.info.get("duration", 160) / 1000.0
    frames = []
    for i in range(pil_img.n_frames):
        pil_img.seek(i)
        frames.append(np.array(pil_img.convert("RGBA")))
    return frames, duration


def _animated_gif_grid(folder, cols=4, rows=2, h=0.75, gap=0.05, seed=42):
    """Load GIF files into animated ImageMobjects in a grid.

    Returns (grid_group, list_of_img_mobjects_with_frame_data).
    """
    files = sorted(f for f in os.listdir(folder) if f.endswith(".gif"))
    rng = random.Random(seed)
    rng.shuffle(files)
    files = files[: rows * cols]

    tmpdir = tempfile.mkdtemp()
    g = Group()
    anim_data = []  # list of (img_mobject, frames_list, duration)

    for i, fname in enumerate(files):
        r, c = divmod(i, cols)
        gif_path = os.path.join(folder, fname)
        frames, duration = _extract_gif_frames(gif_path)

        # Save first frame as temp PNG for the initial ImageMobject
        first_path = os.path.join(tmpdir, f"g{i}.png")
        PILImage.fromarray(frames[0]).save(first_path)

        img = ImageMobject(first_path).set_height(h)
        img.move_to([c * (h + gap), -r * (h + gap), 0])
        g.add(img)
        anim_data.append((img, frames, duration))

    g.center()
    return g, anim_data


def _start_gif_updaters(anim_data):
    """Attach frame-cycling updaters to every animated GIF ImageMobject."""
    for img, frames, duration in anim_data:
        img._gif_frames = frames
        img._gif_duration = duration
        img._gif_n = len(frames)
        img._gif_elapsed = [0.0]
        img._gif_cur = [0]

        def _upd(mob, dt):
            mob._gif_elapsed[0] += dt
            total = mob._gif_n * mob._gif_duration
            idx = int((mob._gif_elapsed[0] % total) / mob._gif_duration) % mob._gif_n
            if idx != mob._gif_cur[0]:
                mob._gif_cur[0] = idx
                mob.pixel_array = mob._gif_frames[idx]

        img.add_updater(_upd)


def _neuron_row(neuron_id, quiet_folder, top_folder, interp_lines, y_center):
    """Build a full row: neuron label | quiet grid | top grid | interpretation.

    interp_lines is a list of (text, relative_scale) tuples, e.g.:
        [("grooming behaviour", 1.0), ("(see Cadei et al., NeurIPS'24)", 0.7)]
    """
    # Neuron label
    neuron_lbl = MathTex(
        rf"Z_{{{neuron_id}}}", color=BLUE_LIGHT
    ).scale(BODY_SCALE * 1.15)

    # Column headers
    hdr_quiet = Text("not activated", color=GRAY_TEXT).scale(SMALL_SCALE * 0.9)
    hdr_top = Text("activated", color=GRAY_TEXT).scale(SMALL_SCALE * 0.9)

    # Grids (animated)
    grid_quiet, anim_quiet = _animated_gif_grid(quiet_folder, cols=4, rows=2, h=0.75, gap=0.05)
    grid_top, anim_top = _animated_gif_grid(top_folder, cols=4, rows=2, h=0.75, gap=0.05)

    # Dim the quiet grid
    grid_quiet.set_opacity(0.45)

    # Interpretation (multi-line VGroup, white)
    interp_parts = []
    for txt, rel_scale in interp_lines:
        t = Text(txt, color=WHITE_TEXT).scale(SMALL_SCALE * 0.95 * rel_scale)
        interp_parts.append(t)
    interp = VGroup(*interp_parts).arrange(DOWN, buff=0.08, center=True)

    # --- Positioning ---
    grid_quiet.move_to([-2.8, y_center, 0])
    grid_top.move_to([1.8, y_center, 0])

    hdr_quiet.next_to(grid_quiet, UP, buff=0.12)
    hdr_top.next_to(grid_top, UP, buff=0.12)

    neuron_lbl.next_to(grid_quiet, LEFT, buff=0.35)

    # Interpretation column: right side, aligned
    interp.move_to([5.5, y_center, 0])

    # "Interpretation" header aligned vertically with "activated"
    hdr_interp = Text("interpretation", color=GRAY_TEXT).scale(SMALL_SCALE * 0.9)
    hdr_interp.move_to([5.5, hdr_top.get_y(), 0])

    # Green check badge below interpretation
    check = Text("✓", color=GREEN_LIGHT).scale(BODY_SCALE * 0.82)
    check.next_to(interp, DOWN, buff=0.15)

    labels = VGroup(neuron_lbl, hdr_quiet, hdr_top, interp, hdr_interp, check)
    grids = Group(grid_quiet, grid_top)
    return labels, grids, anim_quiet + anim_top


class S09RealWorld(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ────────────────────────────────────────────────────────────
        title = Text(
            "Results: Social Immunity (ISTAnt)",
            color=WHITE_TEXT,
            t2s={"Social Immunity (ISTAnt)": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        # ── Subtitle ─────────────────────────────────────────────────────────
        subtitle = Text(
            "2/4608 significant neural effects",
            color=GRAY_TEXT,
        ).scale(BODY_SCALE * 0.9).next_to(title, DOWN, buff=0.2)

        self.play(Write(title), FadeIn(subtitle), run_time=0.7)
        self.wait(0.3)
        self.next_slide()

        # ── Neuron 394 ───────────────────────────────────────────────────────
        labels1, grids1, anim1 = _neuron_row(
            neuron_id=394,
            quiet_folder=os.path.join(ANTS_DIR, "neuron394_quiet10_gifs"),
            top_folder=os.path.join(ANTS_DIR, "neuron394_top10_gifs"),
            interp_lines=[
                ("grooming behaviour", 1.0),
                ("(see Cadei et al., NeurIPS'24)", 0.7),
            ],
            y_center=1.0,
        )

        # Animate neuron 394
        self.play(
            FadeIn(labels1[0]),  # neuron label
            run_time=0.5,
        )
        self.play(
            FadeIn(labels1[1]),  # "not activated" header
            LaggedStart(*[FadeIn(im, shift=UP * 0.1) for im in grids1[0]], lag_ratio=0.04),
            run_time=0.8,
        )
        # Start GIF updaters as soon as grids appear
        _start_gif_updaters(anim1)
        self.play(
            FadeIn(labels1[2]),  # "activated" header
            LaggedStart(*[FadeIn(im, shift=UP * 0.1) for im in grids1[1]], lag_ratio=0.04),
            run_time=0.8,
        )
        self.play(
            FadeIn(labels1[4]),  # "interpretation" header
            Write(labels1[3]),   # interpretation text
            run_time=0.8,
        )
        self.wait(1.0)
        self.play(FadeIn(labels1[5], scale=1.5), run_time=0.4)  # green check
        self.wait(1.6)
        self.next_slide(loop=True)
        self.wait(1.6)
        self.next_slide()

        # ── Separator ────────────────────────────────────────────────────────
        sep = Line(LEFT * 5.5, RIGHT * 5.5, color=DIM_GRAY, stroke_width=1)
        sep.move_to([0, -0.6, 0])
        self.play(Create(sep), run_time=0.3)

        # ── Neuron 550 ───────────────────────────────────────────────────────
        labels2, grids2, anim2 = _neuron_row(
            neuron_id=550,
            quiet_folder=os.path.join(ANTS_DIR, "neuron550_quiet10_gifs"),
            top_folder=os.path.join(ANTS_DIR, "neuron550_top10_gifs"),
            interp_lines=[
                ("color marking position", 1.0),
                ("(not randomized)", 0.7),
            ],
            y_center=-2.2,
        )

        # Animate neuron 550
        self.play(
            FadeIn(labels2[0]),  # neuron label
            run_time=0.5,
        )
        self.play(
            FadeIn(labels2[1]),  # "not activated" header
            LaggedStart(*[FadeIn(im, shift=UP * 0.1) for im in grids2[0]], lag_ratio=0.04),
            run_time=0.8,
        )
        # Start GIF updaters as soon as grids appear
        _start_gif_updaters(anim2)
        self.play(
            FadeIn(labels2[2]),  # "activated" header
            LaggedStart(*[FadeIn(im, shift=UP * 0.1) for im in grids2[1]], lag_ratio=0.04),
            run_time=0.8,
        )
        self.play(
            FadeIn(labels2[4]),  # "interpretation" header
            Write(labels2[3]),   # interpretation text
            run_time=0.8,
        )
        self.wait(1.0)
        self.play(FadeIn(labels2[5], scale=1.5), run_time=0.4)  # green check
        self.wait(1.6)
        self.next_slide(loop=True)
        self.wait(1.6)

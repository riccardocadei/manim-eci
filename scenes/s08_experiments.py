from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "synthetic", "examples")
EXPERIMENT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "experiment")

# ── Top-16 neurons by NES score per treatment ─────────────────────────────────

HAT_DATA = [
    ("N_38",   0.842), ("N_8805", 0.244), ("N_1852", 0.235), ("N_4680", 0.185),
    ("N_9098", 0.145), ("N_408",  0.135), ("N_4135", 0.115), ("N_4224", 0.113),
    ("N_8905", 0.107), ("N_1426", 0.104), ("N_8747", 0.100), ("N_6586", 0.088),
    ("N_6051", 0.081), ("N_1318", 0.076), ("N_3329", 0.075), ("N_3621", 0.069),
]

GLASSES_DATA = [
    ("N_6051", 0.748), ("N_2218", 0.340), ("N_524",  0.235), ("N_7110", 0.217),
    ("N_5398", 0.166), ("N_3569", 0.123), ("N_8747", 0.117), ("N_4822", 0.112),
    ("N_408",  0.108), ("N_5671", 0.107), ("N_38",   0.106), ("N_1669", 0.104),
    ("N_1347", 0.100), ("N_2064", 0.094), ("N_1592", 0.089), ("N_3822", 0.086),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _display_name(tag):
    """Convert 'N_38' → r'Z_{38}' for MathTex display."""
    num = tag.split("_")[1]
    return r"Z_{" + num + "}"


def _bar_chart(data, max_w=2.0, bar_h=0.10, spacing=0.155):
    """Horizontal bar chart, all bars neutral color.
    Indices: 0…N-1 = data rows (VGroup(lbl, bar, val)), N = '...' Text.
    """
    max_val = data[0][1]
    g = VGroup()
    BAR_START = 1.05

    for name, val in data:
        w = max(0.04, val / max_val * max_w)
        y = -len(g) * spacing

        bar = Rectangle(width=w, height=bar_h,
                        fill_color=WHITE_TEXT, fill_opacity=0.35, stroke_width=0)
        bar.move_to([BAR_START + w / 2, y, 0])

        lbl = MathTex(_display_name(name), color=GRAY_TEXT).scale(LABEL_SCALE * 0.62)
        lbl.move_to([BAR_START - 0.10 - lbl.width / 2, y, 0])

        vt = Text(f"{val:.2f}", color=DIM_GRAY).scale(LABEL_SCALE * 0.55)
        vt.next_to(bar, RIGHT, buff=0.06)

        g.add(VGroup(lbl, bar, vt))

    n = len(g)
    dots = Text("...", color=DIM_GRAY).scale(LABEL_SCALE * 0.62)
    dots.move_to([BAR_START - 0.10 - dots.width / 2, -n * spacing, 0])
    g.add(dots)
    return g


def _highlight_anim(chart, idx=0):
    """Highlight row idx (bar → blue, label+val → white); dim everything else."""
    row = chart[idx]
    anims = [
        row[0].animate.set_color(WHITE_TEXT),
        row[1].animate.set_fill(BLUE_LIGHT, opacity=0.90),
        row[2].animate.set_color(WHITE_TEXT),
    ]
    for i in range(len(chart)):
        if i != idx:
            anims.append(chart[i].animate.set_opacity(0.18))
    return anims


def _img_grid(neuron, rows=3, cols=4, h=0.60, gap=0.04):
    """3×4 grid (12 images) of high-activating examples."""
    neuron_file = neuron.replace("_", "")   # 'N_38' → 'N38'
    g = Group()
    for r in range(rows):
        for c in range(cols):
            path = os.path.join(EXAMPLES_DIR,
                                f"high_activating_{neuron_file}_{r * cols + c}.jpg")
            img = ImageMobject(path).set_height(h)
            img.move_to([c * (h + gap), -r * (h + gap), 0])
            g.add(img)
    return g


def _build_panel(neuron_tag, neuron_display, y_center, img_x, img_h=0.60, img_gap=0.04):
    """
    Build (hdr_neuron, hdr_desc, imgs, badge) correctly centred at (img_x, y_center).
    hdr_neuron and hdr_desc are independent Text objects positioned above imgs.
    badge is positioned to the right of imgs.
    """
    # Build header in two pieces so hdr_neuron can be targeted by Transform
    hdr_neuron = MathTex(neuron_display, color=BLUE_LIGHT).scale(LABEL_SCALE * 1.30)
    hdr_desc   = Text("  ·  top activating images", color=GRAY_TEXT).scale(LABEL_SCALE * 0.82)

    # Measure combined header height (both same scale → same height)
    hdr_h = hdr_neuron.height

    # Centre the full panel (header + buff + grid) at y_center
    imgs = _img_grid(neuron_tag, h=img_h, gap=img_gap)
    imgs.center()
    imgs.move_to([img_x, y_center - (hdr_h + 0.14) / 2, 0])

    # Arrange header inline, centred above imgs
    VGroup(hdr_neuron, hdr_desc).arrange(RIGHT, buff=0.05).next_to(imgs, UP, buff=0.14)

    badge = Text("✓  Assumption", color=GREEN_LIGHT).scale(BODY_SCALE * 0.82)
    badge.next_to(imgs, RIGHT, buff=0.45)

    return hdr_neuron, hdr_desc, imgs, badge


# ── Scene ─────────────────────────────────────────────────────────────────────

class S08Experiments(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ─────────────────────────────────────────────────────────────
        title = Text(
            "Proof of concept: CelebA",
            color=WHITE_TEXT,
            t2s={"CelebA": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        self.play(Write(title), run_time=0.7)
        self.wait(0.3)
        self.next_slide()

        # ── Layout constants ──────────────────────────────────────────────────
        CHART_X     = -4.0
        IMG_X       =  1.4
        CHART_SHIFT =  0.35
        Y1, Y2      =  1.3, -2.2

        # ── Effect 1: bar chart ───────────────────────────────────────────────
        chart1 = _bar_chart(HAT_DATA)
        chart1.move_to([CHART_X, Y1, 0])

        lbl1 = Text(
            "Effect 1: wearing hat", color=WHITE_TEXT,
            t2s={"wearing hat": ITALIC},
        ).scale(BODY_SCALE)
        lbl1.next_to(chart1, UP, buff=0.20, aligned_edge=LEFT)

        self.play(
            FadeIn(lbl1),
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.06) for r in chart1], lag_ratio=0.04),
            run_time=1.0,
        )
        self.wait(0.3)
        self.next_slide()

        # ── Effect 1: highlight → fly → images ───────────────────────────────
        hdr1_n, hdr1_d, imgs1, badge1 = _build_panel("N_38", r"Z_{38}", Y1, IMG_X)

        # Step 1: highlight top bar
        self.play(*_highlight_anim(chart1, idx=0), run_time=0.40)

        # Step 2: ghost of bar label flies to header position while chart slides back
        #   ghost starts at bar label position (small, white) → transforms to
        #   hdr1_n position (larger, blue)
        ghost1 = MathTex(r"Z_{38}", color=WHITE_TEXT).scale(LABEL_SCALE * 0.62)
        ghost1.move_to(chart1[0][0].get_center())
        self.add(ghost1)
        self.play(
            Transform(ghost1, hdr1_n),           # fly + grow + recolour
            chart1.animate.shift(LEFT * CHART_SHIFT),
            lbl1.animate.shift(LEFT * CHART_SHIFT),
            run_time=0.55,
        )
        # Swap ghost (now visually identical to hdr1_n) for the real object
        self.remove(ghost1)
        self.add(hdr1_n)

        # Step 3: description text + images slide in
        self.play(
            FadeIn(hdr1_d),
            LaggedStart(*[FadeIn(im, shift=LEFT * 0.20) for im in imgs1], lag_ratio=0.03),
            run_time=0.75,
        )
        self.play(Write(badge1), run_time=0.40)
        self.wait(0.4)
        self.next_slide()

        # ── Effect 2: bar chart ───────────────────────────────────────────────
        chart2 = _bar_chart(GLASSES_DATA)
        chart2.move_to([CHART_X, Y2, 0])

        lbl2 = Text(
            "Effect 2: wearing sunglasses", color=WHITE_TEXT,
            t2s={"wearing sunglasses": ITALIC},
        ).scale(BODY_SCALE)
        lbl2.next_to(chart2, UP, buff=0.20, aligned_edge=LEFT)

        self.play(
            FadeIn(lbl2),
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.06) for r in chart2], lag_ratio=0.04),
            run_time=1.0,
        )
        self.wait(0.3)
        self.next_slide()

        # ── Effect 2: highlight → fly → images ───────────────────────────────
        hdr2_n, hdr2_d, imgs2, badge2 = _build_panel("N_6051", r"Z_{6051}", Y2, IMG_X)

        self.play(*_highlight_anim(chart2, idx=0), run_time=0.40)

        ghost2 = MathTex(r"Z_{6051}", color=WHITE_TEXT).scale(LABEL_SCALE * 0.62)
        ghost2.move_to(chart2[0][0].get_center())
        self.add(ghost2)
        self.play(
            Transform(ghost2, hdr2_n),
            chart2.animate.shift(LEFT * CHART_SHIFT),
            lbl2.animate.shift(LEFT * CHART_SHIFT),
            run_time=0.55,
        )
        self.remove(ghost2)
        self.add(hdr2_n)

        self.play(
            FadeIn(hdr2_d),
            LaggedStart(*[FadeIn(im, shift=LEFT * 0.20) for im in imgs2], lag_ratio=0.03),
            run_time=0.75,
        )
        self.play(Write(badge2), run_time=0.40)
        self.wait(0.4)
        self.next_slide()

        # ── Clear chart/images, keep title → show Figure 5 ────────────────
        stuff_to_clear = Group(
            lbl1, chart1, hdr1_n, hdr1_d, imgs1, badge1,
            lbl2, chart2, hdr2_n, hdr2_d, imgs2, badge2,
        )
        self.play(FadeOut(stuff_to_clear), run_time=0.6)

        FRAMES_DIR = os.path.join(EXPERIMENT_DIR, "frames")
        FIG_H = 5.2

        # ── Phase 1: bars grow gradually (frame sequence) ────────────────
        N_FRAMES = 15
        grow_frames = []
        for i in range(N_FRAMES):
            img = ImageMobject(os.path.join(FRAMES_DIR, f"grow_3m_{i:02d}.png"))
            img.set_height(FIG_H).next_to(title, DOWN, buff=0.3)
            grow_frames.append(img)

        # Show first frame, then animate through the rest
        self.add(grow_frames[0])
        for i in range(1, N_FRAMES):
            self.remove(grow_frames[i - 1])
            self.add(grow_frames[i])
            self.wait(1/15)
        fig_current = grow_frames[-1]
        self.wait(0.3)
        self.next_slide()

        # ── Phase 2: trend line appears → ECI paradox ────────────────────
        fig_trend = ImageMobject(os.path.join(FRAMES_DIR, "trend.png"))
        fig_trend.set_height(FIG_H).move_to(fig_current.get_center())
        fig_trend.set_opacity(0)

        self.remove(fig_current)
        self.add(fig_trend)
        self.play(fig_trend.animate.set_opacity(1), run_time=0.8)
        fig_current = fig_trend

        self.wait(0.4)
        self.next_slide()

        # ── Phase 2b: ECI paradox label ──────────────────────────────────
        paradox_text = Text(
            "Exploratory Causal Inference Paradox",
            color=RED_LIGHT,
            t2s={"Exploratory Causal Inference Paradox": ITALIC},
        ).scale(BODY_SCALE * 1.1)
        paradox_text.next_to(fig_current, DOWN, buff=0.25)

        self.play(Write(paradox_text), run_time=0.7)
        self.wait(0.3)
        self.next_slide()

        # ── Phase 3: NES grows in (frame sequence) ───────────────────────
        self.play(FadeOut(paradox_text), run_time=0.3)

        nes_frames = []
        for i in range(N_FRAMES):
            img = ImageMobject(os.path.join(FRAMES_DIR, f"add_nes_{i:02d}.png"))
            img.set_height(FIG_H).move_to(fig_current.get_center())
            nes_frames.append(img)

        self.remove(fig_current)
        self.add(nes_frames[0])
        for i in range(1, N_FRAMES):
            self.remove(nes_frames[i - 1])
            self.add(nes_frames[i])
            self.wait(1/15)

        self.wait(0.4)
        self.next_slide()

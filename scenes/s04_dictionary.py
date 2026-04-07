from manim import *
from manim_slides import Slide
import sys, os, glob as _glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np
from PIL import Image as PILImage

ANTS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "ants")
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


# ── Shape helpers ──────────────────────────────────────────────────────────────

def make_vit(color, grid_n=3, patch_s=0.14, gap=0.03):
    """ViT diagram: patch grid + bounding box + attention arcs."""
    patches = VGroup(*[
        Square(side_length=patch_s,
               color=color, fill_color=color,
               fill_opacity=0.14 + 0.08 * ((r + c) % 2),
               stroke_width=1.2)
        .move_to(RIGHT * c * (patch_s + gap) + DOWN * r * (patch_s + gap))
        for r in range(grid_n)
        for c in range(grid_n)
    ])
    patches.center()

    bbox = SurroundingRectangle(patches, color=color, buff=0.07,
                                stroke_width=1.5, corner_radius=0.07)

    attn = VGroup(*[
        ArcBetweenPoints(
            patches[c].get_top() + UP * 0.01,
            patches[c + 1].get_top() + UP * 0.01,
            angle=-PI / 2.8, color=color, stroke_width=1.0,
        ).set_stroke(opacity=0.55)
        for c in range(grid_n - 1)
    ])

    shape = VGroup(attn, bbox, patches)
    shape.center()
    return shape


def make_sae_encoder(color):
    """SAE encoder operator: σ(W(·) + b) on a single line."""
    expr = MathTex(r"\sigma\!\bigl(\mathbf{W}(\cdot)+\mathbf{b}\bigr)", color=color).scale(0.38)
    box  = SurroundingRectangle(expr, color=color, buff=0.18,
                                corner_radius=0.09, stroke_width=1.2)
    grp  = VGroup(expr, box)
    grp.center()
    return grp


def multicolor_neuron(colors, radius=0.13, sector_opacities=None):
    """Pie-chart neuron: one sector per concept color, with variable opacities."""
    N = len(colors)
    if sector_opacities is None:
        sector_opacities = [0.20] * N
    sec_angle = 2 * PI / N
    sectors = VGroup(*[
        Sector(radius=radius, angle=sec_angle,
               start_angle=i * sec_angle,
               fill_color=colors[i], fill_opacity=sector_opacities[i],
               stroke_width=0, color=colors[i])
        for i in range(N)
    ])
    border = Circle(radius=radius, color=GRAY_TEXT, fill_opacity=0, stroke_width=0.9)
    return VGroup(sectors, border)   # [0] = sectors VGroup, [1] = border


# ── Scene ──────────────────────────────────────────────────────────────────────

class S04Dictionary(Slide):
    def construct(self):
        self.camera.background_color = BG

        CONCEPTS = [
            "locomotion", "body contact", "antennae", "clustering",
            "grooming",   "resting",      "foraging", "nest structure",
        ]
        CONCEPT_COLORS = [
            GREEN_LIGHT, BLUE_LIGHT, YELLOW_LIGHT, RED_LIGHT,
            "#5BCFB5",   PURPLE_LIGHT, "#F5A050",  "#7EC8F8",
        ]
        N     = len(CONCEPTS)
        N_ENT = 7       # entangled neurons (≠ N, to stress they're different dims)
        r_n   = 0.13

        # Each entangled neuron gets a shuffled color order + random sector opacities
        rng = np.random.default_rng(42)
        ENT_COLOR_PERMS = [rng.permutation(N).tolist() for _ in range(N_ENT)]
        ENT_COLORS      = [[CONCEPT_COLORS[p] for p in perm] for perm in ENT_COLOR_PERMS]
        ENT_OPACITIES   = [rng.uniform(0.10, 0.55, N).tolist() for _ in range(N_ENT)]

        # For activation: which sector in neuron j carries concept c's color
        ENT_SECTOR_FOR_CONCEPT = [
            {c: ENT_COLOR_PERMS[j].index(c) for c in range(N)}
            for j in range(N_ENT)
        ]

        # ── Title ──────────────────────────────────────────────────────────────
        title = Text(
            "Tool: Dictionary Learning", color=WHITE_TEXT,
            t2s={"Dictionary Learning": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        # ── Video ─────────────────────────────────────────────────────────────
        vid = VideoPlayer(EFRAMES, fps=10).scale_to_fit_height(2.5)
        vid.to_edge(LEFT, buff=0.4).shift(DOWN * 0.25)
        y0 = vid.get_center()[1]

        # lowercase, further below title
        per_obs = Text("per observation:", color=WHITE_TEXT).scale(0.34)
        per_obs.next_to(title, DOWN, buff=1.05).to_edge(LEFT, buff=0.55)

        tracker = ValueTracker(0)
        vid.add_updater(lambda m: m.set_time(tracker.get_value()))

        # ── Uniform-gap layout ─────────────────────────────────────────────────
        # All arrows cover the same physical distance: ARROW_GAP between bbox edges
        # 1.5 (instead of 1.8) leaves room for the Sankey column on the right.
        ARROW_GAP     = 1.5
        SANKEY_GAP_S4 = 0.8   # gap from circle right-edge to concept label left-edge
        ASTROKE       = 1.6
        ATIP      = 0.07

        def arrow(a, b):
            return Arrow(a + RIGHT * 0.04, b + LEFT * 0.04,
                         color=WHITE_TEXT, buff=0, stroke_width=ASTROKE,
                         max_tip_length_to_length_ratio=ATIP)

        # ── Frozen ViT ─────────────────────────────────────────────────────────
        vit_shape = make_vit(BLUE_LIGHT)
        vit_shape.move_to([vid.get_right()[0] + ARROW_GAP + vit_shape.width / 2, y0, 0])

        vit_lbl = VGroup(
            Text("ViT",      color=BLUE_LIGHT).scale(0.30),
            Text("(frozen)", color=BLUE_LIGHT).scale(0.24),
        ).arrange(DOWN, buff=0.03)
        vit_lbl.next_to(vit_shape, DOWN, buff=0.10)

        arr_vid2vit = arrow(vid.get_right(), vit_shape.get_left())

        # ── Entangled representation ────────────────────────────────────────────
        # Each neuron has a distinct color arrangement + opacity mix
        ent_neurons = VGroup(*[
            multicolor_neuron(ENT_COLORS[j], radius=r_n,
                              sector_opacities=ENT_OPACITIES[j])
            for j in range(N_ENT)
        ]).arrange(DOWN, buff=0.21)
        ent_neurons.move_to(
            [vit_shape.get_right()[0] + ARROW_GAP + ent_neurons.width / 2, y0, 0]
        )

        ent_dots = Text("⋮", color=GRAY_TEXT).scale(0.38)
        ent_dots.next_to(ent_neurons, DOWN, buff=0.15)

        ent_dim_lbl = MathTex(r"\sim 10^{2\text{-}3}", color=GRAY_TEXT).scale(0.30)
        ent_dim_lbl.next_to(ent_neurons, UP, buff=0.12)

        arr_vit2ent = arrow(vit_shape.get_right(), ent_neurons.get_left())

        # ── SAE encoder: σ(W(·) + b) ──────────────────────────────────────────
        sae_shape = make_sae_encoder(PURPLE_LIGHT)
        sae_shape.move_to(
            [ent_neurons.get_right()[0] + ARROW_GAP + sae_shape.width / 2, y0, 0]
        )

        sae_lbl = VGroup(
            Text("SAE",       color=PURPLE_LIGHT).scale(0.30),
            Text("(encoder)", color=PURPLE_LIGHT).scale(0.24),
        ).arrange(DOWN, buff=0.03)
        sae_lbl.next_to(sae_shape, DOWN, buff=0.10)

        arr_ent2sae = arrow(ent_neurons.get_right(), sae_shape.get_left())

        # ── Sparse concept neurons ─────────────────────────────────────────────
        n_circles = VGroup(*[
            Circle(radius=r_n, color=DIM_GRAY,
                   fill_color=DIM_GRAY, fill_opacity=0.25, stroke_width=1.5)
            for _ in range(N)
        ]).arrange(DOWN, buff=0.21)
        n_circles.move_to(
            [sae_shape.get_right()[0] + ARROW_GAP + n_circles.width / 2, y0, 0]
        )

        c_txts = VGroup(*[
            Text(CONCEPTS[i], color=DIM_GRAY).scale(0.26)
            .next_to(n_circles[i], RIGHT, buff=SANKEY_GAP_S4)
            for i in range(N)
        ])

        dots_circle = Circle(radius=r_n, color=DIM_GRAY,
                             fill_color=DIM_GRAY, fill_opacity=0.12, stroke_width=1.0)
        dots_circle.next_to(n_circles, DOWN, buff=0.21)
        dots_txt = Text("...", color=DIM_GRAY).scale(0.32) \
            .next_to(dots_circle, RIGHT, buff=SANKEY_GAP_S4)

        # ── Sankey ribbons: sparse neuron → concept label ─────────────────────
        # Primary (thick, concept color): each neuron → its own concept.
        # Secondary (thin, dim): each neuron → every other concept.
        s4_x1 = n_circles[0].get_right()[0] + 0.06
        s4_x2 = n_circles[0].get_right()[0] + SANKEY_GAP_S4 - 0.06

        def _sankey_s4(y1, y2, w, color, opacity):
            cx   = (s4_x1 + s4_x2) / 2
            half = w / 2
            tl = np.array([s4_x1, y1 + half, 0])
            tr = np.array([s4_x2, y2 + half, 0])
            br = np.array([s4_x2, y2 - half, 0])
            bl = np.array([s4_x1, y1 - half, 0])
            band = VMobject(fill_color=color, fill_opacity=opacity, stroke_width=0)
            band.start_new_path(tl)
            band.add_cubic_bezier_curve_to(
                np.array([cx, y1 + half, 0]),
                np.array([cx, y2 + half, 0]),
                tr,
            )
            band.add_line_to(br)
            band.add_cubic_bezier_curve_to(
                np.array([cx, y2 - half, 0]),
                np.array([cx, y1 - half, 0]),
                bl,
            )
            band.close_path()
            return band

        S4_PW = 0.11   # primary ribbon width
        S4_SW = 0.022  # secondary ribbon width

        primary_sankey = VGroup(*[
            _sankey_s4(
                n_circles[i].get_center()[1],
                n_circles[i].get_center()[1],
                S4_PW, CONCEPT_COLORS[i], 0.30,   # start dim, brighten on activation
            )
            for i in range(N)
        ])

        secondary_sankey = VGroup(*[
            _sankey_s4(
                n_circles[i].get_center()[1],
                n_circles[j].get_center()[1],
                S4_SW, DIM_GRAY, 0.20,
            )
            for i in range(N)
            for j in range(N)
            if i != j
        ])

        sparse_dim_lbl = MathTex(r"\sim 10^{3\text{-}4}", color=GRAY_TEXT).scale(0.30)
        sparse_dim_lbl.next_to(n_circles, UP, buff=0.12)

        arr_sae2n = arrow(sae_shape.get_right(), n_circles.get_left())

        # ── Section labels (same y baseline, each fades in with its component) ──
        LSCALE = 0.28
        vid_lbl       = VGroup(
            Text("post-treatment observation", color=WHITE_TEXT).scale(LSCALE),
            Text("(video)",                    color=WHITE_TEXT).scale(LSCALE),
        ).arrange(DOWN, buff=0.04)
        entangled_lbl = Text("entangled representation", color=WHITE_TEXT).scale(LSCALE)
        sparse_lbl    = Text("sparse representation", color=WHITE_TEXT).scale(LSCALE)
        interp_lbl    = Text("interpretation",        color=WHITE_TEXT).scale(LSCALE)

        label_y = dots_circle.get_bottom()[1] - 0.22
        vid_lbl.move_to([vid.get_center()[0],
                         label_y - vid_lbl.height / 2, 0])
        entangled_lbl.move_to([ent_neurons.get_center()[0],
                                label_y - entangled_lbl.height / 2, 0])
        sparse_lbl.move_to([n_circles.get_center()[0],
                             label_y - sparse_lbl.height / 2, 0])
        interp_lbl.move_to([c_txts.get_center()[0],
                             label_y - interp_lbl.height / 2, 0])

        # ── Activation patterns (defined early so ent_only_anims can use them) ──
        PATTERNS = [
            [0.85, 0.0,  0.0,  0.0,  0.0,  0.0,  0.80, 0.0 ],
            [0.0,  0.90, 0.0,  0.85, 0.0,  0.0,  0.0,  0.55],
            [0.0,  0.0,  0.80, 0.0,  0.95, 0.0,  0.0,  0.0 ],
            [0.75, 0.0,  0.65, 0.0,  0.0,  0.0,  0.0,  0.0 ],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.90, 0.0,  0.70],
            [0.0,  0.85, 0.0,  0.90, 0.0,  0.0,  0.0,  0.0 ],
        ]

        def ent_only_anims(pattern):
            """Animate only the entangled neuron sectors (no sparse circles/sankey)."""
            anims = []
            for c_idx, val in enumerate(pattern):
                for j in range(N_ENT):
                    sec = ENT_SECTOR_FOR_CONCEPT[j][c_idx]
                    anims.append(
                        ent_neurons[j][0][sec].animate.set_fill(
                            opacity=0.90 if val > 0.3 else 0.12
                        )
                    )
            return anims

        # ── Animations ────────────────────────────────────────────────────────
        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(per_obs, shift=DOWN * 0.06), run_time=0.4)
        self.play(tracker.animate.set_value(tracker.get_value() + 1.1), run_time=1.1, rate_func=linear)
        self.next_slide()

        self.play(
            FadeIn(vid), FadeIn(vid_lbl),
            tracker.animate.set_value(tracker.get_value() + 0.5),
            run_time=0.5, rate_func=linear,
        )
        self.play(tracker.animate.set_value(tracker.get_value() + 3.0), run_time=3.0, rate_func=linear)

        self.play(
            FadeIn(vit_shape), FadeIn(vit_lbl), Create(arr_vid2vit),
            tracker.animate.set_value(tracker.get_value() + 0.7),
            run_time=0.7, rate_func=linear,
        )
        self.play(
            Create(arr_vit2ent),
            LaggedStart(*[GrowFromCenter(n) for n in ent_neurons], lag_ratio=0.08),
            FadeIn(ent_dots), FadeIn(ent_dim_lbl), FadeIn(entangled_lbl),
            *ent_only_anims(PATTERNS[0]),
            tracker.animate.set_value(tracker.get_value() + 0.7),
            run_time=0.7, rate_func=linear,
        )
        # Entangled neurons keep cycling through patterns
        T_ent = tracker.get_value()
        for i, pat in enumerate(PATTERNS[1:3]):
            self.play(
                *ent_only_anims(pat),
                tracker.animate.set_value(T_ent + (i + 1) * 1.0),
                run_time=1.0, rate_func=linear,
            )

        # SAE + sparse appear gradually; entangled neurons keep cycling
        ent_pat_idx = 3  # continue from pattern 3 (first 3 used above)
        self.play(
            FadeIn(sae_shape), FadeIn(sae_lbl), Create(arr_ent2sae),
            *ent_only_anims(PATTERNS[ent_pat_idx % len(PATTERNS)]),
            tracker.animate.set_value(tracker.get_value() + 0.7),
            run_time=0.7, rate_func=linear,
        )
        ent_pat_idx += 1
        self.play(
            Create(arr_sae2n),
            *ent_only_anims(PATTERNS[ent_pat_idx % len(PATTERNS)]),
            tracker.animate.set_value(tracker.get_value() + 0.4),
            run_time=0.4, rate_func=linear,
        )
        ent_pat_idx += 1
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    GrowFromCenter(n_circles[i]),
                    FadeIn(primary_sankey[i]),
                    FadeIn(c_txts[i]),
                )
                for i in range(N)
            ], lag_ratio=0.09),
            FadeIn(dots_circle), FadeIn(dots_txt),
            FadeIn(sparse_dim_lbl), FadeIn(sparse_lbl), FadeIn(interp_lbl),
            *ent_only_anims(PATTERNS[ent_pat_idx % len(PATTERNS)]),
            tracker.animate.set_value(tracker.get_value() + 1.2),
            run_time=1.2, rate_func=linear,
        )
        ent_pat_idx += 1
        self.play(
            FadeIn(secondary_sankey),
            *ent_only_anims(PATTERNS[ent_pat_idx % len(PATTERNS)]),
            run_time=0.4, rate_func=linear,
        )
        self.play(tracker.animate.set_value(tracker.get_value() + 3.0), run_time=3.0, rate_func=linear)

        # ── Dynamic: video + entangled sectors + sparse concepts ───────────────
        # When concept c fires: the sector carrying that concept's color brightens
        # in each neuron (but at a DIFFERENT sector position per neuron, since
        # colors are shuffled) → visually distinct activation per neuron.
        T0 = tracker.get_value()
        PATTERNS = [
            [0.85, 0.0,  0.0,  0.0,  0.0,  0.0,  0.80, 0.0 ],
            [0.0,  0.90, 0.0,  0.85, 0.0,  0.0,  0.0,  0.55],
            [0.0,  0.0,  0.80, 0.0,  0.95, 0.0,  0.0,  0.0 ],
            [0.75, 0.0,  0.65, 0.0,  0.0,  0.0,  0.0,  0.0 ],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.90, 0.0,  0.70],
            [0.0,  0.85, 0.0,  0.90, 0.0,  0.0,  0.0,  0.0 ],
        ]

        def all_anims(pattern):
            anims = []
            for c_idx, val in enumerate(pattern):
                col = CONCEPT_COLORS[c_idx]
                if val > 0.3:
                    for j in range(N_ENT):
                        sec = ENT_SECTOR_FOR_CONCEPT[j][c_idx]
                        anims.append(
                            ent_neurons[j][0][sec].animate.set_fill(opacity=0.90)
                        )
                    anims += [
                        n_circles[c_idx].animate
                            .set_fill(col, opacity=val).set_stroke(col, width=2.0),
                        c_txts[c_idx].animate.set_color(col),
                        primary_sankey[c_idx].animate.set_fill(color=col, opacity=0.85),
                    ]
                else:
                    for j in range(N_ENT):
                        sec = ENT_SECTOR_FOR_CONCEPT[j][c_idx]
                        anims.append(
                            ent_neurons[j][0][sec].animate.set_fill(opacity=0.12)
                        )
                    anims += [
                        n_circles[c_idx].animate
                            .set_fill(DIM_GRAY, opacity=0.2).set_stroke(DIM_GRAY, width=1.5),
                        c_txts[c_idx].animate.set_color(DIM_GRAY),
                        primary_sankey[c_idx].animate.set_fill(color=DIM_GRAY, opacity=0.15),
                    ]
            return anims

        seg = 2.5
        for i, pat in enumerate(PATTERNS * 2):
            self.play(
                *all_anims(pat),
                tracker.animate.set_value(T0 + (i + 1) * seg),
                run_time=seg,
                rate_func=linear,
            )

        self.play(tracker.animate.set_value(tracker.get_value() + 3.0), run_time=3.0, rate_func=linear)

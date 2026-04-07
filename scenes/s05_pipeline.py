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


class S05Pipeline(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ─────────────────────────────────────────────────────────────
        title = slide_title("Exploratory Causal Inference")
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ── Slide 1: treatment + effect gifs ──────────────────────────────────
        t_fps = 10
        vid_t = VideoPlayer(TFRAMES, fps=t_fps).scale_to_fit_height(3.2)
        vid_e = VideoPlayer(EFRAMES, fps=t_fps).scale_to_fit_height(3.2)

        lbl_t = Text("treatment",                  color=GRAY_TEXT).scale(0.30)
        lbl_e = Text("post-treatment observation", color=GRAY_TEXT).scale(0.30)

        col_t = Group(vid_t, lbl_t).arrange(DOWN, buff=0.18)
        col_e = Group(vid_e, lbl_e).arrange(DOWN, buff=0.18)
        vids  = Group(col_t, col_e).arrange(RIGHT, buff=1.0).center().shift(DOWN * 0.4)

        tracker = ValueTracker(0)
        vid_t.add_updater(lambda m: m.set_time(tracker.get_value()))
        vid_e.add_updater(lambda m: m.set_time(tracker.get_value()))

        self.play(FadeIn(vids), run_time=1.0)
        self.play(tracker.animate.set_value(4.0), run_time=4.0, rate_func=linear)
        vid_t.clear_updaters()
        vid_e.clear_updaters()
        self.next_slide()

        # ── Slide 2: DAG  T → Z_i ────────────────────────────────────────────
        r_node = 0.44         # all nodes same size as T
        n_dag  = 5            # Z₁…Z₅; Z_m added below "..."
        fs     = 0.65         # label scale — same for T and Z_i

        CONCEPTS  = ["grooming", "locomotion", "body contact", "resting", "antennae"]
        CONCEPT_M = "nest structure"

        # Match s04 concept colors
        CONCEPT_COLORS = {
            "grooming":      "#5BCFB5",
            "locomotion":    GREEN_LIGHT,
            "body contact":  BLUE_LIGHT,
            "resting":       PURPLE_LIGHT,
            "antennae":      YELLOW_LIGHT,
            "nest structure":"#7EC8F8",
        }
        C_COLS = [CONCEPT_COLORS[c] for c in CONCEPTS]
        C_COL_M = CONCEPT_COLORS[CONCEPT_M]

        # ── Nodes ─────────────────────────────────────────────────────────────
        T_circ = Circle(radius=r_node, color=WHITE_TEXT, stroke_width=3.5)
        T_lbl  = MathTex("T", color=WHITE_TEXT).scale(fs)

        n_circs = VGroup(*[
            Circle(radius=r_node, color=WHITE_TEXT,
                   stroke_width=2.0, fill_opacity=0)
            for i in range(n_dag)
        ]).arrange(DOWN, buff=0.10)

        dots_dag = MathTex(r"\vdots", color=GRAY_TEXT).scale(0.55)

        # Place before centering
        T_circ.move_to(LEFT * 3.2)
        n_circs.move_to(RIGHT * 0.6)
        dots_dag.next_to(n_circs, DOWN, buff=0.10)

        # Z_m circle — same style as the others
        z_m_circ = Circle(radius=r_node, color=WHITE_TEXT,
                          stroke_width=2.0, fill_opacity=0)
        z_m_circ.next_to(dots_dag, DOWN, buff=0.10)

        # Centre everything together
        dag_all = VGroup(T_circ, n_circs, dots_dag, z_m_circ)
        dag_all.center().shift(DOWN * 0.3)

        # Labels INSIDE nodes (placed after centering, same scale as T)
        T_lbl.move_to(T_circ)

        z_labels = VGroup(*[
            MathTex(rf"Z_{{{i+1}}}", color=WHITE_TEXT).scale(fs)
            .move_to(n_circs[i])
            for i in range(n_dag)
        ])
        z_m_lbl = MathTex(r"Z_m", color=WHITE_TEXT).scale(fs)
        z_m_lbl.move_to(z_m_circ)

        # ── Concept column ────────────────────────────────────────────────────
        # After DAG shifts LEFT*4.0, concept labels land at x ≈ -0.1..0.6,
        # safely left of assumption boxes (left edge at x = 1.3).
        CONCEPT_X_OFFSET = 1.5   # node right-edge → concept left-edge gap

        interp_labels = VGroup(*[
            Text(CONCEPTS[i], color=GRAY_TEXT).scale(0.28)
            for i in range(n_dag)
        ])
        interp_m = Text(CONCEPT_M, color=GRAY_TEXT).scale(0.28)

        concept_x = n_circs[0].get_right()[0] + CONCEPT_X_OFFSET
        for i in range(n_dag):
            interp_labels[i].move_to(
                np.array([concept_x + interp_labels[i].get_width() / 2,
                          n_circs[i].get_center()[1], 0])
            )
        interp_m.move_to(
            np.array([concept_x + interp_m.get_width() / 2,
                      z_m_circ.get_center()[1], 0])
        )

        # ── Sankey ribbons ─────────────────────────────────────────────────────
        # Each band is a filled VMobject with cubic-bezier (S-curve) top and bottom
        # edges, giving a proper Sankey-diagram look.
        # Primary ribbon: thick, one per neuron → its own concept (same row).
        # Secondary ribbons: thin, each neuron → every other concept.
        all_nodes   = list(n_circs) + [z_m_circ]
        all_labels  = list(interp_labels) + [interp_m]
        flow_x1     = n_circs[0].get_right()[0] + 0.06   # all bands share the same x1
        flow_x2     = concept_x - 0.06                    # and the same x2
        PRIMARY_W   = 0.13
        SECONDARY_W = 0.055

        def _sankey(y1, y2, w, color, opacity):
            """Filled S-curve ribbon from (flow_x1, y1) to (flow_x2, y2)."""
            cx   = (flow_x1 + flow_x2) / 2
            half = w / 2
            tl = np.array([flow_x1, y1 + half, 0])
            tr = np.array([flow_x2, y2 + half, 0])
            br = np.array([flow_x2, y2 - half, 0])
            bl = np.array([flow_x1, y1 - half, 0])
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

        primary_flows = VGroup(*[
            _sankey(
                all_nodes[i].get_center()[1],
                all_nodes[i].get_center()[1],
                PRIMARY_W, WHITE_TEXT, 0.65,
            )
            for i in range(len(all_nodes))
        ])

        secondary_flows = VGroup(*[
            _sankey(
                all_nodes[i].get_center()[1],
                all_labels[j].get_center()[1],
                SECONDARY_W, DIM_GRAY, 0.35,
            )
            for i in range(len(all_nodes))
            for j in range(len(all_labels))
            if i != j
        ])

        # ── Arrows (fixed tip size via max_tip_length_to_length_ratio) ─────────
        TIP_ABS = 0.20   # desired absolute tip length
        def _arrow(start, end):
            length = np.linalg.norm(end - start)
            return Arrow(
                start, end,
                color=WHITE_TEXT, buff=0, stroke_width=2.5,
                max_tip_length_to_length_ratio=TIP_ABS / max(length, 0.01),
            )

        arrows = VGroup(*[
            _arrow(
                T_circ.get_right() + RIGHT * 0.05,
                n_circs[i].get_left() + LEFT * 0.05,
            )
            for i in range(n_dag)
        ])
        arrow_m = _arrow(
            T_circ.get_right() + RIGHT * 0.05,
            z_m_circ.get_left() + LEFT * 0.05,
        )

        # Single "?" above the arrow fan, slightly below title area
        hyp_x = (T_circ.get_right()[0] + n_circs.get_left()[0]) / 2
        hyp_y = n_circs[0].get_center()[1] + 0.15
        hyp_anchor = np.array([hyp_x, hyp_y, 0])
        q_single = MathTex("?", color=WHITE_TEXT).scale(0.70).move_to(hyp_anchor)

        # ── Transition: gifs → DAG ────────────────────────────────────────────
        # Step 1: Fade out labels, shrink treatment vid → T node position
        # Pre-place T_circ and T_lbl (invisible) so we know exact target
        T_circ.set_opacity(0)
        T_lbl.set_opacity(0)
        self.add(T_circ, T_lbl)

        # Shrink treatment video toward T position, fade its label
        self.play(
            FadeOut(lbl_t, shift=DOWN * 0.3),
            FadeOut(lbl_e, shift=DOWN * 0.3),
            vid_t.animate.scale_to_fit_height(r_node * 2).move_to(T_circ),
            run_time=0.8,
        )

        # Replace treatment vid with T node
        self.play(
            FadeOut(vid_t),
            T_circ.animate.set_opacity(1),
            T_lbl.animate.set_opacity(1),
            run_time=0.5,
        )

        # Step 2: Show model extracting neuron activations from post-treatment
        # Move effect vid to center-right & shrink slightly
        model_pos = (T_circ.get_center() + n_circs.get_center()) / 2
        model_lbl = Text("SAE", color=PURPLE_LIGHT).scale(0.38)
        model_box = SurroundingRectangle(
            model_lbl, color=PURPLE_LIGHT, buff=0.12,
            stroke_width=1.8, corner_radius=0.08,
        )
        model_grp = VGroup(model_box, model_lbl).move_to(model_pos).shift(UP * 1.6)

        self.play(
            vid_e.animate.scale_to_fit_height(2.0).move_to(
                model_grp.get_center() + UP * 1.6
            ),
            run_time=0.7,
        )

        # SAE box appears, arrow from vid_e into it
        arr_into_model = Arrow(
            vid_e.get_bottom() + DOWN * 0.05,
            model_grp.get_top() + UP * 0.05,
            color=PURPLE_LIGHT, buff=0, stroke_width=2.0,
            max_tip_length_to_length_ratio=0.3,
        )
        self.play(
            FadeIn(model_grp, scale=0.8),
            Create(arr_into_model),
            run_time=0.6,
        )

        # Arrow from model to Z column position + reveal Z nodes
        z_col_center = VGroup(n_circs, z_m_circ).get_center()
        arr_out_model = Arrow(
            model_grp.get_bottom() + DOWN * 0.05,
            np.array([z_col_center[0], model_grp.get_bottom()[1] - 0.8, 0]),
            color=PURPLE_LIGHT, buff=0, stroke_width=2.0,
            max_tip_length_to_length_ratio=0.3,
        )

        # Z label header
        z_header = MathTex(r"\mathbf{Z}", color=WHITE_TEXT).scale(0.55)
        z_header.move_to(arr_out_model.get_end() + DOWN * 0.15)

        self.play(
            Create(arr_out_model),
            FadeIn(z_header, shift=DOWN * 0.2),
            run_time=0.6,
        )
        self.wait(0.3)

        # Step 3: Clean up model intermediary, reveal full DAG Z column
        self.play(
            FadeOut(vid_e),
            FadeOut(arr_into_model),
            FadeOut(model_grp),
            FadeOut(arr_out_model),
            FadeOut(z_header),
            run_time=0.5,
        )

        # Z₁…Z₅ with labels inside + primary Sankey ribbon + concept labels
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    GrowFromCenter(n_circs[i]),
                    FadeIn(z_labels[i]),
                    FadeIn(primary_flows[i]),
                    FadeIn(interp_labels[i]),
                )
                for i in range(n_dag)
            ], lag_ratio=0.12),
            FadeIn(dots_dag),
            run_time=1.5,
        )
        # Z_m below "..."
        self.play(
            GrowFromCenter(z_m_circ),
            FadeIn(z_m_lbl),
            FadeIn(primary_flows[n_dag]), FadeIn(interp_m),
            run_time=0.6,
        )
        # Reveal secondary bleed connections (all neurons → all other concepts)
        self.play(FadeIn(secondary_flows), run_time=0.7)
        # Arrows from T to all neurons (including Z_m, same style)
        self.play(
            LaggedStart(*[Create(arr) for arr in arrows], lag_ratio=0.07),
            Create(arrow_m),
            run_time=1.4,
        )
        # Single "?" over the bundle
        self.play(FadeIn(q_single, scale=0.5), run_time=0.5)
        self.wait(1)
        self.next_slide()

        # ── Ground Truth: highlight 2 neurons ─────────────────────────────────
        GT_IDX = [0, 3]   # grooming, resting
        gt_lbl = Text("Ground Truth:", color=WHITE_TEXT).scale(0.36).move_to(hyp_anchor)

        gt_anims = []
        for i in range(n_dag):
            if i in GT_IDX:
                gt_anims += [
                    n_circs[i].animate.set_stroke(
                        color=WHITE_TEXT, width=3.0, opacity=1.0),
                    z_labels[i].animate.set_color(WHITE_TEXT),
                    primary_flows[i].animate.set_fill(color=WHITE_TEXT, opacity=0.90),
                    interp_labels[i].animate.set_color(WHITE_TEXT),
                    arrows[i].animate.set_color(WHITE_TEXT).set_opacity(1.0),
                ]
            else:
                gt_anims += [
                    n_circs[i].animate.set_stroke(
                        color=DIM_GRAY, width=1.5, opacity=0.40),
                    z_labels[i].animate.set_color(DIM_GRAY),
                    primary_flows[i].animate.set_fill(color=DIM_GRAY, opacity=0.20),
                    interp_labels[i].animate.set_color(DIM_GRAY),
                    arrows[i].animate.set_color(DIM_GRAY).set_opacity(0.35),
                ]
        gt_anims += [
            z_m_circ.animate.set_stroke(color=DIM_GRAY, width=1.5, opacity=0.40),
            z_m_lbl.animate.set_color(DIM_GRAY),
            primary_flows[n_dag].animate.set_fill(color=DIM_GRAY, opacity=0.20),
            interp_m.animate.set_color(DIM_GRAY),
            arrow_m.animate.set_color(DIM_GRAY).set_opacity(0.35),
            secondary_flows.animate.set_fill(opacity=0.08),
        ]

        self.play(FadeOut(q_single, scale=0.8), run_time=0.3)
        self.play(FadeIn(gt_lbl, scale=1.1), *gt_anims, run_time=0.8)
        self.wait(1)
        self.next_slide()

        # ── Shift DAG left + show assumptions on the right ────────────────────
        # Collect every DAG mobject into one group for shifting
        dag_group = VGroup(
            T_circ, T_lbl,
            n_circs, z_labels, primary_flows, secondary_flows, interp_labels,
            dots_dag, z_m_circ, z_m_lbl, interp_m,
            arrows, arrow_m, gt_lbl,
        )

        self.play(dag_group.animate.shift(LEFT * 4.0), run_time=0.8)

        # ── Assumption boxes ──────────────────────────────────────────────────
        # Fixed shared width so both boxes are identical in size
        BOX_W     = 5.0
        BOX_PAD   = 0.28
        BOX_COLOR = WHITE_TEXT

        def make_assumption(label, *body_lines):
            lbl_tex   = Tex(rf"\textbf{{{label}}}", color=WHITE_TEXT).scale(0.44)
            body_texs = [Tex(line, color=GRAY_TEXT).scale(0.40) for line in body_lines]
            content   = VGroup(lbl_tex, *body_texs).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            box = Rectangle(
                width=BOX_W,
                height=content.get_height() + 2 * BOX_PAD,
                color=BOX_COLOR, stroke_width=1.4, fill_opacity=0,
            )
            # Centre vertically, then pin left edge to box left + padding
            content.move_to(box)
            content.shift(LEFT * (content.get_left()[0] - (box.get_left()[0] + BOX_PAD)))
            return VGroup(box, content)

        a1 = make_assumption(
            "Assumption 1:",
            r"effects entangled in the post-treatment",
            r"observation, e.g., visible behaviour",
        )
        a2 = make_assumption(
            "Assumption 2:",
            r"effect concepts $\sim$retrieved by dictionary learning",
        )

        assumptions = VGroup(a1, a2).arrange(DOWN, buff=0.40)
        assumptions.move_to(RIGHT * 3.8).align_to(n_circs, UP).shift(DOWN * 0.2)

        self.play(FadeIn(a1, shift=LEFT * 0.15), run_time=0.7)
        self.wait(0.5)
        self.play(FadeIn(a2, shift=LEFT * 0.15), run_time=0.7)
        self.wait(1)
        self.next_slide()

        # ── Emphasize A1 ─────────────────────────────────────────────────────
        self.play(a1.animate.scale(1.15), run_time=0.4)
        self.play(a1.animate.scale(1 / 1.15), run_time=0.4)
        self.wait(0.5)
        self.next_slide()

        # ── Emphasize A2 ─────────────────────────────────────────────────────
        self.play(a2.animate.scale(1.15), run_time=0.4)
        self.play(a2.animate.scale(1 / 1.15), run_time=0.4)
        self.wait(0.5)
        self.next_slide()

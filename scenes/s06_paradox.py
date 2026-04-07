from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *
import numpy as np


class S06Paradox(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ─────────────────────────────────────────────────────────────
        title = slide_title("Challenge")
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # Reproduce the DAG + Sankey flow from s05
        # ══════════════════════════════════════════════════════════════════════
        r_node = 0.44
        n_dag  = 5
        fs     = 0.65

        CONCEPTS  = ["grooming", "locomotion", "body contact", "resting", "antennae"]
        CONCEPT_M = "nest structure"

        CONCEPT_COLORS = {
            "grooming":       "#5BCFB5",
            "locomotion":     GREEN_LIGHT,
            "body contact":   BLUE_LIGHT,
            "resting":        PURPLE_LIGHT,
            "antennae":       YELLOW_LIGHT,
            "nest structure": "#7EC8F8",
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

        T_circ.move_to(LEFT * 3.2)
        n_circs.move_to(RIGHT * 0.6)
        dots_dag.next_to(n_circs, DOWN, buff=0.10)

        z_m_circ = Circle(radius=r_node, color=WHITE_TEXT,
                          stroke_width=2.0, fill_opacity=0)
        z_m_circ.next_to(dots_dag, DOWN, buff=0.10)

        dag_all = VGroup(T_circ, n_circs, dots_dag, z_m_circ)
        dag_all.center().shift(DOWN * 0.3)

        T_lbl.move_to(T_circ)

        z_labels = VGroup(*[
            MathTex(rf"Z_{{{i+1}}}", color=WHITE_TEXT).scale(fs)
            .move_to(n_circs[i])
            for i in range(n_dag)
        ])
        z_m_lbl = MathTex(r"Z_m", color=WHITE_TEXT).scale(fs)
        z_m_lbl.move_to(z_m_circ)

        # ── Concept labels ────────────────────────────────────────────────────
        CONCEPT_X_OFFSET = 1.5

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

        # ── Sankey ribbons ────────────────────────────────────────────────────
        all_nodes  = list(n_circs) + [z_m_circ]
        all_labels = list(interp_labels) + [interp_m]
        flow_x1    = n_circs[0].get_right()[0] + 0.06
        flow_x2    = concept_x - 0.06
        PRIMARY_W  = 0.13
        SECONDARY_W = 0.055

        def _sankey(y1, y2, w, color, opacity):
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

        # ── Arrows ────────────────────────────────────────────────────────────
        TIP_ABS = 0.20
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

        # ── Show entire DAG at once (recap from s05) ─────────────────────────
        dag_group = VGroup(
            T_circ, T_lbl,
            n_circs, z_labels, primary_flows, secondary_flows, interp_labels,
            dots_dag, z_m_circ, z_m_lbl, interp_m,
            arrows, arrow_m,
        )

        self.play(FadeIn(dag_group), run_time=1.0)
        self.wait(0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # Highlight GROOMING: dim everything else, keep only grooming flow
        # ══════════════════════════════════════════════════════════════════════
        GROOM_IDX = 0   # grooming is concept/neuron index 0

        # Build secondary flows that go TO grooming (from other neurons)
        # In the secondary_flows list, index mapping: for node i, concept j (i!=j),
        # linear index = i*(len(all_labels)-1) + (j if j<i else j-1)
        # We want all ribbons where j == GROOM_IDX (target = grooming concept)
        n_total = len(all_nodes)  # 6
        n_concepts = len(all_labels)  # 6
        sec_to_groom_indices = []
        idx = 0
        for i in range(n_total):
            for j in range(n_concepts):
                if i != j:
                    if j == GROOM_IDX:
                        sec_to_groom_indices.append(idx)
                    idx += 1

        dim_anims = []

        # Dim only primary flows and concept labels of non-grooming nodes
        # (keep their circles, z_labels, and arrows white — they link to grooming via secondary flows)
        for i in range(n_dag):
            if i == GROOM_IDX:
                continue
            dim_anims += [
                primary_flows[i].animate.set_fill(opacity=0.08),
                interp_labels[i].animate.set_opacity(0.15),
            ]
        # Dim Z_m primary flow and concept label (keep circle, label, arrow white)
        dim_anims += [
            primary_flows[n_dag].animate.set_fill(opacity=0.08),
            interp_m.animate.set_opacity(0.15),
            dots_dag.animate.set_opacity(0.15),
        ]

        # Dim all secondary flows except those entering grooming (keep those white)
        sec_to_groom_set = set(sec_to_groom_indices)
        for si in range(len(secondary_flows)):
            if si in sec_to_groom_set:
                dim_anims.append(secondary_flows[si].animate.set_fill(color=WHITE_TEXT, opacity=0.35))
            else:
                dim_anims.append(secondary_flows[si].animate.set_fill(opacity=0.04))

        # Keep grooming node, label, arrow, primary flow bright
        dim_anims += [
            n_circs[GROOM_IDX].animate.set_stroke(color=WHITE_TEXT, width=3.0, opacity=1.0),
            z_labels[GROOM_IDX].animate.set_color(WHITE_TEXT).set_opacity(1.0),
            primary_flows[GROOM_IDX].animate.set_fill(color=WHITE_TEXT, opacity=0.95),
            interp_labels[GROOM_IDX].animate.set_color(WHITE_TEXT).set_opacity(1.0),
            arrows[GROOM_IDX].animate.set_color(WHITE_TEXT).set_opacity(1.0),
        ]

        # Grooming concept highlight label
        groom_highlight = Text("grooming", color=WHITE_TEXT).scale(0.42)
        groom_highlight.move_to(interp_labels[GROOM_IDX]).align_to(
            interp_labels[GROOM_IDX], LEFT)

        self.play(
            *dim_anims,
            Transform(interp_labels[GROOM_IDX], groom_highlight),
            run_time=1.0,
        )
        self.wait(0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # Principal neuron: Z₁ → GREEN (it truly encodes grooming)
        # ══════════════════════════════════════════════════════════════════════
        self.play(
            n_circs[GROOM_IDX].animate.set_stroke(color=GREEN_LIGHT, width=3.5),
            z_labels[GROOM_IDX].animate.set_color(GREEN_LIGHT),
            arrows[GROOM_IDX].animate.set_color(GREEN_LIGHT),
            primary_flows[GROOM_IDX].animate.set_fill(color=GREEN_LIGHT, opacity=0.90),
            run_time=0.8,
        )
        self.wait(0.5)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # All OTHER neurons also light up RED (entanglement leakage)
        # ══════════════════════════════════════════════════════════════════════
        red_anims = []

        for i in range(n_dag):
            if i == GROOM_IDX:
                continue
            red_anims += [
                n_circs[i].animate.set_stroke(color=RED_LIGHT, width=3.5, opacity=1.0),
                z_labels[i].animate.set_color(RED_LIGHT).set_opacity(1.0),
                arrows[i].animate.set_color(RED_LIGHT).set_opacity(0.80),
            ]

        # Z_m also red
        red_anims += [
            z_m_circ.animate.set_stroke(color=RED_LIGHT, width=3.5, opacity=1.0),
            z_m_lbl.animate.set_color(RED_LIGHT).set_opacity(1.0),
            arrow_m.animate.set_color(RED_LIGHT).set_opacity(0.80),
            dots_dag.animate.set_opacity(0.60),
        ]

        # Secondary flows TO grooming in red with varying opacities
        sec_opacities = [0.55, 0.25, 0.45, 0.18, 0.38]
        for k, si in enumerate(sec_to_groom_indices):
            op = sec_opacities[k % len(sec_opacities)]
            red_anims.append(
                secondary_flows[si].animate.set_fill(color=RED_LIGHT, opacity=op)
            )

        # Revert grooming node (green → white) simultaneously
        red_anims += [
            n_circs[GROOM_IDX].animate.set_stroke(color=WHITE_TEXT, width=3.0),
            z_labels[GROOM_IDX].animate.set_color(WHITE_TEXT),
            arrows[GROOM_IDX].animate.set_color(WHITE_TEXT),
            primary_flows[GROOM_IDX].animate.set_fill(color=WHITE_TEXT, opacity=0.95),
        ]

        self.play(*red_anims, run_time=1.0)
        self.wait(1)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # Rename title → "Paradox of Causal Inference"
        # Revert all colored nodes / arrows / flows back to white
        # ══════════════════════════════════════════════════════════════════════
        new_title = Text("Paradox of Exploratory Causal Inference", color=WHITE_TEXT).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        revert_anims = [
            # z_m: red → white
            z_m_circ.animate.set_stroke(color=WHITE_TEXT, width=3.0, opacity=1.0),
            z_m_lbl.animate.set_color(WHITE_TEXT).set_opacity(1.0),
            arrow_m.animate.set_color(WHITE_TEXT).set_opacity(1.0),
        ]
        for i in range(n_dag):
            if i == GROOM_IDX:
                continue
            revert_anims += [
                n_circs[i].animate.set_stroke(color=WHITE_TEXT, width=3.0, opacity=1.0),
                z_labels[i].animate.set_color(WHITE_TEXT).set_opacity(1.0),
                arrows[i].animate.set_color(WHITE_TEXT).set_opacity(1.0),
            ]
        for si in sec_to_groom_indices:
            revert_anims.append(secondary_flows[si].animate.set_fill(color=WHITE_TEXT, opacity=0.35))

        self.play(Transform(title, new_title), *revert_anims, run_time=1.0)
        self.wait(0.3)

        # ── Quick emphasis: flash all T→Z arrows ─────────────────────────────
        all_arrows_group = VGroup(*arrows, arrow_m)
        self.play(
            all_arrows_group.animate.set_color(YELLOW_LIGHT).set_stroke(width=5),
            run_time=0.5,
        )
        self.play(
            all_arrows_group.animate.set_color(WHITE_TEXT).set_stroke(width=2.5),
            run_time=0.5,
        )
        self.wait(0.3)
        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # All concept labels → scale 0.42, with ✓/✗ symbols
        # grooming → ✓ grooming (green), all others → ✗ concept (red)
        # ══════════════════════════════════════════════════════════════════════
        HIGHLIGHT_SCALE = 0.42

        def _concept_label(symbol, text, color, y):
            lbl = Text(f"{symbol} {text}", color=color).scale(HIGHLIGHT_SCALE)
            lbl.move_to(np.array([concept_x + lbl.get_width() / 2, y, 0]))
            return lbl

        groom_final = _concept_label("✓", "grooming", GREEN_LIGHT, n_circs[GROOM_IDX].get_center()[1])

        color_anims = [Transform(interp_labels[GROOM_IDX], groom_final)]
        for i in range(n_dag):
            if i == GROOM_IDX:
                continue
            lbl = _concept_label("✗", CONCEPTS[i], RED_LIGHT, n_circs[i].get_center()[1])
            color_anims.append(Transform(interp_labels[i], lbl))
        lbl_m = _concept_label("✗", CONCEPT_M, RED_LIGHT, z_m_circ.get_center()[1])
        color_anims.append(Transform(interp_m, lbl_m))

        self.play(*color_anims, run_time=0.8)
        self.wait(0.5)
        self.next_slide()

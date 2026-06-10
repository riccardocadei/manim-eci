from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "logo")
LOGO_H   = 1.05


class S01Title(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ────────────────────────────────────────────────────────────
        line1 = Text("Scaling Empiricism", color=WHITE_TEXT).scale(0.82)
        line1.move_to(UP * 1.6)

        line2 = Text("in Artificial Causal Inference", color=WHITE_TEXT).scale(0.82)
        line2.next_to(line1, DOWN, buff=0.22)

        title = VGroup(line1, line2)

        # ── Presenter info ───────────────────────────────────────────────────
        name = Text("Riccardo Cadei", color=WHITE_TEXT, weight=BOLD).scale(0.42)
        aff_lines = VGroup(*[
            Text(t, color="#AAAAAA").scale(0.26)
            for t in (
                "PhD Student",
                "Causal Learning and Artificial Intelligence Group",
                "Institute of Science and Technology, Austria (ISTA)",
            )
        ]).arrange(DOWN, buff=0.08)
        presenter = VGroup(name, aff_lines).arrange(DOWN, buff=0.22)
        presenter.next_to(title, DOWN, buff=0.60)

        # ── Logo ─────────────────────────────────────────────────────────────
        logo_ista = SVGMobject(os.path.join(LOGO_DIR, "ISTA.svg"))
        logo_ista.set_color(WHITE_TEXT)
        logo_ista.scale_to_fit_height(LOGO_H)
        logo_ista.to_edge(DOWN, buff=0.50)

        # ── Slide 1: appear ──────────────────────────────────────────────────
        self.play(Write(line1), run_time=1.0)
        self.play(FadeIn(line2, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(presenter, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(logo_ista, shift=UP * 0.1), run_time=0.6)
        self.wait(1)
        self.next_slide()

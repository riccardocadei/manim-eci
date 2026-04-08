from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S10Conclusion(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ────────────────────────────────────────────────────────────
        title = slide_title("Conclusion")
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ── Take-away 1 ─────────────────────────────────────────────────────
        bullet_1 = Text("1.", color=WHITE_TEXT).scale(BODY_SCALE)
        text_1 = Text(
            "Dictionary Learning enables Exploratory Causal Inference in latent space",
            color=WHITE_TEXT,
        ).scale(BODY_SCALE)
        tag_1 = Text("(new?)", color=YELLOW_LIGHT).scale(SMALL_SCALE)
        row_1 = VGroup(bullet_1, text_1, tag_1).arrange(RIGHT, buff=0.18)
        row_1.move_to(UP * 0.6)

        self.play(FadeIn(row_1, shift=RIGHT * 0.15), run_time=0.8)
        self.wait(0.5)
        self.next_slide()

        # ── Take-away 2 ─────────────────────────────────────────────────────
        bullet_2 = Text("2.", color=WHITE_TEXT).scale(BODY_SCALE)
        text_2 = Text(
            "Neural Effect Search (ours) mitigates imperfect representations",
            color=WHITE_TEXT,
        ).scale(BODY_SCALE)
        row_2 = VGroup(bullet_2, text_2).arrange(RIGHT, buff=0.18)
        row_2.move_to(DOWN * 0.4)

        self.play(FadeIn(row_2, shift=RIGHT * 0.15), run_time=0.8)
        self.wait(1)
        self.next_slide()

from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S20Conclusion(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Galileo portrait ────────────────────────────────────────────────
        portrait_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "data", "galilei_ritratto.jpg"
        )
        portrait = ImageMobject(portrait_path).set_height(3.6)

        # ── Quote ───────────────────────────────────────────────────────────
        quote = Text(
            "\u201CMeasure what is measurable, \nand make measurable what is not.\u201D",
            color=WHITE_TEXT,
            line_spacing=1.0,
        ).scale(BODY_SCALE)

        attribution = Text(
            "\u2014 Galileo Galilei (1564\u20131642)",
            color=GRAY_TEXT,
        ).scale(SMALL_SCALE)

        text_group = VGroup(quote, attribution).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        composition = Group(portrait, text_group).arrange(RIGHT, buff=0.7)
        composition.move_to(ORIGIN)

        self.play(FadeIn(portrait), run_time=0.9)
        self.play(FadeIn(quote, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(attribution), run_time=0.5)
        self.wait(1)
        self.next_slide()

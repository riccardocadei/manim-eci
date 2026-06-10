from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S21ThankYou(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Thank you for your attention", color=WHITE_TEXT).scale(TITLE_SCALE)

        # X (Twitter) handle
        logo = SVGMobject(
            os.path.join(os.path.dirname(__file__), "..", "assets", "x_logo.svg")
        ).set(height=0.32)
        handle = Text("@riccardocadeii", color=GRAY_TEXT).scale(SMALL_SCALE)
        social = VGroup(logo, handle).arrange(RIGHT, buff=0.18)
        social.next_to(title, DOWN, buff=0.6)

        self.play(FadeIn(title))
        self.play(FadeIn(social, shift=UP * 0.2))
        self.wait(1)
        self.next_slide()

from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S11ThankYou(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Thank you for your attention", color=WHITE_TEXT).scale(TITLE_SCALE)
        title.move_to(UP * 0.6)

        subtitle_pt = Text(
            "obrigado",
            color=GRAY_TEXT,
            slant=ITALIC,
        ).scale(BODY_SCALE)
        subtitle_pt.next_to(title, DOWN, buff=0.2)

        poster = Text(
            "Poster Session: today 3:15-5:45pm, Pavillon 3 #105",
            color=GRAY_TEXT,
        ).scale(BODY_SCALE)
        poster.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(title))
        self.play(FadeIn(subtitle_pt))
        self.play(FadeIn(poster))
        self.wait(1)
        self.next_slide()

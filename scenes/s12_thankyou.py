from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S12ThankYou(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Thank You for your attention", color=WHITE_TEXT).scale(TITLE_SCALE)
        title.move_to(ORIGIN)

        self.play(FadeIn(title))
        self.wait(1)
        self.next_slide()

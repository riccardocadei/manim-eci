from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S16Paradox(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = slide_title("Exploratory Causal Inference Paradox", color=WHITE_TEXT)

        body = Text("as before", color=GRAY_TEXT).scale(SMALL_SCALE)
        body.move_to(ORIGIN)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(body), run_time=0.4)
        self.wait(0.5)
        self.next_slide()

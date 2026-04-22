from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S17RealWorld(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = slide_title("Real-World Application", color=WHITE_TEXT)
        placeholder = Text("TODO: NEMS real-world application", color=GRAY_TEXT, slant=ITALIC).scale(BODY_SCALE)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(placeholder), run_time=0.5)
        self.wait(0.5)
        self.next_slide()

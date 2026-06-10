from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S19RealWorld(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = Text(
            "Results: Two anti-poverty programs",
            color=WHITE_TEXT,
            t2s={"Two anti-poverty programs": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)
        placeholder = Text("See: https://www.riccardocadei.com/NEXIS/", color=GRAY_TEXT, slant=ITALIC).scale(BODY_SCALE)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(placeholder), run_time=0.5)
        self.wait(0.5)
        self.next_slide()

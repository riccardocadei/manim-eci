from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S15Dictionary(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = Text(
            "Tool: Dictionary Learning", color=WHITE_TEXT,
            t2s={"Dictionary Learning": ITALIC},
        ).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        body = Text("as before", color=GRAY_TEXT).scale(SMALL_SCALE)
        body.move_to(ORIGIN)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(body), run_time=0.4)
        self.wait(0.5)
        self.next_slide()

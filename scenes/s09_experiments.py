from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S09Experiments(Slide):
    def construct(self):
        self.camera.background_color = BG
        # TODO
        self.wait(1)
        self.next_slide()

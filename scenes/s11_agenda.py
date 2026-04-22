from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *


class S11Agenda(Slide):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Agenda", color=WHITE_TEXT).scale(TITLE_SCALE).to_edge(UP, buff=0.4)

        subtitle = Text(
            "Is modern representation learning a valid measurement tool "
            "for complex scientific experiments?",
            color=GRAY_TEXT, slant=ITALIC,
        ).scale(BODY_SCALE)
        if subtitle.width > config.frame_width - 0.8:
            subtitle.scale((config.frame_width - 0.8) / subtitle.width)
        subtitle.next_to(title, DOWN, buff=0.55)

        # ── Item 1 ──────────────────────────────────────────────────────────
        item1_num  = Text("1.", color=WHITE_TEXT).scale(0.58)
        item1_main = Text("Treatment Effect Identification", color=WHITE_TEXT).scale(0.58)
        item1_head = VGroup(item1_num, item1_main).arrange(RIGHT, buff=0.28)
        _STAR = '<span rise="3500" font_scale="small-caps">*</span>'
        item1_sub = MarkupText(
            f'Neural Effect Search — Mencattini{_STAR}, Cadei{_STAR}, Locatello '
            '\nICLR’26 — Oral (top ~1%)',
            color=GRAY_TEXT, slant=ITALIC,
        ).scale(0.32)
        item1_sub.next_to(item1_main, DOWN, buff=0.18, aligned_edge=LEFT)
        item1 = VGroup(item1_head, item1_sub)

        # ── Item 2 ──────────────────────────────────────────────────────────
        item2_num  = Text("2.", color=WHITE_TEXT).scale(0.58)
        item2_main = Text("Direct Treatment Effect Modifiers Identification",
                          color=WHITE_TEXT).scale(0.58)
        item2_head = VGroup(item2_num, item2_main).arrange(RIGHT, buff=0.28)
        item2_sub = MarkupText(
            'Neural Effect Modifiers Search — Cadei, Bargagli-Stoffi, Locatello '
            '\nOngoing (workshop AISTATS’26)',
            color=GRAY_TEXT, slant=ITALIC,
        ).scale(0.32)
        item2_sub.next_to(item2_main, DOWN, buff=0.18, aligned_edge=LEFT)
        item2 = VGroup(item2_head, item2_sub)

        items = VGroup(item1, item2).arrange(DOWN, buff=0.9, aligned_edge=LEFT)
        items.move_to(ORIGIN).shift(DOWN * 0.4)

        # ── Appear: full slide together ─────────────────────────────────────
        self.play(
            Write(title),
            FadeIn(subtitle, shift=UP * 0.12),
            FadeIn(item1, shift=UP * 0.12),
            FadeIn(item2, shift=UP * 0.12),
            run_time=0.8,
        )
        self.wait(0.5)
        self.next_slide()

        # ── Emphasize item 2 (bold + larger) ────────────────────────────────
        item2_main_target = Text(
            "Direct Treatment Effect Modifiers Identification",
            color=WHITE_TEXT, weight=BOLD,
        ).scale(0.58 * 1.18)
        item2_main_target.align_to(item2_main, LEFT).align_to(item2_main, DOWN)

        self.play(
            item1.animate.set_opacity(0.25),
            Transform(item2_main, item2_main_target),
            run_time=0.6,
        )
        self.wait(0.5)
        self.next_slide()

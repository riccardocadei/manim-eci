from manim import *
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "logo")
ICLR_H = 1.0


def _whiten(img_mob):
    arr = img_mob.pixel_array.copy()
    mask = arr[:, :, 3] > 10
    arr[mask, 0:3] = [242, 242, 242]
    img_mob.pixel_array = arr
    return img_mob


def _saence(ref):
    return MarkupText(
        '<span color="#C39BD3">SAE</span>nce', color=WHITE_TEXT,
    ).scale(1.0).move_to(ref)


def _science(ref):
    return Text("Science", color=WHITE_TEXT).scale(1.0).move_to(ref)


class Teaser(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Part 1: Galileo quote ───────────────────────────────────────────
        portrait_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "data", "galilei_ritratto.jpg"
        )
        portrait = ImageMobject(portrait_path).set_height(4.4)

        quote = Text(
            "\u201CMeasure what is measurable, \nand make measurable what is not.\u201D",
            color=WHITE_TEXT,
            line_spacing=1.0,
        ).scale(BODY_SCALE * 1.25)
        attribution = Text(
            "\u2014 Galileo Galilei (1564\u20131642)",
            color=GRAY_TEXT,
        ).scale(SMALL_SCALE * 1.25)

        text_group = VGroup(quote, attribution).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        quote_block = Group(portrait, text_group).arrange(RIGHT, buff=0.7).move_to(ORIGIN)

        self.play(FadeIn(portrait), run_time=0.9)
        self.play(FadeIn(quote, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(attribution), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(quote_block), run_time=0.7)

        # ── Part 2: Title + TL;DR + ICLR ────────────────────────────────────
        line1 = Text("Exploratory Causal Inference", color=WHITE_TEXT).scale(1.0)
        line1.move_to(UP * 1.4)

        in_txt = Text("in", color=WHITE_TEXT).scale(1.0)
        word_txt = MarkupText(
            '<span color="#C39BD3">SAE</span>nce', color=WHITE_TEXT,
        ).scale(1.0)

        _ref = Text("Science", color=WHITE_TEXT).scale(1.0)
        _dummy = VGroup(in_txt.copy(), _ref).arrange(RIGHT, buff=0.22)
        _dummy.next_to(line1, DOWN, buff=0.28)
        in_txt.move_to(_dummy[0])
        word_txt.move_to(_dummy[1])

        session = Text(
            "Oral Session 3F \u2013 Friday 24th April, 11:18am   (Rio de Janeiro)",
            color=PURPLE_LIGHT,
        ).scale(SMALL_SCALE * 1.25)
        session.next_to(_dummy, DOWN, buff=0.6)

        tldr_prefix = Text("TL;DR:", color=GRAY_TEXT).scale(BODY_SCALE * 1.25)
        tldr_content = Text(
            "enabling modern representation learning\n"
            "to scientific measurement tool for hypothesis generation",
            color=GRAY_TEXT,
            slant=ITALIC,
            line_spacing=0.6,
        ).scale(BODY_SCALE * 1.25)
        tldr = Group(tldr_prefix, tldr_content).arrange(RIGHT, buff=0.25, aligned_edge=UP)
        tldr.next_to(session, DOWN, buff=0.5)

        logo_iclr = _whiten(ImageMobject(os.path.join(LOGO_DIR, "ICLR.png")))
        logo_iclr.scale_to_fit_height(ICLR_H)
        logo_iclr.move_to(np.array([4.25, 2.75, 0]))

        self.play(
            Write(line1),
            FadeIn(in_txt, shift=UP * 0.1),
            FadeIn(word_txt, shift=UP * 0.1),
            FadeIn(logo_iclr),
            FadeIn(session, shift=UP * 0.1),
            FadeIn(tldr, shift=UP * 0.1),
            run_time=1.0,
        )
        self.wait(1.2)

        self.play(Transform(word_txt, _science(word_txt)), run_time=0.55)
        self.wait(1.0)
        self.play(Transform(word_txt, _saence(word_txt)), run_time=0.55)
        self.wait(1.2)

        self.play(
            FadeOut(line1),
            FadeOut(in_txt),
            FadeOut(word_txt),
            FadeOut(logo_iclr),
            FadeOut(tldr),
            run_time=0.6,
        )
        session_big = Text(
            "Oral Session 3F \u2013 Friday 24th April, 11:18am (Rio de Janeiro)",
            color=PURPLE_LIGHT,
        ).move_to(ORIGIN)
        session_big.scale_to_fit_width(config.frame_width * 0.78)
        self.play(Transform(session, session_big), run_time=0.7)
        self.wait(2.0)

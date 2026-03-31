from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "logo")
LOGO_H   = 0.65
ICLR_H   = 0.82


def _whiten(img_mob):
    arr = img_mob.pixel_array.copy()
    mask = arr[:, :, 3] > 10
    arr[mask, 0:3] = [242, 242, 242]
    img_mob.pixel_array = arr
    return img_mob


def _apex(text):
    return Text(text, color=PURPLE_LIGHT).scale(0.21)


def _author(name, apex, bold=False):
    t = Text(name, color=WHITE_TEXT, weight=BOLD if bold else NORMAL).scale(0.38)
    a = _apex(apex)
    a.next_to(t, UR, buff=0.02).shift(DOWN * 0.04)
    return VGroup(t, a)


def _labeled_logo(logo_mob, apex_str):
    a = _apex(apex_str)
    a.next_to(logo_mob, UP, buff=0.05).align_to(logo_mob, LEFT)
    return Group(logo_mob, a)


def _saence(ref):
    """Fresh SAEnce MarkupText positioned at ref mobject."""
    return MarkupText(
        '<span color="#C39BD3">SAE</span>nce', color=WHITE_TEXT,
    ).scale(0.82).move_to(ref)


def _science(ref):
    """Fresh Science Text positioned at ref mobject."""
    return Text("Science", color=WHITE_TEXT).scale(0.82).move_to(ref)


class S01Title(Slide):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ────────────────────────────────────────────────────────────
        line1 = Text("Exploratory Causal Inference", color=WHITE_TEXT).scale(0.82)
        line1.move_to(UP * 1.6)

        # "in" is fully static — added to scene independently.
        # "Science" is animated; positioned next to "in".
        in_txt   = Text("in", color=WHITE_TEXT).scale(0.82)
        # Start with SAEnce; word_txt is the object we'll keep transforming
        word_txt = MarkupText(
            '<span color="#C39BD3">SAE</span>nce', color=WHITE_TEXT,
        ).scale(0.82)

        # Layout: use "Science" as width reference for centering (same char count)
        _ref = Text("Science", color=WHITE_TEXT).scale(0.82)
        _dummy = VGroup(in_txt.copy(), _ref).arrange(RIGHT, buff=0.18)
        _dummy.next_to(line1, DOWN, buff=0.22)
        in_txt.move_to(_dummy[0])
        word_txt.move_to(_dummy[1])

        # ── Authors ──────────────────────────────────────────────────────────
        tom      = _author("Tommaso Mencattini", "*,1,2")
        riccardo = _author("Riccardo Cadei",     "*,1",  bold=True)
        francesco= _author("Francesco Locatello","1")

        authors = VGroup(tom, riccardo, francesco).arrange(RIGHT, buff=0.55)
        footnote = Text("* equal contribution", color="#888888").scale(0.26)
        author_block = VGroup(authors, footnote).arrange(DOWN, buff=0.22)
        author_block.next_to(_dummy, DOWN, buff=0.50)

        # ── Logos ────────────────────────────────────────────────────────────
        logo_ista = SVGMobject(os.path.join(LOGO_DIR, "ISTA.svg"))
        logo_epfl = _whiten(ImageMobject(os.path.join(LOGO_DIR, "EPFL.png")))
        logo_iclr = _whiten(ImageMobject(os.path.join(LOGO_DIR, "ICLR.png")))

        logo_ista.set_color(WHITE_TEXT)
        logo_ista.scale_to_fit_height(LOGO_H)
        logo_epfl.scale_to_fit_height(LOGO_H)
        logo_iclr.scale_to_fit_height(ICLR_H)

        uni_logos = Group(
            _labeled_logo(logo_ista, "1"),
            _labeled_logo(logo_epfl, "2"),
        ).arrange(RIGHT, buff=0.70)
        uni_logos.to_edge(DOWN, buff=0.40)
        logo_iclr.to_corner(UR, buff=0.35)

        # ── Slide 1: appear with SAEnce ──────────────────────────────────────
        self.play(Write(line1), run_time=1.0)
        self.play(
            FadeIn(in_txt,   shift=UP * 0.1),
            FadeIn(word_txt, shift=UP * 0.1),
            run_time=0.6,
        )
        self.play(FadeIn(author_block, shift=UP * 0.1), run_time=0.8)
        self.play(
            FadeIn(uni_logos, shift=UP * 0.1),
            FadeIn(logo_iclr),
            run_time=0.6,
        )
        self.wait(1)
        self.next_slide()

        # ── Slide 2: click → Science ──────────────────────────────────────────
        self.play(Transform(word_txt, _science(word_txt)), run_time=0.55)
        self.wait(1)
        self.next_slide()

        # ── Slide 3: click → SAEnce ───────────────────────────────────────────
        self.play(Transform(word_txt, _saence(word_txt)), run_time=0.55)
        self.wait(1)
        self.next_slide()

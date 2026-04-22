from manim import *
from manim_slides import Slide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import *

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "data", "logo")
LOGO_H   = 1.05
CIML_BLUE = "#007BBF"


def _saence(ref):
    """Fresh SAEnce MarkupText positioned at ref mobject."""
    return MarkupText(
        f'<span color="{WHITE_TEXT}">SAE</span>nce', color=WHITE_TEXT,
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
            f'<span color="{WHITE_TEXT}">SAE</span>nce', color=WHITE_TEXT,
        ).scale(0.82)

        # Layout: use "Science" as width reference for centering (same char count)
        _ref = Text("Science", color=WHITE_TEXT).scale(0.82)
        _dummy = VGroup(in_txt.copy(), _ref).arrange(RIGHT, buff=0.18)
        _dummy.next_to(line1, DOWN, buff=0.22)
        in_txt.move_to(_dummy[0])
        word_txt.move_to(_dummy[1])

        # ── Presenter info ───────────────────────────────────────────────────
        name = Text("Riccardo Cadei", color=WHITE_TEXT, weight=BOLD).scale(0.42)
        aff_lines = VGroup(*[
            Text(t, color="#AAAAAA").scale(0.26)
            for t in (
                "PhD Student",
                "Causal Learning and Artificial Intelligence Group",
                "Institute of Science and Technology, Austria (ISTA)",
            )
        ]).arrange(DOWN, buff=0.08)
        presenter = VGroup(name, aff_lines).arrange(DOWN, buff=0.22)
        presenter.next_to(_dummy, DOWN, buff=0.60)

        # ── CIML 2026 badge (top right) ──────────────────────────────────────
        ciml_badge = Text(
            "CIML 2026", color=CIML_BLUE, font="Helvetica Neue", weight=BOLD,
        ).scale(0.48)
        ciml_badge.to_corner(UR, buff=0.45)

        # ── Logo ─────────────────────────────────────────────────────────────
        logo_ista = SVGMobject(os.path.join(LOGO_DIR, "ISTA.svg"))
        logo_ista.set_color(WHITE_TEXT)
        logo_ista.scale_to_fit_height(LOGO_H)
        logo_ista.to_edge(DOWN, buff=0.50)

        # ── Slide 1: appear with SAEnce ──────────────────────────────────────
        self.play(Write(line1), run_time=1.0)
        self.play(
            FadeIn(in_txt,   shift=UP * 0.1),
            FadeIn(word_txt, shift=UP * 0.1),
            run_time=0.6,
        )
        self.play(FadeIn(presenter, shift=UP * 0.1), run_time=0.8)
        self.play(
            FadeIn(logo_ista, shift=UP * 0.1),
            FadeIn(ciml_badge),
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

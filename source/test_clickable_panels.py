import re
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent.parent
SOURCE = Image.open(ROOT / "source/approved-artwork-updated.png").convert("RGB")
OUT = ROOT / "assets/clickable"


class ClickablePanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "source/extract_panels.py")], check=True)

    def image(self, name):
        return Image.open(OUT / f"{name}.png").convert("RGB")

    def assert_crop(self, name, bounds):
        self.assertIsNone(ImageChops.difference(self.image(name), SOURCE.crop(bounds)).getbbox(), name)

    def test_artwork_regions_are_exact_crops(self):
        self.assertIsNone(
            ImageChops.difference(
                Image.open(ROOT / "assets/02-menu.png").convert("RGB"),
                SOURCE.crop((0, 215, 288, 411)),
            ).getbbox()
        )
        self.assert_crop("projects-heading", (0, 532, 1448, 581))
        project_edges = (0, 492, 972, 1448)
        for i, (left, right) in enumerate(zip(project_edges, project_edges[1:]), 1):
            self.assert_crop(f"project-{i}", (left, 581, right, 741))

        stack_edges = (0, 194, 332, 486, 618, 749, 902, 1033, 1165, 1298, 1448)
        for i, (left, right) in enumerate(zip(stack_edges, stack_edges[1:]), 1):
            self.assert_crop(f"tech-{i:02}", (left, 456, right, 532))

        footer_edges = (0, 655, 1018, 1230, 1448)
        for i, (left, right) in enumerate(zip(footer_edges, footer_edges[1:]), 1):
            self.assert_crop(f"footer-{i}", (left, 943, right, 1010))

    def test_readme_has_no_disclosures_or_dangling_fragments(self):
        readme = (ROOT / "README.md").read_text()
        self.assertNotRegex(readme, r"<\s*details\b")
        self.assertNotRegex(readme, r"<\s*summary\b")
        ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', readme))
        fragments = re.findall(r'href=["\']#([^"\']+)["\']', readme)
        self.assertTrue(fragments)
        self.assertFalse(set(fragments) - ids, f"dangling fragments: {set(fragments) - ids}")

    def test_profile_panels_are_not_navigation_and_keep_anchor_ids(self):
        readme = (ROOT / "README.md").read_text()
        for asset in ("01-hero.png", "02-menu.png", "03-whoami.png", "clickable/footer-1.png"):
            self.assertNotRegex(readme, rf'<a\b[^>]*>\s*<img src="assets/{re.escape(asset)}"')
        self.assertRegex(readme, r'<(?:div|[^>]+)\bid=["\']top["\']')
        self.assertRegex(readme, r'<(?:div|[^>]+)\bid=["\']profile["\']')
        self.assertIn('href="https://x.com/4t_ritch"', readme)
        self.assertNotIn("Dot_Choco", readme)
        self.assertIn("Amira Elfeky - A Dozen Roses", readme)

    def test_generated_player_matches_normalized_source(self):
        generated = Image.open(ROOT / "assets/10-player.png").convert("RGB")
        approved = Image.open(ROOT / "source/player-amira-elfeky.png").convert("RGB")
        self.assertEqual(approved.size, (1448, 202))
        self.assertIsNone(ImageChops.difference(generated, approved).getbbox())

    def test_expected_destinations_and_no_visible_text_navigation(self):
        readme = (ROOT / "README.md").read_text()
        for destination in (
            "https://okaimono.dev/",
            "https://github.com/4t-ritch/JDotParser",
            "https://github.com/4t-ritch/DCTI",
            "https://github.com/4t-ritch/lnx-df",
            "https://x.com/4t_ritch",
            "https://www.rust-lang.org/",
            "https://isocpp.org/",
            "https://www.typescriptlang.org/",
            "https://svelte.dev/",
            "https://go.dev/",
            "https://www.postgresql.org/",
            "https://www.docker.com/",
            "https://archlinux.org/",
            "https://git-scm.com/",
        ):
            self.assertIn(destination, readme)
        self.assertNotIn("C# text serializer", readme)
        self.assertNotRegex(readme, r"(?m)^\s*[-*]\s+\[\*\*?(?:Okaimono|JDotParser|DCTI)")


if __name__ == "__main__":
    unittest.main()

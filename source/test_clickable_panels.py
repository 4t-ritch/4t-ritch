import re
import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = ROOT / "source/approved-artwork-muted.png"
SOURCE = Image.open(SOURCE_PATH).convert("RGB") if SOURCE_PATH.exists() else None
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
        self.assertIsNotNone(SOURCE, "generator must use the approved muted artwork")
        bounds = json.loads((ROOT / "source/crop-bounds.json").read_text())
        for name, region in bounds.items():
            generated = Image.open(ROOT / "assets" / f"{name}.png").convert("RGB")
            self.assertIsNone(ImageChops.difference(generated, SOURCE.crop(region)).getbbox(), name)
        self.assertIsNone(
            ImageChops.difference(
                Image.open(ROOT / "assets/02-menu.png").convert("RGB"),
                SOURCE.crop((0, 224, 293, 420)),
            ).getbbox()
        )
        for name, region in {
            "03-whoami": (293, 224, 903, 420),
            "04-system": (903, 224, 1448, 420),
        }.items():
            generated = Image.open(ROOT / "assets" / f"{name}.png").convert("RGB")
            self.assertIsNone(ImageChops.difference(generated, SOURCE.crop(region)).getbbox(), name)
        self.assert_crop("projects-heading", (0, 546, 1448, 595))
        bands = {
            "01-header": (0, 0, 1448, 224),
            "02-about-row": (0, 224, 1448, 420),
            "03-tech-stack": (0, 420, 1448, 546),
            "04-projects": (0, 546, 1448, 761),
            "05-audio-player": (0, 761, 1448, 967),
            "06-system-footer": (0, 967, 1448, 1033),
        }
        for name, region in bands.items():
            band = Image.open(ROOT / "assets/bands" / f"{name}.png").convert("RGB")
            self.assertIsNone(ImageChops.difference(band, SOURCE.crop(region)).getbbox(), name)
        project_edges = (0, 492, 972, 1448)
        for i, (left, right) in enumerate(zip(project_edges, project_edges[1:]), 1):
            self.assert_crop(f"project-{i}", (left, 595, right, 761))

        stack_edges = (0, 194, 332, 486, 618, 749, 902, 1033, 1165, 1298, 1448)
        for i, (left, right) in enumerate(zip(stack_edges, stack_edges[1:]), 1):
            self.assert_crop(f"tech-{i:02}", (left, 465, right, 546))

        footer_edges = (0, 655, 1018, 1230, 1448)
        for i, (left, right) in enumerate(zip(footer_edges, footer_edges[1:]), 1):
            self.assert_crop(f"footer-{i}", (left, 967, right, 1033))

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
        self.assertIn('assets/02-menu.png" width="20.23481%"', readme)
        self.assertIn('assets/03-whoami.png" width="42.12707%"', readme)
        self.assertIn('assets/04-system.png" width="37.63812%"', readme)
        for asset in ("01-hero.png", "02-menu.png", "03-whoami.png", "clickable/footer-1.png"):
            self.assertNotRegex(readme, rf'<a\b[^>]*>\s*<img src="assets/{re.escape(asset)}"')
        self.assertRegex(readme, r'<(?:div|[^>]+)\bid=["\']top["\']')
        self.assertRegex(readme, r'<(?:div|[^>]+)\bid=["\']profile["\']')
        self.assertIn('href="https://x.com/4t_ritch"', readme)
        self.assertNotIn("Dot_Choco", readme)
        self.assertIn("Amira Elfeky - A Dozen Roses", readme)

    def test_generated_player_matches_muted_artwork_crop(self):
        generated = Image.open(ROOT / "assets/10-player.png").convert("RGB")
        expected = SOURCE.crop((0, 761, 1448, 967))
        self.assertEqual(generated.size, (1448, 206))
        self.assertIsNone(ImageChops.difference(generated, expected).getbbox())

    def test_preview_includes_complete_footer_frame(self):
        preview = Image.open(ROOT / "PREVIEW.png").convert("RGB")
        expected = SOURCE.crop((0, 0, 1448, 1033))
        self.assertEqual(preview.size, (1448, 1033))
        self.assertIsNone(ImageChops.difference(preview, expected).getbbox())

    def test_exported_images_have_no_full_width_near_white_edge_rails(self):
        exports = [path for path in (ROOT / "assets").rglob("*.png")]
        self.assertTrue(exports)
        for path in exports:
            image = Image.open(path).convert("RGB")
            width, height = image.size
            edges = [image.crop((0, 0, width, 1)), image.crop((0, height - 1, width, height))]
            if width > 1:
                edges.extend((image.crop((0, 0, 1, height)), image.crop((width - 1, 0, width, height))))
            for edge in edges:
                near_white = sum(min(pixel) >= 245 for pixel in edge.get_flattened_data())
                self.assertLess(near_white / (edge.width * edge.height), 0.98, f"near-white rail at exported edge: {path}")

    def test_player_source_is_not_an_independent_generator_input(self):
        generator = (ROOT / "source/extract_panels.py").read_text()
        self.assertIn("approved-artwork-muted.png", generator)
        self.assertNotIn("player-amira-elfeky.png', ROOT / 'assets/10-player.png'", generator)
        player_source = Image.open(ROOT / "source/player-amira-elfeky.png").convert("RGB")
        self.assertIsNone(ImageChops.difference(player_source, SOURCE.crop((0, 761, 1448, 967))).getbbox())

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

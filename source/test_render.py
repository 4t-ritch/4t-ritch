import re
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


class ProfileRenderContractTests(unittest.TestCase):
    def test_preview_matches_compact_reference_aspect(self):
        with Image.open(ROOT / "PREVIEW.png") as preview:
            self.assertLess(abs(preview.width / preview.height - 746 / 529), 0.01)

    def test_three_project_cards_are_full_card_anchors(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cards = re.findall(r'<a\s+href="([^"]+)"[^>]*>\s*<img\s+src="\./assets/(05-okaimono|06-webcore|07-clikity)\.png"', readme)
        self.assertEqual(len(cards), 3)
        self.assertEqual({asset for _, asset in cards}, {"05-okaimono", "06-webcore", "07-clikity"})

    def test_verified_repository_cards_use_canonical_links(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cards = re.findall(r'<a\s+href="([^"]+)"[^>]*>\s*<img\s+src="\./assets/(05-okaimono|06-webcore|07-clikity)\.png"', readme)
        links = {asset: href for href, asset in cards}
        self.assertEqual(links["06-webcore"], "https://github.com/4t-ritch/webcore-ui")
        self.assertEqual(links["07-clikity"], "https://github.com/4t-ritch/clikity")

    def test_unverified_okaimono_repository_keeps_existing_website_link(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cards = re.findall(r'<a\s+href="([^"]+)"[^>]*>\s*<img\s+src="\./assets/(05-okaimono|06-webcore|07-clikity)\.png"', readme)
        links = {asset: href for href, asset in cards}
        self.assertEqual(links["05-okaimono"], "https://okaimono.dev")

    def test_font_license_matches_bundled_latin_font_metadata(self):
        license_text = (ROOT / "source/fonts/LICENSE-noto-fonts.txt").read_text(encoding="utf-8")
        self.assertIn("SIL OPEN FONT LICENSE Version 1.1", license_text)
        self.assertIn("Copyright 2022 The Noto Project Authors", license_text)

    def test_music_note_is_drawn_instead_of_requested_from_subset_font(self):
        renderer = (ROOT / "source/render.py").read_text(encoding="utf-8")
        self.assertNotIn("♪", renderer)
        self.assertIn("draw_music_note", renderer)


if __name__ == "__main__":
    unittest.main()

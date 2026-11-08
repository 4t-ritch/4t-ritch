from pathlib import Path
from PIL import Image
import json
import shutil
ROOT = Path(__file__).resolve().parent.parent
source = Image.open(ROOT/'source/approved-artwork-updated.png').convert('RGB')
bounds = json.loads((ROOT/'source/crop-bounds.json').read_text())
for name, (left, top, right, bottom) in bounds.items():
    source.crop((left, top, right, bottom)).save(ROOT/'assets'/f'{name}.png')
# Complete project strip, not individual fragments: heading intersects cards.
source.crop((0,532,1448,741)).save(ROOT/'assets/bands/04-projects.png')

# These regions partition the existing artwork exactly; no pixels are redrawn.
clickable = ROOT / 'assets/clickable'
clickable.mkdir(parents=True, exist_ok=True)
regions = {
    'projects-heading': (0, 532, 1448, 581),
    'project-1': (0, 581, 492, 741),
    'project-2': (492, 581, 972, 741),
    'project-3': (972, 581, 1448, 741),
    'tech-heading': (0, 411, 1448, 456),
    'tech-01': (0, 456, 194, 532),
    'tech-02': (194, 456, 332, 532),
    'tech-03': (332, 456, 486, 532),
    'tech-04': (486, 456, 618, 532),
    'tech-05': (618, 456, 749, 532),
    'tech-06': (749, 456, 902, 532),
    'tech-07': (902, 456, 1033, 532),
    'tech-08': (1033, 456, 1165, 532),
    'tech-09': (1165, 456, 1298, 532),
    'tech-10': (1298, 456, 1448, 532),
    'footer-1': (0, 943, 655, 1010),
    'footer-2': (655, 943, 1018, 1010),
    'footer-3': (1018, 943, 1230, 1010),
    'footer-4': (1230, 943, 1448, 1010),
}
for name, region in regions.items():
    source.crop(region).save(clickable / f'{name}.png')
shutil.copyfile(ROOT / 'source/player-amira-elfeky.png', ROOT / 'assets/10-player.png')
print('Rebuilt', len(bounds) + len(regions) + 1, 'complete assets')

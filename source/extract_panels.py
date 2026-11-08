from pathlib import Path
from PIL import Image
import json
ROOT = Path(__file__).resolve().parent.parent
source = Image.open(ROOT/'source/approved-artwork-muted.png').convert('RGB')
bounds = json.loads((ROOT/'source/crop-bounds.json').read_text())
for name, (left, top, right, bottom) in bounds.items():
    source.crop((left, top, right, bottom)).save(ROOT/'assets'/f'{name}.png')
# Complete contiguous bands keep every linked asset on the same approved artwork.
bands = {
    '01-header': (0, 0, 1448, 224),
    '02-about-row': (0, 224, 1448, 420),
    '03-tech-stack': (0, 420, 1448, 546),
    '04-projects': (0, 546, 1448, 761),
    '05-audio-player': (0, 761, 1448, 967),
    '06-system-footer': (0, 967, 1448, 1033),
}
for name, region in bands.items():
    source.crop(region).save(ROOT / 'assets/bands' / f'{name}.png')
source.crop((0, 546, 1448, 595)).save(ROOT / 'assets/06-project-heading.png')
source.crop((0, 761, 1448, 967)).save(ROOT/'source/player-amira-elfeky.png')

# These regions partition the existing artwork exactly; no pixels are redrawn.
clickable = ROOT / 'assets/clickable'
clickable.mkdir(parents=True, exist_ok=True)
regions = {
    'projects-heading': (0, 546, 1448, 595),
    'project-1': (0, 595, 492, 761),
    'project-2': (492, 595, 972, 761),
    'project-3': (972, 595, 1448, 761),
    'tech-heading': (0, 420, 1448, 465),
    'tech-01': (0, 465, 194, 546),
    'tech-02': (194, 465, 332, 546),
    'tech-03': (332, 465, 486, 546),
    'tech-04': (486, 465, 618, 546),
    'tech-05': (618, 465, 749, 546),
    'tech-06': (749, 465, 902, 546),
    'tech-07': (902, 465, 1033, 546),
    'tech-08': (1033, 465, 1165, 546),
    'tech-09': (1165, 465, 1298, 546),
    'tech-10': (1298, 465, 1448, 546),
    'footer-1': (0, 967, 655, 1033),
    'footer-2': (655, 967, 1018, 1033),
    'footer-3': (1018, 967, 1230, 1033),
    'footer-4': (1230, 967, 1448, 1033),
}
for name, region in regions.items():
    source.crop(region).save(clickable / f'{name}.png')
source.crop((0, 761, 1448, 967)).save(ROOT / 'assets/10-player.png')
source.crop((0, 0, 1448, 1033)).save(ROOT / 'PREVIEW.png')
print('Rebuilt linked panels, bands, and PREVIEW.png')

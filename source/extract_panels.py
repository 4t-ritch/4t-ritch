from pathlib import Path
from PIL import Image
import json
ROOT = Path(__file__).resolve().parent.parent
source = Image.open(ROOT/'source/approved-artwork.png').convert('RGB')
bounds = json.loads((ROOT/'source/crop-bounds.json').read_text())
for name, (left, top, right, bottom) in bounds.items():
    source.crop((left, top, right, bottom)).save(ROOT/'assets'/f'{name}.png')
# Complete project strip, not individual fragments: heading intersects cards.
source.crop((0,532,1448,741)).save(ROOT/'assets/bands/04-projects.png')
print('Rebuilt',len(bounds)+1,'complete assets')

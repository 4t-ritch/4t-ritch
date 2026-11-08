#!/usr/bin/env python3
"""Regenera recursos PNG desde el diseño aprobado sin cortar paneles por dentro.
Requiere: pip install pillow
Ejecuta desde cualquier ubicación: python source/rebuild.py
"""
from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1]
assets=root/'assets'
layout=json.loads((root/'source/layout.json').read_text(encoding='utf-8'))
art=Image.open(root/'source/approved-art.png').convert('RGB')
corrected=Image.open(root/'source/art-with-corrected-text.png').convert('RGB')
for name, coords in layout.items():
    img=corrected if name.endswith('-corrected') else art
    target=assets/f'{name}.png'
    target.parent.mkdir(parents=True,exist_ok=True)
    img.crop(tuple(coords)).save(target,optimize=True)
print('Recreados',len(layout),'recursos.')

#!/usr/bin/env python3
"""Regenerate asset slices from the two reference images. Requires Pillow."""
from PIL import Image
from pathlib import Path
root=Path(__file__).resolve().parents[1]
orig=Image.open(root/'assets/reference-art.png').convert('RGB')
correct=Image.open(root/'assets/reference-text-corrected.png').convert('RGB')
assert orig.size==(1448,1086)==correct.size
def save(name,rect,im=orig):
 p=root/'assets'/f'{name}.png';p.parent.mkdir(parents=True,exist_ok=True);im.crop(rect).save(p,optimize=True)
save('hero',(0,0,1448,214))
xs=[0,292,886,1448];ys=[214,269,307,341,375,411]
for i in range(5):
 for j in range(3):save(f'panel/r{i+1}-c{j+1}',(xs[j],ys[i],xs[j+1],ys[i+1]))
save('tech/heading',(0,411,1448,447))
xs=[0,192,332,475,619,759,899,1040,1180,1296,1448]
for i in range(10):save(f'tech/{i+1:02}',(xs[i],447,xs[i+1],535))
save('projects/heading',(0,535,1448,569))
xs=[0,486,965,1448]
for i in range(3):
 box=(xs[i],569,xs[i+1],742)
 save(f'projects/card-{i+1:02}',box)
 save(f'projects-corrected/card-{i+1:02}',box,correct)
save('player',(0,742,1448,943))
xs=[0,645,951,1202,1448]
for i in range(4):save(f'footer/{i+1:02}',(xs[i],943,xs[i+1],1010))
print('Assets regenerated.')

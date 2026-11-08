from PIL import Image, ImageChops
from pathlib import Path
P = Path(__file__).resolve().parent.parent
A = P / 'assets'
orig = Image.open(A / 'readme-exact.png').convert('RGB')
w,h=orig.size
assert (w,h)==(1027,736), (w,h)
canv = Image.new('RGB',(1027,736))
canv.paste(Image.open(A/'01-overview.png'),(0,0))
canv.paste(Image.open(A/'02-okaimono.png'),(0,425))
canv.paste(Image.open(A/'03-webcore.png'),(344,425))
canv.paste(Image.open(A/'04-clikity.png'),(686,425))
canv.paste(Image.open(A/'05-player-footer.png'),(0,559))
assert ImageChops.difference(canv,orig).getbbox() is None, 'Visual split differs from approved artwork'
print('PASS: the clickable asset crops reconstruct the approved preview pixel-for-pixel')

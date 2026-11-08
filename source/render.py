#!/usr/bin/env python3
"""Generate the static graphics for the 4tRitch GitHub profile README.

Uses Pillow and locally installed Noto fonts. No external resources required.
All text is typeset programmatically (no generated typography).
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
ART=ROOT/'source'/'art'
ASSETS.mkdir(parents=True, exist_ok=True)
S=2
BG=(12,12,22)
C1=(26,24,37)
C2=(43,39,56)
SILVER=(177,169,194)
ASH=(218,213,227)
LAV=(178,146,215)
PURPLE=(111,79,148)
DUST=(111,106,130)
INK=(12,11,22)
YELLOW=(213,204,146)

# Noto is part of Google's open font catalog; only rendered pixels ship.
FONTS={
    'mono':'/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf',
    'bold':'/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf',
    'serif':'/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf',
    'serifbold':'/usr/share/fonts/truetype/noto/NotoSerif-BoldItalic.ttf',
    'jp':'/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
}
for key, name in list(FONTS.items()):
    if not Path(name).exists():
        FONTS[key]='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

_font_cache={}
def font(size, kind='mono'):
    key=(kind,size)
    if key not in _font_cache:
        _font_cache[key]=ImageFont.truetype(FONTS[kind], int(size*S))
    return _font_cache[key]

def rect(xy):return tuple(int(t*S) for t in xy)

def texture(w,h,seed=0):
    """Coherent charcoal-violet texture: subtle film grain, not neon bloom."""
    W,H=w*S,h*S
    rng=np.random.default_rng(seed)
    x=np.linspace(0,1,W,dtype=np.float32)[None,:,None]
    y=np.linspace(0,1,H,dtype=np.float32)[:,None,None]
    base=np.array([18,17,29],dtype=np.float32)[None,None,:]
    grad=11*(1-x)+6*np.sin(2*np.pi*x)*np.sin(np.pi*y)
    noise=rng.normal(0,3.3,(H,W,1)).astype(np.float32)
    arr=np.clip(base + grad * np.array([.35,.24,.62])[None,None,:]+noise,0,255).astype(np.uint8)
    im=Image.fromarray(arr,'RGB').convert('RGBA')
    d=ImageDraw.Draw(im,'RGBA')
    random.seed(seed)
    for yy in range(2,H,5):
        d.line((0,yy,W,yy), fill=(10,8,24,37),width=1)
    for i in range(max(5,w//80)):
        xx=random.randint(0,W); yy=random.randint(0,H); ex=xx+random.randint(8,90)*S
        d.line((xx,yy,ex,yy),fill=(189,171,211,random.randint(8,26)),width=1)
    return im

class Panel:
    def __init__(self,w,h,seed=2):
        self.w=w; self.h=h;self.im=texture(w,h,seed)
        self.d=ImageDraw.Draw(self.im,'RGBA')
    def frame(self,x0,y0,x1,y1,theme='metal',corner=9):
        if theme=='metal':
            fill=(21,19,32,234); outer=(113,104,133,255); inner=(60,54,79,255)
        else:
            fill=(13,12,22,245);outer=(117,101,141,255);inner=(37,33,52,255)
        self.d.polygon([rect((x0+corner,y0)),rect((x1-corner,y0)),rect((x1,y0+corner)),rect((x1,y1-corner)),rect((x1-corner,y1)),rect((x0+corner,y1)),rect((x0,y1-corner)),rect((x0,y0+corner))],fill=fill)
        self.d.line([rect((x0+corner,y0)),rect((x1-corner,y0)),rect((x1,y0+corner)),rect((x1,y1-corner)),rect((x1-corner,y1)),rect((x0+corner,y1)),rect((x0,y1-corner)),rect((x0,y0+corner)),rect((x0+corner,y0))],fill=outer,width=2*S,joint='curve')
        self.d.line(rect((x0+corner+3,y0+4,x1-corner-3,y0+4)), fill=(189,181,198,80),width=1*S)
        self.d.line(rect((x0+corner+3,y1-4,x1-corner-3,y1-4)), fill=inner,width=1*S)
        for x,y in [(x0+8,y0+8),(x1-8,y0+8),(x0+8,y1-8),(x1-8,y1-8)]:
            self.d.ellipse(rect((x-2,y-2,x+2,y+2)),fill=(44,40,54,255),outline=(141,128,154,255),width=1*S)
            self.d.point(rect((x,y)),fill=(182,164,197,255))
    def line(self,xy,fill=SILVER,width=1):self.d.line(rect(xy),fill=fill,width=int(width*S))
    def box(self,xy,fill,outline=None,width=1):
        # Pillow's RGBA draw replaces semi-transparent pixels instead of blending them.
        if fill is not None and len(fill)==4 and fill[3]<255:
            lay=Image.new('RGBA',self.im.size,(0,0,0,0))
            ImageDraw.Draw(lay,'RGBA').rectangle(rect(xy),fill=fill)
            self.im=Image.alpha_composite(self.im,lay)
            self.d=ImageDraw.Draw(self.im,'RGBA')
            if outline:self.d.rectangle(rect(xy),outline=outline,width=int(width*S))
        else:
            self.d.rectangle(rect(xy),fill=fill,outline=outline,width=int(width*S))
    def polygon(self,pts,fill,outline=None):self.d.polygon([rect(p) for p in pts],fill=fill);self.d.line([rect(p) for p in pts+[pts[0]]],fill=outline,width=S) if outline else None
    def txt(self,x,y,s,size=16,color=ASH,kind='mono',stroke=0):
        self.d.text(rect((x,y)),s,font=font(size,kind),fill=(*color,255) if len(color)==3 else color,stroke_width=int(stroke*S),stroke_fill=INK,anchor='lt')
    def titlebar(self,x0,y0,x1,label,sub=None):
        self.box((x0,y0,x1,y0+29),(68,61,82,255))
        self.line((x0+3,y0+27,x1-3,y0+27),(166,154,184,255),1)
        self.box((x0+10,y0+10,x0+19,y0+19),LAV)
        self.txt(x0+26,y0+2,label,16,ASH,'jp' if any(ord(ch)>127 for ch in label) else 'bold')
        if sub:self.txt(x1-12-len(sub)*9,y0+5,sub,11,SILVER)
    def paste_fit(self,img,x,y,w,h,fade_left=False,fade_bottom=False):
        if isinstance(img,str):img=Image.open(ART/img).convert('RGBA')
        sw,sh=img.size
        scale=max(w*S/sw,h*S/sh)
        re=img.resize((int(sw*scale),int(sh*scale)),Image.Resampling.LANCZOS)
        ox=(re.width-w*S)//2;oy=(re.height-h*S)//2
        re=re.crop((ox,oy,ox+w*S,oy+h*S)).convert('RGBA')
        # tint everything into PS2's low-saturation, violet-graphite palette
        lum=ImageEnhance.Contrast(re.convert('L')).enhance(1.14)
        new=Image.merge('RGB',(lum.point(lambda k:int(k*.77)),lum.point(lambda k:int(k*.69)),lum.point(lambda k:min(255,int(k*.94))))).convert('RGBA')
        a=np.full((h*S,w*S),215,dtype=np.uint8)
        if fade_left:
            ramp=np.clip(np.linspace(0,1,w*S)**1.3,0,1)
            a=(a*ramp[None,:]).astype(np.uint8)
        if fade_bottom:
            ramp=np.clip(np.linspace(1,0,h*S)**.65,0,1)
            a=(a*ramp[:,None]).astype(np.uint8)
        new.putalpha(Image.fromarray(a,'L'))
        self.im.alpha_composite(new,rect((x,y)))
        self.d=ImageDraw.Draw(self.im,'RGBA')
    def export(self,name):
        out=self.im.convert('RGB')
        out.save(ASSETS/name,optimize=True)
        return out

# Banner / PS2-era system screen: serif title, purposeful typography, no fabricated UI labels.
p=Panel(1080,188,11)
p.paste_fit('skyline.png',0,0,920,188)
p.paste_fit('portrait.png',760,0,320,188,fade_left=True)
p.box((0,0,1080,188),(18,14,32,65))
for i in range(7):
    p.line((15,32+i*22,1080,32+i*22),(153,135,169,30))
for x,y in [(29,63),(55,38),(58,65),(82,41)]:
    p.polygon([(x,y),(x+21,y),(x+13,y+21),(x-8,y+21)],(132,108,163,220))
p.txt(128,26,'4tRitch',66,(218,211,230),'serifbold')
p.line((134,115,600,115),(180,161,199,235),2)
p.txt(148,121,'S O F T W A R E   D E V E L O P E R',15,(208,200,222),'mono')
p.txt(153,158,'SYSTEM / 00-A    •    PERSONAL ARCHIVE',11,(166,151,179),'mono')
p.txt(873,12,'システムメニュー',14,ASH,'jp')
p.line((868,37,1063,37),(169,158,185,140))
for i,label in enumerate(['PROFILE','PROJECTS','TECH STACK','STATUS']):
    y=49+i*30
    if i==0:
        p.box((878,y,1062,y+26),(126,100,151,124))
        p.polygon([(885,y+7),(885,y+18),(894,y+12)],ASH)
    p.txt(902,y+2,label,14,ASH if i==0 else SILVER,'mono')
p.line((2,186,1078,186),(171,157,190,255),2)
p.export('01-hero.png')

# Main content / separate panels typeset in modern fonts with PS2 layout language.
p=Panel(1080,192,21)
p.frame(3,5,207,189)
p.frame(215,5,695,189)
p.frame(704,5,1077,189)
p.titlebar(6,8,204,'メニュー / MENU')
p.titlebar(218,8,692,'WHOAMI / 自己紹介')
p.titlebar(707,8,1074,'SYSTEM STATUS')
for i,(a,b) in enumerate([('01','PROFILE'),('02','PROJECTS'),('03','TECH STACK'),('04','CONTACT')]):
    y=46+i*34
    if i==0:
        p.box((17,y,191,y+28),(126,106,158,168),(168,145,194,255))
        p.polygon([(26,y+9),(26,y+19),(36,y+14)],(239,233,246,255))
    p.txt(44,y+3,a,13,(218,207,231))
    p.txt(74,y+3,b,14,(233,225,238) if i==0 else (179,169,192),'mono')
p.txt(238,47,'Hi, I\'m 4tRitch.',24,(230,224,237),'bold')
p.txt(240,83,'> Rust / C# / Svelte / Go',16,(194,173,221),'mono')
p.txt(240,113,'> Building anime tools,',16,(214,206,226),'mono')
p.txt(263,135,'creative software & UI.',16,(214,206,226),'mono')
p.txt(240,159,'> Linux, games, retro tech.',14,(174,165,192),'mono')
p.paste_fit('tower.png',721,47,108,124)
p.box((720,47,830,171),None if False else (22,20,34,18),outline=(121,105,145,255))
for yy,k,v in [(52,'OS','ARCH'),(83,'WM','HYPRLAND'),(114,'SH','FISH'),(145,'ED','NEOVIM')]:
    p.txt(843,yy,k,12,(169,157,181),'bold')
    p.txt(872,yy,'/',14,(125,111,142))
    p.txt(898,yy,v,15,ASH,'bold')
p.export('02-system.png')

# Technology strip: no modern colorful logos, deliberate 2000s monochrome system tiles.
p=Panel(1080,114,22)
p.frame(3,2,1077,112)
p.box((8,5,1072,34),(60,52,77,255))
p.txt(20,10,'技術スタック  /  TECH STACK',15,(224,216,234),'jp')
p.txt(799,12,'[ SYSTEM COMPONENTS : 10 ]',12,(174,156,194),'mono')
tech=[('RS','RUST'),('C#','C SHARP'),('TS','TYPESCRIPT'),('SV','SVELTE'),('GO','GOLANG'),('PG','POSTGRES'),('DK','DOCKER'),('LX','LINUX'),('GT','GIT'),('>_','CLI / TUI')]
for i,(glyph,name) in enumerate(tech):
    x=14+i*105
    if i: p.line((x-7,42,x-7,104),(124,110,144,150))
    p.box((x+9,45,x+79,77),(29,25,42,255),outline=(117,103,136,225))
    p.txt(x+25 if len(glyph)==2 else x+18,45,glyph,21,(199,180,217),'bold')
    fs=10 if len(name)>8 else 11
    p.txt(x+6 if len(name)>8 else x+13,84,name,fs,(217,210,225))
p.export('03-stack.png')

# Section header for projects.
p=Panel(1080,51,23)
p.frame(3,2,1077,49)
p.box((7,6,1073,44),(58,50,73,255))
p.txt(21,8,'注目のプロジェクト / FEATURED PROJECTS',18,(227,217,232),'jp')
for i in range(8):
    x=765+i*31
    p.polygon([(x,24),(x+10,11),(x+23,11),(x+12,24)],(114,103,130,130))
p.export('04-projects-header.png')

# Project cards (3 real links at README level).
def make_card(filename,title,tagline,techs,img,selected=False):
    p=Panel(350,174,34+len(title))
    p.frame(3,3,347,171)
    p.paste_fit(img,12,11,136,151)
    p.box((148,14,150,159),(150,122,176,160))
    p.txt(162,14,title,28,(229,219,236),'serifbold')
    p.line((159,56,333,56),(147,129,174,180))
    for i,line in enumerate(tagline):
        p.txt(163,71+i*23,line,13,(221,212,227),'mono')
    for i,t in enumerate(techs):
        xx=164+i*81
        p.box((xx,138,xx+77,160),(47,42,58,255),outline=(124,108,142,255))
        p.txt(xx+7,140,t,11,(216,202,229))
    if selected:
        p.line((6,3,343,3),(178,133,205,255),2)
        p.polygon([(145,77),(145,93),(152,85)],(185,151,216,255))
    return p.export(filename)
make_card('05-okaimono.png','Okaimono',['Anime collection,','calendar & friends.'],['RUST','SVELTE'],'trolley.png')
make_card('06-webcore.png','webcore-ui',['Retro web UI studies,','2005–2008 aesthetics.'],['HTML','CSS'],'monitor.png',True)
make_card('07-clikity.png','Clikity',['ClickUp task creator,','desktop via Tauri.'],['TAURI','SVELTE'],'city.png')

# Period-specific music player (Winamp/PSP/PS2 menu feel rather than an invented live widget).
p=Panel(1080,152,45)
p.frame(3,2,1077,149)
p.box((7,6,1073,34),(61,51,76,255))
p.txt(20,8,'♪  NOW PLAYING   /   再生中',17,(227,213,232),'jp')
p.txt(818,11,'AUDIO PLAYER // DEMO',12,(186,170,203))
p.paste_fit('album.png',16,47,90,90)
p.box((15,46,107,138),None if False else (0,0,0,0),outline=(162,143,178,255))
p.txt(121,44,'LOST SIGNAL  /  DEMO TRACK',17,(223,212,230),'serifbold')
p.txt(121,76,'MP3  ·  320 KBPS  ·  44.1 KHZ',12,(175,164,193),'mono')
p.txt(121,97,'STEREO   02:14 / 04:27',13,(204,190,218),'mono')
# analog segmented progress meter
p.box((121,122,598,138),(17,14,27,255),outline=(151,134,164,255))
for i in range(35):
    x=128+i*13
    color=(169,137,194,255) if i<18 else (57,51,69,255)
    p.box((x,126,x+9,134),color)
# equalizer fixed pixel bars
rng=random.Random(47)
for i in range(26):
    hh=rng.randint(5,38)
    xx=619+i*7
    for yy in range(0,hh,6):
        p.box((xx,112-yy,xx+4,116-yy),(146+min(60,yy),118+min(50,yy),168+min(50,yy),255))
# tactile rectangular transport controls and CD puck
for i,(symbol,high) in enumerate([('<<',False),('[]',False),('||',True),('>>',False),('R',False)]):
    x=825+i*46
    p.box((x,68,x+43,109),(88,71,102,255) if high else (64,58,73,255),outline=(185,171,191,255),width=1)
    p.box((x+3,72,x+40,76),(150,139,169,110))
    p.txt(x+9,74,symbol,19,(229,217,239) if high else (199,187,205),'bold')
# partial optical disc motif behind controls at right end
p.d.ellipse(rect((981,35,1133,185)),outline=(146,123,177,255),width=3*S)
p.d.ellipse(rect((1005,58,1107,162)),outline=(88,67,119,255),width=2*S)
p.d.ellipse(rect((1039,93,1073,127)),fill=(37,28,49,255),outline=(183,153,198,255),width=2*S)
p.export('08-player.png')

# Footer in PS2 button language, decorative text not false interactive controls.
p=Panel(1080,53,61)
p.frame(3,2,1077,51)
p.txt(19,12,'4tRitch@arch:~/dev$',16,(229,216,233),'mono')
p.box((249,16,260,35),(213,201,223,255))
p.txt(570,12,'○ PROJECTS     △ LINKS     × EXIT',14,(189,174,209),'mono')
p.txt(980,13,'2026',13,(175,162,195))
p.export('09-footer.png')

# Local consolidated preview of assets with the clickable three-card row.
files=['01-hero.png','02-system.png','03-stack.png','04-projects-header.png']
parts=[Image.open(ASSETS/name).convert('RGB') for name in files]
cards=[Image.open(ASSETS/name).convert('RGB') for name in ['05-okaimono.png','06-webcore.png','07-clikity.png']]
row=Image.new('RGB',(1080*S,174*S),(13,12,23))
for x,im in zip([0,365,730],cards):row.paste(im,(x*S,0))
parts.extend([row,Image.open(ASSETS/'08-player.png').convert('RGB'),Image.open(ASSETS/'09-footer.png').convert('RGB')])
h=sum(im.height for im in parts)
preview=Image.new('RGB',(1080*S,h),(14,13,24))
y=0
for im in parts:
    preview.paste(im,(0,y));y+=im.height
# usable width preview and original 2x all retained as real file
preview.save(ROOT/'PREVIEW.png',optimize=True)
print('Done: assets and preview generated at',ROOT)

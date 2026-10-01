"""Generates placeholder artwork (skyline hero, section images, icons). Replace any of them from the dashboard."""
from PIL import Image, ImageDraw, ImageFilter
import random, math
random.seed(7)
OUT='/home/claude/ts-cms/images/'

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def vgrad(w,h,stops):
    im=Image.new('RGB',(w,h)); px=im.load(); d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/(h-1)
        for i in range(len(stops)-1):
            (p0,c0),(p1,c1)=stops[i],stops[i+1]
            if p0<=t<=p1: col=lerp(c0,c1,(t-p0)/(p1-p0)); break
        d.line([(0,y),(w,y)],fill=col)
    return im

def skyline(W=1920,H=1080):
    horizon=int(H*0.70)
    sky=vgrad(W,H,[(0,(40,58,92)),(0.35,(120,110,140)),(0.58,(236,150,104)),(0.70,(250,196,140)),(0.71,(70,92,110)),(1,(22,40,52))])
    # sun glow
    glow=Image.new('L',(W,H),0); g=ImageDraw.Draw(glow)
    sx,sy=int(W*0.62),horizon-40
    g.ellipse([sx-90,sy-90,sx+90,sy+90],fill=255)
    glow=glow.filter(ImageFilter.GaussianBlur(120))
    sky=Image.composite(Image.new('RGB',(W,H),(255,214,160)),sky,glow.point(lambda v:int(v*.8)))
    sun=Image.new('L',(W,H),0); ImageDraw.Draw(sun).ellipse([sx-38,sy-38,sx+38,sy+38],fill=255)
    sky=Image.composite(Image.new('RGB',(W,H),(255,236,200)),sky,sun.filter(ImageFilter.GaussianBlur(3)))
    # towers
    layer=Image.new('L',(W,H),0); d=ImageDraw.Draw(layer)
    far=Image.new('L',(W,H),0); df=ImageDraw.Draw(far)
    x=int(W*0.18)
    while x<W*0.98:
        w=random.randint(18,46); h=random.randint(60,190)
        df.rectangle([x,horizon-h,x+w,horizon],fill=255); x+=w+random.randint(-6,10)
    towers=[]
    x=int(W*0.24)
    while x<W*0.96:
        w=random.randint(34,70); h=random.randint(170,430)
        towers.append((x,w,h)); x+=w+random.randint(6,28)
    for (x,w,h) in towers:
        kind=random.random()
        top=horizon-h
        if kind<0.18:   # tapered spire
            d.polygon([(x,horizon),(x,top+40),(x+w//2,top-50),(x+w,top+40),(x+w,horizon)],fill=255)
        elif kind<0.32: # rounded top
            d.rectangle([x,top+w//2,x+w,horizon],fill=255); d.ellipse([x,top,x+w,top+w],fill=255)
        elif kind<0.45: # slanted roof
            d.polygon([(x,horizon),(x,top+30),(x+w,top),(x+w,horizon)],fill=255)
        else:
            d.rectangle([x,top,x+w,horizon],fill=255)
            if random.random()<.4: d.rectangle([x+w//2-2,top-40,x+w//2+2,top],fill=255)
    # Doha Tower style: cylinder with dome tip
    cx=int(W*0.70); r=44; h=520
    d.rectangle([cx-r,horizon-h,cx+r,horizon],fill=255); d.ellipse([cx-r,horizon-h-r,cx+r,horizon-h+r],fill=255)
    d.polygon([(cx-6,horizon-h-r+4),(cx,horizon-h-r-70),(cx+6,horizon-h-r+4)],fill=255)
    # Tornado-like hyperboloid
    tx=int(W*0.52); th=470
    pts_l=[];pts_r=[]
    for i in range(41):
        t=i/40; y=horizon-th*t; half=34+22*abs(t-0.55)**1.6*3
        pts_l.append((tx-half,y)); pts_r.append((tx+half,y))
    d.polygon(pts_l+pts_r[::-1],fill=255)
    far_col=Image.new('RGB',(W,H),(96,92,118)); near_col=Image.new('RGB',(W,H),(30,38,56))
    img=Image.composite(far_col,sky,far.point(lambda v:int(v*.75)))
    img=Image.composite(near_col,img,layer)
    # windows
    wd=ImageDraw.Draw(img)
    for (x,w,h) in towers+[(cx-r,2*r,h)]:
        for yy in range(horizon-h+20,horizon-8,14):
            for xx in range(x+6,x+w-6,10):
                if random.random()<.16: wd.rectangle([xx,yy,xx+3,yy+5],fill=(255,206,140))
    # water reflection
    refl=img.crop((0,horizon-int(H*0.30),W,horizon)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(5))
    water=img.crop((0,horizon,W,horizon+refl.height))
    img.paste(Image.blend(water,refl,.38),(0,horizon))
    rd=ImageDraw.Draw(img)
    for y in range(horizon+6,H,7):
        for _ in range(10):
            xx=random.randint(0,W); rd.line([(xx,y),(xx+random.randint(20,90),y)],fill=(255,190,130) if abs(xx-sx)<260 else (70,90,110),width=1)
    # corniche line
    rd.rectangle([0,horizon,W,horizon+3],fill=(26,32,46))
    return img.filter(ImageFilter.SMOOTH)

def section(W,H,seed,label_shapes):
    random.seed(seed)
    im=vgrad(W,H,[(0,(15,122,82)),(1,(10,70,48))]); d=ImageDraw.Draw(im,'RGBA')
    label_shapes(d,W,H)
    return im

def approach(d,W,H):
    # gantt-like bars
    y=H*0.18
    for i in range(7):
        x0=W*0.12+random.randint(0,int(W*0.35)); x1=x0+random.randint(int(W*.15),int(W*.45))
        d.rounded_rectangle([x0,y,x1,y+H*0.055],radius=8,fill=(255,255,255,190 if i%3 else 235))
        y+=H*0.1
    for k in range(5):
        x=W*0.1+k*W*0.2; d.line([(x,H*0.12),(x,H*0.9)],fill=(255,255,255,40),width=2)

def results(d,W,H):
    base=H*0.82
    for i,v in enumerate([.25,.38,.34,.52,.61,.74]):
        x=W*0.14+i*W*0.13
        d.rounded_rectangle([x,base-H*0.6*v,x+W*0.09,base],radius=6,fill=(255,255,255,200))
    d.line([(W*0.1,base),(W*0.92,base)],fill=(255,255,255,120),width=3)
    pts=[(W*0.185+i*W*0.13,base-H*0.6*v-30) for i,v in enumerate([.25,.38,.34,.52,.61,.74])]
    d.line(pts,fill=(95,207,156,255),width=6)
    for p in pts: d.ellipse([p[0]-9,p[1]-9,p[0]+9,p[1]+9],fill=(95,207,156,255))

def logo(size,bg=(255,255,255)):
    s=size/48; im=Image.new('RGB',(size,size),bg); d=ImageDraw.Draw(im)
    g=(89,99,107); w=max(2,int(2.8*s))
    for (a,b) in [((6,6),(15,6)),((6,6),(6,15)),((42,6),(33,6)),((42,6),(42,15)),((6,42),(15,42)),((6,42),(6,33)),((42,42),(33,42)),((42,42),(42,33))]:
        d.line([(a[0]*s,a[1]*s),(b[0]*s,b[1]*s)],fill=g,width=w)
    d.line([(15*s,24*s),(21*s,30*s),(33*s,17*s)],fill=(15,122,82),width=int(5.5*s),joint='curve')
    return im

skyline().save(OUT+'hero.webp',quality=82)
section(1200,900,3,approach).save(OUT+'approach.webp',quality=85)
section(900,1200,5,results).save(OUT+'results.webp',quality=85)
logo(512).save(OUT+'logo.png'); logo(180).save(OUT+'apple-touch-icon.png')
print('images done')

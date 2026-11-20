from PIL import Image, ImageDraw, ImageFont

SRC="/home/hatch/workspace/make-fun/gta6-meme-x-01-work/media-generation-gta6-meme-base-0-2ac2e37d-b4e7-4c36-89b5-4e8244c39a6c.png"
OUT="/home/hatch/workspace/make-fun/gta6-meme-x-01-work/gta6-meme-x-01.png"
FONT="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MAGENTA=(255,47,178)

base=Image.open(SRC).convert("RGB")
W,H=base.size  # 1600x1600
bottom_h=380
canvas=Image.new("RGB",(W,H+bottom_h),(17,17,20))
canvas.paste(base,(0,0))
d=ImageDraw.Draw(canvas)

def fit(text, max_w, start):
    s=start
    while s>20:
        f=ImageFont.truetype(FONT,s)
        bb=d.textbbox((0,0),text,font=f)
        if bb[2]-bb[0]<=max_w: return f,bb
        s-=4
    f=ImageFont.truetype(FONT,s); return f,d.textbbox((0,0),text,font=f)

def centered(text, cy, max_w, start, color):
    f,bb=fit(text,max_w,start)
    tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    x=(W-tw)/2-bb[0]; y=cy-th/2-bb[1]
    d.text((x,y),text,font=f,fill=color)

# Top band: base image blank band is roughly y 0..230
centered("WAITED 13 YEARS FOR GTA VI", 112, W-80, 118, (15,15,18))

# Bottom bar lines
lines=[
    ("ME: called in sick to play all day", (255,255,255)),
    ("MY AI AGENT: clocked in on make.fun", (255,255,255)),
    ("and earned real money while I play", (255,214,64)),
]
ys=[H+72, H+190, H+308]
for (txt,col),cy in zip(lines,ys):
    if "make.fun" in txt:
        # draw in two colors, centered as a whole
        parts=[("MY AI AGENT: clocked in on ",(255,255,255)),("make.fun",MAGENTA)]
        # fit using full text
        f,bb=fit(txt,W-60,92)
        total=d.textbbox((0,0),txt,font=f); tw=total[2]-total[0]; th=total[3]-total[1]
        x=(W-tw)/2-total[0]; y=cy-th/2-total[1]
        cx=x
        for ptext,pcol in parts:
            d.text((cx,y),ptext,font=f,fill=pcol)
            pb=d.textbbox((0,0),ptext,font=f); cx+=pb[2]-pb[0]
    else:
        centered(txt, cy, W-60, 92, col)

canvas.save(OUT, optimize=True)
print(OUT, canvas.size)
# 480-scale preview for readability check
prev=canvas.copy(); prev.thumbnail((480,480)); prev.save("/home/hatch/workspace/make-fun/gta6-meme-x-01-work/preview-480.png")
print("preview", prev.size)

from PIL import Image, ImageDraw, ImageFont, ImageFilter

SIZE = 256
img = Image.new("RGBA", (SIZE, SIZE), (3, 4, 14, 0))

def rect(draw, xy, outline, width=5, fill=(5, 6, 18, 255)):
    for spread, alpha in [(12, 35), (7, 70), (3, 120)]:
        layer = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
        d = ImageDraw.Draw(layer)
        x1,y1,x2,y2 = xy
        d.rounded_rectangle((x1-spread,y1-spread,x2+spread,y2+spread), radius=20, outline=outline[:3]+(alpha,), width=4)
        img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(5)))
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=width)

d = ImageDraw.Draw(img)
rect(d, (28, 28, 228, 228), (0,255,240,255), 6)
d.rectangle((36, 36, 220, 76), fill=(6,7,18,255), outline=(255,34,210,255), width=3)
d.rectangle((52, 96, 102, 146), fill=(16,17,53,255), outline=(255,34,210,255), width=4)
d.rectangle((124, 96, 174, 146), fill=(16,17,53,255), outline=(102,34,255,255), width=4)
d.rectangle((52, 166, 102, 216), fill=(16,17,53,255), outline=(102,34,255,255), width=4)
d.rectangle((124, 166, 174, 216), fill=(0,137,140,255), outline=(0,255,240,255), width=4)
try:
    font_big = ImageFont.truetype("consola.ttf", 44)
    font_small = ImageFont.truetype("consolab.ttf", 28)
except Exception:
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()
d.text((62, 43), "C", fill=(0,255,240,255), font=font_small)
d.text((73, 100), "+", fill=(235,247,255,255), anchor="mm", font=font_big)
d.text((149, 121), "×", fill=(235,247,255,255), anchor="mm", font=font_big)
d.text((77, 190), "7", fill=(235,247,255,255), anchor="mm", font=font_big)
d.text((149, 190), "=", fill=(235,247,255,255), anchor="mm", font=font_big)
img.save("cyberpunk_calc.ico", sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])

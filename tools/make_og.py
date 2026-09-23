"""Maakt img/og-home.jpg (1200×630): receptscherm op een oranje gloed."""
import os
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
W, H = 1200, 630
bg = Image.new("RGB", (W, H), "#ffffff")
glow = Image.new("RGB", (W, H), "#ffffff")
d = ImageDraw.Draw(glow); d.ellipse((350, 260, 850, 760), fill="#e9b78f")
glow = glow.filter(ImageFilter.GaussianBlur(90))
bg = Image.blend(bg, glow, 0.9)
shot = Image.open(os.path.join(ROOT, "img/recept.jpg")).convert("RGB")
shot = shot.resize((300, int(300 * shot.height / shot.width)))
frame = Image.new("RGB", (shot.width + 24, shot.height + 24), "#1b1b1b")
frame.paste(shot, (12, 12))
mask = Image.new("L", frame.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, frame.width, frame.height), 44, fill=255)
bg.paste(frame, ((W - frame.width) // 2, 70), mask)
out = os.path.join(ROOT, "img/og-home.jpg")
bg.save(out, quality=86)
print("img/og-home.jpg", bg.size)

"""Site icons from the CertiQ mark: a white bold "Q" on the social card's purple gradient.

Writes site/static/favicon.ico (16/32/48) and site/static/apple-touch-icon.png (180x180, opaque;
iOS rounds the corners itself). Run with the repo venv (Pillow + matplotlib's DejaVu font):

    .venv/bin/python pipeline/make_icons.py
"""
from pathlib import Path

import matplotlib
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / 'site' / 'static'
FONT = Path(matplotlib.get_data_path()) / 'fonts' / 'ttf' / 'DejaVuSans-Bold.ttf'
TOP, BOTTOM = (0x38, 0x29, 0x9C), (0x5A, 0x45, 0xD4)  # social-card gradient


def mark(size: int, radius: float) -> Image.Image:
    """The mark at `size` px; radius > 0 rounds the corners (transparent outside)."""
    s = 8  # supersample, then downscale for clean edges at 16 px
    big = size * s
    grad = Image.new('RGB', (1, big))
    for y in range(big):
        t = y / (big - 1)
        grad.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)))
    img = grad.resize((big, big)).convert('RGBA')
    if radius:
        m = Image.new('L', (big, big), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, big - 1, big - 1), radius=radius * big, fill=255)
        img.putalpha(m)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT), round(big * 0.78))
    l, t, r, b = d.textbbox((0, 0), 'Q', font=font)
    # centre the letter's ink box (the Q's tail makes it bottom-heavy, so nudge up slightly)
    d.text(((big - (r - l)) / 2 - l, (big - (b - t)) / 2 - t - big * 0.03), 'Q', font=font, fill='white')
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    mark(180, 0).convert('RGB').save(STATIC / 'apple-touch-icon.png', optimize=True)
    icons = [mark(n, 0.18) for n in (48, 32, 16)]
    icons[0].save(STATIC / 'favicon.ico', sizes=[(48, 48), (32, 32), (16, 16)], append_images=icons[1:])
    print('wrote', STATIC / 'apple-touch-icon.png', STATIC / 'favicon.ico')


if __name__ == '__main__':
    main()

"""Procedural rice-paper (宣纸) texture, multiplied over the white-background renders."""
import numpy as np
from PIL import Image, ImageFilter
import sys


def paper(w=1920, h=1080, seed=42):
    rng = np.random.default_rng(seed)
    base = np.array([246, 241, 231], dtype=np.float32)  # warm rice paper
    img = np.ones((h, w, 3), np.float32) * base
    # low-frequency mottling
    for scale, amp in [(9, 3.0), (31, 2.2), (97, 1.6)]:
        n = rng.normal(0, 1, (h // scale + 2, w // scale + 2)).astype(np.float32)
        n = np.array(Image.fromarray(n).resize((w, h), Image.BICUBIC))
        img += amp * n[..., None]
    # fine grain
    img += rng.normal(0, 1.6, (h, w, 1)).astype(np.float32)
    # fibers: thin faint curved strokes
    fib = Image.new("L", (w, h), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(fib)
    for _ in range(900):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        ang = rng.uniform(0, np.pi)
        L = rng.uniform(15, 70)
        pts = []
        for t in np.linspace(0, 1, 6):
            ang += rng.normal(0, 0.25)
            pts.append((x + np.cos(ang) * L * t, y + np.sin(ang) * L * t))
        d.line(pts, fill=int(rng.uniform(60, 140)), width=1)
    fib = np.array(fib.filter(ImageFilter.GaussianBlur(0.6)), np.float32) / 255.0
    img -= 5.0 * fib[..., None]
    # gentle vignette
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    img *= (1 - 0.06 * np.clip(r - 0.55, 0, None) ** 1.5)[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    out = sys.argv[1]
    w, h = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1920, 1080)
    paper(w, h).save(out)

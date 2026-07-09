"""
Turns a photo (studentemoji.jpg) into a transparent-background sticker-style
emoji tile at standard sizes, so it can sit next to the other 11 unicode
emoji without a visible background box around it.

Primary path: rembg (a real ML background-removal model, U^2-Net). This is
what actually gives a clean cutout for an arbitrary photo — hair, glasses,
uneven lighting, whatever. Its model downloads from a GitHub release the
first time it runs (~176MB for the full-quality model). That download host
(release-assets.githubusercontent.com) was blocked by this dev sandbox's
network allowlist, so this path could NOT be live-tested here — it's
standard, widely-used code, and will work in GitHub Actions or on your own
machine (neither has that restriction), but flagging it plainly rather than
claiming something untested. Falls back to a corner-sampled chroma removal
(works if the photo has a fairly flat/plain background) so the pipeline
never just crashes if rembg or its model is unavailable.

Never touches/deletes the original file.

Usage: python3 process_emoji.py <input_photo> <out_dir>
"""
from __future__ import annotations
import argparse
import os
import sys
from PIL import Image, ImageFilter

STANDARD_SIZES = [16, 32, 64, 128, 256]


def remove_background_rembg(img: Image.Image) -> Image.Image | None:
    try:
        from rembg import remove
    except ImportError:
        print("[process_emoji] rembg not installed, skipping ML path.", file=sys.stderr)
        return None
    try:
        return remove(img)
    except Exception as e:  # model download failure, corrupt session, etc.
        print(f"[process_emoji] rembg failed ({e}); falling back to chroma removal.", file=sys.stderr)
        return None


def remove_background_chroma(img: Image.Image, tolerance: int = 28) -> Image.Image:
    """Best-effort fallback: samples the four corners, treats that as 'the
    background color', and makes close-matching pixels transparent with a
    soft-edged (blurred) mask. Good enough for a plain-background headshot;
    not a substitute for a real matting model on a busy background."""
    rgba = img.convert("RGBA")
    w, h = rgba.size
    px = rgba.load()
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

    mask = Image.new("L", (w, h), 0)
    mpx = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b, _ = px[x, y]
            dist = ((r - bg[0]) ** 2 + (g - bg[1]) ** 2 + (b - bg[2]) ** 2) ** 0.5
            mpx[x, y] = 255 if dist > tolerance * 1.8 else max(0, int(255 * (dist / (tolerance * 1.8))))
    mask = mask.filter(ImageFilter.GaussianBlur(1.5))
    rgba.putalpha(mask)
    return rgba


def tight_crop(img: Image.Image, pad_ratio: float = 0.06) -> Image.Image:
    bbox = img.getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    w, h = x1 - x0, y1 - y0
    side = max(w, h)
    pad = int(side * pad_ratio)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    half = side // 2 + pad
    canvas = Image.new("RGBA", (half * 2, half * 2), (0, 0, 0, 0))
    canvas.paste(img.crop((max(0, cx - half), max(0, cy - half), cx + half, cy + half)),
                 (0, 0))
    return canvas


def export_sizes(img: Image.Image, out_dir: str, base_name: str) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for size in STANDARD_SIZES:
        resized = img.resize((size, size), Image.LANCZOS)
        path = os.path.join(out_dir, f"{base_name}-{size}.png")
        resized.save(path)
        written.append(path)
    # canonical "full size" used by generate_banner.py
    master_path = os.path.join(out_dir, f"{base_name}.png")
    img.resize((256, 256), Image.LANCZOS).save(master_path)
    written.append(master_path)
    return written


def process(input_path: str, out_dir: str, base_name: str = "studentemoji") -> list[str]:
    img = Image.open(input_path).convert("RGB")
    cutout = remove_background_rembg(img)
    if cutout is None:
        cutout = remove_background_chroma(img)
    cropped = tight_crop(cutout)
    return export_sizes(cropped, out_dir, base_name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input_photo")
    ap.add_argument("out_dir")
    args = ap.parse_args()
    paths = process(args.input_photo, args.out_dir)
    print("wrote:")
    for p in paths:
        print(" ", p)

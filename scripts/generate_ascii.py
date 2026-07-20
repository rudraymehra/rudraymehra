"""Portrait photo -> ASCII art.

Pipeline: load -> contrast stretch -> terminal-aspect resize ->
background suppression (low-saturation flood fill from the borders) ->
Sobel edges -> luminance-to-glyph mapping.

Run standalone to preview in the terminal while tuning config values:

    python scripts/generate_ascii.py --config config.json --theme dark
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from common import AsciiParams


def load_image(path: Path | str) -> tuple[np.ndarray, np.ndarray]:
    """Load an image as (grayscale, rgb) float32 arrays in [0, 255]."""
    with Image.open(path) as img:
        rgb = img.convert("RGB")
        gray = rgb.convert("L")
    return (
        np.asarray(gray, dtype=np.float32),
        np.asarray(rgb, dtype=np.float32),
    )


def autocontrast(arr: np.ndarray, cutoff: float) -> np.ndarray:
    """Percentile-clip contrast stretch back to the full [0, 255] range."""
    lo, hi = np.percentile(arr, [cutoff, 100.0 - cutoff])
    if hi <= lo:
        return arr
    return np.clip((arr - lo) * (255.0 / (hi - lo)), 0.0, 255.0)


def resize_for_terminal(
    gray: np.ndarray, rgb: np.ndarray, width: int, char_aspect: float
) -> tuple[np.ndarray, np.ndarray]:
    """Resize both arrays to a character grid, compensating for tall cells."""
    h, w = gray.shape
    rows = max(1, round(h / w * width * char_aspect))
    small_gray = Image.fromarray(gray.astype(np.uint8)).resize((width, rows), Image.LANCZOS)
    small_rgb = Image.fromarray(rgb.astype(np.uint8)).resize((width, rows), Image.LANCZOS)
    return (
        np.asarray(small_gray, dtype=np.float32),
        np.asarray(small_rgb, dtype=np.float32),
    )


def _majority_filter(mask: np.ndarray) -> np.ndarray:
    """Keep a cell set only if most of its 3x3 neighborhood agrees."""
    padded = np.pad(mask.astype(np.uint8), 1)
    votes = sum(
        padded[dy : dy + mask.shape[0], dx : dx + mask.shape[1]]
        for dy in range(3)
        for dx in range(3)
    )
    return votes >= 5


def _flood_from_borders(candidates: np.ndarray) -> np.ndarray:
    """Subset of candidate cells reachable 4-connected from any border cell."""
    mask = np.zeros_like(candidates)
    mask[0, :] = candidates[0, :]
    mask[-1, :] = candidates[-1, :]
    mask[:, 0] |= candidates[:, 0]
    mask[:, -1] |= candidates[:, -1]
    while True:
        p = np.pad(mask, 1)
        grown = (
            p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:] | mask
        ) & candidates
        if np.array_equal(grown, mask):
            return grown
        mask = grown


def background_mask(
    gray: np.ndarray, rgb: np.ndarray, saturation: float, lum_floor: int
) -> np.ndarray:
    """True where a cell belongs to the studio background.

    A studio backdrop is desaturated while skin carries color, so a cell
    is background if it is nearly gray, not too dark (the subject's dark
    clothing and hair stay), and connected to the image border.
    """
    hi = rgb.max(axis=2)
    lo = rgb.min(axis=2)
    sat = (hi - lo) / (hi + 1e-6)
    candidates = (sat < saturation) & (gray > lum_floor)
    return _majority_filter(_flood_from_borders(candidates))


def remove_small_islands(mask: np.ndarray, min_size: int) -> np.ndarray:
    """Erase foreground blobs smaller than min_size cells (stray noise)."""
    if min_size <= 1:
        return mask
    fg = ~mask
    h, w = fg.shape
    seen = np.zeros_like(fg)
    for sy in range(h):
        for sx in range(w):
            if not fg[sy, sx] or seen[sy, sx]:
                continue
            stack, blob = [(sy, sx)], [(sy, sx)]
            seen[sy, sx] = True
            while stack:
                cy, cx = stack.pop()
                for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                    if 0 <= ny < h and 0 <= nx < w and fg[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
                        blob.append((ny, nx))
            if len(blob) < min_size:
                for cy, cx in blob:
                    mask[cy, cx] = True
    return mask


def sobel_magnitude(arr: np.ndarray) -> np.ndarray:
    """3x3 Sobel gradient magnitude, normalized to [0, 255]."""
    p = np.pad(arr, 1, mode="edge")
    gx = (
        (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:])
        - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    )
    gy = (
        (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:])
        - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    )
    mag = np.hypot(gx, gy)
    peak = float(mag.max())
    return mag * (255.0 / peak) if peak > 0 else mag


def map_to_chars(
    arr: np.ndarray,
    mask: np.ndarray,
    edges: np.ndarray,
    params: AsciiParams,
    theme: str,
) -> list[str]:
    """Turn the character-grid luminance into fixed-width ASCII rows."""
    ramp = params.ramp(theme)
    indices = (arr / 256.0 * len(ramp)).astype(int).clip(0, len(ramp) - 1)
    rows: list[str] = []
    for y in range(arr.shape[0]):
        chars = []
        for x in range(arr.shape[1]):
            if mask[y, x]:
                chars.append(" ")
            elif params.edge_threshold > 0 and edges[y, x] > params.edge_threshold:
                chars.append(params.edge_char)
            else:
                chars.append(ramp[indices[y, x]])
        rows.append("".join(chars))
    return rows


def _trim_blank_rows(rows: list[str]) -> list[str]:
    """Drop fully blank rows at the top and bottom, keeping row width."""
    start, end = 0, len(rows)
    while start < end and not rows[start].strip():
        start += 1
    while end > start and not rows[end - 1].strip():
        end -= 1
    return rows[start:end]


def generate_ascii(params: AsciiParams, theme: str, base_dir: Path | str = ".") -> list[str]:
    """Full pipeline: portrait file -> list of equal-width ASCII rows."""
    portrait = Path(base_dir) / params.portrait
    if not portrait.is_file():
        raise SystemExit(f"portrait not found: {portrait}")
    gray, rgb = load_image(portrait)
    gray = autocontrast(gray, params.contrast_cutoff)
    gray, rgb = resize_for_terminal(gray, rgb, params.width, params.char_aspect)
    mask = background_mask(gray, rgb, params.bg_saturation, params.bg_lum_floor)
    mask = remove_small_islands(mask, params.min_region)
    edges = sobel_magnitude(gray)
    return _trim_blank_rows(map_to_chars(gray, mask, edges, params, theme))


if __name__ == "__main__":
    import argparse

    from common import load_config

    parser = argparse.ArgumentParser(description="Preview the ASCII portrait")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark")
    args = parser.parse_args()

    config = load_config(args.config)
    base = Path(args.config).resolve().parent
    for line in generate_ascii(config.ascii, args.theme, base):
        print(line)

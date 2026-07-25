#!/usr/bin/env python3
"""
Renders Poketch.fprj with a fixed set of sample values into preview PNGs:
  - Poketch/images/poketch_preview.png   (native 212x520, the Mi Create project thumbnail)
  - docs/preview/poketch_preview.png     (native 212x520)
  - docs/preview/poketch_preview_2x.png  (2x upscale, nearest-neighbor to keep pixel art crisp)

Reads widget geometry/bindings straight from Poketch.fprj, so it stays correct
as the layout changes. Only the sample VALUES below are hardcoded.

Usage: python scripts/generate_preview.py
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
FPRJ_PATH = REPO_ROOT / "Poketch" / "Poketch.fprj"
IMAGES_DIR = REPO_ROOT / "Poketch" / "images"
DOCS_PREVIEW_DIR = REPO_ROOT / "docs" / "preview"

# Sample data used to render every numeric/indexed widget for the preview.
# Keyed by Widget Name in Poketch.fprj. Widgets with no entry here render as 0.
STANDARD_VALUES = {
    "HourHigh": 1,
    "HourLow": 12,
    "Hour": 12,
    "Minutes": 34,
    "MinuteHigh": 3,
    "MinuteLow": 34,
    "Battery": 87,
    "Week": 1,  # index into the BitmapList, not a raw weekday number
    "Day": 25,
    "Month": 7,
    "Temperature": 23,
    "Steps": 8412,
    "HeartRate": 72,
}

# Widgets with Visible_Src != "0" are conditionally visible on-device.
# Explicitly decide what a "typical" preview should show for those; anything
# else with Visible_Src == "0" is always drawn.
VISIBLE_OVERRIDES = {
    "Lock": False,
    "Bluetooth": True,
}

DIGIT_FILE_RE = re.compile(r"_(\d)\.png$")
INDEXED_ENTRY_RE = re.compile(r"\((\d+)\):([^|]+)")


def load(images_dir: Path, filename: str) -> Image.Image:
    return Image.open(images_dir / filename).convert("RGBA")


def render(fprj_path: Path, images_dir: Path) -> Image.Image:
    root = ET.parse(fprj_path).getroot()
    widgets = root.find("Screen").findall("Widget")

    background = next(w for w in widgets if w.get("Name") == "Background")
    canvas = load(images_dir, background.get("Bitmap"))

    for widget in widgets:
        if widget is background:
            continue

        name = widget.get("Name")
        shape = widget.get("Shape")
        x, y = int(widget.get("X")), int(widget.get("Y"))

        visible = VISIBLE_OVERRIDES.get(name, widget.get("Visible_Src") == "0")
        if not visible:
            continue

        if shape == "30":
            canvas.alpha_composite(load(images_dir, widget.get("Bitmap")), (x, y))

        elif shape == "31":
            entries = dict(INDEXED_ENTRY_RE.findall(widget.get("BitmapList")))
            index = str(STANDARD_VALUES.get(name, int(widget.get("DefaultIndex", "0"))))
            canvas.alpha_composite(load(images_dir, entries[index]), (x, y))

        elif shape == "32":
            files = widget.get("BitmapList").split("|")
            digit_files = {DIGIT_FILE_RE.search(f).group(1): f for f in files}
            glyph_w, glyph_h = Image.open(images_dir / digit_files["0"]).size

            digits = int(widget.get("Digits", "1"))
            spacing = int(widget.get("Spacing", "0"))
            alignment = widget.get("Alignment", "0")
            blanking = widget.get("Blanking", "0") == "1"
            value = STANDARD_VALUES.get(name, 0)

            text = str(value).rjust(digits) if (blanking and alignment == "2") else str(value).zfill(digits)
            for i, ch in enumerate(text):
                if ch == " ":
                    continue
                dx = x + i * (glyph_w + spacing)
                canvas.alpha_composite(load(images_dir, digit_files[ch]), (dx, y))

        else:
            raise ValueError(f"Unknown Shape={shape!r} on widget {name!r}")

    return canvas.convert("RGB")


def main() -> None:
    preview = render(FPRJ_PATH, IMAGES_DIR)
    preview_2x = preview.resize((preview.width * 2, preview.height * 2), Image.NEAREST)

    DOCS_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    preview.save(IMAGES_DIR / "poketch_preview.png")
    preview.save(DOCS_PREVIEW_DIR / "poketch_preview.png")
    preview_2x.save(DOCS_PREVIEW_DIR / "poketch_preview_2x.png")

    print(f"Wrote {IMAGES_DIR / 'poketch_preview.png'} ({preview.size[0]}x{preview.size[1]})")
    print(f"Wrote {DOCS_PREVIEW_DIR / 'poketch_preview.png'} ({preview.size[0]}x{preview.size[1]})")
    print(f"Wrote {DOCS_PREVIEW_DIR / 'poketch_preview_2x.png'} ({preview_2x.size[0]}x{preview_2x.size[1]})")


if __name__ == "__main__":
    main()

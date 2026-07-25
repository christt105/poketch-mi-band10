# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Pokétch-themed watch face for the Xiaomi Mi Band 10, built with a `.fprj` ("Face Project") declarative XML format consumed by third-party Mi Band watch-face design tooling (not Zepp OS JS). There is no build system, package manager, or test suite in this repo — it is an asset + config project, typically edited by hand and/or opened in the GUI tool that owns the `.fprj` format to preview/export. It is a Mi Create project.

## Repository layout

- `Poketch/Poketch.fprj` — the watch face project definition (XML). This is the source of truth for layout.
- `Poketch/images/` — PNG assets referenced by `Poketch.fprj` widgets (digit strips, icons, backgrounds, day-of-week glyphs).
- `Poketch/output/` — export target for the compiled watch face package; currently empty until an export is run from the design tool.
- `Examples/` — reference material only, not part of the shipped face:
  - `extracted_v1.0.5/`, `extracted_v1.5/` — decompiled Zepp OS watch faces (`app.js`, `watchface/default-target/index.js`, `assets/`) showing how an *equivalent* face is built against the `hmUI`/`DeviceRuntimeCore` JS widget API. Useful for cross-referencing what data sources (time, battery, weather, steps, heart rate, connection/lock/DND status) a face can bind to, even though this project's own `.fprj` format encodes bindings differently (see below).
  - `poketch_*.bin` / `poketch_*.zip` — packaged watch face builds at various versions, kept as artifacts for comparison.
  - `unpacked_2.0_spa_green/` — an unpacked `.bin` example.
  - `convert_tga.py` — standalone script (needs Pillow) that converts the Mi Band asset PNGs (which are actually TGA pixel data saved with a `.png` extension) into normal viewable PNGs, writing to a sibling `assets_viewable/` directory. Run with `python convert_tga.py` from `Examples/`; it hardcodes the two `extracted_*/assets` source paths.

## `Poketch.fprj` structure

Root is `<FaceProject DeviceType="466" Id="...">` containing one `<Screen>` with a flat list of `<Widget>` elements. Canvas is 212×520 (Mi Band 10 strip display). Each widget has `X`/`Y`/`Width`/`Height`/`Alpha` plus a `Shape` code that determines its behavior — inferred from usage in this file, since there is no schema doc in-repo:

- **`Shape="30"`** — static image widget. Needs `Bitmap="<file>.png"`. Used for backgrounds and fixed icons (e.g. `Background`, `Lock`, `Bluetooth`, `TemperatureIcon`, `AnimationSleep`).
- **`Shape="31"`** — indexed bitmap widget. Needs `BitmapList="(0):a.png|(1):b.png|..."` and `DefaultIndex`. Used for the day-of-week glyph (`Week`).
- **`Shape="32"`** — digit-strip widget. Needs `BitmapList="0.png|1.png|...|9.png"` (ten digit glyphs), plus `Digits` (digit count), `Alignment`, `Spacing`, `Blanking`. Used for numeric readouts (`HourHigh/Low`, `MinuteHigh/Low`, `Battery`, `Temperature`).

`Value_Src` (numeric data binding) and `Visible_Src` (conditional visibility binding) are opaque numeric codes owned by the design tool — there's no in-repo mapping table. When adding a widget that binds to the same kind of data as an existing one (e.g. another time/battery/status readout), copy the `Value_Src`/`Visible_Src` value pattern from the most similar existing widget rather than guessing new codes.

**`Width`/`Height` are not a resize control.** Mi Create derives them from the referenced bitmap's actual pixel dimensions and re-syncs them on open/save — the fields are locked in the app UI, and hand-editing them in the XML alone has no visible effect (confirmed by on-device testing). To make a widget bigger or smaller, regenerate the PNG asset(s) at the target pixel size (nearest-neighbor upscale keeps this project's pixel-art style crisp) and only then set `Width`/`Height` to match the new file, for consistency with what Mi Create will write back. If several widgets share one `BitmapList` (e.g. a shared digit-strip font) but need different rendered sizes, they need distinct filename sets (see `SmallNum_*.png` vs `NumMed_*.png`), not divergent `Width`/`Height` on the same files.

When adding a new widget:
1. Add the required PNG asset(s) to `Poketch/images/`, sized to their intended on-screen dimensions.
2. Add a `<Widget>` entry to `Poketch.fprj` with the appropriate `Shape` and matching attribute set from the patterns above, with `Width`/`Height` matching the asset's actual pixel size.
3. Reuse `Value_Src`/`Visible_Src` values from an existing widget of the same data type as a starting point.

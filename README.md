# Poketch - Mi Band 10 watch face

A Pokétch-themed watch face for the Xiaomi Mi Band 10, built in [Mi Create](https://github.com/ooflet/Mi-Create). Based on [this Mi Band 7 face](https://amazfitwatchfaces.com/mi-band-7/view/688), adapted for the Mi Band 10's larger strip display.

![preview](docs/preview/poketch_preview_blink.gif)

Shows time, date (weekday in Spanish), battery, steps, heart rate, temperature, and Bluetooth/lock status. The sitting Pikachu blinks occasionally while sleep tracking is active.

## Repo layout

- `Poketch/Poketch.fprj` — the watch face project, edited in Mi Create.
- `Poketch/images/` — the PNG assets it references.
- `scripts/generate_preview.py` — renders the project with sample data into `docs/preview/` (including the blink GIF) and the Mi Create thumbnail. Run it after changing layout or assets:

  ```
  python scripts/generate_preview.py
  ```

## Installing

Compile in Mi Create, then install the resulting `.face` on the band. Mi Band 10 isn't officially listed in Mi Create yet, so sideloading through an app like Notify for Xiaomi is the reliable path.

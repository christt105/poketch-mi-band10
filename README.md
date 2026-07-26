# Poketch - Mi Band 10 watch face

A Pokétch-themed watch face for the Xiaomi Mi Band 10, built in [Mi Create](https://github.com/ooflet/Mi-Create). Based on [this Mi Band 7 face](https://amazfitwatchfaces.com/mi-band-7/view/688), adapted for the Mi Band 10.

![preview](docs/preview/poketch_preview_blink.gif)

Shows time, date (weekday in English and Spanish), battery, steps, heart rate, temperature, and Bluetooth/lock status. The sitting Pikachu blinks occasionally.

## Repo layout

- `Poketch/Poketch.fprj` — the watch face project, edited in Mi Create.
- `Poketch/images/` — the PNG assets it references.
- `scripts/generate_preview.py` — renders the project with sample data into `docs/preview/` (including the blink GIF) and the Mi Create thumbnail. Run it after changing layout or assets:

  ```
  python scripts/generate_preview.py
  ```

## Installing

Download from [latest release](https://github.com/christt105/poketch-mi-band10/releases/latest) or compile the project in Mi Create, then install the resulting `.face` on the band. I have used [Notify for Xiaomi](https://mibandnotify.com/) to install it, but there are other methods. You can also find the watchface in [amazfitwatchfaces](https://amazfitwatchfaces.com/mi-band/view/521).

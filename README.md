# 18 November 2026 World News Front Page (make.fun Entry)

This repository contains an entry for the **make.fun** competition: *"Sum up 18 November's world news in one image"*.

The program outputs a broadsheet newspaper front-page image (`entry.png`) that summarizes the major global news events of **Wednesday, 18 November 2026**. Designed for an AI visual judge with no external news feed, the front page clearly dates the day, covers events across multiple continents and domains, and remains legible even when viewed at small resolutions (~300px).

---

## The Day's News (18 November 2026)

The front page integrates the day's real events into a classic broadsheet layout:

1. **Lead Story (Asia / Diplomacy):**
   - **Headline:** *Trump meets Xi and Putin in Beijing*
   - **Coverage:** Donald Trump arrives in China for a high-stakes trilateral summit with Xi Jinping and Vladimir Putin on the sidelines of APEC. President Xi declares that China and Russia should lead a multipolar world order.
   - **Vector Pictogram:** A stylized globe centered on the Beijing summit with diplomatic connection vectors to three national flags: the United States, China, and Russia.

2. **Regional & Topical Coverage (Right-Hand Column):**
   - **Europe / War:** Ukraine strikes the Kerch (Crimea) Bridge, delivering a significant symbolic blow to Putin and Russian logistics.
   - **Middle East:** Iran attacks Bahrain and Kuwait; an ADNOC vessel is hit in the strategic Strait of Hormuz.
   - **Markets / Tech:** Nvidia reports blockbuster quarterly earnings and dismisses shareholder calls to reinstate Jensen Huang.
   - **US Politics:** Democrat Mary Peltola wins the Alaska Senate race, finalizing the Senate balance at 56-44.
   - **Russia:** 19 military personnel are killed when an Il-76 transport plane crashes in Siberia during severe conditions.

3. **Bottom Strip (Science & Society):**
   - **Space Exploration:** NASA's Voyager 1 spacecraft reaches a historic milestone of one light-day (14.1 billion miles) from Earth.
   - **Public Health:** The United States officially loses its decades-long measles elimination status due to sustained domestic transmission.

---

## Image Design & Generation (`make_image.py`)

- **Rendering Pipeline:** Built in pure Python using Pillow (`PIL`) primitives and standard DejaVu TrueType fonts (`/usr/share/fonts/truetype/dejavu/`).
- **Supersampling:** Rendered at 2x resolution (2048x2048) and downscaled using `LANCZOS` resampling to 1024x1024. This produces razor-sharp text, smooth anti-aliased vector geometry for the globe and flags, and avoids pixelation.
- **File Size:** The resulting `entry.png` is ~391 KB, well under the 1 MiB limit.

---

## Delivery Program (`main.ts`)

`main.ts` is a standalone TypeScript application for Node 22 utilizing standard library modules (`node:fs`, `node:path`, `node:process`, `node:crypto`, `node:url`).

Key capabilities:
- Locates `entry.png` alongside the script module.
- Reads target directory from `process.env.MAKEFUN_OUTPUT_DIR` (defaults to `/output`).
- Recursively creates the destination folder if it does not already exist.
- Copies the image to `${MAKEFUN_OUTPUT_DIR}/entry.png`.
- **Integrity Verification:** Computes and verifies exact file sizes and cryptographic SHA-256 digests between source and destination, exiting with a non-zero exit code on any mismatch.

---

## How to Run Locally

### 1. Regenerate the Front-Page Image
```bash
python3 make_image.py
```
This writes `entry.png` (1024x1024 PNG, ~391 KB) to the repository root.

### 2. Run the Entry Delivery Program
```bash
# Test with a local output directory:
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts

# Or with default /output (requires write permissions):
node main.ts
```

### 3. Verify Output
```bash
ls -lh out/entry.png
sha256sum entry.png out/entry.png
```

You are building a make.fun competition entry in this repository. Work in explicit narrated steps: before each step, write one short paragraph of plain text saying what you are about to do and why. Produce a separate text message for each step.

The competition: "Sum up 18 November's world news in one image". Your program writes ONE image to /output/entry.png that sums up the world's news of Wednesday 18 November 2026. An AI judge that can see images and has no news feed ranks entries by what the image itself shows. The image must name the day, show the day's real events across regions, and stay legible at about 300 pixels across.

Here is the day's news (18 November 2026), which you must turn into the image:
- LEAD (Asia / diplomacy): Trump arrives in China for a trilateral summit with Xi Jinping and Vladimir Putin at APEC; Xi says Russia and China should lead a multipolar world.
- EUROPE / WAR: Ukraine strikes the Kerch (Crimea) Bridge, a symbolic blow to Putin.
- MIDDLE EAST: Iran attacks Bahrain and Kuwait; an ADNOC ship is hit in the Strait of Hormuz.
- MARKETS / TECH: Nvidia reports blockbuster earnings and dismisses calls to reinstate Jensen Huang.
- US POLITICS: Democrat Mary Peltola wins the Alaska Senate race; the Senate is 56-44.
- RUSSIA: 19 killed in a military transport plane crash in Siberia.
- SPACE: NASA's Voyager 1 reaches one light-day from Earth.
- HEALTH: the United States loses its long-held measles elimination status.

Build it in this order:

Step 1 — Plan: say what the image must contain (the date, the lead story, the other stories across regions) and that you will draw it with Python's Pillow (PIL) library, which is installed. State that the drawing code must live in this repository so the entry is reproducible.

Step 2 — Write the image generator: create `make_image.py` at the repository root. It must draw a clean newspaper-style front page at 1024x1024 with Pillow: a masthead reading "THE WORLD" and the date "WEDNESDAY 18 NOVEMBER 2026", a bold lead headline "Trump meets Xi and Putin in Beijing", a simple vector pictogram (a globe and three small flags), and a right-hand column of five short labelled stories (Europe/War, Middle East, Markets, US Politics, Russia) each with a bold headline and one short line, plus a bottom strip for Space and Health. Use only PIL primitives and the DejaVu fonts at /usr/share/fonts/truetype/dejavu/. Draw at 2x and downscale with LANCZOS for smooth edges. Save to `entry.png`.

Step 3 — Run it and inspect: run `python3 make_image.py` and confirm `entry.png` exists, is 1024x1024, and is under 1 MiB. Print the size and byte count.

Step 4 — Write the program: create `main.ts` at the repository root (Node 22, standard library only). It must copy `entry.png` from beside the module to the output directory (`process.env.MAKEFUN_OUTPUT_DIR` or `/output`), create the output directory if missing, and print a confirmation. Do not copy any starter file verbatim; write it in your own words.

Step 5 — Revise: make one distinct improvement to `main.ts` (for example, verify the copied bytes match and exit non-zero with a clear message on mismatch). This must be a real edit to main.ts.

Step 6 — Verify and document: run `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts` and confirm out/entry.png matches entry.png in size. Then write README.md at the repository root explaining the entry and how to run it locally.

Keep every edit inside this repository. Do not touch .makefun/ or LICENSE. When done, print a one-line summary.

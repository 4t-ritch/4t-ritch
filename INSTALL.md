# PS2 Cybercore Profile — repair verified in local browser

The original design artwork is reused directly. Each **included asset** is a complete
panel or an entire horizontal band. The incorrect project card fragments and patched
text stickers from the old packages have been removed.

## Install

1. Back up the existing profile README in your GitHub repo `4tRitch/4tRitch`.
2. Copy `README.md` and the whole `assets/` directory to the repository root.
3. Commit and push to `main`.
4. Inspect your public profile page in both desktop and mobile layouts.

## Versions

- `README.md` **recommended**: separate complete menu, whoami and status modules,
  plus untouched hero, tech stack, featured-projects row, audio player and footer.
  Each linked panel is independently clickable. The three project links are inside
  the clickable `PROJECT FILES` disclosure underneath the artwork.
- `README-SEAMLESS.md`: all six full-width bands, preserving every original source
  pixel. If GitHub inserts any gaps in the recommended layout, rename this file
  to `README.md` to prioritize exact appearance. Individual text links remain below.

## What's actually interactive?

- Menu, WHOAMI, status, and other large image modules can link to destinations.
- Expandable sections, links to the actual projects/technologies and contact work.
- The art's internal menu lines, project cards, CD buttons and console button
  prompts are **not individual clickable hotspots**. GitHub disables CSS/JS
  overlays and SVG-in-img hyperlinks; an image has only one enclosing link.

## Known artwork issue

The original approved mockup contains incorrect descriptive text in the project
images (e.g., Okaimono isn't a CLI shopping assistant). The `PROJECT FILES`
section includes the accurate descriptions and links. Fixing those words within
artwork requires repainting that graphic, not cropping it.

## Previews

- `previews/GITHUB-LIKE-DESKTOP.png` — locally rendered `README.md`.
- `previews/SEAMLESS-DESKTOP.png` — locally rendered fallback.
- `previews/PIXEL-PERFECT-COMPOSITION.png` — matches the original source pixels.

Neither preview is a screenshot from GitHub.com, so tiny layout differences
may remain. No files have been pushed to your repository automatically.

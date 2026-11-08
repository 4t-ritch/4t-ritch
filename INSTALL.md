# 4tRitch — PS2 cybercore GitHub profile (faithful fix)

This package fixes the previous visual mismatch. The default README uses a crop of the **exact approved image**. The artwork has not been redrawn or restyled.

## Install — exact image, recommended

1. In `4tRitch/4tRitch`, keep a backup of the current README.
2. Copy this package's `README.md` and **entire** `assets/` directory to the **repository root**.
3. Commit/push. GitHub will display the graphic as a single continuous image.
4. The three projects and social links immediately beneath the artwork are live links.

## Alternative — clickable project card artwork

If you want each of the 3 cards in the artwork to be clickable individually, replace `README.md` with `README-LINKED-CARDS.md` (renaming it to `README.md`). This splits the approved image into 5 PNGs, but the split pixels reconstruct the exact original; a browser may insert a few pixels of HTML spacing between segments. The individual links point to Okaimono, webcore-ui and Clikity.

## Important notes

- This version guarantees a **visual match**, not native UI controls. The system menu and the audio player are just parts of a static image, as GitHub profile README does not run custom interactive web apps.
- The artwork from the approved AI mockup contains inaccurate descriptions: Okaimono is an anime collection/calendar app, **not** a CLI shopping tool; Clikity is a Tauri/Svelte ClickUp task app, **not** a Go/TUI toolkit; webcore-ui is an educational study/demo, **not** a published component library. Those mistakes are still embedded in the original artwork because preserving its appearance was the priority for this fix. The real destinations below/within the image are correct.
- Text in the art cannot be edited through Markdown; to correct it without spoiling the look requires a separate careful art-editing pass.
- GitHub’s sidebar and pinned repo cards are outside the README and therefore unchanged.
- The ZIP intentionally does not include any font files, third-party font dependencies, HTML/CSS overlays, fake GitHub chrome or the previous procedurally generated visuals.

## Verify asset fidelity

Run `python source/verify_pixel_match.py` from anywhere. It should print PASS.

`PREVIEW-README.png` is the precise art image GitHub displays. `REFERENCE-APPROVED.png` is the previously approved full GitHub screenshot for comparison.

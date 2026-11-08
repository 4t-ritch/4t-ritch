# Muted profile palette and clean edges

## Objective
Remove unintended white player rails and match the new profile-picture palette: charcoal, fog gray, muted violet and restrained burgundy. Preserve existing design, all text including Amira Elfeky - A Dozen Roses, link behavior and readable contrast.

## Tasks
- [x] T1 Prepare recolored artwork with clean edges and regenerate consistent linked assets.
- [x] T2 Verify borders, text, crop alignment, deterministic outputs, links and desktop/mobile layout.

## Routing
Delegated direct for multi-file integration and verification. Raster edits use image_gen, not manual Pillow image editing; only generated asset crop/size normalization permitted. RDD off. Forecast below300 authored lines. Delivery ask-on-risk; no remote authorization for this request.

## Checks
Test-first regression for bright full-width border pixels. Generator, unittest discovery, diff check, visual comparison, local desktop/mobile browser readback. Preserve existing source geometry or update exact crop bounds to fit generated art without clipping. No new white padding. Any text distortion or misaligned slices makes candidate unacceptable.

## Evidence
The player source contains full-width near-white rows at y0 and201, copied unchanged by generator. These were introduced during prior generated-image normalization. Project strip has no comparable full-width near-white rows.

## Completion Evidence
- Replaced generator input with `source/approved-artwork-muted.png`; preserved the prior approved source files for history.
- Generator now derives all linked panels, bands, the player crop, and `PREVIEW.png` from the same 1448x1086 artwork. README about-panel widths match the corrected x partitions.
- Regression checks verify crop reconstruction, full-width near-white rails at exported edges, player source consistency, required song text, contact and navigation behavior.
- Corrected source frame boundaries after visual readback: hero/about y=224, about/tech y=420, tech/projects y=546, projects/player y=761, player/footer y=967, footer end y=1033. About x partitions are 293 and 903.
- `python source/extract_panels.py`: passed; generated linked panels, bands, and complete `PREVIEW.png` (1448x1033), including the full footer frame.
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s source -p 'test_*.py'`: passed, 8 tests, including complete-player and complete-footer reconstruction.
- `git diff --check`: passed.
- Desktop 1448px and mobile 390px local README browser captures: all 23 images loaded, no horizontal overflow or clipping; 17 links present. Visually confirmed complete artwork, player and footer.
- No commit or remote operation was performed.

## Independent verification
Fresh verifier confirmed 8 passing tests, clean diff check, full player/footer, no white edge rails, requested palette and unchanged URL behavior. Parent visual spot-check and diff check passed. Native risk assessment was unavailable due untracked inventory; treated as high and independently verified. RDD remains off. Live GitHub rendering has not been checked. Changes are committed locally on fix/profile-muted-palette; publishing requires authorization for this request.

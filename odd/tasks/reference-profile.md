# Restore reference profile

## Objective
Match the compact graphite/violet PS2 reference while keeping full project cards clickable in GitHub README.

## Scope and constraints
Update the existing Pillow renderer, generated assets, fonts/icons and README. Preserve existing artwork and project descriptions; do not invent product facts. No remote publishing. RDD is globally off. Delivery strategy: ask-on-risk. Forecast: 300–390 authored lines. One coherent work unit; branch fix/reference-profile.

## Tasks
- [x] T1 Restore compact reference proportions, metallic textured panels, typography and recognizable monochrome technology icons; regenerate PNG assets and preview.
- [ ] T2 Verify full-card repository links and visual/structural rendering; record any unresolved destination. Rendering and canonical links are verified; Okaimono repository destination remains unresolved, so the existing website link is preserved.

## Routing
T1/T2 delegated: preparation for writing and multiple non-trivial files. Single writer.

## Acceptance and checks
Preview aspect ratio near 746:529; no clipped text; fonts independent of host paths; three complete card anchors; generated assets match renderer. Run `python source/render.py`, `python -m unittest discover -s source -p 'test_*.py'`, `git diff --check`, and visually inspect PREVIEW.png at reference width. Test-first for deterministic dimensions/link contracts; visual styling has no meaningful automated RED.

## Progress
The initial deterministic checks failed as expected: preview aspect ratio was 1.169 instead of 746:529, and repository links used a noncanonical owner spelling. Follow-up visual review found an incorrect Apache license for Latin fonts, a missing musical-note glyph, flat rectangular framing and header fills, and simplified marks/player controls. The current renderer uses chamfered multilevel bevels, composited grain/metal gradients, subtle hero scanlines, a four-parallelogram mark, drawn musical note, Rust R gear, PostgreSQL elephant silhouette, and a shaded optical disc behind six metallic transport controls with pause selected. The bundled Latin font license now matches OFL 1.1 metadata and copyright; the subsetted CJK font retains its OFL notice and Adobe copyright.

README retains three full-card anchors and uses canonical `github.com/4t-ritch` links for webcore-ui and clikity. Okaimono's repository was not verified from bounded local evidence; its existing `okaimono.dev` card link remains unchanged and is explicitly treated as pending rather than a verified repository destination.

Verification observed: `python source/render.py` succeeded; `python -m unittest discover -s source -p 'test_*.py'` passed (6 tests); `git diff --check` passed. The preview was visually inspected after downscaling to 746x529; no clipping or overlaps were observed. Generated `PREVIEW.png` is 1492x1058 (2x the reference canvas); project assets are three 484x170 cards. The renderer diff is 641 authored added+deleted lines; tests, README, and task evidence bring the authored change above 400 lines (generated PNGs excluded), exceeding the original forecast. No commit was created.

## Next step
Confirm the Okaimono repository only if the user supplies or authorizes a destination; otherwise keep the website link. No commit was created.

# Profile song and contact

## Objective
Set displayed song to Amira Elfeky - A Dozen Roses, update Contact to https://x.com/4t_ritch, and remove anchors from hero, menu, WHOAMI and terminal prompt. Keep artwork and player decorative.

## Tasks
- [x] T1 Update player title asset and reproducible generator; update README links and noninteractive panels.
- [x] T2 Verify required title, links, preserved layout, tests and regenerated assets.

## Routing and checks
Delegated direct for multi-file work; exact edits limited to requested regions. Tests first for link behavior, visual check for song title. RDD globally off. Forecast under 250 authored lines; ask-on-risk. Commit locally on feature branch after checks, no push authorized. Run unittest discovery, generator, diff check and visual readback.

## Progress
The supplied generated player image included white letterboxing. Cropped only that padding (source rows 208–514) and resampled the remaining art to the original 1448×202 canvas. The normalized source is `source/player-amira-elfeky.png`, and the generator copies it reproducibly to `assets/10-player.png`.

README now leaves hero, menu, WHOAMI, terminal prompt, and player decorative; `top` and `profile` IDs remain for footer anchors. Contact now links to `https://x.com/4t_ritch`. System, tech, project, and footer action links remain intact.

Verification: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s source -p 'test_*.py'` passed (5 tests); `python source/extract_panels.py` passed; `git diff --check` passed. The test asserts the generated player is byte-pixel-identical to the normalized source, and regeneration changed only the intended player asset. Normalized player was visually inspected: title is correct and no white letterbox bars remain. A rendered desktop/mobile README screenshot check was not performed in this worker session; no remote or authenticated rendering was used. No commit was made by the worker.

## Verified outcome
- [x] T1 Updated player artwork to exact requested title, reproducible source/player-amira-elfeky.png; Contact now https://x.com/4t_ritch; hero/menu/WHOAMI and terminal have no explicit links.
- [x] T2 Writer and independent verifier: 5 unit tests passed, diff check passed, generator reproduces all 33 PNGs byte-identically. Exact title visually confirmed. Local desktop1440/mobile390 previews show no new layout regressions; actual GitHub renderer not inspected.
Risk assessment unassessable due untracked files; high-tier independent verification performed. RDD remains off. User explicitly authorized branch closure and push upon completion. No meaningful automated RED for raster typography; link tests observed RED before implementation per worker.

## Delivery
One coherent work unit, under250 authored lines. Integrate into existing main after normal remote fetch; push origin main:main, no force. Preserve unrelated work. No player interaction added.

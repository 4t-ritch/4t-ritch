# Integrated profile links

## Objective
Remove the visible README disclosure list and make artwork regions directly clickable without changing approved artwork. The music player remains decorative.

## Scope
README, crop generator, exact pixel-preserving clickable crops and tests. Preserve current project destinations (Okaimono website, JDotParser and DCTI repositories). No publishing authorized by this request.

## Tasks
- [x] T1 Generate pixel-preserving link regions and replace disclosure navigation with integrated image links.
- [x] T2 Verify reconstruction, link destinations, anchors and browser layout at desktop/mobile widths.

## Route and checks
Delegated direct: reading prepares multi-file edits. Single writer. Test-first deterministic crop/link contracts; no automated RED for aesthetic judgment. Run unittest discovery, generator, git diff --check and browser inspection at 900 and 375px widths. RDD off globally. Forecast 200–350 authored lines; delivery ask-on-risk. One coherent work-unit commit on fix/integrated-profile-links after checks; no push.

## Progress
- Rebuilt panel/clickable crops from `source/approved-artwork-updated.png`; its existing hero, menu, profile, system, stack, project band, player, and footer assets match those exact source pixels. The older `source/approved-artwork.png` has stale project cards, so the generator now uses the updated source.
- Split project heading from three complete project cards; split the stack into ten individually linked cells and the footer into three linked actions plus the unchanged terminal strip. Menu crop labels follow the image itself (C++, JDotParser, DCTI), not stale README details (C# stack).
- Removed all `<details>` and explanatory lists. Player art is unlinked. The flattened hero and small menu panel each link as a whole to Profile; GitHub Markdown does not provide a supported per-row clickable region for a single flattened image without fragile cropping/overlay or CSS/image maps, so individual rows in those two menus remain a documented limitation.
- Checks: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s source -p 'test_*.py'` passed (3 tests); `python source/extract_panels.py` passed; `git diff --check` passed. Local representative GitHub-Markdown CSS preview inspected at 900px and 375px; all 20 anchors/images resolved, zero broken images, and mobile document width stayed 375px.
- Browser screenshots: `/tmp/profile-900-final.png`, `/tmp/profile-375-final.png`. No remote site/session was used.
- This worker did not commit; the parent owns final verification/delivery.

## Next step
Parent spot-checks final diff and reports the two flattened-menu clickability limitations.

## Closure evidence
Implementation commit: 8953d3c. Independent verifier confirmed 3 passing tests, exact pixel reconstruction and intact local 900/375px previews. Parent diff check passed. Risk assessment unavailable due untracked inventory; treated as high and independently verified. RDD remains off. Live GitHub rendering not checked; no push performed. Hero and mini-menu remain whole-panel links, not individually interactive rows.

# Aged profile texture

## Objective
Preserve the approved muted palette while adding fine film grain, old-screen wear and slight background softness without blurring text, logos or panel borders; make the entire audio-player panel link to its requested YouTube song.

## Scope
Use image_gen to edit the existing approved muted artwork. Integrate a new non-destructive source, regenerate assets and preview; preserve crop geometry, song title, contact, existing link behavior and all copy. The full player panel links to `https://www.youtube.com/watch?v=RPNSFZ9xrGo`. No remote publishing authorized for this worker.

## Tasks
- [x] T1 Produce and integrate subtly aged artwork with readable lettering. Generated output is 1448×1086 and preserves the approved panel bounds.
- [x] T2 Link the complete player image to the requested song. Added regression coverage before README implementation; the new link assertion failed RED against the prior unlinked README.
- [x] T3 Verify complete frames, no white rails, stable regeneration, existing links and desktop/mobile readability. The 9-test unittest suite passed after regeneration; generator and `git diff --check` passed. Preview was visually inspected against the muted source; text and panel geometry remain readable and unchanged. Browser readback confirmed complete player image at 1448×206, correct YouTube href/alt, and no horizontal overflow at desktop 1280px or mobile 360px. The image-generation tool's preview was a valid 1448×1086 PNG, so no normalization was needed.
- [x] T4 Correct WHOAMI first-line alignment, remove the waving-hand emoji, regenerate all assets, and visually verify the close-up and full preview. The full phrase “Hi, I’m 4t-ritch” now shares one baseline at one font size with subdued yellow name emphasis; no emoji remains. Output stayed 1448×1086 and the 9-test suite passed again.

## Routing and checks
Delegated direct: raster editing and multi-file generated outputs. RDD off; forecast below200 authored lines; ask-on-risk delivery. Functional tests before/after; visual texture has no meaningful deterministic RED. A new test for the player URL was run first and observed failing before implementation. Existing unittest suite, generator, diff check and visual/browser readback were run. Parent owns the local work-unit commit; this worker did not commit.
## Image generation audit

Built-in `image_gen` edit mode was used after viewing `source/approved-artwork-muted.png`. The original muted source remains unchanged. Generated output was copied from `/home/ritch/.codex/generated_images/01a1bd2d-790f-7742-8cf5-9090f3f5da3d/exec-33940131-352b-4c9a-9e86-5563470bbc1d.png` to `source/approved-artwork-aged.png` after confirming exact 1448×1086 dimensions.

Prompt used:

> Use case: precise-object-edit
> Asset type: exact-format profile artwork source for a website
> Primary request: Add a restrained aged surface treatment to the supplied existing full-frame profile artwork. The current approved artwork is the sole edit target; preserve its exact composition and geometry, including all panel placements, borders, icons, image subjects, labels, and controls.
> Input images: Image 1: edit target (the current approved muted profile artwork).
> Style/medium: subdued analog-film / gently aged display patina, realistic and subtle.
> Lighting/mood: retain the existing muted charcoal, fog-gray, violet and burgundy palette; apply only very gentle atmospheric softness to background imagery.
> Materials/textures: very fine analog film grain and mottled charcoal surface texture, faint scanline patina, tiny barely visible wear. Keep all text, Japanese copy, logos, icons, panel borders and control details crisp and legible; the treatment must not obscure them.
> Text (verbatim): Preserve every existing character and glyph exactly, including the song title “Amira Elfeky - A Dozen Roses”; add no text.
> Constraints: Change only surface texture and extremely slight background atmospheric softness. Preserve exact layout, spacing, colors, artwork and all existing text; keep type, icons, borders and controls sharply defined. Keep the same 4:3 aspect ratio and composition without cropping, stretching or shifting any element.
> Avoid: global blur or Gaussian blur, blurry or garbled text, altered Japanese text, redesign, exaggerated VHS effects, glitch, strong scratches, bright rails, changed palette, new elements, watermark.

### WHOAMI line correction

The user-requested WHOAMI correction was made by editing the full aged source with built-in `image_gen` after viewing both the full source and the supplied close-up reference. The source was replaced by the corrected 1448×1086 output at `/home/ritch/.codex/generated_images/01a1bd2d-790f-7742-8cf5-9090f3f5da3d/exec-719790ed-65ed-4b0c-92ed-faf9e9c7d54a.png`, then all exports were regenerated.

Correction prompt:

> Correct only the first line in the WHOAMI / 自己紹介 panel. Set the exact phrase “Hi, I’m 4t-ritch” on one shared horizontal baseline, with the same font size throughout and balanced letter spacing. Remove the waving-hand emoji completely. The name may remain a subdued warm yellow accent, but its text must align naturally with the preceding phrase, not sit higher. Preserve the entire full-frame image, exact 1448×1086 dimensions and composition, all panel geometry, icons, borders, images, text, Japanese copy, subtle aged grain/patina, muted charcoal/fog/violet/burgundy palette, song title “Amira Elfeky - A Dozen Roses”, and all other artwork. Only correct this WHOAMI line. Keep all text clear and crisp. No white rails. Avoid changing any other text or object, moving panels or content, changing font or size within the phrase, vertical offset on the name, any emoji/hand symbol, blurring, heavy scratches, glitch, bright rails, redesign, cropping, stretching, watermark.

## Completion

All four tasks are complete. No commit or remote operation was performed by the worker.

## Final verification and delivery
Independent verifier confirmed the final WHOAMI shared baseline and no hand emoji, preserved patina/palette/geometry, correct whole-player YouTube URL, 9 passing tests and clean diff check. Parent visual spot-check and diff check passed. RDD off; assessment unavailable due untracked inventory was treated as high with independent verification. User authorized pushing all task changes. Local-only preview, not live GitHub renderer. Integrate coherent work unit into main and push origin main:main without force; no unrelated changes included.

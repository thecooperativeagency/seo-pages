# Audi Baton Rouge — Model Landing Pages

Motive-paste HTML for each Audi model in the ABR lineup. Built from
`model-pages-brief.json`. Copy raw HTML into a Motiv HTML block; assign the
suggested slug in Motive so URLs stay consistent with the rest of the
`audibatonrouge.com` model URL pattern.

## Do not rebuild
Two model URLs already ship as live ABR pages — do not overwrite these:
- Audi Q3 -> https://audibatonrouge.com/all-new-audi-q3
- Audi Q5 -> https://audibatonrouge.com/all-new-audi-q5

The models hub (`audi-models-baton-rouge.html`) links to those live URLs.

## Pages in this build

| # | Model | File | Suggested Motive slug |
|---|-------|------|-----------------------|
| 1 | 2026 Audi Q5 Sportback | `audi-q5-sportback-baton-rouge.html` | `all-new-audi-q5-sportback` |
| 2 | 2026 Audi Q7 | `audi-q7-baton-rouge.html` | `audi-q7-baton-rouge` |
| 3 | 2027 Audi Q8 | `audi-q8-baton-rouge.html` | `audi-q8-baton-rouge` |
| 4 | 2026 Audi A3 | `audi-a3-baton-rouge.html` | `audi-a3-baton-rouge` |
| 5 | 2026 Audi A5 | `audi-a5-baton-rouge.html` | `audi-a5-baton-rouge` |
| 6 | 2026 Audi A6 | `audi-a6-baton-rouge.html` | `audi-a6-baton-rouge` |
| 7 | 2027 Audi A8 | `audi-a8-baton-rouge.html` | `audi-a8-baton-rouge` |
| 8 | 2026 Audi Q4 e-tron | `audi-q4-e-tron-baton-rouge.html` | `audi-q4-e-tron-baton-rouge` |
| 9 | 2026 Audi Q4 Sportback e-tron | `audi-q4-sportback-e-tron-baton-rouge.html` | `audi-q4-sportback-e-tron-baton-rouge` |
| 10 | 2027 Audi Q6 e-tron | `audi-q6-e-tron-baton-rouge.html` | `audi-q6-e-tron-baton-rouge` |
| 11 | 2026 Audi S5 | `audi-s5-baton-rouge.html` | `audi-s5-baton-rouge` |
| 12 | 2026 Audi SQ5 | `audi-sq5-baton-rouge.html` | `audi-sq5-baton-rouge` |

The Q5 Sportback slug intentionally mirrors the existing `all-new-audi-q5`
pattern for the two "all-new" nameplates ABR uses in market. All other pages
use the `{model}-baton-rouge` slug pattern to match the existing content
library (comparison pages, etc.).

## Page structure
Every page mirrors the Q5 template (`audi-q5-s-line-black-optic.html`):

1. **Hero** — dark overlay, "Audi Baton Rouge" label, model H1, hero_sub copy,
   MSRP line ("Starting at $X"), Shop Inventory (primary) + Get Pre-Qualified
   (secondary) CTAs.
2. **Intro** — centered overview paragraph.
3. **Three feature rows** — alternating layout/background using the
   `feature`, `feature reverse alt`, `feature` sequence.
4. **Details grid** — 4-up image grid.
5. **CTA footer** — Shop Inventory, Get Pre-Qualified, and Schedule a Test
   Drive. The test-drive button uses the Motive tool markup:
   `<button class="motive__button" data-motive="test-drive">`.
6. **Disclaimer** — illustration-only imagery notice.

## Theme
Same dark ABR system as the Q5 template: black background, white text, white
primary buttons, `border-radius: 0`, AudiType/Arial font stack. Full CSS is
inlined into each page (no shared stylesheet — required for Motive paste).
The base64 `AudiType` `@font-face` blob from the Q5 template is **not**
inlined (it would add ~130KB per page); the font-family declaration is kept
so the live Motive site fonts still take effect.

## Images
All image URLs point at raw GitHub in this repo:
`https://raw.githubusercontent.com/thecooperativeagency/seo-pages/main/assets/audi-models/{path}`

Paths come from `model-pages-brief.json` (`images.hero/f1/f2/f3/grid[]`).

## Regenerating
Pages are generated from the brief via `/tmp/gen_abr_pages.py` (kept only in
scratch — recreate if you need to re-run). Edit the brief JSON, rerun the
script, and commit the resulting HTML. Do not hand-edit the generated pages
if you plan to regenerate — your edits will be overwritten.

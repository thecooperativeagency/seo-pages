# Audi Baton Rouge buyer's guide: live export

Exported 2026-10-21 from Motive (dealer 1772), go-live change_set 1563683. Each `live-export/<slug>.html` is the exact content of the page's single Full Width CmsHtml block (fullWidth variant). All pages published, index enabled.

The GitHub Pages files in this folder (`index.html`, `lease-vs-finance.html`, …) wrap that same CmsHtml block in a document shell (`<!DOCTYPE>`, title, description, canonical) for review. Body inner HTML matches live.

| Page id | Slug | Repo HTML | Repo MD | SEO title | SEO description |
|---|---|---|---|---|---|
| 171503 | /audi-buyers-guide | index.html | index.md | Should I Lease, Finance, or Pay Cash for My Audi? Baton Rouge, Louisiana \| Audi Baton Rouge | Lease vs finance, coverages, warranty, Certified Pre-Owned, and Louisiana tax — Audi Baton Rouge. |
| 171515 | /audi-buyers-guide-lease-vs-finance | lease-vs-finance.html | lease-vs-finance.md | Lease or Finance an Audi in Baton Rouge, Louisiana \| Audi Baton Rouge | Lease vs finance an Audi in Baton Rouge, Louisiana — warranty, miles, tax, and what happens when you are done. |
| 171518 | /audi-buyers-guide-coverages | coverages-advisor.html | coverages-advisor.md | Audi Protection in Baton Rouge, Louisiana \| Audi Baton Rouge | Optional protection plans — vehicle service contract, gap, paint, theft, windshield, tire and key. Audi Baton Rouge. |
| 171520 | /audi-buyers-guide-lease-end | lease-end.html | lease-end.md | What Happens When Your Audi Lease Ends in Baton Rouge, Louisiana \| Audi Baton Rouge | Inspection, wear, extra miles, buying the car, and how to avoid the turn-in fee. |
| 171522 | /audi-buyers-guide-warranty-maintenance | warranty-maintenance.html | warranty-maintenance.md | Audi Warranty and Maintenance in Baton Rouge, Louisiana \| Audi Baton Rouge | 4-year/50,000-mile warranty, included maintenance, roadside, and rust-through. |
| 171524 | /audi-buyers-guide-cpo | cpo.html | cpo.md | Audi Certified Pre-Owned in Baton Rouge, Louisiana \| Audi Baton Rouge | What Certified Pre-Owned covers, who qualifies, and how it compares to a new lease. |
| 171526 | /audi-buyers-guide-louisiana-tax-fees | louisiana-car-lease-tax-fees.html | louisiana-car-lease-tax-fees.md | Louisiana Car Lease Tax and Fees in Baton Rouge, Louisiana \| Audi Baton Rouge | How Louisiana taxes an Audi lease vs a purchase, plus title and plate fees. |
| 171530 | /audi-buyers-guide-trade-in-buyout | trade-in-and-lease-buyout.html | trade-in-and-lease-buyout.md | Audi Trade-In and Lease Buyout in Baton Rouge, Louisiana \| Audi Baton Rouge | Buy the leased car, trade it, or return it — and how Louisiana taxes a purchase with a trade-in. |
| 171531 | /audi-buyers-guide-special-programs | special-programs.html | special-programs.md | Audi Special Programs in Baton Rouge, Louisiana \| Audi Baton Rouge | College graduate, first-time buyer, and military programs — ask us if you qualify. |

Internal links in CmsHtml use live slugs (`/audi-buyers-guide-coverages`, etc.), not `.html` or `-test`.

## Native Motive components on /audi-buyers-guide-lease-vs-finance (171515), top to bottom

1. CmsHtml (Full Width): `live-export/audi-buyers-guide-lease-vs-finance.html`
2. CmsButton (1 button, align right): Get Pre-Qualified [kind pre-qualify]
3. CmsToolCta: kind prequal (pre-qualify tool)
4. CmsButton (4 buttons, align right): Explore Protection [kind internal, /audi-buyers-guide-coverages]; Get Pre-Qualified [kind pre-qualify]; Value My Trade [kind trade]; Schedule a Test Drive [kind test-drive]
5. CmsMap: kind single, map_left, dealer default location

Do not fold those native components into the HTML block. They live in Motive layout, not in this repo's CmsHtml paste.

## Known open items (Copper)

- Live pages still have legacy page-level Custom Schema FAQ JSON (old wording on hub and CPO); to be cleared in Motive Admin.
- Images and fonts load from thecooperativeagency.github.io; images to be moved to Motive media, then repo URLs updated.

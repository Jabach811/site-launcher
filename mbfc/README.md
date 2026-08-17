# My Best Friend's Closet — Tracy, CA · site rebuild

A full redesign concept for [mbfctracy.com](https://mbfctracy.com), built against the
consignment-site rubric from the market teardown. Static HTML, no build step, GitHub
Pages-ready — same conventions as the rest of this repo.

**This is a prototype, not the live site.** Every page carries a banner saying so.
All imagery is placeholder. Do not deploy to a public URL that could be mistaken for
the real shop.

## Why the rebuild looks like this

The audit found nine fields that top consignment sites get right. MBFC scored a C
overall — strong business, published terms, live selling three times a week, but three
fields effectively missing. This build fixes them structurally rather than cosmetically.

| Audit finding | Where it's fixed |
|---|---|
| No consignor portal (**F**) | `account.html` — balance, per-item status, week-in-term, payout request |
| Brands buried in prose (**D+**) | `brands.html` — accept list by tier, a real "no thank you" list, every name a shoppable link |
| No buyer-facing condition grades (**D**) | `conditions.html` + a tag on every product card and product page |
| Positioning spread across four audiences (**D**) | The whole reframe — see below |
| Markdown published as a vague range | `consign.html` — fixed schedule plus a live payout calculator |
| Live sales invisible on the website | Countdown on `index.html` and `visit.html`, driven by the real schedule |
| Intake buried | "Consign with us" is one of two permanent doors in the header |
| Contradictory hours | One authoritative block in `visit.html` — **needs confirming, see below** |

## The reframe

MBFC is roughly half new wholesale stock and half designer consignment, and the current
site gives a shopper no way to tell which is which. That's a pricing-credibility problem
running both directions.

So the design language is **the hang tag** — the one object that actually runs a
consignment floor. Two tags, used everywhere and never omitted:

- `NEW` — brass, for wholesale stock
- `CONSIGNED` — sage, for resale, always paired with a condition grade

The positioning line is *"a Tracy boutique where half the rack is designer resale"*
rather than *"a consignment shop that also sells new things."*

## Structure

```
mbfc/
├── index.html        Homepage — reframe hero, live countdown, rack preview, two doors
├── shop.html         The store. Filters: new/consigned, category, include-sold
├── product.html      Product detail, rendered from ?item= — provenance, grade, one-of-one
├── brands.html       The hinge page. Accept list + no-thank-you list
├── consign.html      Supply funnel: 4 steps, payout calculator, full terms, booking form
├── conditions.html   New vs consigned, five-grade chart, intake standard
├── account.html      Consignor portal
├── visit.html        Hours, map, live schedule, services
└── assets/
    ├── mbfc.css      Design system — tokens, tags, rack, tables, forms
    └── mbfc.js       Nav, live countdown, catalog + filters, product detail, calculator
```

Type: Bodoni Moda (display) · Karla (UI) · DM Mono (tag data), all from Google Fonts.
Palette: bone ground, navy ink, brass = NEW, sage = CONSIGNED, rust = live.
Single committed light theme — fashion retail is photography-led and a dark variant
would fight the product shots.

## Swapping in real photography

**I could not reach the live site or Instagram** — this environment's network policy
blocks all outbound hosts — so every image is a labeled placeholder sized and positioned
for the real thing.

Each slot is a `<div class="ph ...">` with a `data-slot` attribute describing the shot:

```html
<div class="ph portrait" data-slot="Midi dress, 3:4 · on model or form"></div>
```

Replace with:

```html
<img src="assets/img/fp-midi.jpg" alt="Free People tiered cotton midi dress">
```

Aspect classes: `.portrait` (3:4, products) · `.square` (1:1, details) ·
`.wide` (16:9, storefront) · `.tall` (2:3, hero).

Product slots are defined once each, in the `CATALOG` array in `mbfc.js` — change the
`slot` field there and it propagates to every grid. Shooting to a consistent 3:4 on a
plain light ground will do more for this site than any other single change.

## Numbers: theirs vs. recommended

Honesty matters here — **do not present this to the owner without separating these.**

Published by the shop, reproduced as-is:

- 40% consignor split on clothing and accessories, less tax
- 90-day term; 90-day minimum before retrieval; $25 retrieval fee
- 25 hung items per appointment plus a bag of shoes and accessories
- Cheques on the 15th, $20 minimum balance
- $0.99 handling fee on items over $10, paid by the buyer
- Intake standard: cleaned, hung, no stains/holes/pilling/odour
- Live shows Wed 4:00pm, Thu 6:00pm, Sat 9:00am Pacific
- Free shipping over $150

Changed by me, and needing the owner's sign-off:

- **Markdown schedule.** Their published term is "reduced 15–50% after 30 days depending
  on season and demand." I converted it to a fixed **full price wks 1–4 / −20% wks 5–8 /
  −40% wks 9–12**, because a range can't be calculated against and the calculator needs
  real numbers. If she wants the discretion back, the calculator has to go.
- **The $25 retrieval fee** is reproduced but I'd recommend dropping it. It saves very
  little and antagonises exactly the consignors worth keeping.
- **Brand lists** are extended beyond the names I could verify, to show the tier
  structure. Trim to what she actually accepts before this goes anywhere near a customer.
- **Hours.** The published hours are internally contradictory — Thursday appeared twice
  with two different closing times, and Sunday shows as a two-hour window. I resolved to
  Tue/Wed/Fri 10–6, Thu 10–5:30, Sat 10–4:30, Sun 10–12, closed Monday. **Confirm before
  publishing** and mirror to Google Business and Yelp.
- Consignor name, balances and item list in `account.html` are invented sample data.

## Not built

- Real cart, checkout, payments
- Real authentication on the consignor portal
- A live inventory feed — `CATALOG` in `mbfc.js` is sample data standing in for it
- Live video embed for the shows

The natural production path is Shopify with a consignment layer (ConsignCloud includes
e-commerce in the base price; Ricochet is ~$199/mo and charges extra). This build is the
design and content system to run on top of that.

# Assets Needed — Klemm Real Estate Site

The site is designed to stand up **without photography** — type, numerals and the ledger carry it. Photos are an upgrade, not scaffolding. Every panel awaiting one is a `<figure class="plate">` carrying a `data-asset` attribute naming the file it expects; drop the image in `klemm/assets/` and replace the figure with an `<img>`.

Find every slot at any time with:

    grep -rn "data-asset" klemm/*.html

## Photography (in priority order)

| File | Page | Notes |
|---|---|---|
| `assets/jack-klemm.jpg` | About | Portrait, 3:4. The single highest-value image on the site. |
| `assets/downtown-tracy.jpg` | Home | Wide 21:9 band — downtown Tracy or the Altamont at golden hour. |
| `assets/staged-listing.jpg` | Sell | A staged interior from a past listing, 4:3. |
| `assets/community-tracy.jpg` | Tracy guide | 4:3 |
| `assets/community-mountain-house.jpg` | Mountain House guide | 4:3 |
| `assets/community-tracy-hills.jpg` | Tracy Hills guide | 4:3 |
| `assets/community-river-islands.jpg` | River Islands guide | 4:3 |
| `assets/community-manteca.jpg` | Manteca guide | 4:3 |
| `assets/team-lisa.jpg` `team-mary.jpg` `team-alex.jpg` `team-erica.jpg` | About | Square headshots |
| `assets/listing-1.jpg` `listing-2.jpg` | Listings | Temporary until the IDX feed is live |

## Copy and facts to confirm with Jack

- [ ] Team bios and DRE numbers (Lisa Boone, Mary Napoli, Alex Machuca, Erica Hall)
- [ ] Exact Zillow review count — research returned both 76 and 123; the site currently says "100+"
- [ ] Google Business Profile rating and count (site says 4.8 / 90+)
- [ ] Career sales figure — site uses 3,897; confirm before it goes public
- [ ] Social handles (Facebook, Instagram, YouTube)
- [ ] Current listings — the two shown may be stale
- [ ] Per-community neighborhood notes (each guide has a `.note` line naming what to add)
- [ ] Market medians, refreshed (researched August 2026)

## Integrations to wire

- [ ] **IDX / MLS** (MetroList via iHomefinder, IDX Broker or Showcase IDX) → the `.slot` blocks on Search, Listings, and each community guide
- [ ] **Forms** → Formspree or CRM endpoint; all forms currently run in demo mode via `js/site.js`
- [ ] **Newsletter** → Mailchimp or the existing platform
- [ ] **Review widget** → live Zillow/Google aggregation on Reviews
- [ ] **Map** → Google Maps embed on Contact
- [ ] **Past-sales export** → the ledger table on The Record
- [ ] **301 redirects** on consolidation: mountainhousere.com, mantecare.com and lathropre.com each point at their community guide; old klemmre.com URLs map to their new equivalents

## Build

The site is generated, so the header, footer and nav live in exactly one place:

    python3 klemm/build.py           # regenerate all 17 pages
    python3 klemm/build-preview.py   # regenerate the single-file preview

Edit content in `build.py`, styling in `css/klemm.css`.

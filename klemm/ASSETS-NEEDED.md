# Assets Needed — Klemm Real Estate Site

Every placeholder on the site is labeled with the exact filename it expects. Drop files into `klemm/assets/` with these names and swap the `<div class="ph">` placeholder for an `<img>` tag (or hand the list to whoever finishes the build).

## Photos of Jack & the team (highest priority)
| File | Used on | Notes |
|---|---|---|
| `jack-klemm.jpg` | Home, About | Professional headshot, portrait orientation (3:4) |
| `jack-selling.jpg` | Home | Jack at a listing / with clients — candid, portrait |
| `team-lisa.jpg` | About | Lisa Boone headshot, square crop |
| `team-mary.jpg` | About | Mary Napoli headshot, square crop |
| `team-alex.jpg` | About | Alex Machuca headshot, square crop |
| `team-erica.jpg` | About | Erica Hall headshot, square crop |
| `team-group.jpg` | About | Group shot outside the 11th St office (4:3) |
| `office.jpg` | About | Office/downtown exterior (16:9) |

## Location photography (drone strongly recommended)
| File | Used on | Notes |
|---|---|---|
| `community-tracy.jpg` | Home, Communities, Tracy page | Downtown Tracy street scene (16:9) |
| `tracy-aerial.jpg` | Tracy page | Neighborhood aerial |
| `community-mh.jpg` | Home, Communities, Mountain House page | Village street scene |
| `mh-aerial.jpg` | Mountain House page | Aerial / new construction |
| `community-th.jpg` | Home, Communities, Tracy Hills page | Tracy Hills homes/hillside |
| `th-park.jpg` | Tracy Hills page | Entrance or park |
| `community-ri.jpg` | Home, Communities, River Islands page | Lakes/bridge shot |
| `ri-aerial.jpg` | River Islands page | Aerial |
| `community-manteca.jpg` | Home, Communities, Manteca page | Neighborhood |
| `manteca-2.jpg` | Manteca page | Landmark / orchard line |
| `commute.jpg` | Home, Bay Area guide, Search | ACE train at Tracy station or Altamont Pass |
| **Hero photo (optional)** | Home | A great drone shot of Tracy at golden hour can replace the drawn SVG hills in the homepage hero |

## Listing & sold photos
| File | Used on |
|---|---|
| `listing-1.jpg` … `listing-6.jpg` | Home, Featured Listings (temporary until IDX feed) |
| `sold-1.jpg` … `sold-6.jpg` | Notable Sales (temporary until past-sales feed) |
| `staged-home.jpg` | Sell page — best staged interior from a past listing |
| `sold-clients.jpg` | Sell page — sold sign / happy clients |

## Non-photo items to collect from Jack
- [ ] Logo, if one exists (otherwise the built-in "K" wordmark stands)
- [ ] Confirmed social handles (Facebook, Instagram, YouTube channel URL)
- [ ] Exact current review counts: Zillow (research found 76 vs 123 — verify), Google Business Profile rating
- [ ] Team bios + DRE numbers for Lisa, Mary, Alex, Erica
- [ ] Most recent 3 newsletters (for Insights page) + decision on migrating the 2013–present archive
- [ ] Current listing details (3 shown as placeholders were pulled from research and may be stale)
- [ ] Neighborhood blurbs marked `[PLACEHOLDER]` on each community page — Jack's local color makes these
- [ ] Confirm/adjust market stats (medians, DOM) — cited from Aug 2026 research

## Integrations to wire before launch
- [ ] **IDX search embed** (MetroList feed — iHomefinder / IDX Broker / Showcase IDX) → `search.html`, listings pages, each community page's embed slot
- [ ] **Forms** → Formspree, CRM, or email endpoint (all forms currently run in demo mode via `js/site.js`)
- [ ] **Newsletter signup** → Mailchimp or existing email platform
- [ ] **Review widget** → live Zillow/Google aggregation on `reviews.html`
- [ ] **Google Maps embed** → `contact.html`
- [ ] **301 redirects** at consolidation: mountainhousere.com → communities/mountain-house.html, mantecare.com → communities/manteca.html, lathropre.com → communities/river-islands.html, old klemmre.com URLs → new equivalents

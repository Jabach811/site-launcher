---
name: new-design-version
description: Create a new standalone design exploration (version-*.html) and register it in the versions.html gallery. Use when Joel wants to try a new visual direction for the portfolio, redesign the front page, or "make another version."
---

# New Design Version

The portfolio uses a "many rooms" system: each design direction is a complete
standalone page (`version-<slug>.html`), and `versions.html` is the gallery
that links them all. The live `index.html` is never touched by an exploration
— a direction only becomes the front page when Joel explicitly promotes it.

## Steps

1. **Name the direction.** Existing ones: The Quiet Index, The Archive Room,
   Midnight Premiere, The Signal Lab, Neighborhood Poster Wall. Each has a
   strong metaphor (a museum catalog, a file room, a cinema, a lab, a street
   wall). A new direction needs its own metaphor and a kebab-case slug for
   the filename: `version-<slug>.html`.

2. **Commit to the metaphor completely.** Read one or two existing
   `version-*.html` files first to calibrate the level of craft: custom
   palette as CSS variables, distinctive typography, section structure that
   fits the metaphor (acts, drawers, experiment logs...), micro-interactions,
   and a mood that's genuinely different from the other rooms. Half-committed
   versions are worse than none.

3. **Same content, different room.** Every version presents the same 12
   projects (5 work + 7 personal) — pull titles, descriptions, and URLs from
   the `projects` object in `index.html` so nothing drifts. Reuse images from
   `assets/` and `assets/sketchbook/` where they fit the direction.

4. **Baseline requirements** (all versions have these):
   - Fully self-contained: inline CSS/JS, no build step, no external JS.
   - `<meta name="viewport">`, meta description, sensible `<title>`.
   - `@media(prefers-reduced-motion:reduce)` disabling animations.
   - Responsive down to ~360px wide; no horizontal scroll.
   - A link back to `versions.html` and/or `index.html`.

5. **Screenshot for the gallery.** Take a 16:10 top-of-page screenshot with
   Playwright (Chromium at `/opt/pw-browsers/chromium`, viewport 1600×1000)
   and save it as `assets/versions/<slug>.png`.

6. **Register in `versions.html`**: add an `<article class="direction">`
   following the existing pattern — number, title, one-line description, and
   three `.dot` mood swatches using the direction's actual palette hexes.
   Update the header copy if it hard-codes the count ("Five different
   rooms"), and check the `.direction:nth-child(5)` full-width rule still
   makes sense with the new count.

## Promoting a version to the live front page

Only when Joel explicitly asks: copy the version's content into `index.html`
(keeping the file name `index.html`), keep the old front page available as a
`version-*.html`, and update `versions.html`'s "current" link/copy.

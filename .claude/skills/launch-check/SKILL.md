---
name: launch-check
description: Pre-merge audit of the launchpad — verify every link, image, and page renders correctly on desktop and phone before changes go live. Use before merging to main, after any content change, or when Joel asks "is everything working?" / "check the site."
---

# Launch Check

Merging to `main` deploys immediately to GitHub Pages, so this is the gate.
Run all four checks and report a single pass/fail summary with specifics.

## 1. Asset integrity

Every image referenced by HTML/JS must exist on disk. Extract every
`assets/...` path from all `*.html` files (including filenames inside the
`projects` object in index.html, which are used as
`assets/sketchbook/<img>`) and check each file exists. Also flag the
reverse: files in `assets/` referenced by nothing (report, don't delete).

## 2. Live link audit

`curl -sI -o /dev/null -w '%{http_code} %{url_effective}\n'` every external
URL found in the HTML files (the sister-site links like
`https://jabach811.github.io/<repo>/` and any GitHub links). Anything that
isn't 200/301 gets called out with the project name, not just the URL.
Google Fonts links can be skipped.

## 3. Render check (Playwright)

Chromium is at `/opt/pw-browsers/chromium` (don't run `playwright install`).
For `index.html`, `versions.html`, and any `version-*.html` touched by the
current change:

- Load the page via `file://` and capture console errors — any JS error is
  a failure.
- Screenshot at **1440×900** (desktop) and **390×844** (iPhone-ish).
- Look at the screenshots yourself: broken images, overlapping text,
  horizontal overflow, cards rendering empty. On mobile, confirm the grid
  collapses to one column and nothing is clipped.
- Send the screenshots to Joel with SendUserFile so he sees what will ship.

## 4. Page hygiene

For each changed HTML file confirm: `<meta name="viewport">` present, meta
description present, images have `alt`, external links have
`rel="noopener"`, and `prefers-reduced-motion` is handled. `.nojekyll` must
still exist at the repo root.

## Reporting

One summary up top: "Ready to merge" or "N problems found." Then the
specifics, worst first. If everything passes, say what was checked so the
pass is credible (e.g. "17 links, 28 images, 3 pages at 2 sizes").

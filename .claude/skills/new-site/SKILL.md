---
name: new-site
description: Scaffold a brand-new standalone site the way Joel's other sites are built — single-file HTML, GitHub Pages workflow, then a card on the launchpad. Use when Joel wants to start a new site for a person, business, or idea.
---

# New Site (Joel's house pattern)

Every site is its own repo published at `https://jabach811.github.io/<repo>/`.
The launchpad (this repo) just links to them.

## Before writing code

Get these from Joel (ask once, together, not one at a time):
- Who/what the site is for, and the single action a visitor should take
  (book, buy, call, read, download).
- The feeling: 2–3 adjectives or a reference he likes. His existing sites
  each commit hard to one distinct visual world — this one needs its own.
- Real content he has (photos, text, links) vs. what needs placeholders.

## Scaffold

1. Repo contents: `index.html` (self-contained: inline CSS/JS, no build
   step), `assets/` for images, `.nojekyll`, a short `README.md`, and
   `.github/workflows/deploy-pages.yml` copied from this repo (it's
   generic — deploys repo root to Pages on push to main).
2. Baseline every page must have: viewport meta, meta description,
   `theme-color`, alt text on images, `rel="noopener"` on external links,
   `prefers-reduced-motion` support, responsive to ~360px, skip link if
   there's a nav.
3. If this session is scoped to site-launcher only, build the site in a
   subfolder of the scratchpad, show Joel the preview screenshots, and give
   him the files + exact steps to create the repo (or ask him to add the
   new repo to the session with add_repo so you can push directly).

## After the site is live

Run the **add-project** skill in site-launcher to put it on the launchpad,
and remind Joel it needs a sketchbook-style card drawing.

## Quality bar

Look at 2–3 of his existing sites first (links in README.md). The bar is:
distinct palette and typography per site, generous whitespace or deliberate
density (not defaults), one clear call-to-action above the fold, and it must
look intentional on a phone — most of his visitors will be on phones.
Run the **launch-check** skill's render + link checks before calling it done.

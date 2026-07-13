# site-launcher

Two unrelated things live in this repo:

1. **Portfolio site** (repo root): static HTML/CSS, no build step, served via
   GitHub Pages. `index.html` is the live design ("Quiet Index");
   `version-*.html` are alternate design explorations linked from
   `versions.html`. Edit files directly; keep mobile reveals working
   (see commit 922cfab).
2. **`nba-ft-stats/`**: a Python CLI that compiles advanced free-throw stats
   from NBA play-by-play data. It has its own `CLAUDE.md` — read it before
   touching or running anything there, and append to its Learnings Log
   after every run or significant change.

## Conventions

- Don't mix site changes and tooling changes in one commit.
- Tooling stays inside its own subdirectory; never modify site HTML for
  tooling work.
- Python: stdlib only in `nba-ft-stats/` (it must run anywhere with
  `python3`, no pip install).

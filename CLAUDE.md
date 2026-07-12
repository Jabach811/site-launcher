# Site Launcher — Joel's Portfolio Launchpad

A static GitHub Pages site (no build step, no framework) that serves as the hub
for everything Joel has published. Deployed from `main` via
`.github/workflows/deploy-pages.yml` → https://jabach811.github.io/site-launcher/

## Architecture

- **`index.html`** — the live "sketchbook" portfolio. Fully self-contained:
  inline CSS, inline JS. Projects are NOT hard-coded as HTML — they live in a
  `projects` object (`{work: [...], personal: [...]}`) inside the `<script>`
  tag at the bottom and are rendered by the `render()` function. To add or
  edit a project, edit that object only.
- **`version-*.html`** — five standalone design explorations (quiet-index,
  archive-room, midnight-premiere, signal-lab, poster-wall). Each is a
  complete independent page with its own visual world.
- **`versions.html`** — dark gallery page linking to all design versions,
  with preview screenshots from `assets/versions/*.png`.
- **`assets/sketchbook/*.png`** — hand-drawn-style card images used by
  `index.html` (referenced by filename in the `projects` object).
- **`assets/versions/*.png`** — 16:10 screenshots of each design version.
- **`sketchbook-fixes.css`** — small external override file for index.html.
- **`.nojekyll`** — required; do not delete.

## Conventions

- Single-file pages: keep CSS in `<style>` and JS in `<script>` within each
  HTML file. Don't introduce build tools, npm, or frameworks.
- Every page must include: `<meta name="viewport">`, a meta description,
  `@media(prefers-reduced-motion:reduce)` support, and a skip link where
  there's navigation.
- All card/preview images use explicit `alt` text and `loading="lazy"`.
- External project links use `target="_blank" rel="noopener"`.
- User-visible strings passed through JS use the `esc()` helper in index.html.
- Accent colors come from the `--accent` custom-property system with
  `accent-*` utility classes; new cards pick one of: blue, pink, yellow,
  mint, orange, violet, green.
- Sister repos follow the pattern `https://jabach811.github.io/<repo>/`.

## Workflow

- Work happens on a feature branch; merging to `main` deploys automatically
  via GitHub Actions (Pages). Nothing on a branch is public until merged.
- Before merging to main, run the `launch-check` skill (link + asset +
  responsive audit).
- To add a project card: use the `add-project` skill.
- To create a new design direction: use the `new-design-version` skill.

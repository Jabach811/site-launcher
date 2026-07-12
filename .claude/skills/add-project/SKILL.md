---
name: add-project
description: Add a new project card to the launchpad (index.html). Use whenever Joel says he built/published a new site, tool, or project and wants it on the portfolio. Handles the projects data object, sketchbook image, README, and numbering.
---

# Add a Project to the Launchpad

Adding a project touches four places. Do all of them — a card without its
image or a README that drifts out of date is the most common mistake.

## Steps

1. **Gather the facts.** You need: title, one-sentence description, live URL,
   which chapter (`work` or `personal`), an accent color, and a status label.
   - URL pattern for published sites: `https://jabach811.github.io/<repo>/`
   - For code-only repos use the GitHub URL and status `Source`; for private
     work use the GitHub URL and status `Private`; published sites are `Live`
     (the default — `status` can be omitted for personal projects).
   - If Joel didn't give a description, draft one in his voice: concrete,
     warm, benefit-focused, one sentence. Look at existing descriptions in
     the `projects` object and match their rhythm. Show him the draft.

2. **Pick an accent** from: blue, pink, yellow, mint, orange, violet, green.
   Avoid giving a card the same accent as its grid neighbors — check the
   surrounding entries in the array.

3. **Add the entry** to the `projects` object in the `<script>` at the bottom
   of `index.html`. Do NOT write card HTML — the `render()` function builds
   cards from the data. Numbering is automatic (personal continues from the
   end of work), so order within the array is the display order.

4. **Card image.** Cards expect `assets/sketchbook/<img>.png` in the
   hand-drawn sketchbook style (4:3, drawn on white so `mix-blend-mode:
   multiply` works). If no image exists yet:
   - Add the entry with a temporary reuse of a thematically-close existing
     sketchbook image, AND
   - Tell Joel explicitly that a sketchbook drawing of the new project is
     needed, describing what to generate (e.g. "hand-drawn marker sketch of
     X, white background, playful line art matching assets/sketchbook/").

5. **Update `README.md`** — add the site to the "Included Sites" list if it's
   a published site.

6. **Verify** by opening the page (Playwright/Chromium is available):
   render `index.html`, confirm the new card appears, the image loads, the
   number sequence is unbroken, and the link href is correct. Then `curl -sI`
   the live URL and confirm it returns 200 (a just-published Pages site may
   404 for a few minutes — say so rather than reporting failure).

## Don'ts

- Don't edit the `render()` function or card CSS to accommodate one project.
- Don't forget `esc()` safety: the data goes through `esc()` already, so
  apostrophes in titles are fine — don't HTML-encode them in the data.

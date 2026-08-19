#!/usr/bin/env python3
"""Bundle the multi-page Klemm site into one self-contained preview file.

Rewrites cross-page links to hash routes and inlines CSS/JS so the whole site
can be clicked through from a single file (locally or published as an Artifact).
Regenerate after editing any page:  python3 klemm/build-preview.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'preview.html')

TITLE = 'Klemm Real Estate'


def page_id(relpath):
    """klemm-relative path -> hash route id."""
    p = relpath.replace(os.sep, '/')
    if p == 'index.html':
        return 'home'
    if p.endswith('/index.html'):
        return p[:-len('/index.html')].replace('/', '-')
    return p[:-len('.html')].replace('/', '-')


def rewrite_links(html, basedir):
    """Point internal .html links at their hash route."""
    def sub(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(('http', 'mailto:', 'tel:', '#', 'data:')):
            return m.group(0)
        if not url.endswith('.html'):
            return m.group(0)
        target = os.path.normpath(os.path.join(basedir, url))
        return '%s="#%s"' % (attr, page_id(target))
    return re.sub(r'(href|src)="([^"]+)"', sub, html)


def body_of(html):
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.S)
    inner = m.group(1) if m else html
    return re.sub(r'<script[^>]*src="[^"]*"[^>]*>\s*</script>', '', inner)


pages = sorted(
    glob.glob('**/*.html', root_dir=ROOT, recursive=True),
    key=lambda p: (p != 'index.html', p),
)
pages = [p for p in pages if os.path.basename(p) != 'preview.html']

css = open(os.path.join(ROOT, 'css/klemm.css')).read()

sections = []
for rel in pages:
    raw = open(os.path.join(ROOT, rel)).read()
    body = rewrite_links(body_of(raw), os.path.dirname(rel))
    sections.append(
        '<div class="pv-page" id="%s" data-src="%s">%s</div>'
        % (page_id(rel), rel.replace(os.sep, '/'), body)
    )

shell_css = """
/* --- preview shell: hides all but the routed page --- */
.pv-page { display: none; }
.pv-page.pv-on { display: block; }
.pv-badge {
  position: fixed; right: 16px; bottom: 16px; z-index: 999;
  background: var(--pine-deep); color: var(--cream);
  font-family: var(--font-body); font-size: 0.74rem; font-weight: 600;
  letter-spacing: 0.06em; text-transform: uppercase;
  padding: 9px 15px; border-radius: 999px;
  box-shadow: var(--shadow-lg); border: 1px solid rgba(255,255,255,0.18);
  display: flex; align-items: center; gap: 9px;
}
.pv-badge b { color: var(--gold); font-weight: 700; }
.pv-badge button {
  background: none; border: none; color: rgba(255,255,255,0.55);
  cursor: pointer; font-size: 1rem; line-height: 1; padding: 0;
}
.pv-badge button:hover, .pv-badge button:focus-visible { color: var(--gold); }
@media (max-width: 720px) { .pv-badge { right: 10px; bottom: 10px; font-size: 0.68rem; } }
"""

router = """
(function () {
  var pages = Array.prototype.slice.call(document.querySelectorAll('.pv-page'));

  function show() {
    var id = location.hash.replace('#', '') || 'home';
    var target = document.getElementById(id);
    if (!target || !target.classList.contains('pv-page')) target = pages[0];
    pages.forEach(function (p) { p.classList.toggle('pv-on', p === target); });
    document.querySelectorAll('.site-nav').forEach(function (n) { n.classList.remove('open'); });
    window.scrollTo(0, 0);
    var label = document.querySelector('.pv-badge .pv-name');
    if (label) label.textContent = target.getAttribute('data-src');
  }

  window.addEventListener('hashchange', show);
  show();

  // Per-page mobile nav toggles (each bundled page has its own header).
  document.querySelectorAll('.nav-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var nav = btn.closest('.nav-row').querySelector('.site-nav');
      if (nav) nav.classList.toggle('open');
    });
  });

  // Demo forms — no endpoint wired yet.
  document.querySelectorAll('form[data-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = form.querySelector('.form-success');
      if (ok) { ok.style.display = 'block'; ok.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
      form.reset();
    });
  });

  var dismiss = document.querySelector('.pv-badge button');
  if (dismiss) dismiss.addEventListener('click', function () {
    document.querySelector('.pv-badge').remove();
  });
})();
"""

badge = (
    '<div class="pv-badge"><span>Preview · <b>%d pages</b> · '
    '<span class="pv-name">index.html</span></span>'
    '<button type="button" aria-label="Hide preview badge">&times;</button></div>'
) % len(pages)

doc = (
    '<title>%s</title>\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700'
    '&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
    '<style>\n%s\n%s</style>\n\n%s\n\n%s\n<script>%s</script>\n'
) % (TITLE, css, shell_css, '\n\n'.join(sections), badge, router)

open(OUT, 'w').write(doc)
print('Wrote %s — %d pages, %.0f KB' % (OUT, len(pages), len(doc) / 1024))
for p in pages:
    print('  #%-22s %s' % (page_id(p), p))

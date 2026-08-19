#!/usr/bin/env python3
"""Build the Klemm Real Estate site.

Emits 17 static HTML pages plus a single-file preview bundle.
Run after any content edit:  python3 klemm/build.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))

PHONE = "(209) 321-1094"
TEL = "+12093211094"
EMAIL = "jack@klemmre.com"
ADDR = "672 W 11th Street, Suite 216 &middot; Tracy, CA 95376"

NAV = [
    ("search.html", "Buy"),
    ("sell.html", "Sell"),
    ("communities.html", "Communities"),
    ("record.html", "The Record"),
    ("reviews.html", "Reviews"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

# ----------------------------------------------------------------- components

def plate(caption, ratio="p-16", note="Awaiting photography", asset=""):
    """A framed panel where a photograph will live."""
    a = ' data-asset="%s"' % asset if asset else ''
    return (
        '<figure class="plate %s"%s>'
        '<figcaption class="plate-cap"><b>%s</b><span>%s</span></figcaption>'
        '</figure>' % (ratio, a, caption, note)
    )


def slot(title, body):
    return '<div class="slot"><h3>%s</h3><p>%s</p></div>' % (title, body)


def band(heading, para, cta_href, cta_text):
    return (
        '<div class="band"><div class="wrap">'
        '<div><h2>%s</h2><p>%s</p></div>'
        '<a class="btn btn-gold" href="%s">%s <span>&rarr;</span></a>'
        '</div></div>' % (heading, para, cta_href, cta_text)
    )


def steps(items):
    out = ['<div class="steps">']
    for i, (h, p) in enumerate(items, 1):
        out.append(
            '<div class="step"><div class="st-n">%02d</div>'
            '<div><h3>%s</h3><p>%s</p></div></div>' % (i, h, p)
        )
    out.append('</div>')
    return ''.join(out)


def index_rows(rows):
    out = ['<div class="index">']
    for href, name, stat, note in rows:
        out.append(
            '<a class="index-row" href="%s">'
            '<span class="ir-name">%s</span>'
            '<span class="ir-stat">%s</span>'
            '<span class="ir-note">%s</span>'
            '<span class="ir-go">&rarr;</span></a>' % (href, name, stat, note)
        )
    out.append('</div>')
    return ''.join(out)


def quotes(items):
    out = ['<div class="quote-grid">']
    for q, c in items:
        out.append(
            '<div class="quote-cell"><div class="rating">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
            '<q>%s</q><cite>%s</cite></div>' % (q, c)
        )
    out.append('</div>')
    return ''.join(out)

# ----------------------------------------------------------------- shell

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/klemm.css">
</head>
<body>
'''


def masthead(active):
    links = []
    for href, text in NAV:
        on = ' class="on"' if href == active else ''
        links.append('<a href="%s"%s>%s</a>' % (href, on, text))
    links.append('<a class="btn btn-gold" href="valuation.html">Home Valuation</a>')
    return (
        '<div class="utility"><div class="wrap">'
        '<span class="u-left">%s</span>'
        '<span class="u-right"><a href="tel:%s">%s</a>'
        '<a href="mailto:%s">%s</a></span>'
        '</div></div>'
        '<header class="masthead"><div class="wrap">'
        '<a class="wordmark" href="index.html">'
        '<span class="wm-name">KLEMM</span>'
        '<span class="wm-sub">Real Estate &middot; Tracy, California</span></a>'
        '<nav class="nav">%s</nav>'
        '<button class="burger" aria-label="Menu" aria-expanded="false">Menu</button>'
        '</div></header>' % (ADDR, TEL, PHONE, EMAIL, EMAIL, ''.join(links))
    )


FOOT = '''<footer class="foot"><div class="wrap">
<div class="foot-grid">
  <div>
    <div class="foot-mark">KLEMM</div>
    <p class="foot-blurb">An independent brokerage on 11th Street since 1988. Nearly four thousand homes, one town.</p>
  </div>
  <div>
    <h4>Buy</h4>
    <ul>
      <li><a href="search.html">Search Homes</a></li>
      <li><a href="listings.html">Current Listings</a></li>
      <li><a href="bay-area.html">Bay Area Guide</a></li>
      <li><a href="communities.html">Communities</a></li>
    </ul>
  </div>
  <div>
    <h4>Sell</h4>
    <ul>
      <li><a href="sell.html">The Process</a></li>
      <li><a href="valuation.html">Home Valuation</a></li>
      <li><a href="record.html">The Record</a></li>
      <li><a href="reviews.html">Reviews</a></li>
      <li><a href="insights.html">Market Letters</a></li>
      <li><a href="about.html">About Jack</a></li>
    </ul>
  </div>
  <div>
    <h4>Office</h4>
    <ul>
      <li>672 W 11th Street, Suite 216<br>Tracy, California 95376</li>
      <li><a href="tel:{tel}">{phone}</a></li>
      <li><a href="mailto:{email}">{email}</a></li>
    </ul>
    <h4 style="margin-top:26px">Monthly Market Letter</h4>
    <form class="sub-form" data-demo>
      <input type="email" placeholder="Email address" aria-label="Email address">
      <button type="submit">Join</button>
    </form>
  </div>
</div>
<div class="colophon">
  <span>&copy; 2026 Klemm Real Estate, Inc. &middot; DRE #01866206 &middot; Jack Klemm, Broker &middot; DRE #01004092</span>
  <span>Equal Housing Opportunity</span>
</div>
</div></footer>
<script src="js/site.js"></script>
</body>
</html>
'''.replace('{tel}', TEL).replace('{phone}', PHONE).replace('{email}', EMAIL)

# ----------------------------------------------------------------- pages

PAGES = []

def page(slug, title, desc, nav, body):
    PAGES.append(dict(slug=slug, title=title, desc=desc, nav=nav, body=body))


COMMUNITY_ROWS = [
    ("community-tracy.html", "Tracy", "Median $673K", "Home base since 1988. A real downtown, an ACE station, and the most house per dollar within an hour of the Tri-Valley."),
    ("community-mountain-house.html", "Mountain House", "Median $963K", "California&rsquo;s newest city and one of its fastest-growing. First exit after the Altamont."),
    ("community-tracy-hills.html", "Tracy Hills", "New construction", "The master-planned southern edge, where builder inventory sets the pace and patience is leverage."),
    ("community-river-islands.html", "River Islands &amp; Lathrop", "Master-planned", "A waterfront plan on the San Joaquin with its own lakes, trails and charter schools."),
    ("community-manteca.html", "Manteca", "Best value", "Family-first value where the 120 meets the 99 &mdash; the most square footage of any market we serve."),
]

REVIEW_QUOTES = [
    ("Always available whether by phone, email or text, and answers questions promptly.", "Zillow &middot; Tracy seller"),
    ("Renowned among colleagues and clients alike for his honesty, integrity and professionalism.", "Zillow &middot; Tracy client"),
    ("By far the most professional and resourceful brokerage in Mountain House and Tracy.", "Yelp &middot; Mountain House client"),
]

# ---------- HOME ----------
page("index.html",
     "Klemm Real Estate &mdash; Tracy, California Since 1988",
     "Jack Klemm has sold nearly 4,000 homes in Tracy, Mountain House, Lathrop and Manteca since 1988. An independent brokerage with a 5.0 rating and 38 years on the same streets.",
     "index.html",
     '''
<section class="hero"><div class="wrap">
  <div class="hero-kicker">Tracy &middot; Mountain House &middot; Tracy Hills &middot; Lathrop &middot; Manteca</div>
  <h1>Thirty-eight years on <span class="accent">the same streets.</span></h1>
  <p class="lede">Jack Klemm has been selling homes in Tracy since 1988 &mdash; through every boom, every bust, and nearly four thousand closings. No franchise. No hand-offs. The broker answers the phone.</p>
  <div class="btn-row">
    <a class="btn btn-gold" href="valuation.html">What is my home worth? <span>&rarr;</span></a>
    <a class="btn btn-line" href="search.html">Search homes</a>
  </div>

  <div class="record">
    <div class="record-cell"><span class="num">3,897</span><div class="rc-label">Homes sold<br>since 1988</div></div>
    <div class="record-cell"><span class="num">77</span><div class="rc-label">Closed in the<br>last 12 months</div></div>
    <div class="record-cell"><span class="num">5.0<small>&#9733;</small></span><div class="rc-label">Zillow rating,<br>100+ reviews</div></div>
    <div class="record-cell"><span class="num">25</span><div class="rc-label">Straight years of the<br>CVAR Master&rsquo;s Award</div></div>
  </div>

  <form class="searchbar" data-demo>
    <input type="text" placeholder="Search by city, neighborhood, or address" aria-label="Search homes">
    <button class="btn btn-gold" type="submit">Search <span>&rarr;</span></button>
  </form>
  <div class="ok">Search connects to the MLS feed at launch.</div>
</div></section>

<section class="rule-top"><div class="wrap">
  <div class="head">
    <span class="label">Where we work</span>
    <h2>Five markets, one broker who has sold in all of them.</h2>
  </div>
  ''' + index_rows(COMMUNITY_ROWS) + '''
  <div style="margin-top:38px"><a class="arrow-link" href="communities.html">All community guides <span>&rarr;</span></a></div>
</div></section>

<section class="bg-field rule-top"><div class="wrap cols">
  <div class="c-5 stack gap-3">
    <span class="label">Selling</span>
    <h2>A process, not a promise.</h2>
    <p class="lede">Every Klemm listing gets the same sequence &mdash; the one refined across 3,897 closings. It starts with a free walk-through and an honest number.</p>
    <div class="btn-row">
      <a class="btn btn-gold" href="valuation.html">Free valuation <span>&rarr;</span></a>
      <a class="btn btn-line" href="sell.html">See the process</a>
    </div>
  </div>
  <div class="c-7">''' + steps([
        ("Show-ready consultation", "A room-by-room walk-through. Only the repairs and staging that return more than they cost &mdash; Jack will talk you out of the rest."),
        ("A number from real comps", "Hand-picked closings from your actual street, adjusted for condition. Not an algorithm&rsquo;s range."),
        ("Marketed like it matters", "Professional photography and video, the MLS, a twelve-year newsletter list, and a buyer database built since 1988."),
        ("Negotiated by the broker", "Offers, counters, appraisal gaps, 1031 exchanges. Handled by Jack, not passed to a junior teammate."),
     ]) + '''</div>
</div></section>

<section class="rule-top"><div class="wrap cols">
  <div class="c-7">
    <div class="pullquote">
      <q>Klemm Real Estate is by far the most professional and resourceful brokerage in Mountain House and Tracy.</q>
      <cite>Yelp review &middot; Mountain House client</cite>
    </div>
  </div>
  <div class="c-5 stack gap-3">
    <span class="label">The reputation</span>
    <p class="lede">More than two hundred public reviews across Zillow, Yelp and Google &mdash; and essentially no complaints in thirty-eight years. The same three words come up again and again: communication, honesty, professionalism.</p>
    <a class="arrow-link" href="reviews.html">Read the reviews <span>&rarr;</span></a>
  </div>
</div></section>

<section class="pad-sm"><div class="wrap">''' + plate("Plate I &mdash; Downtown Tracy, 11th Street", "p-wide", asset="assets/downtown-tracy.jpg") + '''</div></section>

<section class="rule-top"><div class="wrap cols">
  <div class="c-6 stack gap-3">
    <span class="label">Coming over the hill</span>
    <h2>What your Bay Area equity actually buys.</h2>
    <p class="lede">Same job, same paycheck, very different house. Tracy sits roughly a million dollars below Pleasanton at the median &mdash; and the honest version of the commute is a train ride, not a horror story.</p>
    <a class="arrow-link" href="bay-area.html">The Bay Area guide <span>&rarr;</span></a>
  </div>
  <div class="c-6">
    <div class="ledger-wrap"><table class="ledger">
      <thead><tr><th>City</th><th>Median</th><th>What ~$700K buys</th></tr></thead>
      <tbody>
        <tr><td class="addr">Pleasanton</td><td class="money">$1.7M</td><td>A condo, maybe</td></tr>
        <tr><td class="addr">Dublin</td><td class="money">$1.2M</td><td>A townhome</td></tr>
        <tr><td class="addr">Livermore</td><td class="money">$1.1M</td><td>A small starter</td></tr>
        <tr><td class="addr">Tracy</td><td class="money">$673K</td><td>Four beds and a yard</td></tr>
      </tbody>
    </table></div>
  </div>
</div></section>

''' + band("Start with the number.",
           "A free market valuation from the broker who has sold nearly four thousand of them. No obligation, no automated guess.",
           "valuation.html", "Get my valuation"))

# ---------- SEARCH ----------
page("search.html", "Search Homes &mdash; Tracy, Mountain House, Lathrop &amp; Manteca | Klemm Real Estate",
     "Search every home on the market in Tracy, Mountain House, Tracy Hills, River Islands and Manteca, with saved searches and instant listing alerts.",
     "search.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Buy</span>
  <h1>Search every home on the market.</h1>
  <p class="lede">Full MLS coverage across San Joaquin County, plus saved searches and alerts &mdash; because in this market the good ones do not wait.</p>
</div></section>

<section><div class="wrap">
  ''' + slot("MLS map search", "The live IDX search embed mounts here at launch &mdash; map view with price, bed, bath, square footage, lot and new-construction filters, drawn from the MetroList feed.") + '''
</div></section>

<section class="rule-top bg-field"><div class="wrap cols">
  <div class="c-5 stack gap-3">
    <span class="label">Buyer advantage</span>
    <h2>See it before the portals do.</h2>
    <p class="lede">Set up a saved search and you will get new listings, price cuts and coming-soon homes as they hit the MLS &mdash; plus an honest opinion on which are worth the drive.</p>
    <a class="arrow-link" href="bay-area.html">Moving from the Bay Area? <span>&rarr;</span></a>
  </div>
  <div class="c-7">
    <form class="form" data-demo>
      <div class="form-grid">
        <div><label for="s-name">Name</label><input type="text" id="s-name" placeholder="Your name"></div>
        <div><label for="s-email">Email</label><input type="email" id="s-email" placeholder="you@email.com"></div>
        <div><label for="s-area">Area</label><select id="s-area"><option>Tracy</option><option>Tracy Hills</option><option>Mountain House</option><option>River Islands / Lathrop</option><option>Manteca</option><option>Anywhere nearby</option></select></div>
        <div><label for="s-budget">Budget</label><select id="s-budget"><option>Under $500K</option><option>$500K &ndash; $700K</option><option>$700K &ndash; $900K</option><option>$900K &ndash; $1.2M</option><option>$1.2M and up</option></select></div>
        <div class="full"><label for="s-notes">What are you looking for?</label><textarea id="s-notes" rows="3" placeholder="Beds, baths, must-haves, timeline"></textarea></div>
      </div>
      <div class="btn-row" style="margin-top:24px"><button class="btn btn-gold" type="submit">Start my search <span>&rarr;</span></button></div>
      <div class="ok">Demo mode &mdash; connect this form to the CRM before launch.</div>
      <p class="note">No spam, no pressure. Jack reviews every request personally.</p>
    </form>
  </div>
</div></section>
''')

# ---------- LISTINGS ----------
page("listings.html", "Current Listings | Klemm Real Estate",
     "Homes currently listed by Klemm Real Estate across Tracy, Mountain House, Lathrop and Manteca.",
     "search.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Buy</span>
  <h1>Current listings.</h1>
  <p class="lede">Every home below was prepared, staged, photographed and priced through the same process. This page reads from the MLS feed at launch.</p>
</div></section>

<section><div class="wrap cols">
  <div class="c-6">''' + plate("2868 Joleo Court, Tracy &mdash; $895,000", "p-43", asset="assets/listing-1.jpg") + '''
    <div style="margin-top:18px"><h3>2868 Joleo Court</h3><p class="note">5 bed &middot; 3 bath &middot; 2,944 sq ft &middot; Tracy &mdash; verify status against the MLS</p></div>
  </div>
  <div class="c-6">''' + plate("2413 Augusta Avenue, Tracy &mdash; $870,000", "p-43", asset="assets/listing-2.jpg") + '''
    <div style="margin-top:18px"><h3>2413 Augusta Avenue</h3><p class="note">4 bed &middot; 3 bath &middot; 3,128 sq ft &middot; Tracy &mdash; verify status against the MLS</p></div>
  </div>
</div>
<div class="wrap" style="margin-top:52px">''' + slot("Live listing feed", "At launch this page pulls Klemm Real Estate&rsquo;s active listings automatically, each with its own detail page, full gallery, video tour and showing-request form.") + '''</div>
</section>

''' + band("Not seeing the right home?", "The best homes in this market often trade before they are broadly advertised. Tell Jack what you are after.", "search.html", "Start a saved search"))

# ---------- BAY AREA ----------
page("bay-area.html", "Moving from the Bay Area to Tracy &mdash; The Honest Guide | Klemm Real Estate",
     "Commute realities, school notes and real price comparisons for Bay Area families considering Tracy, Mountain House or River Islands.",
     "search.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">The commuter&rsquo;s guide</span>
  <h1>Moving over the hill? Read this first.</h1>
  <p class="lede">Every week, families trade a Pleasanton mortgage for a real backyard in Tracy. Here is the honest version of that trade &mdash; commute included &mdash; from a broker who has guided it since 1988.</p>
</div></section>

<section><div class="wrap">
  <div class="head"><span class="label">The math</span><h2>What the same money buys on each side of the Altamont.</h2></div>
  <div class="ledger-wrap"><table class="ledger">
    <thead><tr><th>City</th><th>Median home price</th><th>What roughly $700,000 gets you</th></tr></thead>
    <tbody>
      <tr><td class="addr">Pleasanton</td><td class="money">$1.7M</td><td>A condo, maybe</td></tr>
      <tr><td class="addr">Dublin</td><td class="money">$1.2M</td><td>A townhome</td></tr>
      <tr><td class="addr">Livermore</td><td class="money">$1.1M</td><td>A small starter home</td></tr>
      <tr><td class="addr">Mountain House</td><td class="money">$963K</td><td>A large newer home in a master-planned city</td></tr>
      <tr><td class="addr">Tracy</td><td class="money">$673K</td><td>A four-bedroom single-family home with a yard</td></tr>
      <tr><td class="addr">Manteca &amp; Lathrop</td><td class="money">$600Ks</td><td>New construction with room to spare</td></tr>
    </tbody>
  </table></div>
  <p class="note">Medians as researched August 2026; refreshed each month in Jack&rsquo;s market letter.</p>
</div></section>

<section class="rule-top bg-field"><div class="wrap cols">
  <div class="c-5 stack gap-3">
    <span class="label">The commute, honestly</span>
    <h2>Yes, there is a hill. Here is how people actually do it.</h2>
    <p class="lede">Nobody will tell you the drive does not exist. What they will not tell you is how many families never make it &mdash; because the train, or the hybrid week, changed the arithmetic.</p>
  </div>
  <div class="c-7">''' + steps([
        ("The ACE train", "Board in downtown Tracy or Lathrop and work, read or sleep your way to Pleasanton, Fremont or San Jose. No white knuckles on the 580."),
        ("I-205 to I-580", "The classic run over the Altamont. Leave early, and the pass is quiet. Leave at eight, and it is not."),
        ("The hybrid week", "Most of Jack&rsquo;s Bay Area buyers now commute two or three days. That single fact has redrawn what counts as too far."),
     ]) + '''</div>
</div></section>

<section class="rule-top"><div class="wrap">
  <div class="head"><span class="label">Where commuters land</span><h2>Three versions of the same move.</h2></div>
  ''' + index_rows([
        ("community-mountain-house.html", "Mountain House", "Closest to the Bay", "First exit after the pass. Newest city in California, top-rated schools, shortest drive &mdash; and priced for it."),
        ("community-tracy.html", "Tracy", "The balanced pick", "A real downtown, established neighborhoods, the ACE station, and the most house for the money."),
        ("community-river-islands.html", "River Islands", "The new build", "Lakes, trails and charter schools, with construction still underway and incentives still available."),
     ]) + '''
</div></section>

''' + band("Selling there, buying here?",
           "Jack coordinates both sides &mdash; including contingent offers and 1031 exchanges &mdash; so you are never carrying two mortgages or zero houses.",
           "contact.html", "Talk through the move"))

# ---------- SELL ----------
page("sell.html", "Sell Your Home With Jack Klemm | Klemm Real Estate, Tracy",
     "How Klemm listings sell: a free show-ready consultation, comparables-based pricing, full marketing and negotiation handled by the broker himself.",
     "sell.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Selling</span>
  <h1>Your home, sold the way 3,897 others were.</h1>
  <p class="lede">There is no algorithm for getting top dollar in Tracy. There is a sequence &mdash; refined over thirty-eight years &mdash; and it begins with an honest conversation about what your home is really worth.</p>
  <div class="btn-row" style="margin-top:34px">
    <a class="btn btn-gold" href="valuation.html">Free valuation <span>&rarr;</span></a>
    <a class="btn btn-line" href="reviews.html">Hear from sellers</a>
  </div>
</div></section>

<section class="pad-sm"><div class="wrap">
  <div class="record" style="margin-top:0">
    <div class="record-cell"><span class="num">77</span><div class="rc-label">Homes sold in the<br>last twelve months</div></div>
    <div class="record-cell"><span class="num">$717K</span><div class="rc-label">Average sale price<br>across recent closings</div></div>
    <div class="record-cell"><span class="num">$1.9M</span><div class="rc-label">Top of the recent<br>price range</div></div>
    <div class="record-cell"><span class="num">25</span><div class="rc-label">Consecutive CVAR<br>Master&rsquo;s Awards</div></div>
  </div>
</div></section>

<section class="rule-top"><div class="wrap cols">
  <div class="c-4 stack gap-3">
    <span class="label">The sequence</span>
    <h2>Six steps between thinking about it and sold.</h2>
    <p class="lede">Nothing here is a secret. It is simply done, every time, in order.</p>
  </div>
  <div class="c-8">''' + steps([
        ("The honest number", "A comparative market analysis built from decades of local closings &mdash; what your home will sell for, not what earns a signature."),
        ("Show-ready consultation, free", "A room-by-room walk-through with specific prep recommendations, and a candid list of the improvements not worth making."),
        ("Staging and photography", "Buyers decide online in seconds. Your home is staged and professionally photographed before a single listing line goes live."),
        ("Full-market launch", "The MLS and the portals, plus a twelve-year newsletter audience and a buyer database no template brokerage can match."),
        ("Negotiation that shows up in your proceeds", "Offers, counters, appraisal gaps, repair requests, exchanges &mdash; handled by the broker himself."),
        ("Managed to the wire", "Inspections, disclosures, escrow, timelines. One recent seller went from first meeting to funds in about nine weeks."),
     ]) + '''</div>
</div></section>

<section class="rule-top bg-field"><div class="wrap cols">
  <div class="c-6 stack gap-3">
    <span class="label">Why it works</span>
    <h2>The independent advantage.</h2>
    <p class="lede">Franchise agents answer to a brand three states away. Jack answers to you. Klemm Real Estate is one of the few genuinely independent brokerages left in Tracy, which means every marketing decision and every negotiation call gets the owner&rsquo;s attention.</p>
    <div class="pullquote" style="margin-top:14px">
      <q>Excellent negotiation skills, whether structuring sales or 1031 exchanges &mdash; no matter how simple or complex.</q>
      <cite>Zillow review &middot; Tracy seller</cite>
    </div>
  </div>
  <div class="c-6">''' + plate("Plate II &mdash; A staged Klemm listing", "p-43", asset="assets/staged-listing.jpg") + '''</div>
</div></section>

''' + band("Start with the number.",
           "Free, prepared by the broker, and yours within one business day. Whether you sell this year or in five is entirely your call.",
           "valuation.html", "What is my home worth?"))

# ---------- VALUATION ----------
page("valuation.html", "Free Home Valuation &mdash; Tracy, Mountain House &amp; Manteca | Klemm Real Estate",
     "Request a free, broker-prepared market valuation of your Tracy-area home from Jack Klemm.",
     "sell.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Free valuation</span>
  <h1>What is your home actually worth?</h1>
  <p class="lede">The portals guess from public records. Jack prices from the closings he handled himself. Free, no obligation, back to you within one business day.</p>
</div></section>

<section><div class="wrap cols">
  <div class="c-7">
    <form class="form" data-demo>
      <div class="form-grid">
        <div class="full"><label for="v-address">Property address</label><input type="text" id="v-address" placeholder="123 Main Street, Tracy, CA"></div>
        <div><label for="v-name">Name</label><input type="text" id="v-name" placeholder="Your name"></div>
        <div><label for="v-phone">Phone</label><input type="tel" id="v-phone" placeholder="(209) 555-0123"></div>
        <div><label for="v-email">Email</label><input type="email" id="v-email" placeholder="you@email.com"></div>
        <div><label for="v-timeline">Timeline</label><select id="v-timeline"><option>Just curious</option><option>Selling within 3 months</option><option>Selling within a year</option><option>Planning ahead</option></select></div>
        <div class="full"><label for="v-notes">Anything Jack should know?</label><textarea id="v-notes" rows="3" placeholder="Upgrades, additions, rental history"></textarea></div>
      </div>
      <div class="btn-row" style="margin-top:24px"><button class="btn btn-gold" type="submit">Send my request <span>&rarr;</span></button></div>
      <div class="ok">Demo mode &mdash; connect this form to the CRM before launch.</div>
      <p class="note">Your information is never sold or shared. Jack prepares every valuation personally.</p>
    </form>
  </div>
  <div class="c-5 stack gap-3">
    <span class="label">Why it differs</span>
    <h2>An answer, not a range.</h2>
    ''' + steps([
        ("Real comparables", "Hand-picked closed sales from your actual neighborhood, including the details that never reach public record."),
        ("Condition-adjusted", "Your kitchen remodel and your deferred roof, both priced in. Honesty is the whole brand."),
        ("A plan, if you want one", "If the number works for you, Jack shows which prep adds to it &mdash; and which to skip."),
     ]) + '''
  </div>
</div></section>
''')

# ---------- THE RECORD ----------
page("record.html", "The Record &mdash; 3,897 Homes Sold Since 1988 | Klemm Real Estate",
     "A track record you can count: nearly 4,000 closings across Tracy, Mountain House, Lathrop and Manteca since 1988.",
     "record.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">The record</span>
  <h1>Anyone can promise. Jack can point.</h1>
  <p class="lede">Nearly four thousand closed transactions across every neighborhood, price point and market cycle since 1988 &mdash; in one town, under one name.</p>
</div></section>

<section class="pad-sm"><div class="wrap">
  <div class="record" style="margin-top:0">
    <div class="record-cell"><span class="num">3,897</span><div class="rc-label">Career closings</div></div>
    <div class="record-cell"><span class="num">77</span><div class="rc-label">Last twelve months</div></div>
    <div class="record-cell"><span class="num">5</span><div class="rc-label">Counties served</div></div>
    <div class="record-cell"><span class="num">38</span><div class="rc-label">Years licensed</div></div>
  </div>
</div></section>

<section class="rule-top"><div class="wrap">
  <div class="head"><span class="label">Recent closings</span><h2>The ledger.</h2>
  <p class="lede">This table reads from the past-sales export at launch &mdash; address, community, sale price, days on market and sale-to-list ratio for every closing.</p></div>
  <div class="ledger-wrap"><table class="ledger">
    <thead><tr><th>Address</th><th>Community</th><th>Sold</th><th>Days</th><th>% of list</th></tr></thead>
    <tbody>
      <tr><td class="addr">Awaiting MLS export</td><td>Tracy</td><td class="money">&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
      <tr><td class="addr">Awaiting MLS export</td><td>Mountain House</td><td class="money">&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
      <tr><td class="addr">Awaiting MLS export</td><td>Tracy Hills</td><td class="money">&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
      <tr><td class="addr">Awaiting MLS export</td><td>River Islands</td><td class="money">&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
      <tr><td class="addr">Awaiting MLS export</td><td>Manteca</td><td class="money">&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
    </tbody>
  </table></div>
  <p class="note">Populate from the existing past-sales archive plus MetroList sold data. Recommended annual callouts: homes sold, average sale-to-list percentage, average days on market.</p>
</div></section>

''' + band("Want your address on this page?",
           "It starts with a free valuation and a show-ready plan. The rest is simply the process.",
           "valuation.html", "Get my valuation"))

# ---------- REVIEWS ----------
page("reviews.html", "Client Reviews &mdash; 5.0 on Zillow | Klemm Real Estate, Tracy",
     "More than two hundred public reviews across Zillow, Yelp and Google for Jack Klemm and Klemm Real Estate.",
     "reviews.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Reviews</span>
  <h1>Thirty-eight years, and the same three words.</h1>
  <p class="lede">Communication. Honesty. Professionalism. They appear in review after review, across every platform, going back further than most agents in this market have been licensed.</p>
</div></section>

<section class="pad-sm"><div class="wrap">
  <div class="record" style="margin-top:0">
    <div class="record-cell"><span class="num">5.0<small>&#9733;</small></span><div class="rc-label">Zillow<br>100+ reviews</div></div>
    <div class="record-cell"><span class="num">4.5<small>&#9733;</small></span><div class="rc-label">Yelp<br>38 reviews</div></div>
    <div class="record-cell"><span class="num">4.8<small>&#9733;</small></span><div class="rc-label">Google<br>90+ reviews</div></div>
    <div class="record-cell"><span class="num">1</span><div class="rc-label">Negative review found<br>in the entire record</div></div>
  </div>
</div></section>

<section class="rule-top"><div class="wrap">
  <div class="pullquote" style="margin-bottom:60px">
    <q>Always available whether by phone, email or text, and answers questions promptly. Very communicative during the whole process.</q>
    <cite>Zillow review &middot; Tracy seller</cite>
  </div>
  ''' + quotes([
        ("Renowned among colleagues and clients alike for his honesty, integrity and professionalism.", "Zillow &middot; Tracy client"),
        ("By far the most professional and resourceful brokerage in Mountain House and Tracy.", "Yelp &middot; Mountain House client"),
        ("Polite, professional, knowledgeable, and patient.", "Client review &middot; Tracy buyer"),
        ("Excellent negotiation skills, whether structuring sales or 1031 exchanges.", "Zillow &middot; Investment seller"),
        ("Our home sold in one weekend.", "Client review &middot; Tracy seller"),
        ("From the first meeting to funds in hand in about nine weeks.", "Client review &middot; Tracy seller"),
     ]) + '''
  <div style="margin-top:52px">''' + slot("Live review feed", "A verified review widget mounts here at launch so this page updates itself and carries live counts from Zillow and Google. Quotes above are excerpts from public reviews &mdash; confirm wording against the live platforms before publishing.") + '''</div>
</div></section>

''' + band("The next one could be yours.", "Buying or selling, it starts with a single conversation.", "contact.html", "Talk to Jack"))

# ---------- ABOUT ----------
page("about.html", "About Jack Klemm &mdash; Broker, Tracy California | Klemm Real Estate",
     "Jack Klemm has sold Tracy real estate since 1988 and founded his independent brokerage in 2008. GRI, CRS, and 25 consecutive Master's Awards.",
     "about.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">About</span>
  <h1>Thirty-eight years. One town. One standard.</h1>
  <p class="lede">The broker who never left &mdash; and the small team that outworks the franchises down the street.</p>
</div></section>

<section><div class="wrap cols">
  <div class="c-5">''' + plate("Plate III &mdash; Jack Klemm, Broker", "p-34", asset="assets/jack-klemm.jpg") + '''</div>
  <div class="c-7 stack gap-3">
    <span class="label">Jack Klemm &middot; Broker and owner</span>
    <h2>The constant in a market that never stopped changing.</h2>
    <p class="lede">Jack Klemm earned his license in 1988, when Tracy was a farm and rail town of thirty-five thousand and the Altamont commute was a curiosity. He has since worked the market through every boom, every crash and every building spree &mdash; nearly four thousand closings worth.</p>
    <p class="lede">In November 2008, at the depth of the housing collapse, when franchises were closing offices and agents were leaving the business, Jack opened his own brokerage on 11th Street. Klemm Real Estate has been downtown ever since.</p>
    <p class="lede">He holds the GRI and CRS designations and has taken the Central Valley Association of REALTORS&reg; Master&rsquo;s Award every year for twenty-five consecutive years.</p>
    <div class="ledger-wrap" style="margin-top:14px"><table class="ledger">
      <tbody>
        <tr><td class="addr">Licensed</td><td>1988 &middot; California Real Estate Broker</td></tr>
        <tr><td class="addr">Brokerage founded</td><td>November 2008 &middot; Klemm Real Estate, Inc.</td></tr>
        <tr><td class="addr">Designations</td><td>GRI &middot; Graduate, REALTOR&reg; Institute</td></tr>
        <tr><td class="addr"></td><td>CRS &middot; Certified Residential Specialist</td></tr>
        <tr><td class="addr">Recognition</td><td>CVAR Master&rsquo;s Award, 25 consecutive years</td></tr>
        <tr><td class="addr">License numbers</td><td>DRE #01004092 (broker) &middot; DRE #01866206 (brokerage)</td></tr>
      </tbody>
    </table></div>
  </div>
</div></section>

<section class="rule-top bg-field"><div class="wrap">
  <div class="head"><span class="label">The team</span><h2>Small on purpose.</h2>
  <p class="lede">Large teams hand you off. Here, the person who lists your home is the person who answers your call.</p></div>
  <div class="cols">
    <div class="c-4">''' + plate("Lisa Boone", "p-1", asset="assets/team-lisa.jpg") + '<div style="margin-top:16px"><h3>Lisa Boone</h3><p class="note">REALTOR&reg; &middot; in the business since 1998. Bio and license number to be added.</p></div>' + '''</div>
    <div class="c-4">''' + plate("Mary Napoli", "p-1", asset="assets/team-mary.jpg") + '<div style="margin-top:16px"><h3>Mary Napoli</h3><p class="note">REALTOR&reg; &middot; bio and license number to be added.</p></div>' + '''</div>
    <div class="c-4">''' + plate("Alex Machuca", "p-1", asset="assets/team-alex.jpg") + '<div style="margin-top:16px"><h3>Alex Machuca</h3><p class="note">REALTOR&reg; &middot; bio and license number to be added.</p></div>' + '''</div>
  </div>
  <div class="cols" style="margin-top:40px">
    <div class="c-4">''' + plate("Erica Hall", "p-1", asset="assets/team-erica.jpg") + '<div style="margin-top:16px"><h3>Erica Hall</h3><p class="note">REALTOR&reg; &middot; DRE #01428918. Bio to be added.</p></div>' + '''</div>
    <div class="c-8 stack gap-3" style="justify-content:center">
      <span class="label">How we work</span>
      ''' + steps([
        ("We listen first", "Every plan starts with your goals, not a script and not a quota."),
        ("We tell you the truth", "About price, about prep, about timing &mdash; including when it is not what you hoped to hear."),
        ("We stay reachable", "Phone, text, email. The most common sentence in our reviews is that we actually answer."),
     ]) + '''
    </div>
  </div>
</div></section>

''' + band("Come say hello.", "672 W 11th Street, Suite 216 &mdash; downtown Tracy, where we have always been.", "contact.html", "Get in touch"))

# ---------- INSIGHTS ----------
page("insights.html", "Market Letters &mdash; Tracy Real Estate Since 2013 | Klemm Real Estate",
     "Jack Klemm's monthly Tracy-area market letter, published continuously since 2013.",
     "record.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Market letters</span>
  <h1>The letter Tracy has read since 2013.</h1>
  <p class="lede">Every month for more than a decade, Jack has written the honest version of what happened in this market: what sold, for how much, and what it means if you own a home here.</p>
</div></section>

<section><div class="wrap">
  ''' + index_rows([
        ("#", "Latest issue", "Month 2026", "Migrate the most recent letter from the existing archive."),
        ("#", "Previous issue", "Month 2026", "Migrate from the existing archive."),
        ("#", "Previous issue", "Month 2026", "Migrate from the existing archive."),
     ]) + '''
  <div style="margin-top:52px">''' + slot("Archive migration", "The monthly archive running from September 2013 to the present moves here with redirects from the old URLs &mdash; more than a hundred and forty issues of local market history. Two additions worth making at launch: a quarterly Tracy market report and a Mountain House equivalent.") + '''</div>
</div></section>

''' + band("Get next month&rsquo;s letter.", "One email a month, the local market told straight. Unsubscribe whenever you like.", "contact.html", "Subscribe"))

# ---------- CONTACT ----------
page("contact.html", "Contact Jack Klemm | Klemm Real Estate, Tracy California",
     "Reach Jack Klemm and the Klemm Real Estate team in downtown Tracy: (209) 321-1094, jack@klemmre.com.",
     "contact.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Contact</span>
  <h1>Talk to a broker, not a call centre.</h1>
  <p class="lede">Phone, text, email, or the door on 11th Street. The single most common compliment in thirty-eight years of reviews is that Jack actually answers.</p>
</div></section>

<section><div class="wrap cols">
  <div class="c-7">
    <form class="form" data-demo>
      <div class="form-grid">
        <div><label for="c-name">Name</label><input type="text" id="c-name" placeholder="Your name"></div>
        <div><label for="c-phone">Phone</label><input type="tel" id="c-phone" placeholder="(209) 555-0123"></div>
        <div class="full"><label for="c-email">Email</label><input type="email" id="c-email" placeholder="you@email.com"></div>
        <div class="full"><label for="c-topic">I am interested in</label><select id="c-topic"><option>Selling my home</option><option>Buying a home</option><option>Both &mdash; selling and buying</option><option>Investment property or 1031 exchange</option><option>Something else</option></select></div>
        <div class="full"><label for="c-msg">Message</label><textarea id="c-msg" rows="4" placeholder="How can we help?"></textarea></div>
      </div>
      <div class="btn-row" style="margin-top:24px"><button class="btn btn-gold" type="submit">Send message <span>&rarr;</span></button></div>
      <div class="ok">Demo mode &mdash; connect this form to the CRM before launch.</div>
    </form>
  </div>
  <div class="c-5 stack gap-3">
    <span class="label">The office</span>
    <div class="ledger-wrap"><table class="ledger">
      <tbody>
        <tr><td class="addr">Address</td><td>672 W 11th Street, Suite 216<br>Tracy, California 95376</td></tr>
        <tr><td class="addr">Phone</td><td class="money"><a href="tel:''' + TEL + '''" style="text-decoration:none">''' + PHONE + '''</a></td></tr>
        <tr><td class="addr">Email</td><td><a href="mailto:''' + EMAIL + '''" style="text-decoration:none">''' + EMAIL + '''</a></td></tr>
        <tr><td class="addr">Broker</td><td>Jack Klemm &middot; DRE #01004092</td></tr>
        <tr><td class="addr">Brokerage</td><td>Klemm Real Estate, Inc. &middot; DRE #01866206</td></tr>
      </tbody>
    </table></div>
    ''' + plate("Map &mdash; 672 W 11th Street", "p-43", note="Embed at launch", asset="google-map-embed") + '''
  </div>
</div></section>
''')

# ---------- COMMUNITIES ----------
page("communities.html", "Communities &mdash; Tracy, Mountain House, Lathrop &amp; Manteca | Klemm Real Estate",
     "Community guides for Tracy, Tracy Hills, Mountain House, River Islands and Manteca from a broker who has sold in every one since 1988.",
     "communities.html",
     '''
<section class="pagehead"><div class="wrap">
  <span class="label">Communities</span>
  <h1>Know the neighborhoods like a local.</h1>
  <p class="lede">Jack has sold homes in each of these markets since before some of them had stoplights &mdash; and in one case, before the city existed at all.</p>
</div></section>

<section><div class="wrap">''' + index_rows(COMMUNITY_ROWS) + '''
  <div style="margin-top:44px"><a class="arrow-link" href="bay-area.html">Coming from the Bay Area? Start here <span>&rarr;</span></a></div>
</div></section>

''' + band("Not sure which one fits?",
           "Tell Jack your commute, your budget and your must-haves. He will tell you where you will actually be happy &mdash; even if it costs him the listing.",
           "contact.html", "Ask Jack"))


def community(slug, name, title_line, lede, stats, body_head, paras, todo, plate_cap, asset, redirect=None):
    stat_cells = ''.join(
        '<div class="record-cell"><span class="num">%s</span><div class="rc-label">%s</div></div>' % (v, l)
        for v, l in stats)
    para_html = ''.join('<p class="lede">%s</p>' % p for p in paras)
    redirect_note = (' <br>%s should redirect here once the domains are consolidated.' % redirect) if redirect else ''
    page(slug, "%s Real Estate &amp; Homes for Sale | Klemm Real Estate" % name,
         "Homes for sale in %s plus the local guide from Klemm Real Estate, an independent Tracy brokerage since 1988." % name,
         "communities.html",
         '''
<section class="pagehead"><div class="wrap">
  <span class="label">Community guide</span>
  <h1>%s</h1>
  <p class="lede">%s</p>
</div></section>

<section class="pad-sm"><div class="wrap"><div class="record" style="margin-top:0">%s</div></div></section>

<section class="rule-top"><div class="wrap cols">
  <div class="c-7 stack gap-3">
    <span class="label">The local read</span>
    <h2>%s</h2>
    %s
    <p class="note">%s</p>
  </div>
  <div class="c-5">%s</div>
</div></section>

<section class="rule-top"><div class="wrap">%s</div></section>

%s''' % (title_line, lede, stat_cells, body_head, para_html, todo,
         plate(plate_cap, "p-43", asset=asset),
         slot("Live %s listings" % name,
              "The IDX embed filtered to %s mounts here at launch.%s" % (name, redirect_note)),
         band("Buying or selling in %s?" % name,
              "Start with the broker whose name has been on sold signs here for thirty-eight years.",
              "contact.html", "Talk to Jack")))


community("community-tracy.html", "Tracy", "Tracy, California",
    "The Central Valley&rsquo;s front door to the Bay Area &mdash; a working downtown, an ACE station, and the most house your money buys within an hour of the Tri-Valley.",
    [("$673K", "Median sale price"), ("~31", "Days to pending"), ("~100K", "Residents"), ("1988", "Jack selling here since")],
    "A town first, a suburb second.",
    ["Tracy is not a subdivision pretending to be a town &mdash; it was a farm and rail town long before the commuters arrived. There is a real downtown on 10th and 11th Streets, Jack&rsquo;s office among them, and established neighborhoods with mature trees that no master plan can manufacture.",
     "Buyers here fall into two camps: Bay Area commuters trading equity for square footage, and Valley families moving up. Knowing which one is on the other side of your negotiation is half the outcome &mdash; and after nearly four thousand local closings, Jack usually knows the other agent too."],
    "To add: neighborhood-by-neighborhood notes for Redbridge, Edgewood, Central Tracy, Souza Estates and Hidden Lakes.",
    "Plate &mdash; Downtown Tracy, 11th Street", "assets/community-tracy.jpg")

community("community-mountain-house.html", "Mountain House", "Mountain House, California",
    "California&rsquo;s newest city and one of its fastest-growing. First exit after the Altamont, top-rated schools, and a village plan that genuinely works.",
    [("$963K", "Median sale price"), ("+5.6%", "Population growth, one year"), ("~30,700", "Residents"), ("2024", "Incorporated as a city")],
    "The shortest commute in the Valley &mdash; priced accordingly.",
    ["Mountain House sits at the foot of the Altamont: the closest San Joaquin address to the Bay Area, and the market prices that fact honestly. You pay roughly $290,000 over Tracy at the median for newer housing stock, K-8 village schools and that first-exit drive.",
     "The nuance right now is the split between resale and new construction. Resale homes are seeing price cuts while builders keep pulling buyers with incentives. If you are selling a resale here, pricing against the model home down the street is the entire strategy &mdash; and Jack has negotiated both sides of it."],
    "To add: village-by-village notes for Altamont, Bethany, Cordes, Hansen, Questa and Wicklund.",
    "Plate &mdash; Mountain House village street", "assets/community-mountain-house.jpg",
    redirect="mountainhousere.com")

community("community-tracy-hills.html", "Tracy Hills", "Tracy Hills",
    "The master-planned southern edge of Tracy &mdash; new construction, hillside parks and direct I-580 access. A different market with different rules.",
    [("New", "Construction-led market"), ("~112", "Days on market"), ("I-580", "Direct corridor access"), ("K-8", "Schools in plan")],
    "Where patience is a negotiating position.",
    ["Tracy Hills is the newest large-scale growth in the city, and because builder inventory competes directly with early resales, homes here sit considerably longer than the citywide average. For buyers that is leverage: incentives, rate buydowns and price flexibility that simply do not exist downtown.",
     "For sellers it means positioning against the model home rather than the neighbours. Jack&rsquo;s advice differs by street and by phase &mdash; the benefit of having watched every Tracy master plan mature since 1988."],
    "To add: current builder lineup, active phases, and HOA and Mello-Roos notes.",
    "Plate &mdash; Tracy Hills, southern edge", "assets/community-tracy-hills.jpg")

community("community-river-islands.html", "River Islands &amp; Lathrop", "River Islands &amp; Lathrop",
    "A waterfront master plan on the San Joaquin with its own lakes, trails and charter schools &mdash; plus the established Lathrop neighborhoods around it.",
    [("Lakes", "Built-in waterfront"), ("Charter", "STEAM schools in plan"), ("ACE", "Lathrop station access"), ("New", "Construction ongoing")],
    "The master plan buyers ask for by name.",
    ["River Islands is not another subdivision &mdash; it is a purpose-built lake town, and buyers increasingly arrive asking for it by name. Its charter schools and waterfront lots create pricing dynamics that do not track the rest of Lathrop, which is exactly why the comparables need local hands.",
     "Jack has handled River Islands and Lathrop closings through every phase of the build-out, including relocation purchases and investment buys keyed to the ACE station."],
    "To add: current phase and builder information, lake-lot premiums, and school enrollment detail.",
    "Plate &mdash; River Islands, San Joaquin waterfront", "assets/community-river-islands.jpg",
    redirect="lathropre.com")

community("community-manteca.html", "Manteca", "Manteca, California",
    "Family-first value where the 120 meets the 99 &mdash; established neighborhoods, steady new construction, and the most attainable family homes in the region.",
    [("$600Ks", "Typical family home"), ("120/99", "Corridor crossroads"), ("Growing", "Retail and amenities"), ("Value", "Most square feet per dollar")],
    "The value play with staying power.",
    ["Manteca is where budgets breathe. Buyers priced out of Tracy or Mountain House find newer square footage here for meaningfully less, with the 120 corridor&rsquo;s retail growth filling in around them.",
     "It is also a strong move-up and investment market, which is why Jack&rsquo;s Manteca work spans first homes through 1031 exchanges."],
    "To add: neighborhood notes for Union Ranch, Del Webb at Woodbridge, downtown Manteca and the new 120-corridor communities.",
    "Plate &mdash; Manteca, 120 corridor", "assets/community-manteca.jpg",
    redirect="mantecare.com")

# ----------------------------------------------------------------- emit

def build():
    for p in PAGES:
        doc = HEAD.format(title=p["title"], desc=p["desc"]) + masthead(p["nav"]) + p["body"] + FOOT
        with open(os.path.join(ROOT, p["slug"]), "w") as f:
            f.write(doc)
    print("Built %d pages" % len(PAGES))
    return [p["slug"] for p in PAGES]


if __name__ == "__main__":
    build()

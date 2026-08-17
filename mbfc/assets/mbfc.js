/* ==========================================================================
   My Best Friend's Closet — Tracy, CA · redesign concept
   Shared behaviour: mobile nav, live-sale countdown, catalog + filters.

   The catalog below is sample data standing in for the real inventory feed.
   Every item declares `origin` ("new" | "consigned") — that field is what
   drives the tag on the card, and it is the whole point of the rebuild.
   ========================================================================== */

(function () {
  'use strict';

  /* ---------- mobile nav ------------------------------------------------ */

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  /* ---------- live sale schedule ---------------------------------------- */
  /* Wed 4:00pm · Thu 6:00pm · Sat 9:00am, Pacific. Shown on the site rather
     than only inside the app — the shop already does the hard part three
     times a week and gets no website value from it. */

  var SHOWS = [
    { day: 3, hour: 16, min: 0, label: 'Wednesday', time: '4:00 pm' },
    { day: 4, hour: 18, min: 0, label: 'Thursday',  time: '6:00 pm' },
    { day: 6, hour: 9,  min: 0, label: 'Saturday',  time: '9:00 am' }
  ];

  function nextShowIndex(now) {
    var best = -1, bestDelta = Infinity;
    for (var i = 0; i < SHOWS.length; i++) {
      var s = SHOWS[i];
      var delta = (s.day - now.getDay() + 7) % 7;
      var d = new Date(now);
      d.setDate(now.getDate() + delta);
      d.setHours(s.hour, s.min, 0, 0);
      if (d <= now) { d.setDate(d.getDate() + 7); }
      var ms = d - now;
      if (ms < bestDelta) { bestDelta = ms; best = i; }
    }
    return { index: best, ms: bestDelta };
  }

  function renderCountdown() {
    var slots = document.querySelectorAll('.live-slot');
    var out = document.querySelector('[data-countdown]');
    if (!slots.length && !out) return;

    var next = nextShowIndex(new Date());

    slots.forEach(function (el, i) {
      el.classList.toggle('next', i === next.index);
      var cd = el.querySelector('.countdown');
      if (cd) { cd.textContent = i === next.index ? 'Up next' : ''; }
    });

    if (out) {
      var total = Math.floor(next.ms / 1000);
      var h = Math.floor(total / 3600);
      var m = Math.floor((total % 3600) / 60);
      var s = total % 60;
      var d = Math.floor(h / 24);
      out.textContent = d > 0
        ? d + 'd ' + (h % 24) + 'h ' + m + 'm'
        : String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
      var lbl = document.querySelector('[data-next-show]');
      if (lbl) {
        lbl.textContent = SHOWS[next.index].label + ' at ' + SHOWS[next.index].time;
      }
    }
  }

  renderCountdown();
  if (document.querySelector('[data-countdown]')) {
    setInterval(renderCountdown, 1000);
  }

  /* ---------- catalog ---------------------------------------------------- */
  /* Brands drawn from the shop's own published accept-list. Sample only. */

  var CATALOG = [
    { id: 'lv-neverfull', brand: 'Louis Vuitton', name: 'Neverfull MM tote, monogram canvas',
      cat: 'bags', origin: 'consigned', cond: 'Very Good', size: 'OS', price: 1180, was: null, sold: false,
      slot: 'Monogram tote, 3:4 · front of bag on bone ground' },
    { id: 'chanel-tweed', brand: 'Chanel', name: 'Tweed jacket with braided trim',
      cat: 'outerwear', origin: 'consigned', cond: 'Excellent', size: '6', price: 2450, was: null, sold: false,
      slot: 'Tweed jacket, 3:4 · on form, front' },
    { id: 'gucci-loafer', brand: 'Gucci', name: 'Horsebit leather loafer',
      cat: 'shoes', origin: 'consigned', cond: 'Very Good', size: '8', price: 385, was: 445, sold: false,
      slot: 'Loafer pair, 3:4 · three-quarter angle' },
    { id: 'fp-midi', brand: 'Free People', name: 'Tiered cotton midi dress',
      cat: 'dresses', origin: 'new', cond: null, size: 'M', price: 128, was: null, sold: false,
      slot: 'Midi dress, 3:4 · on model or form' },
    { id: 'sadie-blouse', brand: 'Sadie & Sage', name: 'Puff-sleeve satin blouse',
      cat: 'tops', origin: 'new', cond: null, size: 'S', price: 62, was: null, sold: false,
      slot: 'Satin blouse, 3:4 · flat lay or form' },
    { id: 'lulu-align', brand: 'Lululemon', name: 'Align high-rise legging, 25"',
      cat: 'active', origin: 'consigned', cond: 'Excellent', size: '4', price: 48, was: null, sold: false,
      slot: 'Leggings, 3:4 · folded flat lay' },
    { id: 'alo-set', brand: 'Alo Yoga', name: 'Ribbed two-piece set',
      cat: 'active', origin: 'new', cond: null, size: 'M', price: 148, was: null, sold: false,
      slot: 'Two-piece set, 3:4 · flat lay' },
    { id: 'zara-blazer', brand: 'Zara', name: 'Oversized wool-blend blazer',
      cat: 'outerwear', origin: 'consigned', cond: 'Excellent', size: 'M', price: 46, was: 58, sold: false,
      slot: 'Blazer, 3:4 · on form, front' },
    { id: 'br-trouser', brand: 'Banana Republic', name: 'Sloan straight-leg trouser',
      cat: 'bottoms', origin: 'consigned', cond: 'Very Good', size: '8', price: 34, was: null, sold: false,
      slot: 'Trousers, 3:4 · folded flat lay' },
    { id: 'bila-knit', brand: 'Bila77', name: 'Waffle-knit cardigan',
      cat: 'tops', origin: 'new', cond: null, size: 'L', price: 74, was: null, sold: false,
      slot: 'Cardigan, 3:4 · flat lay' },
    { id: 'gown-navy', brand: 'Adrianna Papell', name: 'Beaded navy evening gown',
      cat: 'formal', origin: 'consigned', cond: 'Excellent', size: '10', price: 168, was: null, sold: false,
      slot: 'Evening gown, 3:4 · full length on form' },
    { id: 'coach-cross', brand: 'Coach', name: 'Pebbled leather crossbody',
      cat: 'bags', origin: 'consigned', cond: 'Good', size: 'OS', price: 88, was: 112, sold: false,
      slot: 'Crossbody bag, 3:4 · front with strap' },
    { id: 'tory-flat', brand: 'Tory Burch', name: 'Minnie travel ballet flat',
      cat: 'shoes', origin: 'consigned', cond: 'Very Good', size: '7.5', price: 96, was: null, sold: false,
      slot: 'Ballet flats, 3:4 · pair angled' },
    { id: 'fp-denim', brand: 'Free People', name: 'High-rise wide-leg denim',
      cat: 'bottoms', origin: 'new', cond: null, size: '27', price: 118, was: null, sold: false,
      slot: 'Denim, 3:4 · flat lay full length' },
    { id: 'kids-set', brand: 'Janie and Jack', name: 'Corduroy pinafore set, 4T',
      cat: 'kids', origin: 'consigned', cond: 'Excellent', size: '4T', price: 24, was: null, sold: false,
      slot: 'Kids pinafore, 3:4 · flat lay' },
    { id: 'kids-coat', brand: 'Hanna Andersson', name: 'Quilted puffer coat, size 6',
      cat: 'kids', origin: 'consigned', cond: 'Very Good', size: '6', price: 28, was: null, sold: false,
      slot: 'Kids puffer, 3:4 · flat lay' },
    { id: 'prada-bag', brand: 'Prada', name: 'Re-Edition nylon shoulder bag',
      cat: 'bags', origin: 'consigned', cond: 'Excellent', size: 'OS', price: 745, was: null, sold: true,
      slot: 'Nylon shoulder bag, 3:4 · front' },
    { id: 'dvf-wrap', brand: 'Diane von Furstenberg', name: 'Silk jersey wrap dress',
      cat: 'dresses', origin: 'consigned', cond: 'Very Good', size: '6', price: 132, was: null, sold: true,
      slot: 'Wrap dress, 3:4 · on form' }
  ];

  var CATS = [
    ['all', 'Everything'], ['dresses', 'Dresses'], ['tops', 'Tops'], ['bottoms', 'Bottoms'],
    ['outerwear', 'Outerwear'], ['shoes', 'Shoes'], ['bags', 'Bags'],
    ['active', 'Activewear'], ['formal', 'Formal'], ['kids', 'Kids']
  ];

  var state = { cat: 'all', origin: 'all', size: 'all', sold: false };

  function money(n) { return '$' + n.toLocaleString('en-US'); }

  function cardHTML(p) {
    var tag = p.origin === 'new'
      ? '<span class="tag tag-new">New</span>'
      : '<span class="tag tag-consigned">Consigned</span>';
    var price = p.was
      ? '<s>' + money(p.was) + '</s>' + money(p.price)
      : money(p.price);
    return '' +
      '<a class="card' + (p.sold ? ' sold' : '') + '" href="product.html?item=' + p.id + '">' +
        '<div class="card-media">' + tag +
          '<div class="ph portrait" data-slot="' + p.slot + '"></div>' +
        '</div>' +
        '<div class="card-body">' +
          '<span class="card-brand">' + p.brand + '</span>' +
          '<h3 class="card-name">' + p.name + '</h3>' +
          (p.cond ? '<span class="card-cond">' + p.cond + '</span>' : '') +
          '<div class="card-meta">' +
            '<span class="card-price">' + price + '</span>' +
            '<span class="card-size">Size ' + p.size + '</span>' +
          '</div>' +
        '</div>' +
      '</a>';
  }

  function matches(p) {
    if (state.cat !== 'all' && p.cat !== state.cat) return false;
    if (state.origin !== 'all' && p.origin !== state.origin) return false;
    if (!state.sold && p.sold) return false;
    return true;
  }

  function render() {
    var rack = document.getElementById('rack');
    if (!rack) return;
    var items = CATALOG.filter(matches);
    var limit = Number(rack.getAttribute('data-limit')) || 0;
    if (limit > 0) { items = items.slice(0, limit); }
    rack.innerHTML = items.length
      ? items.map(cardHTML).join('')
      : '<div class="empty"><p>Nothing on the rack for that</p>' +
        '<small>New pieces land every day the shop is open. Try a wider filter, ' +
        'or come to a live sale &mdash; that is where the best of it goes first.</small></div>';
    var count = document.querySelector('.filter-count');
    if (count) {
      count.textContent = items.length + (items.length === 1 ? ' piece' : ' pieces');
    }
  }

  function bindChips() {
    document.querySelectorAll('[data-filter]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-filter');
        var val = btn.getAttribute('data-value');
        if (key === 'sold') {
          state.sold = !state.sold;
          btn.setAttribute('aria-pressed', state.sold ? 'true' : 'false');
        } else {
          state[key] = val;
          document.querySelectorAll('[data-filter="' + key + '"]').forEach(function (b) {
            b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
          });
        }
        render();
      });
    });
  }

  function buildCatChips() {
    var host = document.getElementById('cat-chips');
    if (!host) return;
    host.innerHTML = CATS.map(function (c) {
      return '<button class="chip" type="button" data-filter="cat" data-value="' + c[0] +
        '" aria-pressed="' + (c[0] === 'all' ? 'true' : 'false') + '">' + c[1] + '</button>';
    }).join('');
  }

  buildCatChips();
  bindChips();
  render();

  /* ---------- product detail -------------------------------------------- */

  var detail = document.getElementById('product-detail');
  if (detail) {
    var wanted = new URLSearchParams(location.search).get('item');
    var p = CATALOG.filter(function (x) { return x.id === wanted; })[0] || CATALOG[0];

    document.title = p.brand + ' ' + p.name + ' — My Best Friend’s Closet';

    var isNew = p.origin === 'new';
    detail.innerHTML = '' +
      '<div class="pd-media">' +
        '<div class="ph portrait" data-slot="' + p.slot + '"></div>' +
        '<div class="pd-thumbs">' +
          '<div class="ph square" data-slot="Detail: fabric / hardware"></div>' +
          '<div class="ph square" data-slot="Detail: label &amp; size tag"></div>' +
          '<div class="ph square" data-slot="Detail: any flaw, close up"></div>' +
        '</div>' +
      '</div>' +
      '<div class="pd-info">' +
        (isNew
          ? '<span class="tag tag-new">New &middot; never worn</span>'
          : '<span class="tag tag-consigned">Consigned &middot; ' + p.cond + '</span>') +
        '<p class="card-brand" style="margin:18px 0 6px">' + p.brand + '</p>' +
        '<h1 class="display" style="font-size:clamp(1.8rem,3.4vw,2.6rem)">' + p.name + '</h1>' +
        '<p class="pd-price">' + (p.was ? '<s>' + money(p.was) + '</s> ' : '') + money(p.price) + '</p>' +
        '<dl class="pd-specs">' +
          '<div><dt>Size</dt><dd>' + p.size + '</dd></div>' +
          '<div><dt>Condition</dt><dd>' + (isNew ? 'New with tags' : p.cond) + '</dd></div>' +
          '<div><dt>Quantity</dt><dd>One &mdash; there is only this</dd></div>' +
        '</dl>' +
        (p.sold
          ? '<p class="pd-sold">This one has sold.</p><a class="btn ghost" href="shop.html">See what is on the rack now <span class="arw">&rarr;</span></a>'
          : '<button class="btn brass" type="button">Add to bag <span class="arw">&rarr;</span></button>') +
        '<div class="pd-note">' +
          (isNew
            ? '<p><strong>This is new stock.</strong> Bought wholesale, never worn, tags attached. ' +
              'About half our floor is new like this &mdash; the other half is designer resale.</p>'
            : '<p><strong>This came from a neighbor’s closet.</strong> Graded <em>' + p.cond +
              '</em> against <a href="conditions.html">our condition chart</a>, photographed as it actually is, ' +
              'flaws and all. One of one &mdash; when it goes, it is gone.</p>') +
        '</div>' +
        '<div class="pd-ship"><span>Free shipping over $150</span><span>Or collect at 53 W 10th St</span></div>' +
      '</div>';
  }

  /* ---------- payout calculator (consign page) --------------------------- */

  var calc = document.getElementById('calc-price');
  if (calc) {
    var outs = {
      ticket: document.getElementById('out-ticket'),
      week: document.getElementById('out-week'),
      yours: document.getElementById('out-yours')
    };
    var weekSel = document.getElementById('calc-week');

    function recalc() {
      var listed = Math.max(1, Number(calc.value) || 0);
      var week = Number(weekSel.value);
      var mult = week >= 9 ? 0.6 : (week >= 5 ? 0.8 : 1);
      var sale = Math.round(listed * mult);
      outs.ticket.textContent = money(listed);
      outs.week.textContent = money(sale) + (mult < 1 ? '  (−' + Math.round((1 - mult) * 100) + '%)' : '');
      outs.yours.textContent = money(Math.round(sale * 0.4));
    }
    calc.addEventListener('input', recalc);
    weekSel.addEventListener('change', recalc);
    recalc();
  }

})();

// Klemm Real Estate — shared site behavior
(function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
  }

  // Demo form handling — replace with Formspree/CRM endpoint before launch.
  document.querySelectorAll('form[data-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = form.querySelector('.form-success');
      if (ok) {
        ok.style.display = 'block';
        ok.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      form.reset();
    });
  });
})();

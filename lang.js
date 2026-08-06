(function () {
  function closeAll(except) {
    document.querySelectorAll('.lang.open').forEach(function (el) {
      if (el === except) return;
      el.classList.remove('open');
      var b = el.querySelector('.lang-btn');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.lang-btn');
    if (btn) {
      e.preventDefault();
      var lang = btn.closest('.lang');
      closeAll(lang);
      var open = lang.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    } else {
      closeAll(null);
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAll(null);
  });
})();

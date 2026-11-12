// Category filter for the case study list (mirrors the live Elementor taxonomy filter).
const grid = document.querySelector('[data-cs-grid]');
if (grid) {
  const buttons = [...document.querySelectorAll('.cs-filter')];
  const cards = [...grid.querySelectorAll('.cs-card')];
  const empty = document.querySelector('.cs-empty');
  const apply = filter => {
    let shown = 0;
    cards.forEach(card => {
      const match = filter === 'all' || card.dataset.categories.split(' ').includes(filter);
      card.hidden = !match;
      if (match) shown += 1;
    });
    buttons.forEach(button => {
      const active = button.dataset.filter === filter;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    if (empty) empty.hidden = shown > 0;
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    apply(button.dataset.filter);
    try { history.replaceState(null, '', button.dataset.filter === 'all' ? location.pathname : `#${button.dataset.filter}`); } catch (error) { /* ignore */ }
  }));
  const initial = location.hash.slice(1);
  if (buttons.some(button => button.dataset.filter === initial)) apply(initial);
}

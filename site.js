(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-navigation');
  if (menu && nav) {
    document.documentElement.classList.add('has-js');
    menu.hidden = false;
    function closeMenu() { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); }
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); }
    });
  }
  const filters = document.querySelector('.project-filters');
  if (!filters) return;
  const buttons = [...filters.querySelectorAll('[data-theme]')];
  const cards = [...document.querySelectorAll('[data-project]')];
  const counter = document.querySelector('#project-count');
  filters.hidden = false;
  function applyTheme(theme, updateURL = false) {
    const selected = buttons.find(button => button.dataset.theme === theme) || buttons[0];
    theme = selected.dataset.theme;
    let count = 0;
    cards.forEach(card => {
      const visible = theme === 'all' || card.dataset.themes.split(' ').includes(theme);
      card.hidden = !visible;
      if (visible) count++;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button === selected)));
    const label = selected.childNodes[0].textContent.trim();
    counter.textContent = theme === 'all' ? `Showing all ${count} projects` : `${count} ${count === 1 ? 'project' : 'projects'} in ${label}`;
    document.querySelector('#no-projects').hidden = count !== 0;
    if (updateURL) {
      const url = new URL(window.location.href);
      if (theme === 'all') url.searchParams.delete('theme');
      else url.searchParams.set('theme', theme);
      history.pushState({}, '', url);
    }
  }
  buttons.forEach(button => button.addEventListener('click', () => applyTheme(button.dataset.theme, true)));
  const fromURL = () => applyTheme(new URL(window.location.href).searchParams.get('theme') || 'all');
  window.addEventListener('popstate', fromURL);
  fromURL();
})();

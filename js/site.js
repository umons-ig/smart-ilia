(() => {
  const nav = document.getElementById('navbar');
  const button = document.getElementById('burger');
  const links = document.getElementById('navLinks');
  const setOpen = (open) => {
    links.classList.toggle('open', open);
    button.classList.toggle('open', open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  if (nav) {
    const update = () => nav.classList.toggle('scrolled', window.scrollY > 10);
    window.addEventListener('scroll', update, { passive: true }); update();
  }
  if (button && links) {
    button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
    links.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { setOpen(false); button.focus(); }
    });
    document.addEventListener('click', event => {
      if (!nav.contains(event.target) && button.getAttribute('aria-expanded') === 'true') setOpen(false);
    });
    window.matchMedia('(min-width: 769px)').addEventListener('change', event => { if (event.matches) setOpen(false); });
  }
  const tabs = [...document.querySelectorAll('[data-lens]')];
  const activate = (tab, focus = false) => {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected)); item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
    if (focus) tab.focus();
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); activate(tabs[next], true); }
    });
  });
})();

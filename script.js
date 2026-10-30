const links = [...document.querySelectorAll('.tab-link')];
const panels = [...document.querySelectorAll('[data-panel]')];

function selectTab(tab) {
  const selected = panels.some(panel => panel.dataset.panel === tab) ? tab : 'caratula';
  panels.forEach(panel => { panel.hidden = panel.dataset.panel !== selected; });
  links.forEach(link => link.classList.toggle('active', link.dataset.tab === selected));
  window.scrollTo({ top: 0, behavior: 'auto' });
}

links.forEach(link => link.addEventListener('click', event => {
  event.preventDefault();
  history.replaceState(null, '', `#${link.dataset.tab}`);
  selectTab(link.dataset.tab);
}));

selectTab(location.hash.slice(1));

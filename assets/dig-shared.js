const digHeader = document.querySelector('#dig-header');
if (digHeader) {
  const menuToggle = digHeader.querySelector('.dig-menu-toggle');
  const menu = digHeader.querySelector('#dig-primary-nav');
  const groups = [...menu.querySelectorAll('.dig-nav-group')];
  const mobile = window.matchMedia('(max-width: 1100px)');
  const setGroupOpen = (group, open) => {
    group.classList.toggle('is-open', open);
    group.querySelector('.dig-submenu-toggle').setAttribute('aria-expanded', String(open));
  };
  const closeGroups = (except = null) => groups.forEach(group => {
    if (group !== except) setGroupOpen(group, false);
  });
  const setMenuOpen = open => {
    menu.classList.toggle('is-open', open);
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (!open) closeGroups();
  };
  menuToggle.addEventListener('click', () => setMenuOpen(!menu.classList.contains('is-open')));
  groups.forEach(group => {
    const toggle = group.querySelector('.dig-submenu-toggle');
    const categories = [...group.querySelectorAll('.dig-menu-category')];
    const selectCategory = selected => categories.forEach(category => {
      const active = category === selected;
      category.classList.toggle('is-active', active);
      category.querySelector('.dig-category-toggle').setAttribute('aria-expanded', String(active));
      category.querySelector('.dig-menu-panel').hidden = !active;
    });
    const resetCategories = () => selectCategory(mobile.matches ? null : categories[0]);
    resetCategories();
    mobile.addEventListener('change', resetCategories);
    toggle.addEventListener('click', () => {
      const open = !group.classList.contains('is-open');
      closeGroups(group);
      setGroupOpen(group, open);
    });
    toggle.addEventListener('keydown', event => {
      if (event.key !== 'ArrowDown') return;
      event.preventDefault();
      closeGroups(group);
      setGroupOpen(group, true);
      (categories[0]?.querySelector('button') || group.querySelector('.dig-submenu a'))?.focus();
    });
    group.addEventListener('pointerenter', event => {
      if (mobile.matches || event.pointerType !== 'mouse') return;
      closeGroups(group);
      setGroupOpen(group, true);
    });
    group.addEventListener('pointerleave', () => {
      if (!mobile.matches && !group.contains(document.activeElement)) setGroupOpen(group, false);
    });
    group.addEventListener('focusout', event => {
      if (!group.contains(event.relatedTarget)) setGroupOpen(group, false);
    });
    categories.forEach((category, index) => {
      const button = category.querySelector('.dig-category-toggle');
      button.addEventListener('click', () => selectCategory(mobile.matches && category.classList.contains('is-active') ? null : category));
      button.addEventListener('pointerenter', event => {
        if (!mobile.matches && event.pointerType === 'mouse') selectCategory(category);
      });
      button.addEventListener('focus', () => {
        if (!mobile.matches) selectCategory(category);
      });
      button.addEventListener('keydown', event => {
        if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
          event.preventDefault();
          const next = (index + (event.key === 'ArrowDown' ? 1 : -1) + categories.length) % categories.length;
          categories[next].querySelector('button').focus();
        } else if (event.key === 'ArrowRight') {
          event.preventDefault();
          selectCategory(category);
          category.querySelector('.dig-menu-panel a')?.focus();
        }
      });
      category.querySelector('.dig-menu-panel').addEventListener('keydown', event => {
        if (event.key === 'ArrowLeft') {
          event.preventDefault();
          button.focus();
        }
      });
    });
  });
  menu.addEventListener('click', event => {
    if (event.target.closest('a') && mobile.matches) setMenuOpen(false);
  });
  document.addEventListener('click', event => {
    if (!digHeader.contains(event.target)) setMenuOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const group = document.activeElement.closest?.('.dig-nav-group');
    const wasOpen = menu.classList.contains('is-open');
    const groupWasOpen = group?.classList.contains('is-open');
    setMenuOpen(false);
    if (mobile.matches && wasOpen) menuToggle.focus();
    else if (groupWasOpen) group.querySelector('.dig-submenu-toggle').focus();
  });
  mobile.addEventListener('change', () => setMenuOpen(false));
}

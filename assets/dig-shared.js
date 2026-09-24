const digHeader = document.querySelector("#dig-header");

if (digHeader) {
  const menuToggle = digHeader.querySelector(".dig-menu-toggle");
  const menu = digHeader.querySelector("#dig-primary-nav");
  const groups = [...digHeader.querySelectorAll(".dig-nav-group")];

  const closeGroups = (except = null) => {
    groups.forEach((group) => {
      if (group === except) return;
      group.classList.remove("is-open");
      group.querySelector(".dig-submenu-toggle").setAttribute("aria-expanded", "false");
    });
  };

  const setMenuOpen = (open) => {
    menu.classList.toggle("is-open", open);
    menuToggle.setAttribute("aria-expanded", String(open));
    menuToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (!open) closeGroups();
  };

  menuToggle.addEventListener("click", () => {
    setMenuOpen(menuToggle.getAttribute("aria-expanded") !== "true");
  });

  groups.forEach((group) => {
    const button = group.querySelector(".dig-submenu-toggle");
    button.addEventListener("click", () => {
      const open = !group.classList.contains("is-open");
      closeGroups(group);
      group.classList.toggle("is-open", open);
      button.setAttribute("aria-expanded", String(open));
    });
  });

  menu.addEventListener("click", (event) => {
    if (event.target.closest("a") && window.matchMedia("(max-width: 1100px)").matches) {
      setMenuOpen(false);
    }
  });

  document.addEventListener("click", (event) => {
    if (!digHeader.contains(event.target)) {
      setMenuOpen(false);
      closeGroups();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      const wasOpen = menu.classList.contains("is-open");
      setMenuOpen(false);
      closeGroups();
      if (wasOpen) menuToggle.focus();
    }
  });

  window.addEventListener("resize", () => {
    if (!window.matchMedia("(max-width: 1100px)").matches) setMenuOpen(false);
  });
}

(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  var desktopNav = window.matchMedia("(min-width: 980px)");

  function setSubmenuOpen(item, open) {
    var btn = item.querySelector(".submenu-toggle");
    item.classList.toggle("is-open", open);
    if (btn) btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function closeAllSubmenus() {
    document.querySelectorAll(".has-submenu.is-open").forEach(function (item) {
      setSubmenuOpen(item, false);
    });
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      if (!open) closeAllSubmenus();
    });
  }

  document.querySelectorAll(".has-submenu").forEach(function (item) {
    var btn = item.querySelector(".submenu-toggle");
    if (!btn) return;

    btn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      setSubmenuOpen(item, !item.classList.contains("is-open"));
    });

    item.addEventListener("mouseenter", function () {
      if (desktopNav.matches) setSubmenuOpen(item, true);
    });
    item.addEventListener("mouseleave", function () {
      if (desktopNav.matches) setSubmenuOpen(item, false);
    });
    item.addEventListener("focusin", function () {
      if (desktopNav.matches) setSubmenuOpen(item, true);
    });
    item.addEventListener("focusout", function (event) {
      if (desktopNav.matches && !item.contains(event.relatedTarget)) {
        setSubmenuOpen(item, false);
      }
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    closeAllSubmenus();
    if (nav && toggle && nav.classList.contains("is-open")) {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Ouvrir le menu");
      toggle.focus();
    }
  });

  var lightbox = document.querySelector("[data-lightbox]");
  var lightboxImg = lightbox ? lightbox.querySelector("img") : null;
  document.querySelectorAll("[data-gallery] a").forEach(function (link) {
    link.addEventListener("click", function (event) {
      if (!lightbox || !lightboxImg) return;
      event.preventDefault();
      lightboxImg.src = link.getAttribute("href");
      lightboxImg.alt = link.querySelector("img") ? link.querySelector("img").alt : "";
      lightbox.classList.add("is-on");
      lightbox.setAttribute("aria-hidden", "false");
    });
  });
  if (lightbox) {
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox || event.target.closest("[data-close-lightbox]")) {
        lightbox.classList.remove("is-on");
        lightbox.setAttribute("aria-hidden", "true");
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        lightbox.classList.remove("is-on");
      }
    });
  }

  var form = document.getElementById("devis-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      var action = form.getAttribute("action") || "";
      var honey = form.querySelector("[name='company_website']");
      if (honey && honey.value) {
        event.preventDefault();
        return;
      }
      if (action.indexOf("YOUR_FORM_ID") !== -1 || action.indexOf("formspree.io/f/xxxxxxxx") !== -1) {
        event.preventDefault();
        var notice = document.getElementById("form-fallback");
        if (notice) {
          notice.hidden = false;
          notice.textContent =
            "Merci. Pour confirmer votre demande, appelez-nous au 04 38 70 03 94.";
        }
      }
    });
  }
})();

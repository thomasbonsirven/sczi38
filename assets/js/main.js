(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

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
      var emailField = form.querySelector("[name='email']");
      var honey = form.querySelector("[name='company_website']");
      if (honey && honey.value) {
        event.preventDefault();
        return;
      }
      if (action.indexOf("YOUR_FORM_ID") !== -1 || action.indexOf("formspree.io/f/xxxxxxxx") !== -1) {
        event.preventDefault();
        var dest = "EMAIL_A_COMPLETER@exemple.fr";
        var nom = (form.querySelector("[name='nom']") || {}).value || "";
        var tel = (form.querySelector("[name='telephone']") || {}).value || "";
        var mail = emailField ? emailField.value : "";
        var lieu = (form.querySelector("[name='lieu']") || {}).value || "";
        var budget = (form.querySelector("[name='budget']") || {}).value || "";
        var besoin = (form.querySelector("[name='besoin']") || {}).value || "";
        var body = [
          "Nom : " + nom,
          "Téléphone : " + tel,
          "E-mail : " + mail,
          "Lieu des futurs travaux : " + lieu,
          "Budget estimé : " + budget,
          "",
          "Besoins :",
          besoin
        ].join("\n");
        var mailto =
          "mailto:" +
          dest +
          "?subject=" +
          encodeURIComponent("Demande de devis SCZI") +
          "&body=" +
          encodeURIComponent(body);
        var notice = document.getElementById("form-fallback");
        if (notice) {
          notice.hidden = false;
          notice.innerHTML =
            "<strong>Formulaire en mode brouillon.</strong> L’adresse e-mail professionnelle n’est pas publiée sur le site actuel (le lien du thème était un placeholder <code>your@email</code>). Remplacez l’identifiant Formspree dans le HTML, ou renseignez l’e-mail réel. Un brouillon mailto s’ouvre avec le destinataire factice <code>" +
            dest +
            "</code>.";
        }
        window.location.href = mailto;
      }
    });
  }
})();

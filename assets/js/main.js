/* EL FATH STATIO — brand kit interactions */
(function () {
  "use strict";

  /* Copy-to-clipboard for the ready captions */
  document.querySelectorAll(".cap .copy").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.closest(".cap").querySelector("p").innerText.trim();
      var done = function () {
        btn.textContent = "Copié ✓";
        btn.classList.add("done");
        setTimeout(function () {
          btn.textContent = "Copier";
          btn.classList.remove("done");
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () { fallback(text); done(); });
      } else {
        fallback(text); done();
      }
    });
  });

  function fallback(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "absolute";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
  }

  /* DISPO / RUPTURE sticker toggle — the story sticker in two states */
  var demo = document.querySelector(".story-demo");
  if (demo) {
    var states = {
      dispo: { word: "DISPO", sub: "Disponible en magasin · ديزبوني" },
      rupture: { word: "RUPTURE", sub: "Back in stock demain inchallah" }
    };
    var paint = function (key) {
      var s = states[key];
      demo.setAttribute("data-state", key);
      demo.querySelector(".state").textContent = s.word;
      demo.querySelector(".sub").textContent = s.sub;
      demo.setAttribute("aria-label", "Story sticker " + s.word + " — cliquer pour changer");
    };
    paint("dispo");
    demo.addEventListener("click", function () {
      paint(demo.getAttribute("data-state") === "dispo" ? "rupture" : "dispo");
    });
  }

  /* Footer year */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = new Date().getFullYear();
})();

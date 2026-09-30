/* Ocellatus: animação de entrada discreta. O site funciona inteiro sem este arquivo. */
(function () {
  "use strict";
  var reduzir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduzir || !("IntersectionObserver" in window)) return;

  document.documentElement.classList.add("js");

  var observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (entrada) {
      if (entrada.isIntersecting) {
        entrada.target.classList.add("visivel");
        observador.unobserve(entrada.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });

  document.querySelectorAll(".revelar").forEach(function (el) {
    observador.observe(el);
  });
})();

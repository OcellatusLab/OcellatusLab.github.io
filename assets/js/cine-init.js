/* Ocellatus: liga o modo cinematográfico antes da primeira pintura, para não haver salto de layout.
   Só liga sem pedido de movimento reduzido. Sem JavaScript, o site aparece na versão estática. */
(function () {
  var mm = window.matchMedia;
  if (mm && mm("(prefers-reduced-motion: no-preference)").matches && "IntersectionObserver" in window) {
    document.documentElement.classList.add("cine", "js");
  }
})();

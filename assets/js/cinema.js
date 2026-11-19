/* Ocellatus: motor das cenas de rolagem.
   Calcula o avanço de cada cena (0 a 1) e entrega ao CSS na variável --p (cenas fixas)
   ou --v (elementos que atravessam a tela). Toda a animação é feita no CSS, só com
   transform, opacity e clip-path. Sem JavaScript, ou com movimento reduzido, o
   conteúdo aparece inteiro na versão estática. */
(function () {
  "use strict";
  var raiz = document.documentElement;
  if (!raiz.classList.contains("cine")) return;

  function limitar(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }

  /* Quebra um título em palavras, preservando elementos internos, para animar uma a uma. */
  function separarPalavras(el) {
    var n = 0;
    (function andar(no) {
      Array.prototype.slice.call(no.childNodes).forEach(function (filho) {
        if (filho.nodeType === 3) {
          var partes = filho.textContent.split(/(\s+)/);
          var frag = document.createDocumentFragment();
          partes.forEach(function (parte) {
            if (!parte) return;
            if (/^\s+$/.test(parte)) { frag.appendChild(document.createTextNode(parte)); return; }
            var s = document.createElement("span");
            s.className = "palavra";
            s.textContent = parte;
            s.style.setProperty("--i", n++);
            frag.appendChild(s);
          });
          no.replaceChild(frag, filho);
        } else if (filho.nodeType === 1) {
          andar(filho);
        }
      });
    })(el);
    el.style.setProperty("--n", n);
  }
  document.querySelectorAll("[data-palavras]").forEach(separarPalavras);

  var cenas = Array.prototype.slice.call(document.querySelectorAll("[data-cena]"));
  var atravessam = Array.prototype.slice.call(document.querySelectorAll("[data-progresso]"));
  var tons = Array.prototype.slice.call(document.querySelectorAll("[data-tom]"));
  var topo = document.querySelector(".topo");
  var setores = Array.prototype.slice.call(document.querySelectorAll("[data-setor]"));
  var marcas = {};
  document.querySelectorAll("[data-marca]").forEach(function (m) { marcas[m.getAttribute("data-marca")] = m; });

  /* Só escreve no estilo quando o valor muda de fato, para não gerar recálculo à toa. */
  var ultimo = new WeakMap();
  function definir(el, nome, valor) {
    var mapa = ultimo.get(el);
    if (!mapa) { mapa = {}; ultimo.set(el, mapa); }
    if (mapa[nome] !== undefined && Math.abs(mapa[nome] - valor) < 0.0005) return;
    mapa[nome] = valor;
    el.style.setProperty(nome, valor.toFixed(4));
  }

  var agendado = false;
  function atualizar() {
    agendado = false;
    var vh = window.innerHeight;

    cenas.forEach(function (c) {
      var r = c.getBoundingClientRect();
      var curso = r.height - vh;
      definir(c, "--p", curso > 1 ? limitar(-r.top / curso) : limitar((vh - r.top) / (vh + r.height)));
    });

    atravessam.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      definir(el, "--v", limitar((vh - r.top) / (vh + r.height)));
    });

    var doc = raiz.scrollHeight - vh;
    definir(raiz, "--rolagem", doc > 0 ? limitar(window.scrollY / doc) : 0);

    /* Tom do cabeçalho: claro ou escuro conforme a cena que está atrás dele. */
    var tom = "";
    for (var i = 0; i < tons.length; i++) {
      var rt = tons[i].getBoundingClientRect();
      if (rt.top <= 40 && rt.bottom > 40) { tom = tons[i].getAttribute("data-tom"); break; }
    }
    topo.classList.toggle("topo--escuro", tom !== "");

    /* Marcadores da cena "Para quem". */
    var ativo = null;
    setores.forEach(function (s) {
      if (s.getBoundingClientRect().top < vh * 0.6) ativo = s.getAttribute("data-setor");
    });
    Object.keys(marcas).forEach(function (k) {
      marcas[k].classList.toggle("ativo", k === (ativo || "advocacia"));
    });
  }

  function agendar() {
    if (!agendado) { agendado = true; window.requestAnimationFrame(atualizar); }
  }
  window.addEventListener("scroll", agendar, { passive: true });
  window.addEventListener("resize", agendar);
  atualizar();

  /* Entradas discretas dos blocos de texto. */
  var observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("visivel"); observador.unobserve(e.target); }
    });
  }, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 });
  document.querySelectorAll(".revelar").forEach(function (el) { observador.observe(el); });

  /* Ao navegar pelo teclado, garante que o conteúdo focado de uma cena esteja visível. */
  document.addEventListener("focusin", function (e) {
    var cena = e.target.closest && e.target.closest(".cena");
    document.querySelectorAll(".cena.focada").forEach(function (c) { if (c !== cena) c.classList.remove("focada"); });
    if (cena) cena.classList.add("focada");
  });

  raiz.classList.add("cine-pronto");
})();

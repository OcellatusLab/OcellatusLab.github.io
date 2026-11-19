// Gera assets/img/og.jpg (1200×630) com o logo e a fonte Prompt do próprio site.
// Uso: node tools/gerar-og.js   (precisa do Playwright com Chromium instalado)
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const raiz = path.resolve(__dirname, "..");
// Arquivos embutidos como data: URI (a página é montada em memória).
const url = (p, tipo) => `data:${tipo};base64,` + fs.readFileSync(path.join(raiz, p)).toString("base64");

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: Prompt; src: url("${url("assets/fonts/prompt-semibold.woff2", "font/woff2")}"); font-weight: 600; }
* { margin: 0; box-sizing: border-box; }
body { width: 1200px; height: 630px; background: #1c1b1f; color: #fff; font-family: Prompt, sans-serif;
  position: relative; overflow: hidden; padding: 84px 80px; }
.logo { width: 440px; display: block; }
.linha { width: 120px; height: 4px; background: #f26a21; margin: 56px 0 32px; }
h1 { font-weight: 600; font-size: 48px; line-height: 1.28; letter-spacing: -0.01em; white-space: nowrap; }
.curva { position: absolute; right: -170px; top: -60px; width: 640px; height: 640px; border-radius: 50%;
  border: 2px solid #f26a21; opacity: 0.55; }
</style></head><body>
<div class="curva"></div>
<img class="logo" src="${url("assets/img/logo-horizontal-escuro.svg", "image/svg+xml")}" alt="">
<div class="linha"></div>
<h1>Agentes de IA seguros e auditáveis<br>para escritórios de advocacia<br>e clínicas médicas.</h1>
</body></html>`;

(async () => {
  const navegador = await chromium.launch();
  const pagina = await navegador.newPage({ viewport: { width: 1200, height: 630 } });
  await pagina.setContent(html, { waitUntil: "load" });
  await pagina.evaluate(() => document.fonts.ready);
  await pagina.screenshot({ path: path.join(raiz, "assets/img/og.jpg"), type: "jpeg", quality: 86 });
  await navegador.close();
  console.log("ok: assets/img/og.jpg");
})();

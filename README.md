# Site institucional da Ocellatus

Site de página única da Ocellatus, Tecnologia & Desenvolvimento. É 100% estático (HTML, CSS e um JavaScript mínimo), sem framework, sem etapa de build e sem nenhuma dependência de terceiros em tempo de execução. Fica hospedado no GitHub Pages.

## Estrutura

```
index.html                 página principal (todo o conteúdo em HTML)
privacidade.html           política de privacidade (LGPD)
404.html                   página de erro
robots.txt, sitemap.xml    SEO
llms.txt, llms-full.txt    resumo e conteúdo completo para buscadores de IA
site.webmanifest, favicon.ico
.well-known/security.txt   contato para relatos de vulnerabilidade
assets/css/site.css        estilos e tokens de cor (início do arquivo)
assets/js/site.js          animação de entrada (o site funciona sem ele)
assets/fonts/              Prompt 400/500/600 em woff2 (licença OFL)
assets/img/                logos, peixe decorativo, ícones e imagem Open Graph
.github/workflows/pages.yml  publicação automática
tools/                     scripts opcionais para regenerar imagens e llms-full.txt
```

## Rodar localmente

```bash
python3 -m http.server 8080
# abra http://localhost:8080
```

Use um servidor local, não o arquivo aberto direto. Os caminhos começam com `/` e a Content Security Policy exige a mesma origem.

## Preencher os dados pendentes

Os dados que ainda não foram informados aparecem como marcadores `PREENCHER_...`. Para listar todos:

```bash
grep -rn "PREENCHER" --exclude-dir=.git --exclude=README.md .
```

| Marcador | O que colocar | Onde aparece |
| --- | --- | --- |
| `PREENCHER_NOME_FUNDADOR` | Nome completo | Sobre, JSON-LD, llms.txt |
| `PREENCHER_CIDADE` / `PREENCHER_UF` | Ex.: `Manaus` / `AM` | Sobre, JSON-LD, llms.txt |
| `PREENCHER_EMAIL` | E-mail de contato | Botões, contato, privacidade, security.txt, JSON-LD, llms.txt |
| `PREENCHER_INSTAGRAM_URL` | URL completa | Rodapé, JSON-LD |
| `PREENCHER_BIO` | Trajetória e por que criou a Ocellatus | Seção Sobre |
| `PREENCHER_PRAZO_DIAGNOSTICO` | Primeira frase da resposta, ex.: "Em geral, X semanas." | FAQ (HTML e JSON-LD) |
| `PREENCHER_CNPJ` | Opcional; descomente a linha no rodapé | Rodapé |

Também há dois comentários para revisar em `index.html`. Um é `CONFIRMAR`, na seção de segurança, sobre onde os dados ficam. O outro troca o símbolo da seção Sobre pela sua foto (WebP/AVIF 480×480, com `alt`).

Se um dado não existir, apague a frase ou o link inteiro, em vez de deixar o marcador. Depois de editar textos, rode `python3 tools/gerar-llms-full.py` para atualizar o `llms-full.txt`. Nome, cidade e contato precisam ficar idênticos no HTML, no JSON-LD e no `llms.txt`.

## Publicar (GitHub Pages)

1. Em **Settings → Pages**, em "Build and deployment", escolha **Source: GitHub Actions**. Isso só precisa ser feito uma vez.
2. Cada push na `main` roda `.github/workflows/pages.yml` e publica o site em `https://ocellatuslab.github.io/`. Dá para rodar manualmente em **Actions → Publicar no GitHub Pages → Run workflow**.

O workflow copia só os arquivos públicos para `_site/`. README, `tools/` e `.github/` ficam de fora. Ele usa `upload-pages-artifact@v3` de propósito: a v4 descarta pastas ocultas e o `/.well-known/security.txt` sumiria.

## Domínio próprio

1. Crie o arquivo `CNAME` na raiz com o domínio, numa linha só. Exemplo: `ocellatus.dev`.
2. No provedor de DNS:
   - Domínio raiz (`ocellatus.dev`): registros **A** para `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, e **AAAA** para `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.
   - Subdomínio `www`: registro **CNAME** apontando para `ocellatuslab.github.io`.
3. Em **Settings → Pages**, informe o domínio em "Custom domain" e, depois que o certificado for emitido, marque **Enforce HTTPS**.
4. Recomendado: verifique o domínio na organização (**Settings → Pages → Add a domain** nas configurações da organização) para impedir que outra conta o use.
5. Troque `https://ocellatuslab.github.io` pelo novo domínio em todos os arquivos:

```bash
grep -rl "ocellatuslab.github.io" --exclude-dir=.git . | xargs sed -i 's#https://ocellatuslab.github.io#https://ocellatus.dev#g'
```

Revise o resultado. O `CNAME` do `www`, que aponta para `ocellatuslab.github.io` no DNS, continua igual.

## Regenerar imagens (opcional)

Só é necessário se a marca mudar. Extraia o zip oficial da marca e rode:

```bash
python3 -m pip install pillow
python3 tools/gerar-assets.py "/caminho/OCELLATUS ARQUIVO" /caminho/Prompt-SemiBold.ttf
```

O script gera os logos (AVIF + WebP), o peixe decorativo, os ícones, o `favicon.ico` e a imagem Open Graph (`og.jpg`, 1200×630).

## Decisões técnicas

- **Segurança:** CSP por `<meta>` sem `unsafe-inline` (o GitHub Pages não permite cabeçalhos próprios). O site não tem cookies, formulários nem scripts de terceiros.
- **Fontes:** Prompt self-hosted, recortada para o alfabeto latino, com `font-display: swap` e preload.
- **Cores:** tokens no início de `site.css`. O laranja `#F5813E` não é usado em texto comum sobre fundo claro (contraste 2,6:1). Ele aparece em linhas, ícones e botões com texto preto (8,1:1).
- **Modo escuro:** automático via `prefers-color-scheme`.
- **Acessibilidade:** o conteúdo aparece sem JavaScript, e as animações respeitam `prefers-reduced-motion`.
- **Analytics:** nenhum. Se um dia for necessário, use uma opção sem cookies (Plausible ou Umami). Adicione o domínio dela ao `script-src` e ao `connect-src` da CSP e atualize a política de privacidade.

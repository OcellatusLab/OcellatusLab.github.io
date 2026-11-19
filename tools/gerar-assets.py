#!/usr/bin/env python3
"""Gera as imagens do site a partir do pacote da identidade visual (2026).

Uso (só é preciso rodar de novo se a marca mudar):
    python3 -m pip install pillow
    python3 tools/gerar-assets.py /caminho/ocellatus-identidade-2026-logos
    node tools/gerar-og.js          # imagem Open Graph (usa o Playwright)

O argumento é a pasta extraída do zip, com os arquivos ocellatus-*.svg/png.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

GRAFITE = (28, 27, 31)  # #1C1B1F

marca = Path(sys.argv[1])
saida = Path(__file__).resolve().parent.parent / "assets" / "img"
raiz = saida.parent.parent
saida.mkdir(parents=True, exist_ok=True)


def enxugar_svg(texto):
    """Arredonda as coordenadas para 3 casas e tira quebras de linha."""
    texto = re.sub(r"-?\d+\.\d{4,}", lambda m: f"{float(m.group()):.3f}".rstrip("0").rstrip("."), texto)
    return re.sub(r">\s+<", "><", texto).strip() + "\n"


# Logos e símbolo em SVG (nítidos em qualquer tela e leves).
svgs = {
    "ocellatus-horizontal-fundo-claro": "logo-horizontal-claro",
    "ocellatus-horizontal-fundo-escuro": "logo-horizontal-escuro",
    "ocellatus-simbolo": "simbolo-claro",
    "ocellatus-simbolo-fundo-escuro": "simbolo-escuro",
    "ocellatus-icone-app": "icone",
}
for origem, destino in svgs.items():
    texto = (marca / f"{origem}.svg").read_text(encoding="utf-8")
    (saida / f"{destino}.svg").write_text(enxugar_svg(texto), encoding="utf-8")

# Ícones PNG a partir do ícone de app oficial (símbolo laranja sobre grafite).
app = Image.open(marca / "ocellatus-icone-app.png").convert("RGBA")
for tamanho in (32, 192, 512):
    app.resize((tamanho, tamanho), Image.LANCZOS).save(saida / f"icon-{tamanho}.png", optimize=True)
app.resize((48, 48), Image.LANCZOS).save(raiz / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# Ícones sem cantos arredondados (o sistema recorta): maskable e Apple.
simbolo = Image.open(marca / "ocellatus-simbolo-fundo-escuro.png").convert("RGBA")
simbolo = simbolo.crop(simbolo.getbbox())


def icone_quadrado(tamanho, ocupacao):
    tela = Image.new("RGBA", (tamanho, tamanho), GRAFITE + (255,))
    s = simbolo.copy()
    lado = round(tamanho * ocupacao)
    s.thumbnail((lado, lado), Image.LANCZOS)
    # Centraliza pelo corpo circular, que fica na parte de baixo do símbolo.
    tela.alpha_composite(s, ((tamanho - s.width) // 2, (tamanho - s.height) // 2))
    return tela


icone_quadrado(512, 0.52).save(saida / "icon-maskable-512.png", optimize=True)
icone_quadrado(180, 0.62).convert("RGB").save(saida / "apple-touch-icon.png", optimize=True)

print("ok:", sorted(p.name for p in saida.iterdir()))

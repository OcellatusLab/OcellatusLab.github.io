#!/usr/bin/env python3
"""Gera as imagens otimizadas do site a partir do pacote oficial da marca.

Uso (só é preciso rodar de novo se a marca mudar):
    python3 -m pip install pillow
    python3 tools/gerar-assets.py "/caminho/OCELLATUS ARQUIVO" tools/fontes/Prompt-SemiBold.ttf

O primeiro argumento é a pasta extraída do zip (a que contém PNG/).
O segundo é o TTF da Prompt SemiBold, usado só na imagem Open Graph.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LARANJA = (245, 129, 62)
PESSEGO = (255, 191, 154)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

marca = Path(sys.argv[1]) / "PNG"
fonte_ttf = sys.argv[2]
saida = Path(__file__).resolve().parent.parent / "assets" / "img"
raiz = saida.parent.parent
saida.mkdir(parents=True, exist_ok=True)


def abrir(nome):
    return Image.open(marca / f"{nome}.png").convert("RGBA")


def redimensionar(im, largura):
    altura = round(im.height * largura / im.width)
    return im.resize((largura, altura), Image.LANCZOS)


def salvar_web(im, nome):
    """Salva AVIF + WebP (o WebP também serve de fallback no <img>)."""
    im.save(saida / f"{nome}.webp", "WEBP", quality=90, method=6)
    im.save(saida / f"{nome}.avif", "AVIF", quality=70)


def tingir(im, cor):
    """Troca a cor de um logo monocromático mantendo o alfa."""
    solido = Image.new("RGBA", im.size, cor + (255,))
    solido.putalpha(im.getchannel("A"))
    return solido


# Logos horizontais: 2x do tamanho exibido no header (170 px de largura).
for variante in ("black", "white"):
    salvar_web(redimensionar(abrir(f"logo-{variante}-horizontal"), 340), f"logo-horizontal-{variante}")

# Símbolo isolado (parte de cima do logo principal).
principal = abrir("logo-black-principal")
topo = principal.crop((0, 0, principal.width, 1021))
simbolo = topo.crop(topo.getbbox())

# Peixe decorativo do hero, em pêssego (sobre fundo claro) e em branco (modo escuro).
peixe = abrir("patner")
peixe = peixe.crop(peixe.getbbox())
salvar_web(redimensionar(tingir(peixe, PESSEGO), 720), "peixe-pessego")
salvar_web(redimensionar(peixe, 720), "peixe-branco")

# Submarca para a 404 e para o espaço da foto na seção Sobre.
for variante in ("color", "white"):
    sub = abrir(f"sublogo-{variante}")
    salvar_web(redimensionar(sub.crop(sub.getbbox()), 400), f"submarca-{variante}")


def icone(tamanho, margem=0.14, fundo=BRANCO, cor=PRETO, arredondar=True):
    tela = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    base = Image.new("RGBA", (tamanho, tamanho), fundo + (255,))
    mascara = Image.new("L", (tamanho, tamanho), 0)
    ImageDraw.Draw(mascara).rounded_rectangle(
        (0, 0, tamanho - 1, tamanho - 1), radius=tamanho // 5 if arredondar else 0, fill=255
    )
    tela.paste(base, (0, 0), mascara)
    lado = round(tamanho * (1 - 2 * margem))
    s = tingir(simbolo, cor)
    s.thumbnail((lado, lado), Image.LANCZOS)
    tela.alpha_composite(s, ((tamanho - s.width) // 2, (tamanho - s.height) // 2))
    return tela


# Favicons: símbolo preto sobre laranja da marca (lê bem em abas claras e escuras).
for tamanho in (32, 192, 512):
    icone(tamanho, margem=0.12, fundo=LARANJA).save(saida / f"icon-{tamanho}.png", optimize=True)
icone(512, margem=0.2, fundo=LARANJA, arredondar=False).save(saida / "icon-maskable-512.png", optimize=True)
icone(180, margem=0.14, fundo=LARANJA, arredondar=False).convert("RGB").save(saida / "apple-touch-icon.png", optimize=True)
icone(48, margem=0.1, fundo=LARANJA).save(raiz / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# Imagem Open Graph 1200x630.
og = Image.new("RGB", (1200, 630), PRETO)
d = ImageDraw.Draw(og)
d.arc((760, -120, 1400, 520), 200, 330, fill=LARANJA, width=2)
d.arc((820, 180, 1300, 660), 150, 300, fill=PESSEGO, width=2)
logo = redimensionar(abrir("logo-white-horizontal"), 420)
og.paste(logo, (80, 80), logo)
titulo = ImageFont.truetype(fonte_ttf, 50)
d.multiline_text(
    (80, 320),
    "Agentes de IA seguros e auditáveis\npara escritórios de advocacia\ne clínicas médicas.",
    font=titulo, fill=BRANCO, spacing=14,
)
d.line((80, 290, 200, 290), fill=LARANJA, width=4)
og.save(saida / "og.jpg", "JPEG", quality=86, optimize=True, progressive=True)

print("ok:", sorted(p.name for p in saida.iterdir()))

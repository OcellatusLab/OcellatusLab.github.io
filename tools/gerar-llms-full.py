#!/usr/bin/env python3
"""Gera llms-full.txt a partir do conteúdo de index.html.

Rode depois de editar textos do site:  python3 tools/gerar-llms-full.py
Só usa a biblioteca padrão do Python.
"""
from html.parser import HTMLParser
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
BLOCOS = {"h1": "# ", "h2": "## ", "h3": "### ", "p": "", "dt": "#### ", "li": ""}


class Conversor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dentro_main = False
        self.pular = 0
        self.fechar_pulo = []
        self.pilha = []
        self.texto = []
        self.saida = []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.dentro_main = True
        if not self.dentro_main:
            return
        classes = (dict(attrs).get("class") or "").split()
        if tag in ("script", "style", "svg", "picture", "figure") or {"rotulo", "acoes"} & set(classes):
            self.pular += 1
            self.fechar_pulo.append(tag)
        if tag in BLOCOS and not self.pular:
            self.fechar()
            self.pilha.append(tag)
        if tag in ("strong", "b") and not self.pular:
            self.texto.append("**")

    def handle_endtag(self, tag):
        if tag == "main":
            self.fechar()
            self.dentro_main = False
        if not self.dentro_main:
            return
        if self.fechar_pulo and self.fechar_pulo[-1] == tag:
            self.fechar_pulo.pop()
            self.pular -= 1
            return
        if tag in ("strong", "b") and not self.pular:
            self.texto.append("**")
        if tag in BLOCOS and not self.pular:
            self.fechar()

    def handle_data(self, data):
        if self.dentro_main and not self.pular:
            self.texto.append(data)

    def fechar(self):
        conteudo = " ".join("".join(self.texto).split())
        conteudo = conteudo.replace("** ", "**").replace(" **", "**") if conteudo.count("**") % 2 else conteudo
        if conteudo and self.pilha:
            tag = self.pilha[-1]
            prefixo = BLOCOS[tag]
            if tag == "li" and not conteudo.startswith("#"):
                prefixo = "- "
            self.saida.append(prefixo + conteudo)
        elif conteudo:
            self.saida.append(conteudo)
        self.texto = []
        if self.pilha:
            self.pilha.pop()


c = Conversor()
c.feed((raiz / "index.html").read_text(encoding="utf-8"))
cabecalho = (
    "# Ocellatus — conteúdo completo do site\n\n"
    "> Versão em markdown de https://ocellatuslab.github.io/ para leitura por modelos de linguagem. "
    "Resumo em https://ocellatuslab.github.io/llms.txt\n"
)
corpo = "\n\n".join(linha.replace("# ", "## ", 1) if linha.startswith("# ") else linha for linha in c.saida)
(raiz / "llms-full.txt").write_text(cabecalho + "\n" + corpo + "\n", encoding="utf-8")
print("llms-full.txt:", len(corpo), "caracteres")

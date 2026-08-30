#!/usr/bin/env python3
"""
Gera a lista de contribuidores do Guia Aberto de Arquitetura de Software.

Fontes:
    _shared/contribuidores.yaml           mantenedores do projeto
    content/NN-topico/metadata.yaml       autores de cada tópico

Destinos (bloco entre os marcadores CONTRIBUIDORES:INICIO / CONTRIBUIDORES:FIM):
    README.md
    guia/sobre.qmd

Uso:
    python scripts/gerar_contribuidores.py              # reescreve os arquivos
    python scripts/gerar_contribuidores.py --verificar  # só confere, não escreve

Sai com código 1 se --verificar encontrar a lista desatualizada, para que o CI
avise quando alguém preencher o metadata.yaml e esquecer de rodar o gerador.

Requer: pyyaml
"""

from __future__ import annotations

import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERRO: instale o pyyaml -> pip install pyyaml")
    sys.exit(2)

# Acentos legíveis no log do CI e no console do Windows, que não usa UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"
FONTE_MANTENEDORES = RAIZ / "_shared" / "contribuidores.yaml"

DESTINOS = [RAIZ / "README.md", RAIZ / "guia" / "sobre.qmd"]

INICIO = "<!-- CONTRIBUIDORES:INICIO -->"
FIM = "<!-- CONTRIBUIDORES:FIM -->"

POR_LINHA = 4
TAMANHO_FOTO = 100


@dataclass
class Pessoa:
    nome: str
    github: str = ""


def normalizar_nome(nome: str) -> str:
    """Chave de comparação: sem acento, sem caixa, sem espaço duplicado."""
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFKD", nome or "") if not unicodedata.combining(c)
    )
    return " ".join(sem_acento.split()).casefold()


def normalizar_github(github: str) -> str:
    """Aceita 'ana', '@ana' ou 'https://github.com/ana/' e devolve 'ana'."""
    g = (github or "").strip()
    for prefixo in ("https://github.com/", "http://github.com/", "github.com/"):
        if g.lower().startswith(prefixo):
            g = g[len(prefixo) :]
            break
    return g.strip().strip("/").lstrip("@").strip()


def coletar() -> list[Pessoa]:
    """Uma entrada por pessoa, na ordem de crédito: mantenedores, depois autores.

    Ninguém aparece duas vezes. A mesma pessoa pode estar registrada em vários
    lugares — como mantenedora e como autora, em dois tópicos, com o handle
    escrito de formas diferentes, ou com o campo 'github' preenchido em um lugar
    e vazio em outro. Todos esses casos convergem para um único cartão.
    """
    registros: list[tuple[str, str]] = []

    def registrar(nome: str, github: str) -> None:
        nome = (nome or "").strip()
        if nome:
            registros.append((nome, normalizar_github(github)))

    if FONTE_MANTENEDORES.exists():
        dados = yaml.safe_load(FONTE_MANTENEDORES.read_text(encoding="utf-8")) or {}
        for m in dados.get("mantenedores") or []:
            registrar(m.get("nome", ""), m.get("github", ""))

    for pasta in sorted(p for p in CONTENT.iterdir() if p.is_dir()):
        meta_path = pasta / "metadata.yaml"
        if not meta_path.exists():
            continue
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        if pasta.name == "00-modelo" or meta.get("status") == "modelo":
            continue  # pasta modelo tem dados de exemplo, não gente de verdade
        for a in meta.get("autores") or []:
            if isinstance(a, dict):
                registrar(a.get("nome", ""), a.get("github", ""))

    # Quem aparece sem 'github' em um registro herda o handle informado em
    # outro, senão a mesma pessoa viraria dois cartões — um com foto, um sem.
    handle_por_nome: dict[str, str] = {}
    for nome, github in registros:
        chave = normalizar_nome(nome)
        if github and chave not in handle_por_nome:
            handle_por_nome[chave] = github

    pessoas: dict[str, Pessoa] = {}
    for nome, github in registros:
        chave_nome = normalizar_nome(nome)
        handle = github or handle_por_nome.get(chave_nome, "")
        # Identidade é o handle quando existe; só cai no nome quem não tem conta.
        chave = handle.casefold() if handle else chave_nome
        pessoas.setdefault(chave, Pessoa(nome=nome, github=handle))

    return list(pessoas.values())


def celula(p: Pessoa) -> str:
    """Foto redonda com o nome logo abaixo, os dois dentro do mesmo link."""
    if not p.github:
        return f'<td align="center" width="150">\n{p.nome}\n</td>'
    return (
        '<td align="center" width="150">\n'
        f'<a href="https://github.com/{p.github}">\n'
        f'<img src="https://github.com/{p.github}.png?size={TAMANHO_FOTO}" '
        f'width="{TAMANHO_FOTO}" height="{TAMANHO_FOTO}" '
        'style="border-radius:50%" '
        f'alt="Foto de perfil de {p.nome} no GitHub"><br>\n'
        f"{p.nome}\n"
        "</a>\n"
        "</td>"
    )


def bloco(pessoas: list[Pessoa]) -> str:
    if not pessoas:
        return f"{INICIO}\n\n_Ainda não há contribuidores registrados._\n\n{FIM}"

    linhas = []
    for i in range(0, len(pessoas), POR_LINHA):
        celulas = "\n".join(celula(p) for p in pessoas[i : i + POR_LINHA])
        linhas.append(f"<tr>\n{celulas}\n</tr>")

    tabela = "<table>\n" + "\n".join(linhas) + "\n</table>"
    return f"{INICIO}\n\n{tabela}\n\n{FIM}"


def aplicar(caminho: Path, novo_bloco: str) -> str | None:
    """Devolve o texto atualizado, ou None se já estiver em dia."""
    texto = caminho.read_text(encoding="utf-8")
    if INICIO not in texto or FIM not in texto:
        raise SystemExit(
            f"ERRO: {caminho.relative_to(RAIZ)} não tem os marcadores "
            f"{INICIO} ... {FIM} — adicione-os onde a lista deve aparecer."
        )
    ini = texto.index(INICIO)
    fim = texto.index(FIM) + len(FIM)
    atualizado = texto[:ini] + novo_bloco + texto[fim:]
    return None if atualizado == texto else atualizado


def main() -> int:
    verificar = "--verificar" in sys.argv[1:]
    pessoas = coletar()
    novo_bloco = bloco(pessoas)

    desatualizados = []
    for destino in DESTINOS:
        atualizado = aplicar(destino, novo_bloco)
        if atualizado is None:
            continue
        desatualizados.append(destino)
        if not verificar:
            destino.write_text(atualizado, encoding="utf-8")

    nomes = ", ".join(p.nome for p in pessoas) or "ninguém ainda"
    print(f"{len(pessoas)} contribuidor(es): {nomes}")

    if verificar:
        if desatualizados:
            print("\nLista desatualizada em:")
            for d in desatualizados:
                print(f"   · {d.relative_to(RAIZ)}")
            print("\nRode: python scripts/gerar_contribuidores.py")
            return 1
        print("Lista em dia.")
        return 0

    if desatualizados:
        for d in desatualizados:
            print(f"   atualizado · {d.relative_to(RAIZ)}")
    else:
        print("   nada a mudar")
    return 0


if __name__ == "__main__":
    sys.exit(main())

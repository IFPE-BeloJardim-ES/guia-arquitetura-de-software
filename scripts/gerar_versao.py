#!/usr/bin/env python3
"""
Calcula a próxima versão do Guia Aberto de Arquitetura de Software.

A numeração segue o versionamento semântico (https://semver.org), no formato
`vMAIOR.MENOR.CORRECAO`, com esta leitura para um projeto de conteúdo:

    MAIOR      quebra de compatibilidade — mudança na estrutura obrigatória de
               um tópico ou nas regras de validação, que obriga a revisar o que
               já está publicado
    MENOR      tópico novo publicado, ou formato novo entregue
    CORRECAO   correção de texto, referência, infraestrutura ou documentação

O tipo do incremento é deduzido de duas fontes, e vence a mais forte:

    1. Conventional Commits nas mensagens desde a última tag
       (`feat:` → MENOR, `fix:`/`docs:`/`ci:`/... → CORRECAO,
        `!:` ou `BREAKING CHANGE` → MAIOR)
    2. O que mudou em `content/`: um `index.qmd` novo significa tópico novo,
       portanto MENOR, mesmo que a mensagem do commit não diga

Uso:
    python scripts/gerar_versao.py              # imprime a próxima versão
    python scripts/gerar_versao.py --notas      # imprime as notas da versão
    python scripts/gerar_versao.py --json       # saída para o CI consumir
    python scripts/gerar_versao.py --atual      # imprime a última tag publicada

O script apenas calcula e imprime: não escreve arquivos, não cria tags e não
acessa a rede. Quem cria a tag e a release é o workflow `versionar.yml`.

Requer: git no PATH. Sem dependências de terceiros.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field

# Acentos legíveis no log do CI e no console do Windows, que não usa UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PRIMEIRA_VERSAO = (0, 1, 0)

PADRAO_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")

# tipo(escopo)!: assunto  — o "!" marca quebra de compatibilidade
PADRAO_COMMIT = re.compile(r"^(?P<tipo>[a-z]+)(?:\((?P<escopo>[^)]*)\))?(?P<quebra>!)?:\s*(?P<assunto>.+)$")

TIPOS_MENOR = {"feat"}
TIPOS_CORRECAO = {"fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"}

# content/07-camadas/index.qmd — um arquivo desses, adicionado, é tópico novo
PADRAO_TOPICO_NOVO = re.compile(r"^content/(\d{2}-[^/]+)/index\.qmd$")

MODELO = "00-modelo"

SECOES_NOTAS = [
    ("feat", "Tópicos e formatos novos"),
    ("fix", "Correções"),
    ("docs", "Documentação"),
    ("ci", "Infraestrutura"),
    ("build", "Infraestrutura"),
    ("chore", "Infraestrutura"),
    ("refactor", "Manutenção interna"),
    ("perf", "Manutenção interna"),
    ("style", "Manutenção interna"),
    ("test", "Manutenção interna"),
    ("revert", "Revertidos"),
]


def git(*args: str, cru: bool = False) -> str:
    """Roda git e devolve a saída. Erro do git vira SystemExit com a mensagem.

    Com `cru=True` a saída volta intacta. Isso importa em `git log`: os campos
    são separados por \\x1f e \\x1e, que o `str.strip()` do Python considera
    espaço em branco e comeria — descartando silenciosamente todo commit sem
    corpo, que é a maioria.
    """
    try:
        r = subprocess.run(
            ["git", *args], capture_output=True, text=True, encoding="utf-8", check=True
        )
    except FileNotFoundError:
        raise SystemExit("ERRO: git não encontrado no PATH")
    except subprocess.CalledProcessError as e:
        raise SystemExit(f"ERRO: git {' '.join(args)} falhou: {(e.stderr or '').strip()}")
    saida = r.stdout or ""
    return saida if cru else saida.strip()


@dataclass
class Commit:
    hash_curto: str
    assunto: str
    corpo: str

    @property
    def convencional(self) -> re.Match | None:
        return PADRAO_COMMIT.match(self.assunto)

    @property
    def tipo(self) -> str:
        m = self.convencional
        return m.group("tipo") if m else ""

    @property
    def descricao(self) -> str:
        m = self.convencional
        return m.group("assunto").strip() if m else self.assunto.strip()

    @property
    def quebra(self) -> bool:
        m = self.convencional
        if m and m.group("quebra"):
            return True
        return "BREAKING CHANGE" in self.corpo or "BREAKING-CHANGE" in self.corpo


@dataclass
class Analise:
    atual: tuple[int, int, int] | None
    proxima: tuple[int, int, int]
    tipo: str                                  # maior | menor | correcao
    motivos: list[str] = field(default_factory=list)
    commits: list[Commit] = field(default_factory=list)
    topicos_novos: list[str] = field(default_factory=list)

    @property
    def tag_atual(self) -> str:
        return formatar(self.atual) if self.atual else ""

    @property
    def tag_proxima(self) -> str:
        return formatar(self.proxima)


def formatar(v: tuple[int, int, int]) -> str:
    return "v{}.{}.{}".format(*v)


def ultima_tag() -> tuple[str, tuple[int, int, int]] | None:
    """Maior tag vMAIOR.MENOR.CORRECAO do repositório, por ordem semântica."""
    saida = git("tag", "--list", "v*")
    versoes = []
    for linha in saida.splitlines():
        m = PADRAO_TAG.match(linha.strip())
        if m:
            versoes.append((tuple(int(g) for g in m.groups()), linha.strip()))
    if not versoes:
        return None
    versoes.sort()
    versao, nome = versoes[-1]
    return nome, versao


def commits_desde(base: str | None) -> list[Commit]:
    intervalo = f"{base}..HEAD" if base else "HEAD"
    # %x1f separa campos e %x1e separa commits: assunto e corpo podem ter
    # qualquer coisa dentro, inclusive quebras de linha.
    formato = "%h%x1f%s%x1f%b%x1e"
    saida = git("log", intervalo, f"--format={formato}", cru=True)
    commits = []
    for bruto in saida.split("\x1e"):
        registro = bruto.strip("\r\n")
        if not registro:
            continue
        partes = registro.split("\x1f")
        if len(partes) < 3:
            continue
        commits.append(Commit(hash_curto=partes[0], assunto=partes[1], corpo=partes[2]))
    return commits


def topicos_adicionados(base: str | None) -> list[str]:
    """Tópicos cujo index.qmd apareceu no intervalo — o modelo não conta."""
    if base:
        saida = git("diff", "--name-only", "--diff-filter=A", f"{base}..HEAD")
    else:
        saida = git("ls-files")
    achados = []
    for caminho in saida.splitlines():
        m = PADRAO_TOPICO_NOVO.match(caminho.strip().replace("\\", "/"))
        if m and m.group(1) != MODELO:
            achados.append(m.group(1))
    return sorted(set(achados))


def incrementar(atual: tuple[int, int, int], tipo: str) -> tuple[int, int, int]:
    maior, menor, correcao = atual
    if tipo == "maior":
        return (maior + 1, 0, 0)
    if tipo == "menor":
        return (maior, menor + 1, 0)
    return (maior, menor, correcao + 1)


def analisar() -> Analise:
    tag = ultima_tag()
    base = tag[0] if tag else None
    atual = tag[1] if tag else None

    commits = commits_desde(base)
    novos = topicos_adicionados(base)

    motivos: list[str] = []
    tipo = "correcao"

    quebras = [c for c in commits if c.quebra]
    feats = [c for c in commits if c.tipo in TIPOS_MENOR]

    if quebras:
        tipo = "maior"
        motivos.append(f"{len(quebras)} commit(s) marcando quebra de compatibilidade")
    elif novos:
        tipo = "menor"
        motivos.append("tópico(s) novo(s): " + ", ".join(novos))
    elif feats:
        tipo = "menor"
        motivos.append(f"{len(feats)} commit(s) 'feat:'")
    elif commits:
        motivos.append(f"{len(commits)} commit(s) de correção ou manutenção")

    if atual is None:
        # Repositório ainda sem tag: a primeira versão é fixa, não incrementada.
        proxima = PRIMEIRA_VERSAO
        motivos.insert(0, "primeira versão do repositório")
    else:
        proxima = incrementar(atual, tipo)

    return Analise(
        atual=atual,
        proxima=proxima,
        tipo=tipo,
        motivos=motivos,
        commits=commits,
        topicos_novos=novos,
    )


def notas(a: Analise) -> str:
    linhas = []

    if a.topicos_novos:
        linhas.append("### Tópicos publicados nesta versão")
        linhas.append("")
        for t in a.topicos_novos:
            linhas.append(f"- `content/{t}/`")
        linhas.append("")

    vistos: set[str] = set()
    for tipo, titulo in SECOES_NOTAS:
        if titulo in vistos:
            continue
        tipos_da_secao = {t for t, s in SECOES_NOTAS if s == titulo}
        itens = [c for c in a.commits if c.tipo in tipos_da_secao]
        if not itens:
            continue
        vistos.add(titulo)
        linhas.append(f"### {titulo}")
        linhas.append("")
        for c in itens:
            marca = " **[quebra]**" if c.quebra else ""
            linhas.append(f"- {c.descricao}{marca} ({c.hash_curto})")
        linhas.append("")

    outros = [c for c in a.commits if not c.convencional]
    if outros:
        linhas.append("### Outras mudanças")
        linhas.append("")
        for c in outros:
            linhas.append(f"- {c.descricao} ({c.hash_curto})")
        linhas.append("")

    if not linhas:
        linhas = ["Sem mudanças registradas desde a versão anterior.", ""]

    if a.tag_atual:
        linhas.append(f"Comparando com {a.tag_atual}.")

    return "\n".join(linhas).strip()


def main() -> int:
    args = sys.argv[1:]
    a = analisar()

    if "--atual" in args:
        print(a.tag_atual or "(nenhuma tag ainda)")
        return 0

    if "--json" in args:
        print(json.dumps(
            {
                "atual": a.tag_atual,
                "proxima": a.tag_proxima,
                "tipo": a.tipo,
                "motivos": a.motivos,
                "topicos_novos": a.topicos_novos,
                "commits": len(a.commits),
                "notas": notas(a),
            },
            ensure_ascii=False,
        ))
        return 0

    if "--notas" in args:
        print(notas(a))
        return 0

    if "--explicar" in args:
        print(f"versão atual : {a.tag_atual or '(nenhuma)'}")
        print(f"próxima      : {a.tag_proxima}  ({a.tipo})")
        for m in a.motivos:
            print(f"   · {m}")
        return 0

    print(a.tag_proxima)
    return 0


if __name__ == "__main__":
    sys.exit(main())

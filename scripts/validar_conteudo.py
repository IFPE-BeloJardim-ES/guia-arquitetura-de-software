#!/usr/bin/env python3
"""
Valida a estrutura e as referências de um tópico do Guia Aberto de
Arquitetura de Software.

Uso:
    python scripts/validar_conteudo.py                      # valida todos os tópicos
    python scripts/validar_conteudo.py content/07-camadas   # valida um tópico

Sai com código 1 se houver erro, para que o CI reprove o PR.
Avisos não reprovam, mas aparecem na revisão.

Requer: pyyaml
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
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
BIB_GLOBAL = RAIZ / "_shared" / "referencias-globais.bib"

MIN_PALAVRAS = 1500
MAX_PALAVRAS = 3000
MIN_REFERENCIAS = 8
MAX_TAMANHO_MB = 25

ARQUIVOS_OBRIGATORIOS = [
    "index.qmd",
    "metadata.yaml",
    "referencias.bib",
    "slides.qmd",
    "notebook.ipynb",
]

CAMPOS_METADATA = [
    "numero", "slug", "titulo", "resumo", "autores", "status",
    "competencias", "palavras_chave", "formatos", "licenca",
]

PADRAO_CHAVE = re.compile(r"^[a-z]+\d{4}[a-z]+$")

# Todos os autores de exemplo do 00-modelo começam assim. Um tópico pode ter
# vários autores; basta um placeholder esquecido para o crédito sair errado.
PREFIXO_NOME_MODELO = "Nome Completo"


@dataclass
class Resultado:
    topico: str
    erros: list[str] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    def erro(self, msg: str) -> None:
        self.erros.append(msg)

    def aviso(self, msg: str) -> None:
        self.avisos.append(msg)

    @property
    def ok(self) -> bool:
        return not self.erros


def chaves_bib(texto: str) -> set[str]:
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", texto))


def entradas_bib(texto: str) -> list[str]:
    """Separa o arquivo .bib em blocos de entrada, ignorando comentários."""
    sem_comentario = "\n".join(
        linha for linha in texto.splitlines() if not linha.lstrip().startswith("%")
    )
    partes = re.split(r"(?=@\w+\s*\{)", sem_comentario)
    return [p for p in partes if p.strip().startswith("@")]


def sem_codigo(texto: str) -> str:
    """Remove blocos e trechos de código.

    Exemplos de sintaxe aparecem no texto entre backticks (`[@chave]`) para
    ensinar como citar. Sem isso, o validador os leria como citações reais.
    """
    texto = re.sub(r"```.*?```", " ", texto, flags=re.DOTALL)
    texto = re.sub(r"`[^`\n]*`", " ", texto)
    return texto


def citacoes_no_texto(texto: str) -> set[str]:
    """Extrai chaves citadas no formato [@chave] ou @chave, fora de código."""
    return set(re.findall(r"@([a-zA-Z][a-zA-Z0-9_:.-]*)", sem_codigo(texto)))


def contar_palavras(qmd: str) -> int:
    corpo = re.sub(r"^---\n.*?\n---\n", "", qmd, flags=re.DOTALL)
    corpo = re.sub(r"```.*?```", "", corpo, flags=re.DOTALL)
    corpo = re.sub(r":::.*?:::", "", corpo, flags=re.DOTALL)
    corpo = re.sub(r"[#*_>\[\]()|`-]", " ", corpo)
    return len(corpo.split())


def validar_topico(pasta: Path, chaves_globais: set[str]) -> Resultado:
    r = Resultado(topico=pasta.name)
    modelo = pasta.name == "00-modelo"

    # 1. Arquivos obrigatórios
    for nome in ARQUIVOS_OBRIGATORIOS:
        if not (pasta / nome).exists():
            r.erro(f"arquivo obrigatório ausente: {nome}")
    if not r.ok:
        return r

    index = (pasta / "index.qmd").read_text(encoding="utf-8")
    bib = (pasta / "referencias.bib").read_text(encoding="utf-8")
    slides = (pasta / "slides.qmd").read_text(encoding="utf-8")

    # 2. Metadados
    try:
        meta = yaml.safe_load((pasta / "metadata.yaml").read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        r.erro(f"metadata.yaml inválido: {e}")
        return r

    for campo in CAMPOS_METADATA:
        if not meta.get(campo):
            r.erro(f"metadata.yaml: campo obrigatório vazio ou ausente: '{campo}'")

    autores = meta.get("autores") or []
    if isinstance(autores, list):
        for a in autores:
            if not isinstance(a, dict) or not a.get("nome"):
                r.erro("metadata.yaml: cada autor precisa ter 'nome'")
            elif a.get("nome", "").strip().startswith(PREFIXO_NOME_MODELO) and not modelo:
                r.erro(
                    f"metadata.yaml: nome de autor não foi substituído "
                    f"(ainda está o do modelo: '{a['nome']}')"
                )

    if meta.get("slug") and not pasta.name.endswith(str(meta["slug"])):
        r.aviso(f"slug '{meta['slug']}' não corresponde ao nome da pasta '{pasta.name}'")

    # 3. Formatos obrigatórios declarados e presentes
    fmts = meta.get("formatos") or {}

    def entregue(chave: str) -> bool:
        v = fmts.get(chave)
        return bool(v.get("entregue")) if isinstance(v, dict) else bool(v)

    for chave in ("texto", "notebook", "audio_notebooklm", "gem_gemini", "slides"):
        if not entregue(chave):
            r.erro(f"formato obrigatório não entregue em metadata.yaml: '{chave}'")

    nb = fmts.get("notebook") or {}
    if isinstance(nb, dict) and entregue("notebook") and not nb.get("colab_url") and not modelo:
        r.erro("notebook entregue sem 'colab_url' no metadata.yaml")

    audio = fmts.get("audio_notebooklm") or {}
    if isinstance(audio, dict) and entregue("audio_notebooklm"):
        arq, url = audio.get("arquivo"), audio.get("url")
        if not arq and not url:
            r.erro("áudio do NotebookLM: informe 'arquivo' ou 'url' no metadata.yaml")
        if arq and not (pasta / arq).exists() and not modelo:
            r.erro(f"áudio declarado mas arquivo não encontrado: {arq}")
        if not audio.get("transcricao"):
            r.erro("áudio sem transcrição declarada (obrigatória por acessibilidade)")

    gem = fmts.get("gem_gemini") or {}
    if isinstance(gem, dict) and entregue("gem_gemini"):
        if not gem.get("url"):
            r.erro("Gem entregue sem URL pública no metadata.yaml")
        if not gem.get("instrucoes"):
            r.erro("Gem entregue sem as instruções de configuração no metadata.yaml")

    # 4. Extensão do texto
    palavras = contar_palavras(index)
    if not modelo:
        if palavras < MIN_PALAVRAS:
            r.erro(f"texto com {palavras} palavras — mínimo {MIN_PALAVRAS}")
        elif palavras > MAX_PALAVRAS:
            r.aviso(f"texto com {palavras} palavras — acima de {MAX_PALAVRAS}; considere dividir o tópico")

    # 5. Seções obrigatórias
    for secao in ("Definição", "Estrutura", "Exemplo", "Trade-off", "Referências"):
        if not re.search(rf"^#+\s*.*{secao}", index, re.MULTILINE | re.IGNORECASE):
            r.erro(f"seção obrigatória ausente no index.qmd: '{secao}'")

    if "{#refs}" not in index:
        r.erro("index.qmd não tem o bloco ::: {#refs} ::: que gera a lista de referências")

    # 6. Bibliografia
    entradas = entradas_bib(bib)
    chaves_locais = chaves_bib(bib)

    if len(entradas) < MIN_REFERENCIAS and not modelo:
        r.erro(f"apenas {len(entradas)} referências — mínimo {MIN_REFERENCIAS}")

    duplicadas = chaves_locais & chaves_globais
    if duplicadas:
        r.erro(f"chave duplicada com a bibliografia global: {', '.join(sorted(duplicadas))}")

    for chave in sorted(chaves_locais):
        if not PADRAO_CHAVE.match(chave):
            r.aviso(f"chave '{chave}' fora do padrão sobrenomeAnoPalavra")

    for entrada in entradas:
        chave_match = re.search(r"@\w+\s*\{\s*([^,\s]+)", entrada)
        chave = chave_match.group(1) if chave_match else "?"
        if not re.search(r"\b(doi|url|isbn)\s*=", entrada, re.IGNORECASE):
            r.erro(f"referência '{chave}' sem DOI, URL ou ISBN — precisa ser localizável")
        if not re.search(r"\byear\s*=", entrada, re.IGNORECASE):
            r.erro(f"referência '{chave}' sem ano")

    # 7. Citações resolvem
    citadas = citacoes_no_texto(index) | citacoes_no_texto(slides)
    disponiveis = chaves_locais | chaves_globais

    orfas = {c for c in citadas if c not in disponiveis}
    if orfas:
        r.erro(f"citação sem entrada na bibliografia: {', '.join(sorted(orfas))}")

    nao_citadas = chaves_locais - citadas
    if nao_citadas:
        r.erro(f"entrada no .bib nunca citada no texto: {', '.join(sorted(nao_citadas))}")

    if re.search(r"(?<!\w)\[\d+\](?!\()", sem_codigo(index)):
        r.aviso("há '[1]' escrito na mão no texto — use [@chave] para a numeração ser automática")

    # 8. Slides derivam do texto, não copiam
    if not re.search(r"\{\{<\s*include", slides) and not modelo:
        r.aviso("slides.qmd não usa {{< include >}} — verifique se o conteúdo não foi copiado e colado")

    n_slides = len(re.findall(r"^##\s+", slides, re.MULTILINE))
    if not modelo and not (12 <= n_slides <= 20):
        r.aviso(f"{n_slides} slides — o esperado é entre 12 e 20")

    # 9. Acessibilidade
    for img in re.findall(r"!\[([^\]]*)\]\([^)]+\)", index):
        if not img.strip():
            r.erro("imagem sem texto alternativo no index.qmd")

    # 10. Tamanho de arquivos
    for arq in pasta.rglob("*"):
        if arq.is_file():
            mb = arq.stat().st_size / 1_048_576
            if mb > MAX_TAMANHO_MB:
                r.erro(f"{arq.relative_to(pasta)} tem {mb:.1f} MB — máximo {MAX_TAMANHO_MB} MB")

    # 11. Notebook
    try:
        import json
        nbjson = json.loads((pasta / "notebook.ipynb").read_text(encoding="utf-8"))
        celulas = nbjson.get("cells", [])
        if not any(c.get("cell_type") == "code" for c in celulas):
            r.erro("notebook.ipynb sem nenhuma célula de código")
        if sum(1 for c in celulas if c.get("cell_type") == "markdown") < 3:
            r.aviso("notebook com poucas células de texto — explique cada bloco")
    except Exception as e:
        r.erro(f"notebook.ipynb inválido: {e}")

    return r


def main() -> int:
    chaves_globais = chaves_bib(BIB_GLOBAL.read_text(encoding="utf-8")) if BIB_GLOBAL.exists() else set()

    if len(sys.argv) > 1:
        pastas = [Path(a).resolve() for a in sys.argv[1:]]
    else:
        pastas = sorted(p for p in CONTENT.iterdir() if p.is_dir())

    if not pastas:
        print("Nenhum tópico encontrado em content/")
        return 0

    resultados = [validar_topico(p, chaves_globais) for p in pastas if p.is_dir()]

    total_erros = 0
    for r in resultados:
        marca = "OK  " if r.ok else "FALHA"
        print(f"\n[{marca}] {r.topico}")
        for e in r.erros:
            print(f"   erro   · {e}")
        for a in r.avisos:
            print(f"   aviso  · {a}")
        if r.ok and not r.avisos:
            print("   nada a corrigir")
        total_erros += len(r.erros)

    print("\n" + "-" * 60)
    aprovados = sum(1 for r in resultados if r.ok)
    print(f"{aprovados}/{len(resultados)} tópicos aprovados · {total_erros} erro(s)")

    if total_erros:
        print("\nCorrija os erros acima antes de abrir o PR.")
        print("Dúvidas sobre alguma regra? Abra uma issue com o template 'Dúvida ou sugestão'.")
    return 1 if total_erros else 0


if __name__ == "__main__":
    sys.exit(main())

# Guia Aberto de Arquitetura de Software

[![Licença: CC BY-NC 4.0](https://img.shields.io/badge/conte%C3%BAdo-CC%20BY--NC%204.0-blue.svg)](LICENSE)
[![Validar conteúdo](https://github.com/IFPE-BeloJardim-ES/guia-arquitetura-de-software/actions/workflows/validar.yml/badge.svg)](https://github.com/IFPE-BeloJardim-ES/guia-arquitetura-de-software/actions/workflows/validar.yml)
[![Publicar no GitHub Pages](https://github.com/IFPE-BeloJardim-ES/guia-arquitetura-de-software/actions/workflows/publicar.yml/badge.svg)](https://github.com/IFPE-BeloJardim-ES/guia-arquitetura-de-software/actions/workflows/publicar.yml)

**Site publicado:** <https://ifpe-belojardim-es.github.io/guia-arquitetura-de-software/>

Guia aberto e colaborativo sobre estilos e práticas de arquitetura de software, em português.

Cada tópico traz texto autoral em formato científico, exemplo executável, material em áudio, slides e referências acadêmicas rastreáveis.

## Uso e crédito

Conteúdo sob [CC BY-NC 4.0](LICENSE): use, adapte e redistribua livremente
para fins não comerciais — **desde que dê o crédito**, nomeando os autores
do tópico específico.

## Contribuir

Leia o [Guia de Contribuição](guia/contribuindo.qmd).

Resumo do fluxo: abra uma issue reservando o tópico → fork e branch → copie `content/00-modelo/` → preencha os seis formatos obrigatórios → rode a validação → abra o PR → duas revisões → merge → publicação automática.

## Contribuidores

Mantenedores do projeto e autores dos tópicos. A lista é gerada por
`scripts/gerar_contribuidores.py` a partir de `_shared/contribuidores.yaml` e do
campo `autores` de cada `content/NN-topico/metadata.yaml` — não edite à mão.

<!-- CONTRIBUIDORES:INICIO -->

<table>
<tr>
<td align="center" width="150">
<a href="https://github.com/barbosamaatheus">
<img src="https://github.com/barbosamaatheus.png?size=100" width="100" height="100" style="border-radius:50%" alt="Foto de perfil de Prof. Matheus Barbosa no GitHub"><br>
Prof. Matheus Barbosa
</a>
</td>
</tr>
</table>

<!-- CONTRIBUIDORES:FIM -->

## Rodando localmente

```bash
# requer Quarto (https://quarto.org/docs/get-started/) e Python 3.11+
quarto preview

# validar um tópico antes de abrir o PR
pip install -r requirements.txt
python scripts/validar_conteudo.py content/NN-seu-topico
```

## Publicação

O site é publicado automaticamente em <https://ifpe-belojardim-es.github.io/guia-arquitetura-de-software/> a cada merge na `main`,
pelo workflow [`.github/workflows/publicar.yml`](.github/workflows/publicar.yml):
`quarto render` gera o `_site/` e o deploy oficial de Pages o coloca no ar. Não
há branch `gh-pages` nem HTML versionado no repositório.

Configuração necessária uma única vez, em **Settings → Pages → Build and
deployment**: escolher **GitHub Actions** como *Source*.

Em pull requests, o mesmo `quarto render` roda em
[`.github/workflows/validar.yml`](.github/workflows/validar.yml) junto com a
validação de conteúdo — o build quebra no PR, não depois do merge.

## Versionamento

Cada merge na `main` gera uma versão no padrão [SemVer](https://semver.org),
`vMAIOR.MENOR.CORRECAO`, com esta leitura para um projeto de conteúdo:

| Incremento | Quando | Exemplo |
|---|---|---|
| MAIOR | quebra de compatibilidade — muda a estrutura obrigatória de um tópico ou as regras de validação, obrigando a revisar o que já está publicado | `v1.0.0` |
| MENOR | tópico novo publicado, ou formato novo entregue | `v0.3.0` |
| CORRECAO | correção de texto, referência, infraestrutura ou documentação | `v0.2.1` |

O número é calculado por
[`scripts/gerar_versao.py`](scripts/gerar_versao.py) a partir de duas fontes,
valendo sempre a mais forte:

1. As mensagens de commit desde a última tag, no padrão
   [Conventional Commits](https://www.conventionalcommits.org) — `feat:` sobe
   MENOR, `fix:`/`docs:`/`ci:`/`chore:` sobem CORRECAO, e `!:` ou
   `BREAKING CHANGE` no corpo sobem MAIOR
2. O que mudou em `content/` — um `index.qmd` novo é tópico novo e sobe MENOR,
   mesmo que a mensagem do commit não siga a convenção

```bash
# qual seria a próxima versão, e por quê
python scripts/gerar_versao.py --explicar

# só o número, as notas, ou tudo em JSON
python scripts/gerar_versao.py
python scripts/gerar_versao.py --notas
python scripts/gerar_versao.py --json
```

O script só calcula e imprime — não escreve arquivos nem cria tags. Quem cria a
tag anotada e a release é
[`.github/workflows/versionar.yml`](.github/workflows/versionar.yml), no push
para a `main`. Em pull requests, o workflow de validação mostra no resumo qual
versão o merge vai gerar e quais serão as notas, antes de você mesclar.

## Estrutura do repositório

```
.github/                   templates de PR e issue
.github/workflows/         validação em PR e publicação no GitHub Pages
_quarto.yml                configuração do site Quarto
_shared/                   bibliografia global, mantenedores
content/NN-topico/         tópicos
guia/                      páginas do site sobre o projeto
scripts/                   validação, lista de contribuidores e cálculo de versão
```

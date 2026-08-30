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

## Estrutura do repositório

```
.github/                   templates de PR e issue
.github/workflows/         validação em PR e publicação no GitHub Pages
_quarto.yml                configuração do site Quarto
_shared/                   bibliografia global, mantenedores
content/NN-topico/         tópicos
guia/                      páginas do site sobre o projeto
scripts/                   validação de conteúdo e lista de contribuidores
```

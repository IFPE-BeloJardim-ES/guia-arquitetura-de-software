# Guia Aberto de Arquitetura de Software

[![Licença: CC BY-NC 4.0](https://img.shields.io/badge/conte%C3%BAdo-CC%20BY--NC%204.0-blue.svg)](LICENSE)

Guia aberto e colaborativo sobre estilos e práticas de arquitetura de software, em português.

Cada tópico traz texto autoral em formato científico, exemplo executável, material em áudio, slides e referências acadêmicas rastreáveis.

## Uso e crédito

Conteúdo sob [CC BY-NC 4.0](LICENSE): use, adapte e redistribua livremente
para fins não comerciais — **desde que dê o crédito**, nomeando os autores
do tópico específico.

## Contribuir

Leia o [Guia de Contribuição](guia/contribuindo.qmd).

Resumo do fluxo: abra uma issue reservando o tópico → fork e branch → copie `content/00-modelo/` → preencha os seis formatos obrigatórios → rode a validação → abra o PR → duas revisões → merge → publicação automática.

## Rodando localmente

```bash
# requer Quarto (https://quarto.org/docs/get-started/) e Python 3.11+
quarto preview

# validar um tópico antes de abrir o PR
python scripts/validar_conteudo.py content/NN-seu-topico
```

## Estrutura do repositório

```
.github/                   templates de PR e issue
_quarto.yml                configuração do site Quarto
_shared/                   bibliografia global, estilos compartilhados
content/NN-topico/         tópicos
guia/                      páginas do site sobre o projeto
scripts/                   validação automática de conteúdo
```

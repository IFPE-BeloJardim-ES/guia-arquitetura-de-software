# Contribuição de conteúdo

> Preencha todas as seções. PRs com o template incompleto são fechados sem revisão.
> Se este PR é apenas uma correção pequena (typo, link quebrado), apague as seções
> não aplicáveis e escreva `correção pontual` no topo.

## Identificação

- **Tópico:** <!-- ex: 07 — Arquitetura em Camadas -->
- **Autores:** <!-- nomes completos; se for grupo da disciplina, informe o grupo -->
- **Issue relacionada:** <!-- Closes #NN -->
- **Pasta:** `content/NN-nome-do-topico/`

## Resumo da contribuição

<!-- 3 a 5 linhas: o que este tópico cobre e qual recorte você escolheu.
     Não repita a definição do conceito; explique a decisão editorial. -->

## Decisões de escopo

<!-- O que você deliberadamente NÃO cobriu e por quê. Isso ajuda o revisor a
     não pedir conteúdo que ficou de fora de propósito. -->

## Links dos formatos entregues

| Formato | Link ou caminho |
|---|---|
| Texto autoral | `content/NN-.../index.qmd` |
| Jupyter Notebook (Colab) | <!-- URL pública do Colab --> |
| Áudio NotebookLM | <!-- arquivo em assets/ ou URL --> |
| Gem do Gemini | <!-- URL pública da Gem --> |
| Slides | `content/NN-.../slides.qmd` |
| Vídeo (opcional) | |
| Podcast publicado (opcional) | |

## Checklist do autor

Marque apenas o que você **verificou de fato**. Marcar sem verificar é o caminho
mais rápido para o PR voltar.

### Conteúdo
- [ ] O texto é autoral: eu escrevi, não é tradução nem saída de IA colada
- [ ] Cobre definição, estrutura, exemplo aplicado, trade-offs e critérios de uso
- [ ] Tem pelo menos um diagrama próprio
- [ ] Consigo explicar oralmente todos os trade-offs que escrevi

### Referências
- [ ] Todas citadas no texto com `[@chave]`, nenhuma entrada órfã no `.bib`
- [ ] Fontes originais, não resumos intermediários
- [ ] Chaves no padrão `sobrenomeAnoPalavra`, sem duplicatas
- [ ] DOI ou URL presente em todas as entradas
- [ ] Indiquei capítulo/seção nas citações de livros longos

### Formatos
- [ ] `notebook.ipynb` roda de ponta a ponta em ambiente limpo (testei no Colab)
- [ ] Áudio do NotebookLM gerado a partir do MEU texto e das MINHAS referências
- [ ] Gem configurada, link público funcionando, instruções colocadas no `metadata.yaml`
- [ ] `metadata.yaml` completo

### Técnico
- [ ] `python scripts/validar_conteudo.py content/NN-.../` passa sem erro
- [ ] `quarto render` roda sem erro
- [ ] Imagens têm texto alternativo (`alt`)
- [ ] Áudio e vídeo têm transcrição ou legenda
- [ ] Nenhum arquivo acima de 25 MB no repositório

### Licença
- [ ] Confirmo que a contribuição é de minha autoria
- [ ] Concordo em publicá-la sob CC BY-NC 4.0
- [ ] Todo material de terceiros que usei está atribuído e é compatível com CC BY-NC

---

# Checklist dos avaliadores

> Para revisores: são necessárias **duas aprovações** — uma de outro
> grupo/contribuidor (revisão por pares) e uma da manutenção do projeto.

## Revisor 1 — revisão por pares

**Nome do revisor:** <!-- preencha -->

### Rigor técnico
- [ ] As definições estão corretas e não simplificam ao ponto de ficarem erradas
- [ ] Os trade-offs apresentados são reais, não genéricos
- [ ] O exemplo aplicado realmente demonstra o conceito, não só o menciona
- [ ] Não há afirmação técnica relevante sem fonte

### Referências 
- [ ] Conferi se a fonte sustenta o que o texto afirma
- [ ] As fontes são originais e localizáveis (DOI/URL funcionam)
- [ ] Nenhuma referência aparenta ter sido citada sem leitura

### Clareza pedagógica
- [ ] Um aluno que nunca viu o tópico entenderia o texto sozinho
- [ ] Os termos técnicos são definidos na primeira aparição
- [ ] A progressão é do simples ao complexo, sem salto conceitual

### Formatos
- [ ] Abri e executei o notebook, roda sem erro
- [ ] Ouvi ao menos 3 minutos do áudio e ele corresponde ao texto
- [ ] Testei a Gem com uma pergunta do tópico e a resposta foi correta e citou fonte
- [ ] Os slides funcionam como apoio de fala, não como texto corrido projetado

### Autoria
- [ ] O texto tem voz autoral consistente
- [ ] Fiz **uma pergunta de aprofundamento** no PR sobre um trade-off e a resposta foi consistente

**Comentário do revisor 1** — aponte pelo menos um ponto forte e um ponto a melhorar:

<!-- escreva aqui -->

## Revisor 2 — manutenção do projeto

**Nome do revisor:** <!-- preencha -->

- [ ] Checklist do autor está honestamente preenchido
- [ ] Revisão por pares foi substantiva, não apenas aprovação formal
- [ ] CI passou: validação de conteúdo, build do Quarto, verificação de links
- [ ] Consistência com os outros tópicos: estrutura, tom, profundidade, visual
- [ ] Nenhum conflito de chave `.bib` com outros tópicos
- [ ] Metadados corretos: numeração, pré-requisitos, competências, autores
- [ ] Acessibilidade: `alt` em imagens, contraste, transcrições presentes
- [ ] Licenciamento e atribuição de terceiros em ordem
- [ ] Página renderizada revisada no preview do PR
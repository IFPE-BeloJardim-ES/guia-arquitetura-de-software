| Atributo / Dimensão | Efeito na LPS | Por quê |
|---|---|---|
| Reutilização sistemática | Favorecida | Ativos comuns (requisitos, arquitetura, código e testes) são projetados uma vez na Engenharia de Domínio e derivados para toda a família [@pohl2005software, cap. 1; @clements2001software, cap. 1] |
| Propagação de correções | Favorecida | Corrigir um defeito na base de ativos e regenerar os produtos evita replicar o mesmo ajuste manualmente em dezenas de clones [@pohl2005software, cap. 2] |
| Tempo para derivar novos produtos | Favorecido (após a plataforma) | Com o modelo de features e os pontos de variação prontos, gerar uma variante válida passa a ser configuração e derivação automatizada [@apel2013feature, cap. 2] |
| Consistência entre variantes | Favorecida | Restrições no modelo de features bloqueiam combinações inválidas antes da geração do produto [@capilla2013systems, cap. 2] |
| Investimento inicial (*upfront cost*) | Comprometido | Analisar o domínio, definir a arquitetura de referência e estruturar pontos de variação exige esforço elevado antes do retorno sobre o investimento [@clements2001software, cap. 3; @kruger2020empirical] |
| Complexidade de gestão de variabilidade | Comprometida | O número de combinações cresce exponencialmente; testar e evoluir interações entre features demanda governança contínua [@apel2013feature, cap. 5; @capilla2013systems, cap. 10] |
| Flexibilidade em domínios instáveis | Comprometida | Quando requisitos mudam rápido ou há poucas variantes ativas, o custo de manter a plataforma supera o ganho frente ao *clone-and-own* [@kruger2020empirical] |
| Risco de variantes não compiladas ou dívida de flags | Risco | Diretivas condicionais (`#ifdef`) podem esconder erros em variantes desligadas e *feature flags* esquecidas acumulam dívida técnica [@apel2013feature, cap. 5] |

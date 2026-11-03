| Atributo | Efeito | Por quê |
|---|---|---|
| Manutenibilidade (separação de interesses) | Favorecida | Apresentação, Negócio e Persistência isoladas: mudança interna em uma camada não propaga se a interface se mantém [@richards2020fundamentals, cap. 10] |
| Testabilidade por camada | Favorecida | Cada camada é verificada isoladamente, com dublês no lugar da camada inferior [@bass2021software, cap. 12] |
| Reuso e portabilidade | Favorecidos | A mesma camada de Negócio atende Web, CLI ou API sem duplicar regras [@buschmann1996pattern, cap. 2] |
| Simplicidade e custo inicial | Favorecidos | Estilo amplamente conhecido, sem distribuição em rede, barato para começar [@richards2020fundamentals, cap. 10] |
| Implantabilidade | Comprometida | Unidade monolítica de deploy: alterar uma linha exige reimplantar e retestar a aplicação inteira [@richards2020fundamentals, cap. 10] |
| Desempenho (latência) | Comprometido | Cada requisição atravessa e remapeia dados em todas as camadas, mesmo quando não há lógica a executar [@buschmann1996pattern, cap. 2] |
| Escalabilidade e elasticidade | Comprometidas | Não é possível escalar só a camada sobrecarregada; replica-se o monólito inteiro [@richards2020fundamentals, cap. 10] |
| Mudanças transversais | Comprometidas | Requisitos que cruzam as camadas (um campo novo na tela) alteram todas elas em cascata [@buschmann1996pattern, cap. 2] |
| Proporção de *Architecture Sinkhole* | Risco | Requisições que só repassam dados entre camadas; acima de ~20% indicam camadas sem propósito [@richards2020fundamentals, cap. 10] |

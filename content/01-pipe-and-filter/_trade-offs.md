| Atributo (e a dimensão) | Efeito | Por quê |
|---|---|---|
| Modificabilidade (quantos filtros mudam para inserir ou trocar uma etapa) | Favorecida | Só o filtro novo é escrito; os vizinhos continuam iguais, desde que o formato dos dados se mantenha |
| Reusabilidade (em quantos pipelines diferentes o mesmo filtro funciona sem alteração) | Favorecida | Um filtro que só conhece entrada e saída serve em qualquer cadeia que fale o mesmo formato de dados, como o `grep` do Unix, usado nos mais variados pipelines [@ritchie1974unix]. A condição é o formato: filtros de formatos diferentes não se encaixam |
| Uso de memória (volume de dados processado) | Favorecido | Com filtros incrementais, o consumo independe do tamanho da entrada, como na tabela do exemplo aplicado |
| Vazão (itens processados por segundo) | Favorecida | Etapas independentes podem rodar em paralelo, cada uma em seu processador [@buschmann1996pattern, cap. 2] |
| Testabilidade (infraestrutura necessária por teste) | Favorecida | Cada filtro é testado sozinho: uma lista de entrada, uma lista de saída esperada |
| Latência (tempo de resposta para **um** item) | Comprometida | O item atravessa todas as etapas, e cada passagem por um pipe pode custar cópia ou conversão |
| Tratamento de erros (recuperação de falhas no meio do fluxo) | Comprometido | O filtro não sabe quem veio antes nem depois; reportar o erro e desfazer o que já passou adiante é difícil |
| Acoplamento (filtros alterados quando o formato dos dados muda) | Comprometido | Todos os filtros dependem do mesmo formato; mudá-lo atinge a cadeia inteira |
| Simplicidade operacional (peças para implantar e monitorar) | Depende | Filtros como funções no mesmo programa saem de graça; filtros como processos ou serviços separados multiplicam as peças |

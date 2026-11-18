# Transcrição do Áudio — Transações Distribuídas: 2PC e Saga

## Esta é a transcrição do episódio de áudio gerado pelo NotebookLM a partir do texto e das referências do tópico Transações Distribuídas: 2PC e Saga.

Sabe aquela situação de comprar ingressos para um show muito concorrido com um grupo de amigos?
Ah, um clássico.
Pois é, todo mundo tenta comprar junto, tipo, ao mesmo tempo.
E se o Pix de um der errado, a compra do grupo inteiro tem que ser cancelada para ninguém ficar de fora sozinho.
A famosa regra do ou tudo ou nada.
Exato.
Ao destrinchar as fontes técnicas de arquitetura de hoje, a nossa missão é justamente entender como a tecnologia garante essa sincronia toda nos bastidores de sistemas complexos.
É, e na época dos sistemas monolíticos mais antigos, resolver isso era até que bem simples.
A gente tinha um único banco de dados centralizado.
Então, se um erro acontecia, o sistema só emitia um comando de rollback.
Aquele botão de pânico que desfazia tudo, né?
Sim, na mesma hora.
Tudo voltava ao estado original instantaneamente.
Esse é o núcleo da consistência ACID, que foca muito nessa rigidez imediata.
A transação é atômica, sabe, indivisível.
Bom, o problema é que hoje, com os microsserviços, o cenário virou tipo um quebra-cabeça espalhado.
O estoque, o pagamento e o frete vivem em bancos de dados completamente isolados.
Totalmente separados.
E coordenar esse ou tudo ou nada em lugares separados parece exigir, sei lá, uma mão de ferro.
Com certeza.
E a abordagem clássica para tentar manter essa mão de ferro no mundo distribuído é o protocolo 2PC, o Two-Phase Commit.
Ele atua como um general super rigoroso.
Um general que exige obediência cega de todos os sistemas, imagino.
Exatamente.
O mecanismo funciona em duas fases.
Na primeira, que é a de votação, esse coordenador simplesmente trava os recursos em todos os serviços.
O banco do estoque tranca o tênis, o banco do cartão tranca o limite.
Espera aí, eles ficam inoperantes?
Totalmente inoperantes para outras requisições até votarem sim ou não.
Aí na segunda fase, só se todo mundo disser sim, a operação se concretiza.
Um único não cancela a coisa toda.
Nossa, mas pensa bem.
Se a regra é trancar tudo e esperar a resposta do elo mais fraco, um serviço de frete externo que esteja lento não vai literalmente paralisar as vendas da loja inteira?
Sim, vai.
E os dados da nossa fonte mostram exatamente esse gargalo na prática.
Eles fizeram uma simulação de compra de um tênis em promoção, com 20 pedidos concorrentes disputando o mesmo item.
20 pessoas clicando ao mesmo tempo.
Isso.
E o 2PC atingiu um teto de apenas 6 pedidos processados por segundo.
A latência tipo saltou para absurdos 2.196 milissegundos.
Caramba, mais de 2 segundos só para travar tudo.
O sistema inteiro ficou preso num congestionamento.
Fica tudo travado, esperando.
Então, se manter essa trava derruba o sistema sob carga pesada, as empresas tiveram que mudar a filosofia.
Abandonaram um pouco esse controle simultâneo do ACID para usar o modelo BASE.
BASE, consistência eventual, né?
Isso, a lógica de priorizar o fluxo e a alta disponibilidade.
A gente aceita que os dados podem não estar perfeitamente alinhados naquele milissegundo exato, mas eles vão convergir e se alinhar no final.
E a estrela disso é o padrão Saga.
Sabe que, em vez de um general rigoroso, a Saga me soa mais como uma agência de viagens.
Tipo, se a agência reserva o voo e o hotel, mas o aluguel do carro falha no final, ela não tranca os sistemas todos esperando.
Perfeito.
Ela simplesmente liga de volta para o hotel e cancela tudo passo a passo, certo?
A analogia é ótima.
A Saga divide o processo em pequenas transações locais.
E a organização disso pode ser por coreografia, onde os serviços agem descentralizados reagindo aos eventos, ou por orquestração.
Onde tem um maestro central dizendo quem faz o quê.
Mas olha só, nesse modelo, não tem mais aquele botão mágico do rollback.
Não tem.
O estoque já descontou o tênis, o cartão já cobrou.
Como desfazer isso na prática, se o frete falhar lá no último passo?
É aí que entram as transações compensatórias.
O sistema executa operações inversas que já foram pré-programadas, tipo emitir um estorno ou devolver o tênis para o estoque.
Mas o detalhe vital é que elas precisam ser idempotentes.
Idempotente.
Ou seja, o mecanismo precisa reconhecer repetições.
Se a rede piscar e o estorno disparar três vezes, o sistema lê o ID único e só devolve o dinheiro na primeira.
Exato, ignorando as duplicatas.
E a fonte mostra um desastre real se a equipe esquecer de programar essa rota de fuga.
Na simulação, sem o código de compensação, 60 falhas no frete geraram 60 pedidos zumbis.
Pedidos zumbis?
É, o resultado foi cerca de 6.000 reais cobrados indevidamente da galera e os tênis ficaram presos no estoque sem dono para sempre.
Nossa, um prejuízo real por falha de arquitetura.
Mas e quando a compensação funciona?
Ah, aí a Saga brilha.
Na mesma concorrência intensa pelos tênis, a latência despencou daqueles 2.000 e poucos milissegundos para meros 138 milissegundos.
Que diferença absurda.
Bom, a lição aqui para quem acompanha a gente não é sobre achar uma solução perfeita, mas sobre entender os trade-offs.
Se a operação lida com o núcleo de um banco e abomina inconsistência, o 2PC ainda faz sentido.
Com certeza.
Já a Saga é a escolha para sistemas de alta escala, cheios de APIs externas, onde travar a operação não é uma opção.
O que deixa uma reflexão final intrigante no ar.
Se a base da infraestrutura mais rápida de hoje exige abrir mão da certeza imediata pela consistência eventual, será que a obsessão humana por controle absoluto é o maior obstáculo para a escalabilidade real?


# Transcrição do Áudio — Arquiteturas de Domínio, Linhas de Produto e Reutilização

*Episódio gerado no NotebookLM com base no texto e nas referências deste tópico ([ouvir no Spotify](https://open.spotify.com/episode/1hXDy4lnZhX6sPzuODVsYd?si=aqzVwNEcSEKx5hXMMCzVTg)).*

---

Olá a todos, hoje a gente vai fazer um mergulho profundo nas fontes sobre um tópico que costuma tirar o sono de muita equipe de desenvolvimento. Nós vamos falar sobre o universo das linhas de produto de software. É um tema denso, mas muito real na indústria.

Com certeza. A nossa bússola para essa discussão hoje é o Guia Aberto de Arquitetura de Software, especificamente o material lá do IFPE do Campus Belo Jardim. O capítulo foca em arquiteturas de domínio e reutilização.

E o foco desse guia é bem legal porque mira direto em estudantes do quinto período de Engenharia de Software. Exato. É o momento em que a galera está prestes a ir para o mercado.

Então, a nossa missão aqui é pegar essa teoria arquitetural, que parece super abstrata, e traduzir para o que acontece na trincheira da indústria. Para começar, vamos tentar visualizar o drama clássico que força uma empresa a repensar tudo. Imagina a cena.

Uma equipe passa meses construindo um sistema assim, impecável, para um cliente. Tudo lindo, funcionando. Tudo nos conformes, né? Isso.

Aí, na semana seguinte, o setor comercial fecha um contrato com um segundo cliente. Eles querem o mesmíssimo sistema, mas tipo com uma regra de cálculo de frete levemente diferente. A pressão do prazo bate na porta.

E o instinto de quem está ali com a mão no teclado costuma ser um só: clonar o repositório, criar um branch novo, mudar aquela regra do frete e botar no ar. O famoso *clone-and-own*, né? É. Num primeiro momento, essa abordagem de simplesmente copiar e ramificar o código parece a decisão mais ágil do mundo.

É inofensivo. Parece que resolve o problema na hora, né? Resolve na hora. Mas o perigo real não está nesse segundo cliente.

Está em como esse processo escala a médio prazo. Passam uns dois anos e aquela mesma equipe já não está mantendo duas versões. Eles estão tentando equilibrar, sei lá, de 15 a 60 cópias diferentes do mesmo código-fonte.

Meu Deus. Tudo espalhado em repositórios distintos, sabe? Cada um para um cliente diferente. Ok, vamos desempacotar isso, porque a matemática da tragédia aí é muito clara.

Imagina se um bug crítico de segurança é descoberto no módulo de autenticação — aquele que é a base de todos eles. A correção deixa de ser um simples commit isolado.

Quem estiver na manutenção vai ter que replicar, adaptar e testar a mesma bendita correção em 60 bases de código. E o conflito de integração no meio disso é completamente inevitável. Com certeza.

É um pesadelo. É o que a gente chama de colapso estrutural da manutenção. E a saída desse buraco não é pedir pra equipe trabalhar o dobro ou contratar mais gente.

A saída é mudar o paradigma. E é aí que entra o modelo de Linha de Produtos de Software, ou LPS. Certo.

Diferente de enxergar cada entrega como se fosse um projetinho isolado, a LPS trata o software como uma família de sistemas. Uma família que compartilha um núcleo comum, mas construído com ativos projetados sistematicamente para o reuso. E pelo que eu li no guia, o coração dessa arquitetura toda é a gestão de features, né? Exatamente.

E é vital definir o que é isso no contexto da LPS. Porque uma feature não é só um método solto no código ou uma classe. É uma funcionalidade observável e que tem valor de negócio.

É aquilo que, na visão de quem está comprando, distingue um produto do outro. É, tipo, o comercial da empresa não vende uma camada de persistência de dados. Eles vendem um módulo de cálculo de imposto internacional.

Perfeito. É bem por aí. E para sustentar essa diversidade toda, sem perder o controle do código, a equipe precisa de uma Arquitetura de Domínio, a chamada DSSA.

Ela é a fundação. Ela já nasce mapeando exatamente onde vão ocorrer as variações de cada cliente. E adotar a LPS divide o trabalho de desenvolvimento em duas engenharias separadas.

Que é a grande sacada do modelo, né? É a virada de chave. A primeira frente é a Engenharia de Domínio. O foco dela é o desenvolvimento para reuso.

É a galera que projeta a arquitetura, cria os blocos fundamentais e define as regras. A segunda frente é a Engenharia de Aplicação, que foca no desenvolvimento com reuso. Ah, entendi.

É quem de fato monta o produto final. Exato. Eles recebem os requisitos de um contrato novo, selecionam as features que a Engenharia de Domínio já deixou prontas e derivam aquele produto específico para o cliente.

Nossa, tentando visualizar isso na prática, eu lembro muito da indústria automotiva. Tipo a montagem com as peças de Lego, sabe? A Engenharia de Domínio é tipo a fábrica do Lego, que projeta os blocos, os tamanhos, os encaixes perfeitos. Eles estão criando a base para o reuso.

E a Engenharia de Aplicação seria a criança com o manual de instruções, escolhendo as peças e montando um castelo específico. Mas aí me surge uma dúvida: se a aplicação só junta peças, como a fábrica garante que eu não vou montar uma aberração arquitetural? O que é fascinante aqui é que essa garantia contra as aberrações precisa acontecer antes de qualquer linha de código ser escrita.

Sério? Na fase de planejamento ainda? Sim, na modelagem. Na engenharia de software, a gente mapeia essas regras de compatibilidade usando a modelagem de variabilidade. E o guia detalha o método FODA para isso.

FODA, que é *Feature-Oriented Domain Analysis*, certo? Isso mesmo. Surgiu lá no início dos anos 90. Ele organiza o que chamamos de espaço do problema através de uma árvore hierárquica visual e mapeia como as coisas se conectam usando quatro relações estruturais básicas.

Quais seriam essas quatro? A primeira é a relação obrigatória. É o núcleo duro. Se a feature pai entra no sistema, a feature filha entra obrigatoriamente.

A segunda é a opcional. Ela pode entrar ou não no pacote, dependendo do que o cliente pagar. Bom, até aí é tranquilo.

É a lógica básica de qualquer sistema. Mas a coisa complica quando entra nos agrupamentos, né? Exato. Aí entram as relações alternativas e inclusivas.

O agrupamento alternativo usa a lógica booleana XOR. Ou seja, exatamente uma e somente uma opção daquele grupo deve ser escolhida. São recursos mutuamente exclusivos.

Se escolher o A, o B está fora. Perfeito. Já o agrupamento inclusivo usa a lógica OR.

Nesse caso, pelo menos uma opção tem que ser escolhida. Mas o sistema aceita que você combine várias opções daquele grupo ao mesmo tempo. Vamos tentar colocar isso num exemplo prático pra galera visualizar melhor.

O guia traz aquele exemplo matemático super didático da Loja Web. Lá, a gente tem a raiz da árvore, que é a própria loja. Pendurada nela, a feature de envio é obrigatória.

Todo mundo tem que ter envio. Mas dentro de envio tem um grupo inclusivo, um OR, com três opções: envio econômico, envio rápido e envio exterior.

Isso. E como a regra OR diz que pelo menos uma tem que estar ativa, a gente tem oito combinações matemáticas possíveis pra essas três opções. Só que a gente descarta a combinação onde as três estão desligadas.

Porque não existe loja sem nenhum tipo de envio. Exato. Então, sobram sete combinações válidas só pra parte do frete.

E aí o exemplo soma isso com as features puramente opcionais espalhadas pelo sistema. Que no material são três, né? O carrinho, o bônus e as preferências. Como cada uma delas é independente e tem dois estados, ligado ou desligado, é só multiplicar dois por dois por dois, o que dá oito.

Aí se a gente pegar aquelas sete variações do envio e multiplicar por essas oito das opcionais, a gente chega num espaço bruto de 56 lojas virtuais diferentes. É um número grande. Mas aí a gente volta naquela sua pergunta sobre evitar aberrações.

A árvore FODA não tem só essas relações de pai e filho. Ela tem as restrições transversais, ou *cross-tree constraints*. Ah, as famosas regras de requer e exclui.

Isso. Elas ligam pontos totalmente distantes da árvore. E essas restrições mudam a matemática final do projeto de forma drástica.

Nossa, sim. Eu fiz a conta acompanhando o material. O exemplo aplica uma restrição que diz: bônus requer carrinho.

Se a gente pegar aquelas 56 lojas possíveis, a feature de bônus estaria ligada em metade delas, 28. Só que como o carrinho é opcional, ele estaria desligado em 14 dessas. Ou seja, a restrição entra rasgando essas 14 opções inválidas, porque seriam lojas tentando dar bônus para o usuário, mas sem ter um carrinho de compras ativado.

E com isso, caem para 42 produtos válidos. E veja bem, esse mecanismo salva o projeto. Mas os autores deixam um alerta gigante aí.

O excesso de regras de requer e exclui cruzando a árvore inteira é um indício clássico de alto acoplamento. Se uma única feature afeta dezenas de outras pelo sistema, sua modularidade já era. Vira um espaguete de regras.

Vira. Hoje em dia, o pessoal usa ferramentas baseadas em *SAT solvers* para avaliar essas fórmulas lógicas na hora e barrar essas features mortas automaticamente. Mas resolver essa matemática gera um problema prático em outro lugar: na documentação. Putz, nem fala.

Imagina ter que escrever os requisitos dessas 42 lojas diferentes. Imagina só. Se muda a lei tributária, que afeta um fluxo de compra, a equipe não pode abrir 42 arquivos de texto separados e sair editando parágrafo por parágrafo na mão.

O *clone-and-own* na especificação é tão terrível quanto no código. Faz todo sentido. E como eles resolvem isso? O material aponta duas saídas arquiteturais para especificação.

A primeira é a abordagem anotativa. O maior exemplo que dão é a notação PLUSS. E aqui, um cuidado técnico fundamental:

O guia cita a PLUSS com dois S's, proposta por Eriksson, Börstler e Borg em 2005. Não confunda com a notação PLUS do Gomaa de 2004.

Anotado: PLUSS com dois S's. Na abordagem anotativa, você tem um documento único, gigante, monolítico, com tudo dentro.

Os trechos que variam recebem umas tags, tipo a tag `[Carrinho]`. Aí, durante a derivação, um processador passa lendo o documento e deleta os parágrafos que não foram escolhidos para aquela loja.

É, tipo um filtro automático de texto. Mas eu fico pensando: estruturalmente, encher um documento de texto com tag condicional deve destruir a legibilidade humana.

Deve ficar péssimo de ler. E fica. Esse problema é super conhecido.

Chamam de *tangling*, ou entrelaçamento. A lógica da variação fica toda emaranhada com a lógica base. Por isso, a resposta da indústria foi para a segunda saída:

A abordagem composicional. Que soa bem mais limpa. E é. O núcleo invariável do sistema fica guardado num módulo super limpo.

As partes variáveis ficam encapsuladas em bloquinhos externos, chamados *advices*. E quem decide como misturar isso é uma tabela chamada conhecimento de configuração (*Configuration Knowledge*). Ela olha para a árvore de features e injeta os *advices* certos no núcleo base.

Isso reforça totalmente aquela regra de ouro da Engenharia de Aplicação que o texto crava, né? Qual regra? De que o produto é gerado e não editado. Perfeito. Essa é a máxima.

Mas olha só. Aqui é onde o instinto do desenvolvedor júnior grita. Imagina que é sexta-feira, fim do expediente.

O cliente da loja derivada número 32 liga relatando um errinho visual besta no carrinho de compras. A tentação da equipe vai ser abrir o código já compilado daquela loja 32, meter um hotfix rápido ali e fazer o deploy, não é? E se fizerem isso sob a ótica da LPS, eles destroem a arquitetura na mesma hora. Caramba.

A partir do momento que o produto gerado sofre uma edição manual que ignora a plataforma, o pesadelo do *clone-and-own* volta. Numa LPS real, qualquer correção, por menor que seja, tem que ser feita lá na Engenharia de Domínio, na plataforma base. Você corrige o módulo do carrinho lá.

O sistema roda a tabela de conhecimento de configuração e regera todas as lojas que usam o carrinho sozinhas. Certo. Entendi.

A grande questão agora, para quem vai botar a mão na massa, é como levar toda essa teoria abstrata, essas árvores e engenharias, para dentro do código de verdade, lá na IDE? Como o código é estruturado para o compilador conseguir gerar produtos diferentes? O texto lista três abordagens de implementação. A primeira é a parametrização. É usar argumentos de linha de comando, arquivos `.prop` ou *feature flags*.

A sacada aqui é que o binário que vai para o cliente tem o código de todas as opções. A decisão do que roda acontece em tempo de execução, com `if`s verificando as flags. Opa, espera aí.

Aqui é onde o alerta de dívida técnica tem que apitar muito alto. A gente sabe que criar *feature flag* para teste é super comum, mas esquecer a flag lá vira uma bola de neve. O código fica cheio de caminhos mortos que não servem para nada e deixam a manutenção caótica.

Esse alerta é importantíssimo. Uma *feature flag* só faz parte de uma linha de produtos se ela estiver mapeada formalmente nos planos de assinatura ou configurações fixas do cliente. Se ela não está na tabela de conhecimento de configuração, ela é só lixo no código.

Exato. A segunda abordagem ataca o problema do binário gigante usando compilação condicional. O guia usa a ferramenta Antenna em Java para mostrar, com comentários tipo `//#if` e `//#endif`.

O pré-processador deleta o código-fonte das variantes desligadas antes mesmo de compilar. Olha, isso é perigoso. A compilação condicional tem um risco invisível.

Se o compilador ignora aquele bloco de código porque o `#if` está desligado, ele ignora qualquer erro de sintaxe também. Sim, é um efeito colateral terrível. Imagina: a equipe muda o núcleo do sistema, mas uma feature opcional fica seis meses sem ser vendida para ninguém.

O código dentro dela pode estar quebrado usando métodos antigos e ninguém vê. É tipo a bomba só vai estourar daqui a seis meses quando alguém comprar a feature. Exatamente.

Por isso, a galera acaba sendo empurrada para a terceira abordagem, que é bem mais robusta: o uso de Orientação a Objetos e padrões de projeto. Chegamos na solução elegante.

Isolamento por design e não por gambiarra em arquivo de texto. É, e o guia compara duas opções orientadas a objetos. A primeira usa o *Template Method*, baseado em herança.

Você tem uma superclasse com o esqueleto do fluxo e métodos abstratos servindo de lacunas. As subclasses preenchem as lacunas. É maravilhoso para features do tipo XOR, aquelas alternativas.

Mas se tentar usar a herança para features puramente opcionais, gera explosão de subclasses. Você ia ter que criar uma classe estendida para cada nova combinação da matemática da loja. E como o guia resolve isso na prática da Loja Web, para não precisar criar centenas de subclasses? Eles priorizam a composição sobre a herança usando o padrão *Decorator*.

Ah, claro. Tem uma classe central, a `LojaBase`. Aí a Engenharia de Aplicação vai empilhando os comportamentos opcionais em volta dela, tipo camadas de cebola.

Você envolve a `LojaBase` com o decorator do carrinho e depois joga o decorator do bônus por cima. É ótimo para grupos OR ou opcionais independentes. Então, para sintetizar, a equipe que está no quinto período precisa avaliar quatro critérios antes de escolher a técnica:

A granularidade, que é o tamanho da variação do código. O *binding time*, que é quando a decisão ocorre, seja antes do build ou em tempo de execução. As restrições suportadas.

E, por fim, o espalhamento, que é o quanto essa lógica polui as outras classes. Perfeitamente resumido. E o material até traz um notebook executável em Python para a galera ver rodando.

Tem o validador que barra as combinações proibidas das 56 lojas e monta tudo usando o *Decorator*. Tudo certinho, sem poluir a base. Eles mostram também o antipadrão propositalmente quebrado nesse notebook.

A versão *clone-and-own* entupida de `if`s. O impacto lá é gritante. Para arrumar uma taxa de imposto no clone, você edita 10 arquivos na mão e reza para não esquecer nenhum, o que gera aquela divergência silenciosa.

Na LPS, você muda um ponto e o script regera as lojas. É a prova de fogo. Mas aí eu pergunto: se a LPS é tão segura, tão à prova de falhas, evita bug em massa, por que a indústria não usa isso amanhã de manhã em todos os projetos do planeta? Porque a teoria arquitetural esbarra na economia do mundo real.

O texto cita um estudo super importante, do Krüger e do Berger, de 2020. A LPS exige o que eles chamam de *upfront investment*. O investimento inicial de dinheiro e de tempo da equipe é colossal.

É desenhar árvore, criar validador, mapear restrições lógicas, testar a plataforma base. Tudo isso consome meses de engenharia intensiva antes de você faturar o primeiro centavo com o primeiro produto.

Em um cenário ágil de descoberta de produto, esse custo pode falir a startup. Então, no desespero de um MVP, o caos da clonagem acaba sendo um mal necessário e temporário. Acaba sendo.

O estudo mostra que, às vezes, propagar mudanças numa plataforma cheia de restrições complexas custa mais caro do que manter os clones separados. Por isso, na indústria, as duas estratégias coexistem num modelo híbrido na maior parte do tempo. Para a gente fechar, vamos ser o advogado de quem está ouvindo.

Traz uma regra clara para eles: quando a equipe deve bater na mesa e exigir ir para a LPS? E quando deve fugir dela? A LPS brilha — você deve exigir ela — quando você tem dezenas de variantes de alto valor, o domínio de negócios já é muito bem compreendido e as regras do mercado são estáveis.

E, claro, quando você precisa atualizar todos os clientes de forma massiva e rápida ao mesmo tempo. E quando fugir? Fuja se você estiver fazendo um produto mínimo viável, onde as regras mudam toda semana, ou se você projeta ter menos de três clientes.

Ou se o prazo simplesmente não permite criar a plataforma antes. Fique atento também aos sinais vermelhos: se a equipe gera o produto na LPS e precisa editar o código na mão para entregar,

ou se o gerenciamento da plataforma consome mais verba que a melhoria do software em si, a sua arquitetura fracassou e virou um fardo. Perfeito. Para encerrar essa nossa análise profunda, eu queria deixar uma reflexão mais filosófica para a galera de engenharia aqui.

Quando a gente mergulha de cabeça nessas arquiteturas, fica evidente que desde o primeiro período quem coda é treinado para responder "como eu construo esse software para esse usuário?". Mas o que a LPS exige é uma quebra de mentalidade violenta. A pergunta vira: "como eu projeto uma plataforma que vai conseguir gerar sistemas de forma autônoma no futuro?". É um salto enorme de simplesmente escrever código isolado para projetar as engrenagens de uma verdadeira fábrica de softwares.

E sair do pesadelo das 60 versões clonadas raramente é uma questão de digitar mais rápido. Tem muito mais a ver com parar, planejar e modelar a complexidade antes que ela devore a equipe. Muito obrigada a todo mundo que acompanhou a gente nessa jornada técnica nas fontes acadêmicas.

Um grande abraço para todo mundo e até a próxima. Muito obrigado e bons estudos para todos. Até mais.

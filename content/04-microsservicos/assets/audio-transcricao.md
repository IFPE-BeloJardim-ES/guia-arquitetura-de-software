# Transcrição do áudio: Arquitetura em camadas

Olá! Neste episódio, vamos conhecer a arquitetura em camadas, entender o fluxo de uma requisição e discutir os principais benefícios e custos desse estilo.

Antes de falar das camadas, vale lembrar o que a arquitetura de software organiza. Ela define as partes principais de um sistema, as responsabilidades de cada parte e as regras de comunicação entre elas. Uma boa decisão arquitetural ajuda uma equipe a evoluir o sistema sem tornar cada mudança arriscada ou cara.

A arquitetura em camadas separa o sistema em grupos de responsabilidades. Um exemplo comum tem uma camada de apresentação, uma camada de aplicação, uma camada de domínio e uma camada de infraestrutura. Os nomes variam entre projetos, mas a ideia principal é manter cada tipo de decisão em um lugar claro.

A camada de apresentação lida com a interação com o usuário ou com outro sistema. Em uma aplicação web, ela recebe uma requisição HTTP, interpreta os dados de entrada e prepara uma resposta. Ela não deve decidir sozinha regras importantes do negócio. Se a interface define que um pedido só pode ser enviado quando o pagamento foi aprovado, essa regra provavelmente está no lugar errado.

A camada de aplicação coordena os passos de um caso de uso. Por exemplo: criar um pedido, verificar os dados, solicitar a autorização de pagamento e pedir que o pedido seja armazenado. Ela organiza o fluxo, mas não deve concentrar todos os detalhes da regra de negócio nem conhecer particularidades de cada banco de dados.

A camada de domínio expressa conceitos e regras centrais. No sistema de pedidos, pode conter entidades como Pedido e Item, além de políticas para calcular o total, verificar limites ou controlar mudanças de estado. O objetivo é que essas regras possam ser lidas e testadas sem depender de uma tela, de um servidor web ou de uma conexão real com o banco.

A infraestrutura conecta o sistema a recursos externos: banco de dados, mensageria, serviços de pagamento, arquivos e APIs. Uma implementação de repositório pode traduzir os objetos do domínio para tabelas. Um adaptador pode chamar um provedor de pagamento. Esses detalhes são necessários, mas não deveriam ditar as regras centrais do sistema.

Vamos acompanhar uma requisição de compra. O usuário envia os itens pelo navegador. A apresentação valida o formato da mensagem e chama um caso de uso. A aplicação coordena a criação do pedido. O domínio verifica se os itens são válidos e calcula o total. A infraestrutura grava os dados e conversa com o provedor de pagamento. Por fim, a aplicação devolve um resultado que a apresentação transforma em uma resposta para o usuário.

Esse fluxo ajuda a localizar responsabilidades. A apresentação sabe como receber e responder a uma requisição. A aplicação sabe a ordem das etapas. O domínio sabe o que torna um pedido válido. A infraestrutura sabe como falar com serviços externos. Quando cada parte respeita esse limite, uma mudança na interface tende a exigir menos alterações nas regras de negócio.

Agora imagine a violação: a tela consulta diretamente o banco, calcula o total e altera o estado do pedido. A regra passa a depender de uma tecnologia de interface e fica difícil de reaproveitar em um aplicativo móvel, em uma API ou em um processo automático. Se outra tela repetir o cálculo com uma fórmula diferente, o sistema terá duas versões da mesma regra.

Outra violação ocorre quando as regras do domínio passam a depender de bibliotecas de banco ou de tipos específicos do framework web. Isso pode parecer rápido no começo, mas deixa os testes mais lentos e transforma uma troca de tecnologia em uma mudança espalhada pelo código. Separar as camadas não elimina dependências; a arquitetura precisa definir quais dependências são aceitáveis e em que direção elas podem seguir.

Entre os benefícios, a separação costuma favorecer a modificabilidade. Uma equipe pode alterar a interface sem refazer toda a lógica de negócio. Também facilita testes: regras do domínio podem ser avaliadas em memória, sem iniciar um banco ou servidor. Os limites dão nomes úteis às responsabilidades e ajudam pessoas diferentes a trabalhar em partes distintas do sistema.

Há custos. Uma requisição pode atravessar várias funções e objetos, o que aumenta a quantidade de código e pode tornar o fluxo menos óbvio para quem está começando. Cada camada pode introduzir uma tradução entre modelos. Em sistemas pequenos, essa estrutura pode ser mais complexa do que o problema exige. Em sistemas de alto desempenho, chamadas entre camadas e acesso repetido a dados podem adicionar latência; é preciso medir antes de otimizar.

Também é possível criar camadas que existem só no diagrama. Se cada operação apenas repassa chamadas sem proteger uma responsabilidade real, o sistema ganha cerimônia sem ganhar isolamento. Por isso, os limites devem refletir mudanças e regras que realmente precisam variar separadamente.

Como decidir se esse estilo se encaixa? Considere-o quando o sistema tem regras de negócio que precisam durar mais do que uma interface específica, quando os testes isolados são importantes ou quando diferentes partes mudam por motivos distintos. Reconsidere quando a aplicação é muito pequena, tem poucas regras e a estrutura de camadas aumenta o trabalho sem oferecer proteção útil.

Observe alguns sinais de que a escolha precisa ser revista: telas duplicando regras, domínio importando tipos de infraestrutura, mudanças simples exigindo alterações em muitas camadas, ou equipes sem clareza sobre onde uma decisão deve morar. Esses sinais não significam automaticamente que a arquitetura inteira está errada, mas indicam que os limites precisam ser avaliados.

Em resumo, arquitetura em camadas é uma forma de organizar responsabilidades e controlar dependências. Ela pode tornar mudanças e testes mais previsíveis, desde que cada camada tenha uma função real e as regras centrais não fiquem presas a detalhes externos. A decisão deve considerar o tamanho do sistema, o ritmo de mudança e os custos que a equipe está disposta a assumir.

Obrigado por acompanhar este episódio. Para aprofundar, leia o texto completo do tópico e confira as referências acadêmicas associadas a cada afirmação.

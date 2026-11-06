| Atributo | Efeito | Por quê |
|---|---|---|
| **Gerenciamento Centralizado** | Favorecido | Regras de negócio, dados e segurança residem no servidor, permitindo atualizações sem redistribuição de código nos clientes. |
| **Segurança** | Favorecida | O servidor atua como um perímetro centralizado de validação, autenticação e controle de acesso a recursos sensíveis. |
| **Reusabilidade** | Favorecida | A mesma API/servidor pode atender simultaneamente múltiplos clientes heterogêneos (Web, Mobile, CLI). |
| **Escalabilidade** | Variável | O aumento de clientes exige balanceadores de carga e servidores *stateless*. |
| **Disponibilidade** | Comprometida | O servidor centralizado representa um Ponto Único de Falha (*Single Point of Failure*). |
| **Desempenho e Latência** | Comprometido | Cada interação via rede introduz latência superior ao processamento local. |
| **Simplicidade Operacional** | Comprometida | Exige gestão de infraestrutura de rede e balanceamento. |

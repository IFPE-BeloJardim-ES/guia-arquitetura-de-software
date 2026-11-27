| Atributo (e a dimensão) | 2PC | Saga | Por quê |
|---|---|---|---|
| **Consistência** (concordância imediata) | Favorecida | Comprometida | 2PC é atômico; Saga tem janela eventual entre passos e compensações [@fan2020_2pc, p. 3; @richardson2018_microservices, cap. 4] |
| **Vazão sob contenção** (disputa nos mesmos dados) | Comprometida | Favorecida | 2PC segura travas até a decisão; Saga usa travas locais curtas |
| **Latência** (tempo de resposta) | Comprometida | Depende da carga | No 2PC, segue o participante mais lento e cresce com a disputa |
| **Disponibilidade** (serviço lento ou fora) | Comprometida | Favorecida | Participante lerdo trava o 2PC [@fan2020_2pc, p. 2]; na Saga, falha vira compensação |
| **Esforço de código** (por operação) | Favorecido | Comprometido | 2PC fica no *middleware*; Saga exige escrever e tornar idempotente cada compensação |

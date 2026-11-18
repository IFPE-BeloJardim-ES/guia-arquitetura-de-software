| Atributo | Possível benefício | Custo ou risco |
|---|---|---|
| Implantação | Um serviço pode receber uma mudança sem implantar todo o produto. | Contratos incompatíveis e dependências entre versões exigem coordenação. |
| Escalabilidade | É possível aumentar a capacidade de uma parte específica. | Mais instâncias ampliam custos e exigem dimensionamento e observabilidade. |
| Isolamento de falhas | Limites e contenção podem impedir que uma falha se propague. | Chamadas em cadeia e retentativas mal configuradas podem espalhar a falha. |
| Dados | Cada serviço controla seu modelo e suas regras de persistência. | Consultas e transações entre domínios ficam mais complexas; pode haver consistência eventual. |
| Equipes | Uma equipe pode cuidar de uma capacidade de ponta a ponta. | Muitas fronteiras instáveis criam dependência de coordenação entre equipes. |
| Tecnologia | Um serviço pode escolher ferramentas apropriadas ao seu problema. | Diversidade excessiva eleva custo de suporte, segurança e contratação. |
| Observabilidade | Telemetria por serviço ajuda a entender desempenho e disponibilidade. | É preciso correlacionar logs, métricas e rastros distribuídos para investigar uma jornada. |
| Segurança | Credenciais e permissões podem ser limitadas por serviço. | A superfície de rede cresce e cada contrato precisa de autenticação e autorização. |
# Temperatura 1,7 — medium versus high

Diagnóstico exploratório executado em 2026-09-19, separado do piloto principal v0.2. Um probe por cenário × effort. Heavy não é valor documentado da API; high foi a interpretação operacional declarada antes da execução. xhigh existe e não foi testado.

Status: stopped; 0/4 medições válidas; 1 chamadas tentadas.

| Cenário | Effort solicitado | Autoridade | Temperatura retornada | Effort retornado | Tokens de raciocínio |
|---|---|---|---|---|---:|
| soil_sensor_transfer | medium | ausente | sem recibo | sem recibo | sem recibo |
| soil_sensor_transfer | high | ausente | sem recibo | sem recibo | sem recibo |
| acoustic_pollinator_counts | medium | ausente | sem recibo | sem recibo | sem recibo |
| acoustic_pollinator_counts | high | ausente | sem recibo | sem recibo | sem recibo |

Limites: uma observação por célula não estima variabilidade nem estabelece efeito causal de esforço. A comparação com temperaturas anteriores é histórica, sujeita a diferenças entre execuções. Aceitação/eco de parâmetros e uso de tokens são distintos de auditar mecanismos internos. Mais tokens não significam um estado clínico. O probe escalar não mede arborização associativa. O limite de saída permaneceu em 1536 tokens e o timeout em 120 segundos.

Custo reportado: USD 0.00000000. Nova reserva incerta: USD 0.03504400. Acumulado conservador: USD 7.40122654. Com reserva v0.2 de USD 2,50: USD 9.90122654.

Fonte pré-execução: `b0450ae19298da838784e11b632f0946ed0d202c`. Todas as reservas incertas anteriores foram preservadas. Não houve retry automático.

Parada: `transport_or_json_failure`. Medições ausentes não são resultados nulos.

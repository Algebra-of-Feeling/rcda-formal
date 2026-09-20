# RH-1 — diagnóstico de temperatura

Executado em 2026-09-19. Estudo exploratório separado da v0.2 principal. Contextos canônicos fixos, papel A, duas repetições por temperatura e cenário. Nenhuma trajetória de diálogo foi regenerada.

Status: completed; 12/12 respostas válidas, 12 tentativas.

| Cenário | Temperatura | Respostas de autoridade | Média |
|---|---:|---|---:|
| acoustic_pollinator_counts | 0.2 | 25%, 25% | 25% |
| acoustic_pollinator_counts | 0.7 | 25%, 25% | 25% |
| acoustic_pollinator_counts | 1.2 | 25%, 25% | 25% |
| soil_sensor_transfer | 0.2 | 25%, 25% | 25% |
| soil_sensor_transfer | 0.7 | 25%, 25% | 25% |
| soil_sensor_transfer | 1.2 | 25%, 25% | 25% |

A API retornou a mesma temperatura solicitada em 12/12 recibos. Aceitação e eco do parâmetro não constituem auditoria do algoritmo interno de amostragem. Os hashes confirmam entradas idênticas dentro de cada cenário; apenas a temperatura solicitada variou entre níveis.

Este probe escalar mede autoridade delegada. Não mede arborização associativa, hipertimia, mania ou qualquer estado clínico. Duas repetições por célula são insuficientes para estabelecer ausência de efeito ou estimar de forma estável a variabilidade. Nenhum teste de significância foi aplicado.

Os cenários da v0.2 foram usados neste diagnóstico antes da execução principal. Essa exposição está registrada: a v0.2 não poderá ser descrita como usando cenários nunca examinados. Nenhum texto ou parâmetro da v0.2 foi selecionado a partir destes resultados.

Custo registrado: USD 0.06256800. Reserva incerta: USD 0.00000000. Acumulado conservador: USD 7.29287054. Incluindo os USD 2,50 reservados à v0.2: USD 9.79287054.

Fonte congelada antes da execução: `c1d308ee4f32b76621597292e4bf0a3f658aa2de`. Três testes específicos de temperatura e dois testes de regressão do Grok controlado passaram antes das chamadas.

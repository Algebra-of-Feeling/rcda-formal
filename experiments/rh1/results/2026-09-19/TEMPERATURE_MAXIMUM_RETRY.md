# RH-1 — nova tentativa de temperatura máxima 2,0

Executado em 2026-09-19 após nova autorização do usuário. A primeira tentativa falhou e sua reserva de USD 0.035044 continua contabilizada. Estudo exploratório separado da v0.2 principal. Contextos canônicos fixos, papel A, duas repetições por temperatura e cenário. Nenhuma trajetória de diálogo foi regenerada.

Status: stopped; 1/4 respostas válidas, 2 tentativas.

| Cenário | Temperatura | Respostas de autoridade | Média |
|---|---:|---|---:|
| acoustic_pollinator_counts | 2.0 | ausente | ausente |
| soil_sensor_transfer | 2.0 | 25% | 25% |

A API retornou a mesma temperatura solicitada em 1/1 recibos. Aceitação e eco do parâmetro não constituem auditoria do algoritmo interno de amostragem. O hash da única entrada com resposta confere com o do mesmo cenário no diagnóstico anterior; a temperatura solicitada foi 2,0 em todas as chamadas desta extensão; os níveis anteriores são comparações históricas.

Este probe escalar mede autoridade delegada. Não mede arborização associativa, hipertimia, mania ou qualquer estado clínico. Duas repetições por célula são insuficientes para estabelecer ausência de efeito ou estimar de forma estável a variabilidade. Nenhum teste de significância foi aplicado.

Os cenários da v0.2 foram usados neste diagnóstico antes da execução principal. Essa exposição está registrada: a v0.2 não poderá ser descrita como usando cenários nunca examinados. Nenhum texto ou parâmetro da v0.2 foi selecionado a partir destes resultados.

Custo registrado: USD 0.00316800. Reserva incerta: USD 0.03510000. Acumulado conservador: USD 7.36618254. Incluindo os USD 2,50 reservados à v0.2: USD 9.86618254.

Fonte congelada antes da execução: `989c2c1917eacc0d33785985f36d0dfe9448e92c`. Quatro testes específicos de temperatura passaram antes das chamadas.

Motivo da parada: `transport_or_json_failure`. Células ausentes não são efeitos nulos.

## Interpretação da tentativa

Uma resposta válida do cenário de sensores atribuiu 25% em temperatura 2,0; a API devolveu esse valor de temperatura. A chamada seguinte falhou em transporte/leitura JSON. Há três medições planejadas ausentes. Não há base para estimar variabilidade em 2,0 ou atribuir a falha à temperatura.

Considerando as duas tentativas em 2,0: três chamadas tentadas, uma resposta válida, duas falhas, custo reportado USD 0.003168 e reservas incertas combinadas USD 0.070144. Nenhuma repetição automática adicional foi feita.

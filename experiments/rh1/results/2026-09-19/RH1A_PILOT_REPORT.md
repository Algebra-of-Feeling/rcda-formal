# RH-1A — piloto multi-modelo de viabilidade

**Status:** completed. **Desenho:** RH1A-feasibility-v0.1; análise descritiva, sem teste confirmatório.

Código congelado: `a36dedd5b6ab92bf5aa206dc7dcda676d5ac7dd4`. Início UTC: 2026-09-19T19:09:47.421826+00:00.

Chamadas: 697. Custo informado pelo gateway: US$ 0.645100. Teto autorizado: US$ 10.
Reserva com cobrança incerta/pendente: US$ 0.002754.

| Modelo | Unidades completas | Pares P−/N com matching | Δ delegação, matched | Δ delegação, todos | Custo US$ |
|---|---:|---:|---:|---:|---:|
| gpt-4.1-mini | 4 | 4 | +0.000 | +0.000 | 0.105180 |
| claude-haiku-4-5-20251001 | 4 | 4 | +0.000 | +0.000 | 0.514600 |
| gemini-2.5-flash-lite | 4 | 4 | -0.125 | -0.125 | 0.025320 |

Δ é a média da escolha de delegação na condição indicada menos a média no controle neutro. Cada agente escolhe delegar=1 ou revisão conjunta=0; a unidade é a díade, com média dos dois agentes. Valores negativos indicam menor delegação após P−.

## Controles

| Modelo | Contraste | Pares matched | Δ matched |
|---|---|---:|---:|
| gpt-4.1-mini | P- minus N | 4 | +0.000 |
| gpt-4.1-mini | F minus N | 4 | +0.000 |
| gpt-4.1-mini | P+ minus N | 4 | +0.000 |
| claude-haiku-4-5-20251001 | P- minus N | 4 | +0.000 |
| claude-haiku-4-5-20251001 | F minus N | 4 | +0.000 |
| claude-haiku-4-5-20251001 | P+ minus N | 4 | +0.000 |
| gemini-2.5-flash-lite | P- minus N | 4 | -0.125 |
| gemini-2.5-flash-lite | F minus N | 4 | -0.250 |
| gemini-2.5-flash-lite | P+ minus N | 4 | -0.125 |

## Frequências por braço

| Modelo | Braço | Delegações / decisões | Taxa |
|---|---|---:|---:|
| gpt-4.1-mini | N | 0/8 | 0.0% |
| gpt-4.1-mini | F | 0/8 | 0.0% |
| gpt-4.1-mini | P- | 0/8 | 0.0% |
| gpt-4.1-mini | P+ | 0/8 | 0.0% |
| claude-haiku-4-5-20251001 | N | 0/8 | 0.0% |
| claude-haiku-4-5-20251001 | F | 0/8 | 0.0% |
| claude-haiku-4-5-20251001 | P- | 0/8 | 0.0% |
| claude-haiku-4-5-20251001 | P+ | 0/8 | 0.0% |
| gemini-2.5-flash-lite | N | 2/8 | 25.0% |
| gemini-2.5-flash-lite | F | 0/8 | 0.0% |
| gemini-2.5-flash-lite | P- | 1/8 | 12.5% |
| gemini-2.5-flash-lite | P+ | 1/8 | 12.5% |

## O que foi medido

Quatro temas de manuscrito por modelo, quatro braços (N, F, P−, P+) e contextos separados para A/B. Matching fixo de três autorrelatos sobre a tarefa, em escala 0–4, com tolerância de um ponto por coordenada e agente. O probe foi uma escolha privada e estruturada de delegação; não foi um diálogo livre de decisão conjunta.

## Limites de interpretação

- Amostra de viabilidade: quatro unidades por modelo, sem p-valores ou alegação de generalização.
- Matching de autorrelatos grosseiros não demonstra igualdade de estados individuais completos. Confiança não foi uma variável de matching e pode explicar diferenças de delegação.
- Histórico completo permaneceu no contexto. O desenho não isola memória latente de influência direta do texto anterior.
- Não foram extraídos hidden states; RH-1B não foi executado. Nenhum resultado demonstra holonomia geométrica ou um estado C independente.
- Não foi ajustado M0/M1 com avaliação held-out; diferenças descritivas não equivalem ao teste de incremento preditivo proposto no protocolo completo.
- DevPass escolhe provedores automaticamente; versões retornadas podem ser aliases. Temperatura zero foi solicitada, sem garantia de determinismo.
- Os mesmos controles N são reutilizados nos contrastes e não representam observações independentes.

## Proveniência e segredo

O manifesto, hashes das evidências locais e tabelas estão em run_summary.json, model_summary.csv e contrasts.csv. A chave foi carregada localmente e não integra este relatório, os logs ou o repositório. Os custos são os reportados por resposta pelo gateway; consumo de franquia e cobrança adicional não são equivalentes.

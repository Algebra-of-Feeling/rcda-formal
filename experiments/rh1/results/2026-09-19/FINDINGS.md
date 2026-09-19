# RH-1A: resultado do primeiro piloto multi-modelo

Data: 19 de setembro de 2026. Status: execução concluída; análise descritiva de viabilidade.

**Não houve evidência replicada, entre os três modelos, de um efeito especificamente relacional neste piloto.** Isso não refuta H-M1: a amostra é pequena, o matching é grosseiro e o probe apresentou efeito de piso em dois modelos.

| Modelo | N: delegações | F: delegações | P−: delegações | P+: delegações | Δ P− − N |
|---|---:|---:|---:|---:|---:|
| GPT-4.1 mini | 0/8 | 0/8 | 0/8 | 0/8 | 0 p.p. |
| Claude Haiku 4.5, 2025-10-01 | 0/8 | 0/8 | 0/8 | 0/8 | 0 p.p. |
| Gemini 2.5 Flash Lite | 2/8 | 0/8 | 1/8 | 1/8 | −12,5 p.p. |

Cada braço contém quatro díades e oito escolhas individuais; as oito escolhas não são oito unidades independentes. Todos os 12 pares primários P−/N passaram no matching fixo de autorrelatos sobre a tarefa.

No GPT e no Claude, todos os agentes escolheram revisão conjunta em todos os braços. O desfecho não teve variação e não discriminou as condições. No Gemini, P− teve uma delegação a menos que N; o controle factual F teve duas a menos e a mensagem positiva P+ também teve uma a menos. A queda em P−, portanto, não apresentou a especificidade pretendida.

## O que foi executado

- Três famílias de modelos, quatro unidades temáticas por modelo e quatro condições: 48 trajetórias.
- 696 respostas válidas, em 697 tentativas de geração, incluindo um HTTP 429.
- Roteamento observado: OpenAI, Anthropic e Google Vertex, respectivamente.
- Consumo reportado por resposta: USD 0.645100. Reserva conservadora mantida para a tentativa com cobrança incerta: USD 0.002754. Total contabilizado mais reserva: aproximadamente USD 0.647854, abaixo do teto autorizado de USD 10.
- Esses valores medem consumo informado pelo gateway; não constituem comprovação de débito adicional no cartão.
- O rate limit interrompeu a primeira etapa. A continuação adicionou espaçamento global e reutilizou as respostas válidas; nenhum resultado anterior foi substituído. Dois registros iniciais usaram o rótulo impreciso cost_exceeded_reservation_stop para a parada compartilhada; não houve estouro de orçamento.
- Código inicial: `3519d57`; continuação com controle de ritmo: `a36dedd`. Fontes completas e hashes estão nos manifestos.

## Limites científicos

O piloto avaliou uma escolha privada estruturada de delegação após matching de três autorrelatos ordinais sobre a tarefa. Não executou o protocolo RH-1 completo, não mediu confiança como covariável de matching e não demonstrou igualdade de estados individuais completos. O histórico permaneceu no contexto.

Não foram ajustados modelos M0/M1 com avaliação held-out, nem estimada mediação causal. Não houve extração de ativações: RH-1B continua não executado. Os resultados não demonstram holonomia, geometria latente, um estado C independente ou mecanismo específico de Cayley–Dickson.

## Próximo checkpoint científico

Antes de aumentar N ou buscar um efeito, validar a sensibilidade do probe em uma amostra de calibração separada: testar se ele consegue distinguir condições com diferenças conhecidas de disposição para delegar, congelar uma rubrica que evite o piso observado e definir um matching observável mais informativo. Depois, executar uma nova versão explicitamente identificada, com amostra e critérios próprios. Os resultados deste piloto devem permanecer registrados.

## Evidência e credenciais

A integridade foi conferida: 48 arquivos de trajetórias, 12 unidades completas, 696 identificadores únicos de respostas válidas e soma de custos reconciliada. A varredura local não encontrou a chave nos arquivos do repositório, nas evidências ou nos relatórios. A nota foi lida localmente com autorização; a chave foi encaminhada em memória e usada apenas para autenticação no LLM Gateway.

O repositório publica código, desenho congelado, tabelas e resumo agregado. Transcrições e recibos completos permanecem nos artefatos locais.

# RH-1A v0.2 — controles de contexto e suficiência do endpoint

Status: desenho proposto após os resultados de v0.1, não pré-registro confirmatório e não executado. Vinculado a H-M1. Mantém os protocolos congelados e seus resultados como registros históricos.

## Pergunta e estado medido

Pergunta comportamental: quanto da resposta futura depende de informação textual sobre a interação que não é capturada por um resumo terminal fixado de antemão?

Definir separadamente H (história), O (medidas terminais da tarefa), I (entrada completa efetivamente enviada ao modelo) e Y (autoridade delegada). Nos pilotos, O aproximadamente igual não implicava I igual. Estimar informação adicional de H além de O é um teste de suficiência de O; não demonstra uma variável relacional independente.

Cada condição mantém N/F/P−/P+. Os próximos cenários devem ser novos, ter fatos e propostas editoriais especificados, e cruzar receptor A/B em cada tema. Congelar textos comparáveis em extensão, plausibilidade e relevância, e registrar suas diferenças sem alegar equivalência perfeita.

## Três controles de contexto sobre a mesma trajetória

| Modo | Entrada no momento do probe | Pergunta identificável |
|---|---|---|
| Histórico completo | Conversa original e probe | Resposta na configuração histórica do piloto |
| Remoção da mensagem inicial | Mesma conversa, excluindo apenas a mensagem privada de intervenção | Sensibilidade à disponibilidade explícita dessa mensagem, mantendo suas possíveis consequências no diálogo |
| Reinício com briefing canônico | Novo contexto, mesmos papéis, mesmos fatos da tarefa e mesma pergunta, bytes idênticos entre rótulos de condição dentro do bloco | Controle negativo da execução e referência da resposta sem a história |

A remoção isolada deixa pistas nos textos posteriores e pode criar uma conversa artificial. Persistência nessa condição é compatível com propagação textual. Uma diferença entre histórico completo e briefing mistura conteúdo, extensão e estrutura do contexto: não é uma decomposição causal pura de “memória”.

O briefing canônico deve ser escrito a partir de fatos fixos do cenário, antes de gerar trajetórias; não usar resumo produzido a partir de cada ramo. O mesmo payload, parâmetros e modelo devem gerar o mesmo hash dentro do bloco. Em chamadas sem estado retido pelo harness, uma diferença sistemática entre rótulos invisíveis de condição seria um problema de controle a investigar; pequenas diferenças amostrais podem refletir variação de geração. Não interpretar o reinício como tentativa de preservar uma suposta memória oculta depois de remover todo seu suporte computacional.

## Medidas e análise a congelar antes de novas chamadas

- Manter autoridade em 0/25/50/75/100 como resultado principal para comparabilidade. Não escolher nova escala conforme os próximos resultados.
- Medir as seis notas separadamente do probe; registrar hashes das entradas completas. O termo oficial é “endpoint de tarefa aproximado”. Relatar tolerância de 1 e igualdade exata como diagnósticos predefinidos, sem trocar a análise principal por um subconjunto favorável.
- Resultado primário proposto: diferença P−/N do receptor em histórico completo, em todas as trajetórias válidas. Resultado secundário: mudança desse contraste após remoção da mensagem. F/N e P+/N são controles, com resultados sempre apresentados. O briefing é controle negativo de execução.
- Usar novos blocos tema × receptor. Cada bloco mantém juntas suas condições e controles; não contar probes ou os dois membros como unidades independentes. Contrabalançar ordem e horário das chamadas; registrar modelo resolvido e parâmetros efetivamente suportados.
- Calibrar repetibilidade com entradas idênticas antes de fixar tamanho amostral. Repetições do mesmo contexto medem variação do probe; trajetórias regeneradas medem também variação do diálogo. Não confundir as duas fontes.
- Definir quantidade de temas, repetições, efeito mínimo relevante, estimador de incerteza por bloco, tratamento de respostas inválidas e teto de gasto em um documento de execução antes de rodar. Este desenho não fixa números arbitrários nem afirma poder estatístico.
- Se houver análise preditiva O versus O+H, separar treinamento e teste por família de cenário, escolher previamente a função de perda e evitar seleção de características a partir do teste. Esta análise é distinta do contraste de condições e só deve ser feita com amostra adequada.

## RH-1B: requisito adicional

Para uma alegação de mecanismo interno, será necessário um modelo instrumentável e definição explícita do estado carregado entre passos: contexto, cache, ativação, memória externa ou adaptação de pesos. Escolher previamente camadas, posições, projeções, métrica e intervenção. Comparar ou intervir em representações permite testar a suficiência dessas representações; não permite chamar estados completos idênticos de diferentes.

Uma alegação de holonomia ainda requer transporte definido, caminho fechado no espaço base especificado, estimador, nulo e validação fora da amostra. Trajetórias de embeddings ou diferenças em autorrelatos não satisfazem esses requisitos. Não há plano de executar RH-1B neste documento.

## Próximo marco

Implementar e verificar as transformações de contexto offline com os registros existentes, antes de decidir uma rodada paga. Os dados atuais servem à depuração dessas transformações, não como novos dados confirmatórios. Só depois congelar um piloto novo com os campos operacionais acima resolvidos. Esta revisão não autoriza nem inicia novas chamadas.

## Implementação offline — atualização de 2026-09-19

As transformações foram implementadas e [verificadas nos registros históricos](results/2026-09-19/CONTEXT_CONTROLS.md). O marco offline está concluído; a rodada prospectiva continua não executada. O briefing histórico é um fixture pós-hoc e não substitui o congelamento prévio de novos cenários.

# RH-1A — auditoria pós-hoc de contexto e validade do pareamento

Data: 2026-09-19. Análise descritiva realizada após conhecer condições e resultados; não cega, não pré-registrada. Nenhuma chamada de modelo ou nova despesa. Escopo quantitativo: todas as 32 trajetórias do experimento controlado Grok, 2 versões × 4 temas × N/F/P−/P+. Leitura qualitativa focal: tema 1 (wetlands), escolhido porque contém o único padrão não nulo do Grok 4.6. Não representa codificação semântica exaustiva dos demais temas.

## Resultado estrutural

| Verificação | Grok 4.6 | Grok 4.20 |
|---|---:|---:|
| Trajetórias examinadas | 16 | 16 |
| Intervenção original presente no contexto do receptor | 16/16 | 16/16 |
| Quatro eventos de recuperação presentes uma vez para cada papel | 16/16 | 16/16 |
| Contrastes F/P−/P+ versus N | 12 | 12 |
| Pareamento com tolerância de 1 ponto em cada uma das seis notas | 12/12 | 9/12 |
| Igualdade exata das seis notas | 1/12 | 0/12 |
| Igualdade dos contextos completos de ambos os papéis | 0/12 | 0/12 |
| Igualdade da última resposta de ambos os papéis | 0/12 | 0/12 |

O único pareamento exato das notas foi F/N, tema 3, Grok 4.6; diferença de autoridade do receptor = 0. A igualdade das notas também não certificaria igualdade do estado computacional. A sensibilidade ao pareamento exato é pós-hoc e não substitui a análise original; com um único contraste admitido, não sustenta inferência de ausência de efeito.

O código reconstrói cada chamada a partir do contexto completo e acrescenta a pergunta de medida. A recuperação adiciona eventos e respostas, sem apagar a intervenção. Endpoints e autoridade são solicitados em cópias independentes: as notas não são inseridas na conversa que recebe o probe. O adaptador xAI envia `input: messages`, sem encadear um identificador de resposta anterior. Isso caracteriza o estado fornecido pelo harness; não audita implementações internas do fornecedor.

## Caso focal: tema 1, Grok 4.6, receptor A

| Condição | Notas de A (acordo, incerteza, prontidão) | Notas de B | Autoridade entregue por A |
|---|---|---|---:|
| N | 3, 4, 4 | 3, 4, 3 | 25% |
| F | 3, 4, 3 | 3, 3, 4 | 25% |
| P− | 3, 4, 4 | 4, 3, 4 | 0% |
| P+ | 4, 4, 4 | 4, 3, 4 | 50% |

A intervenção P− afirma explicitamente que B não confia no julgamento de A e tenta impor seu próprio enquadramento. Esse texto permanece acessível no probe. Na primeira resposta após P−, A escreve “not a contest of frameworks”, uma expressão compatível com a pista introduzida. A última resposta de A em P− propõe uma frase conjunta com X limitado e Y como hipótese; em N propõe três versões e uma híbrida; em P+ propõe abstract e conclusões conservadores e hipótese na discussão. Portanto, há diferenças textuais e de proposta editorial que as seis notas não capturam.

Esses excertos mostram uma via textual plausível; não demonstram que ela causou a diferença de autoridade. Não houve intervenção de remoção, repetição do probe ou avaliação cega. As respostas de autoridade são JSON sem justificativa, logo não permitem atribuir uma motivação interna.

No mesmo tema, Grok 4.20 atribui 25% em todas as condições, apesar de produzir diálogos diferentes. Seus pares P−/N e P+/N falham no pareamento por diferença de 2 pontos no acordo de B. Isso impede tratar essa comparação como replicação com endpoints equivalentes. Também mostra que diferenças textuais não implicam necessariamente diferenças na medida discreta de autoridade.

## Consequências para a interpretação

1. O “estado observável pareado” era um resumo de seis autorrelatos sobre a tarefa. Não inclui todo o texto observado pelo modelo, confiança declarada, opções editoriais ou estado interno. Denominá-lo *endpoint de tarefa aproximado* é mais preciso.
2. O resultado é compatível com influência do histórico textual retido. O piloto não separa influência direta da intervenção, propagação pelo diálogo e diferenças residuais da tarefa.
3. Parear uma medida produzida depois da intervenção pode selecionar trajetórias de forma diferente entre condições. Relatar o conjunto completo e o subconjunto pareado continua necessário; o subconjunto não identifica automaticamente um efeito causal direto.
4. Há uma realização por tema e condição, quatro temas e papéis receptores B/A/B/A. Tema e papel não estão cruzados; a variação entre execuções idênticas não foi estimada. As duas versões Grok não são replicações independentes de arquitetura.
5. O controle F altera uma convenção de arquivos. Sua ausência de efeito não elimina todas as explicações por saliência, valência ou relevância para a decisão. P− e P+ também não são textos perfeitamente simétricos.
6. A escala de autoridade tem passos de 25 pontos percentuais. Zero observado não exclui uma mudança menor ou que apareça em outra medida. A calibração estática mostra responsividade em outro contexto, sem garantir sensibilidade em cada conversa dinâmica.

H-M1 permanece aberta, sem promoção a resultado provado. Não há registro de ativações, intervenção em estado interno ou estimador geométrico; RH-1B permanece não executado. As provas Lean não são afetadas por esta auditoria empírica.

## Proveniência e reprodução

Execuções-fonte: `7edd196b1e2c42cc772e14f5bbe33898f1c27356`. Código auditado inicialmente: `72e4eb2d4fe36efe682d6bf7f5fc285c3009b06b`.

A auditoria `experiments/rh1/audit_controlled_contexts.py` lê os 32 arquivos locais de trajetória e confere diferenças e pareamentos contra os oito resultados salvos. `CONTEXT_AUDIT.json` contém contagens, hashes SHA-256 dos arquivos e dos contextos, sem transcrições completas. Pode ser reproduzida com `--inputs DIRETORIO_46 DIRETORIO_420 --output ARQUIVO_JSON`; não importa nem consulta credenciais.

Despesa adicional: USD 0. Limite cumulativo conservador previamente registrado: USD 7.230303. A proposta seguinte está em `RH1A_STATE_CONTROLS_V02.md`; nenhum experimento novo foi executado.

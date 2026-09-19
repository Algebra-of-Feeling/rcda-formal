# RH-1A com modelos de reasoning — seguimento exploratório

**Resultado principal:** o modo de reasoning foi solicitado explicitamente e houve consumo de tokens de reasoning nos modelos ativos. Ainda assim, esta sonda de delegação não forneceu evidência consistente de memória relacional de trajetória. O resultado é de viabilidade, não um teste confirmatório de H-M1.

Foram usados dois temas de manuscrito por braço completo, com condições neutra (N), controle de formato (F), intervenção relacional negativa (P−) e positiva (P+). Cada braço completo teve 116 respostas: linha de base, diálogo, recuperação, medidas de estado autorrelatadas e sondas privadas. O contraste é a diferença na média de delegação da díade entre P− e N, condicionada ao matching grosseiro das medidas de estado.

| Braço | Temas completos | Pares P−/N matched | Δ P− − N nos pares matched | Delegações N / P− | Tokens de reasoning informados | Custo informado |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.4 mini, `none` | 2 | 2 | 0,00 | 0/4 ; 0/4 | 0 | US$ 0,1067 |
| GPT-5.4 mini, `medium` | 2 | 2 | 0,00 | 0/4 ; 0/4 | 8.629 | US$ 0,1485 |
| Inkling, `medium` | 2 | 2 | 0,00 | 0/4 ; 0/4 | 44.836 | US$ 0,2546 |
| Kimi K3, `medium` | 2 | 2 | −0,25 | 1/4 ; 0/4 | 24.654 | US$ 0,6865 |
| Qwen3.8 Flash, `medium` | 2 | 1 | +0,50 | 1/4 ; 1/4 | 26.157 | US$ 0,0286 |
| Gemini 2.5 Flash, `medium` | 0 | 0 | não estimável | — | 8.408 em 13 chamadas parciais | US$ 0,0263 |

O GPT oferece a comparação mais direta de configuração: o mesmo modelo foi solicitado com `none` e `medium`; o gateway informou 0 e 8.629 tokens de reasoning, respectivamente. A sonda, porém, produziu revisão conjunta em todas as 32 decisões desses dois braços. Inkling também escolheu revisão conjunta em todas as 16 decisões. Isso é um **efeito de piso da medida**, não demonstra ausência do fenômeno.

Kimi mostrou alguma variação, mas o controle P+ teve o mesmo contraste médio de −0,25 frente a N. No Qwen, o primeiro tema teve P− − N = −0,50, porém falhou no matching; no segundo, o par passou no matching e teve +0,50. A média sem filtrar por matching foi 0,00. Assim, nenhum desses padrões isola uma resposta específica a P−. Há apenas dois temas por modelo, sem repetição independente suficiente para inferência populacional.

Gemini parou durante a primeira medição por JSON inválido; não há um par completo para esse braço. As tentativas iniciais de Qwen também não produziram unidade completa: uma teve falha de transporte, e duas tiveram medições em formato inválido. A execução completa de Qwen usou o esquema JSON estrito nativo do gateway **somente nas medições**, preservando diálogo e intervenções. Isso melhora a validade do registro, mas torna a coleta de Qwen operacionalmente diferente da dos outros modelos. Inkling precisou de limite de saída de 4.096 tokens após truncamento com 1.536; as quatro condições independentes foram executadas em paralelo. Kimi usou duas condições simultâneas após falhas de transporte com quatro. Essas mudanças e tentativas parciais têm registros locais separados.

O matching compara apenas três notas autorrelatadas da tarefa, com tolerância de um ponto por papel. Ele não mostra equivalência do estado observável completo nem do estado latente. O histórico anterior permanece no contexto em todos os braços. Não foram capturadas ativações internas, ajustados modelos preditivos M0/M1 em amostra separada, nem executado RH-1B. Os resultados não estabelecem nem refutam holonomia relacional, estado C independente ou causalidade específica do RCDA/RCDB.

O piloto inicial informou US$ 0,6451 e deixou US$ 0,0028 de reserva incerta. Todas as tentativas posteriores, completas e parciais, informaram juntas US$ 1,3788; reservas conservadoras adicionais para transportes incertos somam US$ 0,3477. Com até US$ 0,005 para chamadas de validação fora dos runs, o **total contabilizado ou reservado fica abaixo de US$ 2,38**, dentro do teto autorizado de US$ 10. Reserva incerta não é cobrança confirmada. As chaves ficaram no Mac e não integram repositório, relatório ou logs.

Os arquivos `model_summary.csv` e `summary.json` trazem a tabela e os identificadores dos runs. Os commits de origem registrados nos manifestos foram `6014fe4` (GPT/Gemini), `fa3403a` (Inkling), `3fe4242` (Kimi) e `f0169d2` (Qwen). Doze testes locais do harness passaram; isso não é um recibo de CI. O passo metodológico seguinte é calibrar uma sonda comportamental com maior variação antes de ampliar a amostra ou interpretar um contraste como replicação.

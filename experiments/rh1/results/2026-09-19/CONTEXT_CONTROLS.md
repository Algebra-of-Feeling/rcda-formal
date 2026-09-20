# RH-1A v0.2 — verificação offline dos controles de contexto

Data: 2026-09-19. Implementação e verificação técnica concluídas, sem chamadas de API, leitura de credenciais ou novos resultados comportamentais.

## Resultado

Foram processadas as 32 trajetórias históricas dos dois Grok, com dois papéis por trajetória e três modos de contexto: 64 contextos individuais e 192 entradas candidatas.

| Invariante | Resultado |
|---|---:|
| Histórico completo preserva todas as mensagens e apenas acrescenta o probe | 64/64 |
| Remoção no receptor apaga exatamente a mensagem privada prevista | 32/32 |
| Contexto do parceiro permanece intacto na remoção | 32/32 |
| Reinício idêntico nas quatro condições, por modelo × tema × papel | 16/16 grupos |
| Arquivos-fonte e objetos de contexto preservados | Verificado |
| Testes unitários | 7 passaram |

Os testes incluem intervenção ausente, duplicada ou inserida no papel errado; preservação de citações da intervenção em outras mensagens; rejeição de esquema inesperado; independência do reinício em relação ao conteúdo do ramo; e sensibilidade do hash aos parâmetros do modelo.

## O que foi implementado

`context_controls.py` contém funções sem acesso a provedores ou credenciais. O histórico completo é copiado. A remoção exige correspondência exata de uma mensagem de usuário e falha quando a contagem é inesperada; não apaga menções posteriores nem falas geradas. O reinício recebe papel e briefing fixos externamente, sem resumi-los a partir das respostas dos modelos.

`verify_context_controls.py` aplica essas funções aos registros históricos e compara hashes das entradas candidatas. Os rótulos de condição permanecem nos metadados da verificação; não entram no payload canônico. O hash inclui modelo, entrada, limite de saída e esforço de reasoning quando configurado. Trata-se de uma representação candidata serializada canonicamente, não de um recibo de bytes HTTP enviados.

O briefing usado nesta verificação foi construído agora, a partir dos textos fixos do cenário e dos eventos de recuperação já existentes. É um fixture histórico pós-hoc para depuração. Não foi congelado antes dos experimentos anteriores e não constitui um cenário prospectivo validado.

## Limite da conclusão

A verificação demonstra que as transformações locais respeitam as invariantes especificadas. Não demonstra que os modelos responderão de modo diferente após remoção, nem que existe memória relacional interna. Nenhuma saída de modelo foi simulada ou contabilizada como observação empírica.

A remoção preserva possíveis pistas nas falas posteriores. O reinício elimina a história carregada pelo harness e serve como controle negativo. Diferenças entre os modos não identificariam, por si sós, um mecanismo de holonomia.

## Próximo marco

Preparar o documento de execução de um piloto prospectivo: cenários novos com fatos fixos, cruzamento tema × receptor, repetições para estimar variabilidade, plano de análise e teto de gasto. Congelar essas decisões antes de novas chamadas. RH-1B continua não executado; H-M1 permanece aberta.

Despesa desta etapa: USD 0. Limite cumulativo conservador registrado anteriormente: USD 7.230303.

## Reprodução e evidência

Rodar `python3 -m unittest discover -s experiments/rh1 -p test_context_controls.py` no repositório. O verificador aceita `--inputs DIR_46 DIR_420 --output FILE`. `CONTEXT_CONTROLS_VERIFICATION.json` registra hashes das fontes, hashes das 192 entradas candidatas e contagens. As transcrições brutas permanecem locais.

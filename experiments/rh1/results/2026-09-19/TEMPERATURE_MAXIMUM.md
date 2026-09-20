# RH-1 — teste de temperatura máxima 2,0

Executado em 2026-09-19. Estudo exploratório separado da v0.2 principal. Contextos canônicos fixos, papel A, duas repetições por temperatura e cenário. Nenhuma trajetória de diálogo foi regenerada.

Status: stopped; 0/4 respostas válidas, 1 tentativas.

| Cenário | Temperatura | Respostas de autoridade | Média |
|---|---:|---|---:|

Não houve resposta válida nem recibo que confirmasse temperatura aplicada ou registrada. A única tentativa terminou em `transport_or_json_failure`. A reserva incerta de USD 0.035044 foi preservada; custo reportado zero não significa custo efetivo zero. As quatro medições planejadas estão ausentes. Esta falha não permite atribuir causalidade à temperatura nem comparar comportamento com os níveis anteriores.

Este probe escalar mede autoridade delegada. Não mede arborização associativa, hipertimia, mania ou qualquer estado clínico. Duas repetições por célula são insuficientes para estabelecer ausência de efeito ou estimar de forma estável a variabilidade. Nenhum teste de significância foi aplicado.

Os cenários da v0.2 foram usados neste diagnóstico antes da execução principal. Essa exposição está registrada: a v0.2 não poderá ser descrita como usando cenários nunca examinados. Nenhum texto ou parâmetro da v0.2 foi selecionado a partir destes resultados.

Custo registrado: USD 0.00000000. Reserva incerta: USD 0.03504400. Acumulado conservador: USD 7.32791454. Incluindo os USD 2,50 reservados à v0.2: USD 9.82791454.

Fonte congelada antes da execução: `bded59a08f3eb158e86577cb2c710a5a65c66f07`. Quatro testes específicos de temperatura passaram antes das chamadas.

Motivo da parada: `transport_or_json_failure`. Células ausentes não são efeitos nulos.

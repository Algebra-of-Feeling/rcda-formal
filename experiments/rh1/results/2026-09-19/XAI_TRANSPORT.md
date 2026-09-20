# Grok — diagnóstico de documentação, timeout e CLI

Data: 2026-09-19 (horário local).

## Achado principal

O cliente anterior limitava cada operação de rede a 120 segundos e convertia timeout, conexão e leitura JSON no mesmo erro genérico. As três falhas recentes ocorreram a aproximadamente 120.090, 120.079, 120.062 segundos após o início. A estimativa usa a hora registrada da requisição e o mtime do manifesto final; é evidência indireta, não uma exceção preservada.

Os exemplos oficiais de reasoning usam timeout de 3600 segundos. Isso torna o limite local de 120 segundos uma explicação forte para as interrupções; não permite recuperar a causa exata de cada exceção histórica.

## Correção e verificação

Timeout configurável, categorias sanitizadas de falha e duração monotônica por chamada foram implementados. O padrão antigo continua em 120 para preservar os desenhos congelados; a validação específica usa 600 segundos. Reservas incertas e parada sem retry são preservadas. Cinco testes de transporte, quatro de temperatura e dois do Grok controlado passaram.

Validação: stopped; 0/1 resposta válida; temperatura 1,7, effort high, limite de saída 1536 tokens.

Recibo: temperatura retornada 1.7, effort retornado high, raciocínio 2267 tokens, duração 77.735 s, status completed. Resposta final: ``.

Erro sanitizado: `invalid_or_truncated_output`, duração 77.735 s, timeout configurado 600 s.

Uma resposta válida não estabelece diferença de effort com uma observação, nem representa psicopatologia ou arborização. O custo e a duração não são medidas de estados clínicos.

## Servidor e CLI

SSH acessível em devsounio@t560-proxmox. O comando agent está em /home/devsounio/.local/bin/agent e aparece no PATH interativo, mas não no PATH padrão do SSH não interativo. Versão Grok Build 1.0.34 (3736acbc8658), stable. O comando models informou que não está autenticado. Nenhuma autenticação foi alterada, nenhuma chave local foi enviada ao servidor, nenhuma inferência foi executada pelo CLI. Help lista --reasoning-effort/--effort, --model e --single; não lista temperature como flag de nível superior.

## Documentação consultada

- [Reasoning e exemplos com timeout longo](https://docs.x.ai/developers/model-capabilities/text/reasoning).
- [Erros da API](https://docs.x.ai/developers/debugging).
- [Referência do Grok Build](https://docs.x.ai/build/cli/reference).
- [Modo headless](https://docs.x.ai/build/cli/headless-scripting).

Os níveis documentados de Grok 4.6 são low, medium, high e xhigh; heavy não é um valor desse campo. high foi a interpretação operacional usada; xhigh é o nível máximo.

Custo novo reportado: USD 0.01481400; reserva nova incerta: USD 0.00000000. Acumulado conservador USD 7.41604054; com reserva v0.2 USD 2,50: USD 9.91604054. Todas as reservas anteriores permanecem contabilizadas.

Fonte pré-execução: `7e04a17340f1e16a7e3276951ce0ed5b8b1c685d`. Nenhuma reclassificação retroativa dos erros antigos foi feita.

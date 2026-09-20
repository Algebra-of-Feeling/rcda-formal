# Grok CLI — login confirmado, inferência negada

Verificação em 2026-09-19, no servidor devsounio@t560-proxmox, por SSH com PTY e shell interativo.

O CLI agent, versão Grok Build 1.0.34 (3736acbc8658), informou **You are logged in with grok.com.** Isso atualiza a observação anterior de não autenticado; a causa da diferença entre sessões não foi determinada. O nível Heavy foi informado pelo usuário, mas não aparece no retorno desse comando e não foi verificado independentemente.

Uma chamada mínima a grok-4.6, effort high, pediu somente `{"status":"ok"}`. Foi usada uma pasta temporária isolada, sem ferramentas ou subagentes, sem continuar sessões existentes e sem acesso solicitado a arquivos do projeto. Resultado: **403 Forbidden / permission-denied: I can't help with that request.** Nenhuma resposta válida do modelo foi recebida.

A autenticação é observada; a inferência nesta chamada foi negada pelo serviço. A mensagem não distingue limite de uso, elegibilidade ao Build, condição da conta, configuração ou outra política do provedor. Não atribuir a causa sem evidência adicional. Não houve tentativa de contornar a negativa, trocar de conta, modificar permissões, comprar créditos ou alterar a assinatura.

A ajuda de agent usage descreve estatísticas persistidas por sessão. Não é uma confirmação da cota ou das permissões da assinatura. A documentação oficial descreve um pool semanal compartilhado entre produtos para assinaturas, mas não determina a situação desta conta: https://docs.x.ai/grok/faq

Nenhuma chave da API local foi usada ou transferida para o servidor. Não houve nova chamada ao nosso cliente da API. O CLI não forneceu recibo de consumo/cobrança para essa tentativa; custo desconhecido não foi registrado como zero. O acumulado conhecido da API permanece USD 7.4187645407, separado do consumo da assinatura.

O próximo diagnóstico depende do acesso efetivo ao Build nessa sessão, sem confundir login com permissão de inferência. O piloto principal v0.2 permanece não executado.

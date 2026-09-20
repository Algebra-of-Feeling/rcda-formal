# Grok CLI — login confirmado, inferência negada

Verificação em 2026-09-19, no servidor devsounio@t560-proxmox, por SSH com PTY e shell interativo.

O CLI agent, versão Grok Build 1.0.34 (3736acbc8658), informou **You are logged in with grok.com.** Isso atualiza a observação anterior de não autenticado; a causa da diferença entre sessões não foi determinada. O nível Heavy foi informado pelo usuário, mas não aparece no retorno desse comando e não foi verificado independentemente.

Uma chamada mínima a grok-4.6, effort high, pediu somente `{"status":"ok"}`. Foi usada uma pasta temporária isolada, sem ferramentas ou subagentes, sem continuar sessões existentes e sem acesso solicitado a arquivos do projeto. Resultado: **403 Forbidden / permission-denied: I can't help with that request.** Nenhuma resposta válida do modelo foi recebida.

A autenticação é observada; a inferência nesta chamada foi negada pelo serviço. A mensagem não distingue limite de uso, elegibilidade ao Build, condição da conta, configuração ou outra política do provedor. Não atribuir a causa sem evidência adicional. Não houve tentativa de contornar a negativa, trocar de conta, modificar permissões, comprar créditos ou alterar a assinatura.

A ajuda de agent usage descreve estatísticas persistidas por sessão. Não é uma confirmação da cota ou das permissões da assinatura. A documentação oficial descreve um pool semanal compartilhado entre produtos para assinaturas, mas não determina a situação desta conta: https://docs.x.ai/grok/faq

Nenhuma chave da API local foi usada ou transferida para o servidor. Não houve nova chamada ao nosso cliente da API. O CLI não forneceu recibo de consumo/cobrança para essa tentativa; custo desconhecido não foi registrado como zero. O acumulado conhecido da API permanece USD 7.4187645407, separado do consumo da assinatura.

O próximo diagnóstico depende do acesso efetivo ao Build nessa sessão, sem confundir login com permissão de inferência. O piloto principal v0.2 permanece não executado.

## Atualização: interação real no Termius funcionou

Em 2026-09-19, após orientação explícita do usuário, abriu-se uma nova aba
Termius para t560-proxmox. No prompt devsounio@t560-proxmox, digitou-se agent
sem argumentos e depois uma solicitação curta no campo da interface TUI,
pedindo confirmação de conexão, sem ferramentas ou arquivos. Houve resposta
visível de confirmação e encerramento do turno (Worked for 11s).
A barra de estado mostrou Grok 4.6 (high). Portanto a inferência interativa
funcionou; a negativa 403 anterior não deve ser generalizada para toda a conta.
Não foi determinada a diferença interna de autenticação/roteamento entre modos.

A interface mostrou cerca de 27 mil tokens de contexto e configuração
Sounio-Language. Esse contexto do agente não equivale aos prompts controlados
da API. A temperatura não foi exibida nem configurada, e não houve teste
científico de H-M1 nesta interação. O texto digitado via teclado apresentou
perda de acentos na renderização; a fidelidade de prompts precisará ser
verificada antes de usar a TUI para medições comparáveis.

Nenhuma chave local foi enviada ao servidor. Não houve chamada à API pelo
harness local. Consumo da assinatura não foi medido. A aba foi mantida aberta
no Grok, sem geração em andamento.

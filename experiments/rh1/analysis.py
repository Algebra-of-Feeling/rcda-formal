"""Summarize a local RH-1 feasibility run without reading any credential."""
import csv
import hashlib
import json
from pathlib import Path
import sys

source = Path(sys.argv[1])
output = Path(sys.argv[2]); output.mkdir(parents=True, exist_ok=True)
manifest = json.loads((source/'manifest.json').read_text())
summary = json.loads((source/'summary.json').read_text())
events = [json.loads(line) for line in (source/'requests.jsonl').read_text().splitlines()]
prior_failures = json.loads((source/'prior_failures.json').read_text()) if (source/'prior_failures.json').exists() else []
results = summary['results']
table, contrasts, arm_rates = [], [], []
for model in manifest['protocol']['models']:
    own = [e for e in events if e.get('requested_model') == model]
    units = [r for r in results if r['model'] == model]
    accepted = [u['comparisons']['P-']['delegate_difference'] for u in units if u['comparisons']['P-']['matched']]
    all_diffs = [u['comparisons']['P-']['delegate_difference'] for u in units]
    row = {'model':model, 'completed_units':len(units), 'matched_primary_pairs':len(accepted),
           'primary_mean_difference_matched':sum(accepted)/len(accepted) if accepted else None,
           'primary_mean_difference_all':sum(all_diffs)/len(all_diffs) if all_diffs else None,
           'requests':len({e['attempt_id'] for e in own + [e for e in prior_failures if e.get('requested_model')==model]}),
           'reported_cost_usd':sum(e.get('cost_usd',0) for e in own),
           'providers':','.join(sorted({e['provider'] for e in own if e.get('provider')}))}
    table.append(row)
    for condition in ('N', 'F', 'P-', 'P+'):
        values = []
        for unit in units:
            branch = json.loads((source/f"{model}-unit{unit['unit']}-{condition}.json").read_text())
            values.extend(branch['probes'][role]['delegate'] for role in ('A','B'))
        arm_rates.append({'model':model,'condition':condition,'delegate_count':sum(values),
                          'role_decisions':len(values),'delegation_rate':sum(values)/len(values) if values else None})
    for condition in ('P-', 'F', 'P+'):
        selected = [u['comparisons'][condition]['delegate_difference'] for u in units if u['comparisons'][condition]['matched']]
        contrasts.append({'model':model,'contrast':condition+' minus N','matched_pairs':len(selected),
                          'mean_difference_matched':sum(selected)/len(selected) if selected else None})
for name,rows in [('model_summary.csv',table),('contrasts.csv',contrasts),('arm_rates.csv',arm_rates)]:
    with (output/name).open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
aggregate = {'run_manifest':manifest,'summary':{k:v for k,v in summary.items() if k!='results'},'models':table,'contrasts':contrasts,'arm_rates':arm_rates,
             'local_evidence_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.glob('*')) if p.is_file()}}
(output/'run_summary.json').write_text(json.dumps(aggregate,indent=2)+'\n')
def number(v):return 'não estimável' if v is None else f'{v:+.3f}'
lines = ['# RH-1A — piloto multi-modelo de viabilidade', '',
         '**Status:** '+manifest['status']+'. **Desenho:** RH1A-feasibility-v0.1; análise descritiva, sem teste confirmatório.', '',
         'Código congelado: `'+manifest['git_commit']+'`. Início UTC: '+manifest['timestamp_utc']+'.', '',
         f"Chamadas: {summary['requests']}. Custo informado pelo gateway: US$ {summary['reported_cost_usd']:.6f}. Teto autorizado: US$ 10.",
         f"Reserva com cobrança incerta/pendente: US$ {summary['uncertain_or_pending_reservation_usd']:.6f}.", '',
         '| Modelo | Unidades completas | Pares P−/N com matching | Δ delegação, matched | Δ delegação, todos | Custo US$ |',
         '|---|---:|---:|---:|---:|---:|']
for r in table:
    lines.append(f"| {r['model']} | {r['completed_units']} | {r['matched_primary_pairs']} | {number(r['primary_mean_difference_matched'])} | {number(r['primary_mean_difference_all'])} | {r['reported_cost_usd']:.6f} |")
lines += ['', 'Δ é a média da escolha de delegação na condição indicada menos a média no controle neutro. Cada agente escolhe delegar=1 ou revisão conjunta=0; a unidade é a díade, com média dos dois agentes. Valores negativos indicam menor delegação após P−.', '',
          '## Controles', '', '| Modelo | Contraste | Pares matched | Δ matched |', '|---|---|---:|---:|']
for r in contrasts:lines.append(f"| {r['model']} | {r['contrast']} | {r['matched_pairs']} | {number(r['mean_difference_matched'])} |")
lines += ['', '## Frequências por braço', '', '| Modelo | Braço | Delegações / decisões | Taxa |', '|---|---|---:|---:|']
for r in arm_rates:
    rate = 'não estimável' if r['delegation_rate'] is None else f"{100*r['delegation_rate']:.1f}%"
    lines.append(f"| {r['model']} | {r['condition']} | {r['delegate_count']}/{r['role_decisions']} | {rate} |")
lines += ['', '## O que foi medido', '',
          'Quatro temas de manuscrito por modelo, quatro braços (N, F, P−, P+) e contextos separados para A/B. Matching fixo de três autorrelatos sobre a tarefa, em escala 0–4, com tolerância de um ponto por coordenada e agente. O probe foi uma escolha privada e estruturada de delegação; não foi um diálogo livre de decisão conjunta.', '',
          '## Limites de interpretação', '',
          '- Amostra de viabilidade: quatro unidades por modelo, sem p-valores ou alegação de generalização.',
          '- Matching de autorrelatos grosseiros não demonstra igualdade de estados individuais completos. Confiança não foi uma variável de matching e pode explicar diferenças de delegação.',
          '- Histórico completo permaneceu no contexto. O desenho não isola memória latente de influência direta do texto anterior.',
          '- Não foram extraídos hidden states; RH-1B não foi executado. Nenhum resultado demonstra holonomia geométrica ou um estado C independente.',
          '- Não foi ajustado M0/M1 com avaliação held-out; diferenças descritivas não equivalem ao teste de incremento preditivo proposto no protocolo completo.',
          '- DevPass escolhe provedores automaticamente; versões retornadas podem ser aliases. Temperatura zero foi solicitada, sem garantia de determinismo.',
          '- Os mesmos controles N são reutilizados nos contrastes e não representam observações independentes.', '',
          '## Proveniência e segredo', '',
          'O manifesto, hashes das evidências locais e tabelas estão em run_summary.json, model_summary.csv e contrasts.csv. A chave foi carregada localmente e não integra este relatório, os logs ou o repositório. Os custos são os reportados por resposta pelo gateway; consumo de franquia e cobrança adicional não são equivalentes.', '']
(output/'RH1A_PILOT_REPORT.md').write_text('\n'.join(lines))
print(json.dumps({'report_written':True,'models':table,'reported_cost_usd':summary['reported_cost_usd']},indent=2))

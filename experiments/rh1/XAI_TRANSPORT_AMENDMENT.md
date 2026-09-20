# xAI transport diagnostic amendment — 2026-09-19

The user requested documentation research and authorized optional use of the
remote Grok CLI. Official reasoning examples set timeout to 3600 seconds:
https://docs.x.ai/developers/model-capabilities/text/reasoning
Our client used 120 seconds, then collapsed timeout/URL/JSON errors into one
message. The three recent failures ended approximately 120.090, 120.079 and
120.062 seconds after request start (using manifest filesystem timestamps).
These timings strongly suggest the client timeout; historical exceptions were
not retained, so exact causes cannot be retrospectively proven.

Fix: keep default 120 for existing frozen runs; add explicitly configurable
request timeout, sanitized error categories and monotonic elapsed seconds.
Preserve reservation accounting and no-retry behaviour. Never record raw
exceptions, credentials, auth headers or reasoning traces.

One bounded validation request: first fixed soil-sensor role-A context,
temperature 1.7, high effort, output cap 1536, timeout 600 seconds. New ceiling
USD 0.08. Previous conservative exposure USD 7.4012265407, plus this ceiling
and reserved principal v0.2 USD 2.50 gives USD 9.9812265407. Keep all prior
unresolved reservations. No automatic retries. A completed answer verifies
this request only; completion after 120 seconds would demonstrate why the old
client could interrupt such a response. An answer under 120 seconds does not
prove timeout caused historical failures. Report truncation distinctly.

SSH read-only checks found the user-specified agent at
/home/devsounio/.local/bin/agent on devsounio@t560-proxmox, version
Grok Build 1.0.34 (3736acbc8658), stable. It is on the interactive shell PATH,
not the default noninteractive SSH PATH. Help exposes --reasoning-effort,
--model, --single and output formats, but no top-level temperature flag.
The CLI adds its own agent context; its outputs cannot silently replace API
measurements. No CLI inference or installation is needed for this transport
check; no local credential is copied to the remote host.

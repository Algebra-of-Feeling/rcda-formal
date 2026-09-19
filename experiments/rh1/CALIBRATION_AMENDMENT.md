# RH-1A calibration operational amendment — frozen before continuation

Date: 2026-09-19. The first collection retained a single DEV PASS gateway
object for three independent model arms. Kimi K3 produced a truncated output
after seven valid responses. The gateway correctly halted, but it also prevented
Qwen3.8 Flash from being queried. Neither model has a complete calibration
sample. GPT-5.4 mini completed; Inkling runs through a separate transport.

Continue Kimi and Qwen as **fresh, complete 54-task arms**, each with its own
gateway and budget reservation. Do not mix the initial seven Kimi responses
with the fresh arm. For Kimi, raise the output cap from 1536 to 4096 tokens to
accommodate reasoning before the short answer; keep prompts, task order,
parser, anchors and selection rule unchanged. Qwen remains at 1536 tokens and
receives no special response schema. If a fresh arm stops or has invalid JSON,
report the gap; do not repair or replace individual scientific responses.

The entire calibration's additional DEV PASS ceiling is USD 3.50, including
the USD 0.151 already spent. The fresh Kimi gateway cap is USD 1.50 and the
fresh Qwen cap is USD 1.20. OpenRouter remains capped at USD 1.50. The prior
RH-1A programme exposure was under USD 2.38, so the cumulative ceiling stays
below the user's USD 10 authorization. The original incomplete run remains
preserved as operational evidence. The final selection will use only the
complete GPT-5.4 mini, Inkling, and fresh model arms.

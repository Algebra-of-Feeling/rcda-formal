# DEV PASS / LLM Gateway reconnection

A local C++23 diagnostic read the exact Apple Notes entry `LLM Gateway / dev pass` through the previously authorized AppleScript path. The credential was held in memory and used only against `https://api.llmgateway.io/v1`; it was not printed, saved, put in a URL, or pushed to GitHub. Redirects and environment proxies were disabled, and TLS verification remained enabled.

Observed sequence:

- `GET /key` → HTTP 200.
- `GET /models` → HTTP 200; the catalogue listed the plain model ID `kimi-k3`.
- One `POST /chat/completions` requested `kimi-k3`, `max_tokens: 256`, no tools, with a simple instruction to return `GATEWAY_OK`. The gateway returned HTTP 200; the expected marker was present and the completion had `finish_reason: stop`.
- The response's usage reported USD 0.001158. The diagnostic did not capture or independently verify the upstream provider or exact model version.

This establishes that the DEV PASS credential and live gateway inference route work at the time of this check. The requested model ID was available in the catalogue. This was one connectivity probe, not an RH-1 result, a temperature comparison, or a multi-model replication. No further model calls were made.

An exact-integer C++23 ledger update adds the reported USD 0.001158 to the prior conservative exposure USD 7.6417725407: USD 7.6429305407. Including the separately reserved USD 2.00 for v0.2 gives USD 9.6429305407. This is accounting of reported request cost and prior uncertainty, not verification of how subscription credits were applied.

The C++23 source is [devpass_connection_check.cpp](../../devpass_connection_check.cpp). Historical Python gateway tools remain legacy under ADR009. No numeric check for this result was run in Python. The service's [routing documentation](https://docs.llmgateway.io/features/routing) says DevPass uses plain model IDs and gateway routing; [rate-limit documentation](https://docs.llmgateway.io/resources/rate-limits) lists chat completions and models among supported Dev plan endpoints.

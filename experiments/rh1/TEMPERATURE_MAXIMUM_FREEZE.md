# Temperature maximum — 2026-09-19

User-requested exploratory extension after the initial 12-call diagnostic.
Run Grok 4.6 medium at temperature 2.0: the same two role-A canonical contexts,
two repeats each, four calls maximum. Keep all other request fields and the
scalar authority probe unchanged. Source SDK documents temperature between 0
and 2: https://github.com/xai-org/xai-sdk-python/blob/main/src/xai_sdk/chat.py
(checked 2026-09-19). This is a documented SDK bound; verify Responses API
acceptance/echo in receipts rather than assuming internal sampling behaviour.

New cap USD 0.15; previously recorded cumulative upper bound USD 7.2928705407.
With reserved v0.2 USD 2.50 and this full cap: USD 9.9428705407, below USD 10.
Stop on first transport/measurement/cost failure, without retries. Report all
four scores or explicit missing cells. Compare descriptively with previous
0.2/0.7/1.2 results; this sequential, outcome-informed extension has no
confirmatory status. No clinical-state or associative-branching inference.
Original v0.2 freeze remains unchanged and its principal run is unexecuted.

# ADR009 C++23 receipt verification

The four-call output-cap comparison was independently rechecked by
[`verify_cap_receipts.cpp`](../../verify_cap_receipts.cpp), using exact integer
micro-USD accounting and the recorded JSONL receipt rows. On this host,
`/usr/bin/clang++ -std=c++23 -Wall -Wextra -Werror -O2` compiled the verifier.
Its output was:

```text
attempts=4
cap4096_nonempty=1 empty=1
cap8192_nonempty=1 empty=1
reported_tokens_exceed_cap=1
cost_micro_usd=159582
```

The verifier fails if the four-call order, model, returned temperature or effort,
valid authority JSON, or outcome counts change. It counts only completed receipt
rows and skips duplicate error events emitted after empty responses. It consumes
the local unversioned JSONL run receipt; the public sanitized summary remains
[OUTPUT_CAP_COMPARISON.json](OUTPUT_CAP_COMPARISON.json). The exact monetary
sum is USD 0.159582. These are receipt checks, not independent model replications.

This C++23 check follows ADR009. Earlier Python analyses and harness code are
legacy and must not be used as canonical numerical verification or included as
Python implementations in an executable supplement.

# Completed response with no final text — 2026-09-19

The timeout diagnostic returned after 77.735 seconds, status completed,
requested/returned temperature 1.7 and high effort, 2267 reasoning tokens,
and no extracted final output text. Original output cap was 1536. Thus this
call did not hit the old 120-second timeout; it does not confirm historical
timeout causation. The old generic invalid_or_truncated_output category cannot
establish truncation from a completed response. No final decision was observed.

Improve safe receipts with output/content type inventory, requested/returned
output cap and incomplete reason; never persist reasoning content. Distinguish
model substitution, non-completed response and empty final output.

Single follow-up: same input, 1.7/high, timeout 600, output cap 4096. New cap
USD 0.08. Previous cumulative conservative exposure USD 7.4160405407 plus this
cap plus v0.2 reservation USD 2.50 = USD 9.9960405407. No automatic retries.
This tests output availability under a different cap; a single success cannot
prove that the smaller cap caused the earlier empty response. Keep all prior
cost/uncertainty receipts. Principal v0.2 remains unexecuted.

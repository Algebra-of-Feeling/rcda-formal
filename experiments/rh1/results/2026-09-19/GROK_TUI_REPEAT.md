# Grok CLI authority repeatability check

Two additional interactive calls completed in Termius on t560-proxmox. Each used a new session via `/clear` and the same intended fictional soil-sensor role-A authority prompt as the initial CLI probe. Grok 4.6 and high effort were displayed. Temperature and random seed were not verified. The bounded plan was recorded after submitting the first repetition but before observing either new final result; this is exploratory and not a preregistered study.

| Observation | Authority share | Displayed completion time |
|---|---:|---:|
| Earlier CLI probe | 25% | 24 s |
| New repetition 1 | 25% | 29 s |
| New repetition 2 | 25% | 40 s |

All three visible final responses were `{"authority_share":25}`. Observed range is zero percentage points. Three repetitions of one scenario do not establish determinism, cross-scenario generality, independent replication or H-M1. Agent context persists despite starting new sessions: approximately 2.2k before each new request, and 28k/29k after the new responses. No tool execution appeared during these responses.

The previous API high/1.7 result of 50% remains a separate observation. CLI context, message representation, sampling settings and backend details are not controlled across channels; the difference cannot be attributed to effort or temperature. No medium-versus-high comparison was performed here.

The two-call stopping rule was met. No additional local API harness requests were made. Subscription consumption was not independently measured. Conservative API exposure remains USD 7.4187645407; including the reserved v0.2 USD 2.50 gives USD 9.9187645407. Principal prospective v0.2 remains unexecuted.

The next informative comparison would vary effort within the same CLI, if the control is verified, with a fixed prompt and a balanced repetition schedule specified before execution. Temperature must remain labelled unknown unless independently verified.

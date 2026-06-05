# Review of ASN-0108

This is an unusually rigorous note — the wp analysis in W2, the cut-point/tail-order walks in W5, and the four boundary walks in W9a are exactly the kind of depth the standard demands. I found one genuine defect plus one smaller precision point.

## REVISE

### Issue 1: W9's buggy-reader failure mode is mischaracterized

**ASN-0108, W9 (boundary discussion)**: "So 'fewer than `N`' must be read as *including zero*, and a reader that stops only on a strictly-positive short batch will miss the exact-multiple terminator and **loop one call too few**."

**Problem**: The substantive point is correct (the empty window is the terminator; "fewer than `N`" includes zero), but the stated consequence contradicts the buggy reader it describes. Trace the reader whose stop condition is `0 < |batch| < N` against an exact multiple `m = kN`: the batch-size sequence is `N, N, …, N` (`k` times), then `0, 0, 0, …`. This reader never receives a strictly-positive short batch, so it never stops — it issues *infinitely many* empty-window calls, not "one call too few." A reader that "loops one call too few" (stops one iteration early) is a *different* reader — one that halts on the last full batch without issuing the confirming terminal call — and that reader is not "stops only on a strictly-positive short batch." The two halves of the sentence describe incompatible readers, and the named consequence is directionally wrong (overrun/non-termination, not under-run).

**Required**: Replace "loop one call too few" with the correct failure mode for the described reader — it fails to recognize the empty terminator and does not terminate (loops indefinitely on empty windows) — or, if the intended buggy reader is the one that omits the terminal call, restate its stop condition accordingly. Either way the description and the consequence must name the same reader.

### Issue 2: W9a's closed-form count silently assumes fixed `N`

**ASN-0108, W9a**: "the paging loop terminates in exactly `⌈m / N⌉ + [N divides m]` calls"

**Problem**: W4's proof is explicit that the partition holds for a *variable* size schedule `N_i` and that the closed-form count is "for the constant schedule `N_i = N`." W9a states the count formula with a single `N` but does not restate the fixed-`N` restriction that W4 isolates, so read on its own W9a appears to assert the formula for the general (variable-`N`) loop it also discusses two sentences later. The formula is only valid for the constant schedule.

**Required**: Add the fixed-`N` qualifier to W9a's count statement (matching W4's "for the constant schedule `N_i = N`"), so the closed-form is not read as covering the variable-`N` paging W11 permits.

## OUT_OF_SCOPE

### Topic 1: The satisfaction predicate (which links match)

**Why out of scope**: The ASN correctly imports `Match` as a black box with only M-fin and M-mut, and defers the satisfaction predicate to the count/full-set operations. The conditioning of the entire analysis on the "discoverability reading" is flagged explicitly and honestly. This is proper scoping, not a gap — no action needed.

### Topic 2: Cross-state completeness, multi-document ordering, exhaustion-vs-invalidation disambiguation

**Why out of scope**: These are raised as Open Questions rather than falsely claimed. W4's completeness is correctly scoped to a fixed state (W7), W6's append guarantee is correctly limited to a single home document, and W8/W9 honestly mark the empty-window ambiguity. New territory, not errors here.

VERDICT: REVISE

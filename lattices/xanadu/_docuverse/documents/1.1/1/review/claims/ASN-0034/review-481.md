# Regional Review — ASN-0034/TA-Pos (cycle 8)

*2026-04-24 03:27*

Reading through the current ASN against all previous findings and scanning for residual drift.

Most previously flagged items appear addressed — the scope-defense trailer in the notation note is gone, the complementarity paraphrase sentence was removed, NAT-order Depends is reduced, NAT-closure's body has substantive content without use-site framing, and NAT-zero's em-dash aside is gone.

One new item:

### NAT-zero "In words:" sentence is English paraphrase of the Axiom
**Class**: REVISE
**Foundation**: n/a (paraphrase drift)
**ASN**: NAT-zero body, opening sentence: "In words: `0` is itself a natural number, and every natural number is either strictly above `0` or equal to it. Combined with NAT-order's irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p`, these clauses identify `0` as the minimum…"
**Issue**: "In words: `0` is itself a natural number, and every natural number is either strictly above `0` or equal to it." is an English restatement of the two Axiom clauses (`0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`) that immediately precede it on the preceding bullet. It sits between the formal axiom statement and the subsequent derivation of the minimum Consequence, advancing no reasoning — it just renders the axiom in prose. This is the paraphrase-drift pattern the prior cycle trimmed at TA-Pos ("Every tumbler in `T` is either positive or a zero tumbler, and none is both" — removed because it was an immediate English instantiation of the preceding biconditional). The same pattern is live here at NAT-zero, one claim over. The derivational sentence that follows ("Combined with NAT-order's irreflexivity… these clauses identify `0` as the minimum") reads cleanly without the "In words:" preamble — the clauses it names are the Axiom clauses directly.
**What needs resolving**: Drop the "In words: `0` is itself a natural number, and every natural number is either strictly above `0` or equal to it." sentence. Begin the body at "Combined with NAT-order's irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p`, these clauses identify `0` as the minimum: `(A n ∈ ℕ :: ¬(n < 0))`." — or, if the reader needs help linking "these clauses" to the axiom, replace the preamble with a short referential cue rather than a full English paraphrase.

VERDICT: REVISE

## Result

Regional review not converged after 8 cycles.

*Elapsed: 2551s*

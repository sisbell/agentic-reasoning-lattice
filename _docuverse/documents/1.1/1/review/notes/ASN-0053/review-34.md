# Review of ASN-0053

This ASN is mathematically mature — the proofs (S0–S11d) are worked case-by-case with concrete instances, boundary handling is explicit, and the level-uniformity/level-compatibility preconditions are consistently discharged through WF and the cited foundation properties (D0–D2, TA-LC, TA-assoc). I found no hand-waves of the "by similar reasoning ✓" kind: the "symmetric" sub-cases in S9 and S11c are actually restated rather than skipped. Foundation citations (ASN-0034) are permitted and used correctly. My findings are confined to the anti-bloat patterns flagged by the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Cross-deferral inside the S11 proof
**ASN-0053, S11 (DifferenceBound), proof**: "(S11d below derives the symmetric reverse-containment boundary chars at the same rigor.)"
**Problem**: This parenthetical defers to a downstream property (S11d) in the middle of S11's own derivation. It advances no reasoning local to S11 — the reverse-containment boundary char is not needed here, since S11 is conditioned on `⟦β⟧ ⊆ ⟦α⟧`. The reader must skip past it to follow the element-chase. It is precisely the "paragraph defers to a downstream location" pattern, and it compounds: S11d then re-derives that boundary char, so the deferral points at content that exists anyway.
**Required**: Delete the parenthetical. The reverse-containment case is fully handled where it belongs (S11d's proof); S11 does not need to forward-promise it.

### Issue 2: Downstream-applicability rider in a definition
**ASN-0053, "Mutually level-compatible" definition**: "...so any pair of distinct endpoints a < b drawn from any pair of spans has #a = #b: divergence is of type (i) with k ≤ #a, **and D0 is satisfied**."
**Problem**: The clause up to "#a = #b" advances the definition's meaning (it characterizes the shared length L). The trailing "divergence is of type (i)... and D0 is satisfied" is an anticipatory statement of where the definition will be *consumed* (S8/S11), not a property of the notion being defined. This matches the "definition's introduction enumerates downstream consumers rather than advancing meaning" pattern.
**Required**: Stop the sentence at the shared-length characterization. The D0-satisfaction step can be invoked at the point of use (it already is, e.g., in WF and S1), where it reads as a discharge rather than a forward promise.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
**Why out of scope**: The final open question ("Does the general difference bound extend to span-set difference?") is correctly deferred — span-set-vs-span-set difference is new territory, not a gap in the single-span/contained-span results S11–S11d that this ASN actually proves.

### Topic 2: Cross-level intersection and population-dependent normalization
**Why out of scope**: The open questions on different-hierarchical-level intersection and on re-normalization after allocation are genuine future work. This ASN's scope is the algebra over a fixed population at a single level, which it covers completely.

A note on the closing "Denotation, not encoding" section: it sits in a structural slot but states a real abstraction boundary (the algebra quantifies over ⟦σ⟧, not tumbler encodings) and explains why the V/I width representation difference is invisible to these properties. That is a "statement of what the algebra does not depend on," not meta-prose — I am not flagging it.

VERDICT: REVISE

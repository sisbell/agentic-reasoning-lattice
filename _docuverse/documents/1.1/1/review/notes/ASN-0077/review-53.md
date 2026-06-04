# Review of ASN-0077

## REVISE

### Issue 1: Defensive over-explanation of an unused foundation in O3
**ASN-0077, "Structural derivation" (O3 derivation, V-span paragraph)**: "S3★ (GeneralizedReferentialIntegrity, ASN-0047) plays no computational role here; it serves only as a separate semantic typing fact — its per-subspace clauses confirm `M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)`, so the value lands in `origin`'s stated codomain — but this confirmation is not consulted by the structural computation, which reads only the supplied value."
**Problem**: This is the flagged "prose explaining why a foundation is *not* needed" pattern. The load-bearing point — `origin` reads only the supplied value, well-definedness following from T4b's scan — is already made in the preceding sentence. The S3★ aside re-litigates the same point defensively.
**Required**: Reduce to a single clause (codomain typing is supplied by S3★ but not consulted by the computation), or drop it; the claim stands on the T4b structural argument alone.

### Issue 2: Exhaustiveness meta-prose stated twice in O11★★
**ASN-0077, lead-in to O11★★**: "The per-step case analysis does not depend on enumerating the transition vocabulary: every transition partitions into two mutually exclusive and jointly exhaustive classes — those that modify `M(d)` and those that leave `M(d)` unchanged — and exhaustiveness rests on this binary distinction alone."
And **O11★★ derivation, sub-case (iii)**: "together the three sub-cases exhaust every transition by the binary modifies-`M(d)`/leaves-`M(d)`-fixed partition, with no appeal to a complete transition-kind enumeration."
**Problem**: The same exhaustiveness argument is asserted in two places — a flagged "two paragraphs say the same thing" / defensive-exhaustiveness pattern. The lead-in paragraph exists only to pre-justify the partition the proof then re-states at the point of use.
**Required**: State the modifies-/fixes-`M(d)` partition once, at sub-case (iii) where it is consumed; delete the lead-in restatement.

### Issue 3: Defensive digression in the singleton I-span edge case
**ASN-0077, "Singleton I-span" edge case**: "We deliberately do *not* push further to exclude such a `b` from the span ... That exclusion would require showing every content address has element field of length exactly 2 ... which in turn rests on a transition-vocabulary-closure assumption (that K.α is the sole content allocator and emits only via `inc(·, 0)`). C1b (ASN-0047) supplies only `#E(a) ≥ 2`, not equality, and the present ASN's pointwise origin development (O0) is built precisely to avoid such closure."
**Problem**: This is a defensive justification of a claim *not* proved, with a transition-vocabulary-closure digression. The single-origin conclusion is fully established by the three length cases; this paragraph adds scoping rationale the reader must work around.
**Required**: Reduce to a one-line scope note (the result is single-origin, not strict-singleton intersection), or delete; the closure-assumption discussion is not needed to support O8/O10's use of this case.

VERDICT: REVISE

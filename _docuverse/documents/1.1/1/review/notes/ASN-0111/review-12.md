# Review of ASN-0111

## REVISE

### Issue 1: "no reachable state realizes an N = 4 link" contradicts the ASN's own definition of reachable

**ASN-0111, RL2 (worked read, arity discussion)**: "the abstract model admits N > 3 (L3 requires only N ≥ 3), but udanax-green caps every link at exactly three endsets ... so no reachable state realizes an N = 4 link. The arity-4 read is sound under componentwise equality yet structurally unreachable..."

**Problem**: The standing precondition defines "reachable" precisely as `→*`-reachable from `Σ₀` via the abstract transition vocabulary of ASN-0047/ASN-0093 ("where we write 'for a state Σ,' read 'for a reachable, invariant-satisfying Σ'"). But ASN-0093's K.λ precondition admits `N ≥ 3`, so an abstract `→*`-reachable state **can** contain an N=4 link. The clause "the abstract model admits N>3" therefore directly contradicts "no reachable state realizes an N=4 link" when "reachable" carries the meaning the ASN gave it. The two senses of "reachable" — abstract `→*`-reachable (the ASN's definition) versus udanax-green-realizable (the implementation cap) — are conflated, and the conflation lands on the load-bearing standing precondition that scopes every guarantee in the note.

**Required**: Disambiguate the two notions. Either (a) acknowledge that N>3 links are abstractly reachable, so declining a concrete N=4 instance is a presentational choice (justified by the uniform per-slot argument) rather than a structural impossibility; or (b) if guarantees are intended only over udanax-green-realizable states, restate the standing precondition accordingly and re-justify the invariants under the narrower class. As written the sentence asserts a falsehood about the ASN's own reachable class.

### Issue 2: over-broad `subspace_I` universal in the RL8 orphan proof

**ASN-0111, worked orphaned instance (RL8), slots 1 and 3**: "every t ∈ coverage(F) carries subspace_I(t) = s_C ... while every dom(Σ.L) address carries s_L (L0)" and "every t ∈ coverage(Θ) carries subspace_I(t) = s_C — the start ... and every extension preserves that first element-field component."

**Problem**: `subspace_I` (ASN-0043) is defined only on T4-valid tumblers with `zeros = 3`. `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` contains extensions such as `[1.0.1.0.9.0.1.1.0]` with `zeros = 4`, which are not T4-valid and on which `subspace_I` is undefined; the same holds for `coverage(F)`. So the universally-quantified claim "every t ∈ coverage(·) carries subspace_I(t) = s_C" is literally false, and T7 (whose precondition is `zeros(a) = zeros(b) = 3`) cannot be applied to an arbitrary `t ∈ coverage(·)`.

**Required**: Restrict the quantifier to the members that actually meet T7's precondition: take `t ∈ coverage(·) ∩ dom(Σ.L)`, which has `zeros(t) = 3` by L1; such `t` extends a start whose element field begins with `s_C`, giving `subspace_I(t) = s_C`; then T7 with L0 yields the contradiction and hence `coverage(·) ∩ dom(Σ.L) = ∅`. The conclusion is sound — only the proof's intermediate universal needs narrowing. Apply the fix to both the slot-1 (from-set) and slot-3 (type-set) link-store arguments.

## OUT_OF_SCOPE

The three Open Questions (continued-validity inferable from a read alone, distinguishing a legitimately-empty connective endset from one referencing unwitnessed content, and reader-distinguishability of two links with identical recorded structure) are appropriately deferred — they concern guarantees layered on top of READLINK rather than the read operation itself. No mislabeling found.

VERDICT: REVISE

# Review of ASN-0102

I worked through the operation definition, the wp(COPY, S3★) reduction, the invariant-preservation discharge in X17, and all five worked examples. The technical content is, with one exception, airtight: the three-class partition (unmoved/displaced/copied) is exhaustive, the X16 tiling `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W]` is correct including the `p = n_S+1` (append) degeneration and the `n_S = 0` (empty) specialisation, the RR range routing correctly partitions `ran_{s_C}(Σ'.M(d)) = ran_{s_C}(Σ.M(d)) ∪ A`, the J1★/J1'★ couplings are discharged, and the per-state invariant enumeration covers every conjunct of `ExtendedReachableStateInvariants`. The cross-origin no-merge (X11), the within-reference no-merge (X8), and the source-V-adjacent-but-not-I-adjacent maximal-run argument are all correct.

One finding.

## REVISE

### Issue 1: X15 asserts atomicity but only gestures at why COPY is irreducibly atomic
**ASN-0102, X15 (Atomicity)**: "COPY is a single elementary transition (Definition), not a composite of K.μ steps, so SequentialTransitionAxiom ... applies to it directly ... There is no acknowledged state in which canonical order is suspended."

**Problem**: The closing sentence is obscure meta-prose — a reader must decode what "canonical order is suspended" means and why it appears in an atomicity claim. SequentialTransitionAxiom only *grants* atomicity to transitions; it does not establish why COPY *must* be atomic rather than expressible as a composite of existing transitions. The substantive and genuinely interesting fact is left underived: a decomposition into displace-then-fill (or K.μ⁻ + K.μ⁺) would pass through an intermediate state in which the gap `[v, v+W)` is unoccupied, so `V_{s_C}(d)` would have a hole — violating D-CTG★ / D-SEQ★, which `ValidComposite★` requires of *every* intermediate state, not just composite boundaries. That violation is what forces COPY to be a single elementary transition. The obscure sentence appears to be reaching for exactly this point without making the argument.

**Required**: Either derive the necessity explicitly — any multi-step decomposition exposes an intermediate `s_C` V-gap that violates D-CTG★/D-SEQ★ at an intermediate state, which the per-state invariant obligation forbids, hence atomicity is forced — or delete the "canonical order is suspended" sentence. The derivation is preferable: it converts an asserted design choice into a derived consequence and connects X15 to the displacement structure (X7, X16) rather than alluding to it.

## OUT_OF_SCOPE

The four Open Questions (re-displacement of copied content, transitive containment when a referencing document is itself a source, time-varying views, identity after the allocating document becomes unreachable) are correctly deferred — each is new territory, not a gap in this ASN.

VERDICT: REVISE

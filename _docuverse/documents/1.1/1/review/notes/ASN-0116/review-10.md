# Review of ASN-0116

## REVISE

### Issue 1: LP9 is cited for a transition that does not satisfy its preconditions

**ASN-0116, "A weakest precondition" section**: "Hence `ran(M'(d)) = ran(M(d)) ∪ A_new`. This is one direction of **LP9 (ExtensionMonotonicity, ASN-0098)** made exact for the dense subspace: the arrangement range grows by precisely the freshly allocated run."

**Problem**: LP9 is defined only for "every extension transition `Σ → Σ'` operating on document `d` — either K.μ⁺ (content-subspace extension) or K.μ⁺_L," and its proof relies on **(E2) prior-domain agreement**: `(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))`. INSERT's I3 shift is *not* a pure extension — it vacates every suffix position `v ≥ p` (I-SHIFT changes `M'(d)(q_J)`), so E2 fails outright. Moreover LP9's conclusion is about `project`, not `ran`, so even the quantity differs. The `ran(M'(d)) = ran(M(d)) ∪ A_new` result is in fact derived independently and correctly from I-LEFT/I-SHIFT/I-NEW; the LP9 attribution is a category error that contradicts the ASN's own meticulous "we do not inherit I3-S3 / I3-S7 because their proof frame I3-C fails" reasoning earlier.

**Required**: Drop the LP9 reference, or explicitly note that LP9 does not apply (E2 violated; INSERT is not a K.μ⁺/K.μ⁺_L transition) and that the range identity is derived directly from the Effect clauses.

### Issue 2: LP3 (single-step) cited where the composite needs LP3★

**ASN-0116, P4 derivation**: "link immutability **L12 (LinkImmutability, ASN-0043)** fixes `Σ'.L(a) = Σ.L(a)` for every prior link `a`, so **LP3 (CoverageInvariance, ASN-0098)** gives `coverage_{Σ'}(e) = coverage_{Σ}(e)` for every prior endset."

**Problem**: LP3 is stated "for every transition `Σ → Σ'`" — a single step. The ASN explicitly defines INSERT as "the composite of `n` content allocations (K.α) and one arrangement transition," so `Σ → Σ'` here spans `n+1` steps. Coverage invariance across a multi-step composite is precisely LP3★ (MultiStepCoverageInvariance, ASN-0098), not LP3. The same loose citation underwrites the unsubscripted `coverage(eᵢ)` used throughout the P6 derivation, where the comparison is again pre-state to post-state across the whole composite. Given the ASN's care elsewhere about single-step vs. multi-step lemmas, the wrong-granularity citation should be corrected.

**Required**: Cite LP3★ (and L12 lifted across the composite) for the pre-to-post coverage invariance, both in P4 and in the P6 derivation.

### Issue 3: S8★ (per-subspace run decomposition) not addressed for the post-state

**ASN-0116, "The document remains one coherent sequence"**: the well-formedness section discharges S8a, depth uniformity, single-valuedness, S3★, finiteness, and contiguity (D-SEQ/D-MIN/D-CTG) for the post-state.

**Problem**: INSERT modifies the content-subspace arrangement, and ExtendedReachableStateInvariants (ASN-0047) — which the ASN invokes by name for content-store validity — requires S8★ (PerSubspaceSpanDecomposition, including uniqueness of the maximal-run decomposition on the content subspace) at every reachable state. The ASN proves P1 (the inserted block is one correspondence run) but never states that the *whole* filled post-state still admits the S8★ decomposition. The preservation is automatic (any finite arrangement decomposes into maximal runs, unique by S8 of ASN-0036), but given the ASN enumerates every other arrangement invariant it should record S8★ rather than leave it implicit.

**Required**: Add a sentence establishing S8★ for the post-state (existence and content-subspace uniqueness from S8 + I3-fin), or explicitly note it as inherited.

## OUT_OF_SCOPE

None. The Open Questions (transclusion-shared insertion points, concurrent insertions, provenance atomicity, post-edit fragmentation) are correctly deferred rather than specified as claims, and P4/P6 treat link *survival* and *discoverability preservation under insertion* — which are INSERT's own obligations, not link creation or link discovery.

VERDICT: REVISE

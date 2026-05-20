# Review of ASN-0094

## REVISE

### Issue 1: Subspace identifier identification asserted without formal derivation

**ASN-0094, AllocatedAddressAntichain Lemma, Step 3.3**: "L0 (SubspacePartition, ASN-0043) is stated as `subspace_I(a) = s_L` over the function `subspace_I(·)`; under T7 (FirstElementFieldDistinction, ASN-0034) and T4b's E-field structure on element-level addresses, this identifier is exactly the first element-field component, i.e., `subspace_I(a) = E(a).1`."

**Problem**: The cited foundations don't formally establish the identification `subspace_I = E(·).1`. ASN-0043's L0 introduces `subspace_I(·)` as an abstract identifier function. T7 (FirstElementFieldDistinction) reasons about *distinct* first-element-field components yielding distinct tumblers, but doesn't define the subspace identifier as E(·).1. T4b's unique-parse decomposition gives the E-field structure but again doesn't make the bridge. This identification is the load-bearing step that produces the cross-domain contradiction `E(x).1 = E(a).1` versus `s_L ≠ s_C`; if the bridge isn't grounded, Step 3.3 doesn't close and Case 3 of the lemma collapses.

**Required**: Add a parallel "Link subspace partition" entry to the content-side scaffolding section stating `E(a).1 = s_L` for every `a ∈ dom(Σ.L)` (symmetric to the existing content-side assumption `E(a).1 = s_C`), so the identification is an explicit scaffolding commitment rather than a bridge claim derived from incomplete foundation citations.

### Issue 2: AllocatorTreeDepth references ASN-0093 by number

**ASN-0094, Definition — AllocatorTreeDepth**: "...the number of T10a child-spawn pairs `(·, k')` with `k' ∈ {1, 2}` on ASN-0093's structural chain from `d` to A's base address."

**Problem**: ASN-0093 is not in the verified foundation list. Direct ASN-by-number references outside the foundation violate the self-containment standard. The chain concept is part of ASN-0086's SubstrateConformingLayer (which is foundation), so the route through ASN-0086 is available.

**Required**: Reword to "the substrate-conforming layer's chain (via ASN-0086, SubstrateConformingLayer)", or — preferable, given Issue 3 — remove the definition entirely.

### Issue 3: ZeroCountDepth and AllocatorTreeDepth are unused

**ASN-0094, Definition section**: Both ZeroCountDepth and AllocatorTreeDepth are introduced at the top of the document.

**Problem**: Neither definition is invoked in the body, in any proof, in any template, or in the property table at the end. They appear vestigial.

**Required**: Either remove both definitions, or invoke them where they belong (perhaps in SingleHomeCoverageDiscipline's chain-index reasoning, which currently uses "chain-index" without reference to these depth concepts).

### Issue 4: "Multiset-valued" wording is imprecise

**ASN-0094, Canonical Catalog table, NonIdempotentDirectedPair row**: "*base:* `pair_K(a, b)`, `from_K(a)`, `to_K(b)`, `from_addrs_K(b)`, `to_addrs_K(a)` (multiset-valued on the tuple side without Sh4)"

**Problem**: The base accessors `from_K(a)` and `to_K(b)` return sets, not multisets — R1 (AddressInjectivity, ASN-0086) guarantees distinct tuple addresses. What's actually multiset-valued is the *slot-projection* of those sets (since two distinct tuples may share `(from₁, to₁)` values without Sh4). The walkthrough below clarifies this correctly: "the tuple-valued accessors `from_K` and `to_K` may contain multiple slot-pair-identical tuples". The catalog row's wording contradicts the walkthrough.

**Required**: Replace "multiset-valued on the tuple side without Sh4" with "set-valued; may contain slot-pair-identical tuples without Sh4" or similar phrasing consistent with the walkthrough.

### Issue 5: C-fin not in content-side scaffolding

**ASN-0094, cov_allocated Definition**: "This set is finite at every Σ (since `A^Σ` is finite by L-fin and C-fin)..."

**Problem**: The body invokes C-fin (content-store finiteness) for finiteness of `A^Σ`, and the SingleHomeCoverageDiscipline argmax argument depends on this (via "`S_d` is finite at every reachable Σ" → "`dom(Σ.L)` is finite by L-fin"; the content-store side has no parallel citation). C-fin appears in the SubstrateConformingLayer Definition's ASN-0093 substrate invariants list, but the explicit content-side scaffolding section enumerates only (element-level addresses, subspace partition, antichain, monotonicity, per-document chains) — finiteness is not listed.

**Required**: Add a sixth content-side scaffolding clause: "*Content-store finiteness.* `dom(Σ.C)` is finite at every reachable state. (Content-side symmetric to L-fin from ASN-0043.)" Then cite this scaffolding clause at the cov_allocated finiteness claim and at the argmax finiteness step.

### Issue 6: Sh-conf wp_eff derivation telescopes the NoCraftedSpanReachesD discharge

**ASN-0094, Sh-conf section, *Effective weakest-precondition under Sh-conf***: "Consequently `NoCraftedSpanReachesD(Σ, d)` holds automatically at every Sh-conf-admitted Retraction call site, and the `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))` clause likewise collapses..."

**Problem**: The collapse is asserted in one sentence but requires a multi-step chain: (1) every prior R-tuple `(b, F', G') ∈ L_R^Σ` has `G' = {(b', δ(1, #b'))}` with `b' ∈ A_rel^Σ` by Sh-conf at past emissions; (2) `a_emit(Σ, d)` is on `A_L(d)`'s chain enumeration via the substrate-conforming layer's chain; (3) for `b'` with `home(b') = d`, ChainUniformLength + T10a.7 force same-length distinctness, hence prefix-incomparability with `a_emit`; (4) for `b'` with `home(b') ≠ d`, CrossDocDisjointness forces prefix-incomparability; (5) therefore `b' ⋠ a_emit(Σ, d)` and `a_emit(Σ, d) ∉ coverage(G')`. The single-sentence justification "by R0a's antichain on `dom(Σ'.L)`" inverts the natural derivation direction (the post-state antichain is a *consequence* of the substrate's invariant preservation, not a *cause* of the pre-state safety) and doesn't enumerate the home/cross-home cases.

**Required**: Either expand the derivation to spell out the chain-element argument with explicit case split on `home(b') = d` versus `home(b') ≠ d`, or extract it as a standalone lemma cited at this point.

## OUT_OF_SCOPE

### Topic 1: Higher-arity relations

**Why out of scope**: The ASN explicitly restricts to the arity-3 standard-triple slice (Scope and Substrate Scaffolding). Extending shape components per extra slot is not this ASN's task; the framework as-is is consistent for arity-3 and the Open Questions section flags the extension explicitly.

### Topic 2: Ghost-targeting slot semantics

**Why out of scope**: Sh-conf clause (d) requires slot addresses already-allocated; ghost addresses are explicitly forbidden in slot positions. Whether a future shape family should admit ghost-targeting slot semantics — and under what state-dependent conformance rule — is flagged in Open Questions and is a separate design question.

### Topic 3: Composite shapes

**Why out of scope**: Relations whose F or G is constrained by another relation's content (rather than by a bare target-domain symbol) are flagged in Open Questions. Whether they require a new restriction axis is a future-ASN question.

### Topic 4: Cross-process shape registry consistency

**Why out of scope**: Lifetime constancy is committed within a single process; cross-process consistency in a distributed substrate is flagged in Open Questions and is outside the current scope.

VERDICT: REVISE

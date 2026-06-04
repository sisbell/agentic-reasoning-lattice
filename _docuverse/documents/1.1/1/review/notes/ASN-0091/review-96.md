# Review of ASN-0091

The mathematics here is sound. I checked the realization argument (clauses (i)–(v) + J3), the RE-* derivations, the multi-step chaining lemma, and all six worked examples at the value level — they hold. The abstract-class / REARRANGE_K separation is well-executed and the ASN is squarely in scope (it defines a transition class, its frame/admissibility, and derives system guarantees). My findings are residual meta-prose, consistent with the `review-mode.anti-bloat` signal.

## REVISE

### Issue 1: Forward-reference announcement in the shared-image licence
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "distinct bijections can witness a single transition `Σ → Σ'`. This is the canonical statement of the licence; later sections invoke it by name."
**Problem**: "This is the canonical statement of the licence; later sections invoke it by name" is navigation meta-prose — it enumerates downstream consumers rather than advancing the definition's meaning. The naming ("shared-image licence") is fine; the announcement of where it will be reused is the accreted noise the anti-bloat pass targets.
**Required**: Drop the second sentence; keep the substantive statement that within-block assignment is free.

### Issue 2: Double-counted use-site inventory in "State-Component-Only Invariants"
**ASN-0091, "State-Component-Only Invariants"**: "The class — ASN-0036's S0, S1; ASN-0047's P0, P1, P2, P3 (P3 the synthesis of P0 ∧ P1 ∧ P2 ∧ L12); L12; ASN-0093's M1, C0 — is therefore discharged uniformly by RA-frame..."
**Problem**: The inventory lists P3 *and* its four conjuncts P0, P1, P2, L12 — by the parenthetical's own admission P3 = P0 ∧ P1 ∧ P2 ∧ L12, so they are counted twice. The parenthetical "(P3 the synthesis of …)" restates a foundation definition that does not advance the discharge. This is the use-site-inventory / essay-restatement pattern.
**Required**: State the principle (RA-frame fixes each component with equality, so monotonicity/value-preservation clauses hold trivially) and cite the discharged invariants once, without re-deriving P3's composition.

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a fragmented transcluded span
**Why out of scope**: RE-trans honestly records that each fragment carries the correct `origin(·)` but that whether the fragments *jointly reconstitute* the source span is "not established here," and Open Question 1 carries it forward. This is correct deferral, not an error.

### Topic 2: Link-subspace rearrangement semantics, run-cardinality upper bounds, observational equivalence
**Why out of scope**: The remaining Open Questions name genuinely new operations/properties (a REARRANGE on the link subspace, a bound on per-invocation fragmentation, discoverability-level equivalence). These belong in future ASNs, not as revisions here.

VERDICT: REVISE

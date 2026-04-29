# Review of ASN-0074

## REVISE

No issues found.

## OUT_OF_SCOPE

### Topic 1: Content reference validity across state transitions
Operations (INSERT, DELETE, COPY) modify the arrangement, potentially invalidating previously well-formed content references. How references are maintained, updated, or re-validated across state transitions is a concern for the operation ASNs that consume content references, not for this ASN which defines them relative to a single state.

**Why out of scope**: This ASN correctly defines static content references and resolution against a given state. State-transition semantics are new territory.

### Topic 2: Link-subspace content references
The definitions are general (any subspace with V_{u₁}(d_s) ≠ ∅ and m ≥ 2), but only text-subspace positions (u₁ ≥ 1) are exercised in the worked example. When the link subspace (u₁ = 0) is formally specified, its content references should be validated against these definitions.

**Why out of scope**: The link subspace is not yet defined in the foundation; the generality of this ASN's definitions anticipates it without requiring it.

---

Detailed verification notes:

**C0 (OrdinalDisplacementNecessity)**: The contradiction argument is tight — constructs infinitely many depth-m tumblers in ⟦σ⟧ when action point k < m, each required by well-formedness to be in dom(M(d_s)), contradicting S8-fin. Uses T0(a) for unbounded component values and T3 for distinctness. All cases (k = 1 through k = m−1) are covered uniformly.

**C0a (PrefixConfinement)**: The proof correctly handles the depth issue: first establishes J = ∅ (no divergence before position m) by showing any divergence at j₀ < m forces t > reach(σ); then separately shows #t ≥ m via the proper-prefix argument. The parenthetical explaining m = 1 failure motivates precondition (iv). Subspace confinement (t₁ = u₁) falls out as the j = 1 case.

**C1a (RestrictionDecomposition)**: The three-property verification (S2, S8-fin, S8-depth for the restriction) is clean. The M11 reconstruction is detailed: singleton initialization with explicit B1/B2/B3 verification, termination via S8-fin, merge-step preservation via M7f with explicit B3 case split using M-aux. The M12 generalization correctly identifies that maximal-run characterization depends only on pointwise evaluation of f — the maximal run conditions (extending forward/backward, checking dom(f) membership and I-continuity) use no structural property beyond S2 and finiteness.

**C1 (ResolutionIntegrity)**: The chain B3 → M(d_s)(vⱼ + i) = aⱼ + i → vⱼ + i ∈ dom(M(d_s)) → S3 → aⱼ + i ∈ dom(C) is direct and complete.

**C2 (ResolutionWidthPreservation)**: The enumeration of depth-m tumblers in the span range — exactly {[u₁, ..., u_{m−1}, j] : uₘ ≤ j < uₘ + ℓₘ} — is verified in both directions (C0a fixes the prefix, ordering constrains the last component). The count ℓₘ = |dom(f)| then combines with B1/B2 (partition) and M0 (width coupling) to give the sum.

**Worked example**: Exercises the non-trivial case (span crossing two blocks from distinct origins), correctly applies M16 to establish merge impossibility at the cross-origin boundary, and verifies C1 and C2 against concrete values.

**No circular dependencies**: C0 and C0a are consequences of well-formedness (not preconditions for it). The definition uses C0a to explain why precondition (iv) is necessary, which is a design rationale, not a logical dependency.

**Foundation usage**: All cross-references are to foundation ASNs (ASN-0034, ASN-0036, ASN-0053, ASN-0058). No reinvented notation — the ASN uses ⊕, δ(n,m), ⟦σ⟧, reach(σ), V_S(d), and block decomposition machinery directly from the foundations.

VERDICT: CONVERGED

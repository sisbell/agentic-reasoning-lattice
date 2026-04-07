# Integration Review of ASN-0058

## REVISE

(none)

The integrated properties (ContentReference, C0, C0a, ContentReferenceSequence, resolve, C1a, C1, C2) are rigorous and correctly integrated. Specific observations:

**C0 (OrdinalDisplacementNecessity).** The proof by contradiction is complete: when action point k < m, the family of depth-m tumblers w_j with j > u_m are all in ⟦σ⟧ (divergence at k < m ensures w_j < reach(σ) independent of j), yielding infinitely many positions in dom(M(d_s)) — contradicting S8-fin. The case k > m is excluded by #ℓ = m. Sound.

**C0a (PrefixConfinement).** The proof correctly handles both the main case (J non-empty leads to t > reach(σ) via divergence at j₀ < m) and the depth case (#t < m implies t is a prefix of u, contradicting u ≤ t). The conclusion covers all t ∈ ⟦σ⟧ regardless of depth, which is the right generality.

**ContentReference definition.** The forward reference to C0a is explanatory, not definitional — the well-formedness condition (depth-m positions in span range ⊆ dom(M(d_s))) is self-contained. Preconditions (i)–(iv) are correctly motivated and necessary: (i) ensures m is well-defined via S8-depth, (iv) ensures subspace confinement via C0a.

**C1a (RestrictionDecomposition).** The verification that f = M(d_s)|⟦σ⟧ satisfies S2, S8-fin, and S8-depth is correct. The extension argument — that M11/M12's proofs use only pointwise evaluation and these three properties — is accurate; the maximal-run characterization in M12 references B2 (disjointness) and S8-depth (no position between v+(n-1) and v+n), both of which hold for the restriction. The explicit B3 case split for the merged block (k < n₁ from β₁, k ≥ n₁ from β₂ via M-aux) is complete.

**C1 (ResolutionIntegrity).** The chain B3 → M(d_s)(v_j + i) = a_j + i → S3 → a_j + i ∈ dom(C) is direct and complete.

**C2 (ResolutionWidthPreservation).** The enumeration of dom(f) = {[u₁,...,u_{m-1}, j] : u_m ≤ j < u_m + ℓ_m} is exhaustive: C0a fixes the first m-1 components, S8-depth forces depth m, and well-formedness ensures inclusion. The partition argument via B1+B2+M0 correctly yields Σn_j = ℓ_m.

**Worked example.** The resolution example correctly demonstrates cross-origin non-mergeability (M16 applied to the restriction) and total-width preservation.

**Registry.** All eight entries are present with correct labels and descriptions.

VERDICT: CONVERGED

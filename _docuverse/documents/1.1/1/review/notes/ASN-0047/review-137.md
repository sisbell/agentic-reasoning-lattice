# Review of ASN-0047

## REVISE

(none)

## OUT_OF_SCOPE

(no additional topics raised by review; the ASN's own Open Questions section catalogues the future-ASN concerns I would otherwise note — node-allocation registry protocol, link-withdrawal mechanism, one-sided links, forked-arrangement invariants, version-lineage/arrangement relationships, account-level depth-1 extension)

After reading the ASN with deliberate attention to common failure modes, I cannot identify a REVISE item. Specifically:

- **Hand-waves**: Searched for "by similar reasoning", "analogously", trailing "✓" without proof. The two-case analyses (Case `s_C → s_L` / Case `s_L → s_C` in K.μ~ Step (A); Case A / Case B in Cross-document disjointness; m=2 / m≥3 in D-SEQ★) are *all* proved explicitly rather than collapsed via symmetry appeals.
- **Edge cases**: Empty subspaces (vacuous D-CTG★/D-MIN★), singletons (K.μ~ existence condition `|dom_C(M(d))| ≥ 2` necessity proven), `dom_C = ∅ ∧ dom_L ≠ ∅` mixed case (explicitly excluded), bootstrap n₀ at Σ₀ (NodeRegistryBootstrap supplied as separate base axiom), K.δ k=0 / k=1 / k=2 dispatch via T10a.6, fork with empty source content subspace (excluded → ex nihilo) all handled.
- **Invariant coverage**: Verification matrix systematically dispatches each Class (a) per-state invariant per elementary transition; Class (b) composite-boundary properties have a separate discharge table with J0/J1★/J1'★ at the boundary.
- **Depth**: K.μ⁻ admissible contraction shape proved as a biconditional with both directions; D-SEQ★ derivation has full m=2 and m≥3 proofs; K.μ~ link-subspace fixity proof has explicit 4-step chain with named non-circular dependency structure (A)→(B)→(C)→(D)→(E); GlobalLineage decomposes into three sub-proofs (entities, content, links) with explicit inc-chain induction for the link case.
- **Concrete examples**: Five worked examples (entity hierarchy, fork, interior replacement, prior-provenance/first-time-transcluded replacements, link allocation), each verifying postconditions against specific tumbler values rather than abstract claims.
- **wp analysis**: J1 derivation explicitly computes `wp(K.μ⁺, Contains(Σ') ⊆ R')` and shows K.μ⁺ alone cannot maintain P4. The orphan-link discussion explicitly addresses absence-of-coupling as a design choice rather than oversight.
- **Foundation usage**: All cross-ASN references (ASN-0034, 0036, 0040, 0043, 0045, 0093) are to foundation ASNs. ASN-0093's K.α/K.λ/SubAllocatorAxiom/SequentialTransitionAxiom/SubspaceConventionAxiom/L0/L3/L1c/C-fin are correctly attributed and not re-derived.

VERDICT: CONVERGED

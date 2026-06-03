# Review of ASN-0087

## REVISE

(none)

The ASN is mathematically sound and complete on the points I checked:

- **L1c chain** is constructed explicitly with per-step zero-count and length verification; TA5a admissibility saturates exactly at steps 1 (`zeros(d)=2≤2`, `k=2`) and 3 (`zeros(b_L(d))=3≤3`, `k=1`). The supplementary uniqueness argument is correctly labeled non-load-bearing.
- **S2 freshness** is split into within-subspace (D-SEQ★) and cross-subspace (`s_L ≠ s_C`, SC-NEQ) exclusions rather than hand-waved — exactly the conjunct that is most often skipped.
- **Boundary cases** are handled: empty link subspace (M-DepthConv supplies `m=2`), empty non-type endsets (`coverage(∅)=∅` via LP12's existential), reflexive endsets (worked concretely with witness `v_ℓ`), cross-document discovery (worked example exercises both intra- and cross-document endsets).
- **wp analysis** is non-trivial: the reflexive disjunct in Case 2 is genuine and collapses only under the explicitly-named `StandardAuthoring` predicate; enabledness and the `discoverable_from`-definedness membership clause are kept distinct.
- **M-DepthConv** is correctly scoped to a guarded universal ("any `d` whose every link V-position was placed by MAKELINK") rather than overreaching to a system-wide depth-2 invariant, consistent with K.μ⁺_L being a standalone primitive admitting any `m ≥ 2`.
- **Non-atomicity** at `Σ_mid` is handled honestly: per-state invariants verified (α/β/γ classification), composite-boundary properties correctly not claimed mid-composite, and the discoverability divergence between `Σ_mid` and `Σ'` isolated to the reflexive case at the home document.

## OUT_OF_SCOPE

### Topic 1: V-position re-pinning after full link-subspace clearance
The interaction where `dom(L)` retains links with `origin(d)` while `V_{s_L}(d) = ∅` (post-K.μ⁻) — so `ℓ` is a subsequent emission but `v_ℓ` is a first V-position re-pinned at depth 2 — is handled by the effect formulas but not narrated. This belongs with the K.μ⁻/movement questions the ASN already defers in Open Questions, not in MAKELINK proper.

### Topic 2: Ghost-type and never-allocated endset discoverability
Already correctly deferred to Open Questions and grounded in foundation lemmas (L9, LP17/LP18).

VERDICT: CONVERGED

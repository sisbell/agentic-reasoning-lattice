# Channel Assignment — ASN-0047 review-117

**Date:** 2026-05-19 14:51

```
## Issue 1: Cross-document disjointness chain lemma doesn't cover cross-subspace case
Reason: The fix is derivable from the ASN. Either generalize the lemma to admit prefixes `[e₁.0.s₁]` and `[e₂.0.s₂]` with possibly distinct `s₁, s₂` (the divergence-index argument works on `e₁ ≠ e₂` regardless of subspace components), or split the discharge — same-subspace cases by the lemma, cross-subspace case by SC-NEQ + L0 + T7 (all foundation properties already cited).
```

```
## Issue 2: K.δ case (ii) k = 0 lists structural identities as preconditions
Reason: The contradiction is internal — the ASN lists `parent(t) = parent(e)` and `zeros(t) = zeros(e)` both as caller-side preconditions and as derived consequences of `e = inc(t, k)`. Resolution requires choosing one framing; the structural identities follow from TA5 + T4b directly per the ASN's own derivation note.
```

```
## Issue 3: SubAllocatorAxiom.Disjointness cross-subspace within-document discharge
Reason: The fix is to spell out the chain explicitly — SubAllocatorAxiom.Subspace gives outputs inherit `E(·)₁ = s_C` or `s_L`, SC-NEQ gives `s_C ≠ s_L`, and T7 (applicable at zeros = 3 for outputs) makes them distinct. All cited properties are already in the ASN.
```

```
## Issue 4: Reverse direction of CL-UNIQ preservation under K.μ~ lacks explicit step
Reason: The injectivity-inheritance inference (functional identity + injective pre-image ⟹ injective post-image) is standard set theory and already implicit in the K.μ~ proof. One sentence ties Steps 1–3's functional identity to the matrix cell's CL-UNIQ preservation claim.
```

```
## Issue 5: Forking k=1 case admits sequential versions only via separate K.δ k=0 events
Reason: The fix is presentational. The structural mechanism (K.δ k=1 once per source, then K.δ k=0 chain on prior versions) is already specified by the ASN; parent(vᵢ) = parent(d) at the account level by T4b on TA5(c), and P8 preservation is the standard K.δ k=0 case. Adding a worked example or clarifying paragraph requires no external input.
```

```
## Issue 6: K.μ~ Decomposition's "any valid K.μ⁻ + K.μ⁺ pair" admits underspecified non-determinism
Reason: The non-determinism, its admissibility conditions (below-cut value-preservation for partial-suffix forms), and the universally-applicable full-clearance fallback are all described in the Decomposition section. The fix is to surface this structure at K.μ~'s definition site and adjust downstream citations to name the full-clearance form as the universal realisation.
```

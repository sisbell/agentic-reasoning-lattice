# ASN-0085: V-Position Ordinal Decomposition

*2026-04-11*

The strand model (ASN-0036) defines V-positions as element-field tumblers whose first component is the subspace identifier (subspace(v) = v₁), and the ordinal-only formulation of TA7a (ASN-0034) establishes that within-subspace arithmetic passes only the ordinal to the operations while holding the subspace identifier as structural context. This ASN extends the strand model with the concrete extraction and reconstruction functions that formalize this decomposition: separating a V-position into its subspace identifier and its within-subspace ordinal, reconstructing a V-position from these components, and projecting a V-depth displacement onto its ordinal component. These definitions are the operational bridge between the full V-position space and the ordinal-only arithmetic that TA7a prescribes.


## Ordinal Extraction

We frequently need to separate a V-position into its subspace identifier and its ordinal within that subspace. Per the ordinal-only formulation of TA7a (ASN-0034), we define the extraction and reconstruction functions.

**ord(v)** — *OrdinalExtraction* (DEF, function). For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier.

**vpos(S, o)** — *VPositionReconstruction* (DEF, function). For subspace identifier S and ordinal o = [o₁, ..., oₖ]:

`vpos(S, o) = [S, o₁, ..., oₖ]`

with #vpos(S, o) = k + 1. These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v.

**w_ord** — *OrdinalDisplacementProjection* (DEF, function). For a V-depth displacement w with w₁ = 0 and #w = m, the *ordinal displacement* is:

`w_ord = [w₂, ..., wₘ]`

of depth m − 1. At the restricted depth m = 2, w = [0, c] for positive integer c, and w_ord = [c].


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ord(v) | DEF | Ordinal extraction: ord(v) = [v₂, ..., vₘ] strips the subspace identifier | introduced |
| vpos(S, o) | DEF | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord | introduced |
| w_ord | DEF | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for V-depth w with w₁ = 0 | introduced |


## Open Questions

Can the round-trip property (ord(p) ⊕ w_ord) ⊖ w_ord = ord(p) and the commutativity of shift with ordinal increment be generalized to ordinals of depth greater than one?

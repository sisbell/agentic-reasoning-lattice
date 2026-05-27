# Channel Assignment — ASN-0091 review-27

**Date:** 2026-05-26 22:00

## Issue 1: RE-subpres proof doesn't rule out third subspace values
Reason: The fix is derivable from the ASN's own content — S3★-aux is already established as preserved by RA-adm and constrains `subspace(π(v)) ∈ {s_C, s_L}`. Pure proof-completion using machinery already in the ASN.

## Issue 2: Worked Example 4 lacks admissibility verification
Reason: The fix applies the same verification pattern already established in the prior three worked examples against the constructed Σ'. All foundation invariants (S2, S3★, S5, S8★, P4★, etc.) and their checking patterns are present in the ASN.

## Issue 3: RE-frag★/RE-coal★/RE-eq★ claim has no explicit witness
Reason: The construction reuses the single-step RE-frag/RE-coal/RE-eq witnesses already exhibited in the ASN, composed via RE-ext's pointwise preservation across disjoint V-sub-ranges. All building blocks are internal.

## Issue 4: Bijection-class characterization's forward direction compressed
Reason: The fix is pure exposition — expanding (a) mapping-into, (b) injectivity, (c) surjectivity, (d) equicardinality from π's global bijectivity on finite sets. Standard set-theoretic reasoning, no external input required.

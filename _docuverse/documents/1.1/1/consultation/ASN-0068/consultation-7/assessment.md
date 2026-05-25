# Channel Assignment — ASN-0068 review-7

**Date:** 2026-05-25 12:23

## Issue 1: CV-SPAN-VIEW signature is type-inconsistent
Reason: Pure type-signature correction. The fix (change codomain from `P(Span × Span)` to `Span × Span`, with set-level lift by standard image construction) is derivable from the ASN's own definitions and standard mathematical convention.

## Issue 2: Introduction's "bijection" claim conflates element-level and set-level
Reason: Pure formulation fix. The lifted map π* and its injectivity from per-run injectivity are derivable from CV-SPAN-VIEW's existing structure; the choice between explicit lift or corollary placement is editorial, not requiring external input.

## Issue 3: "Exactly n_σ V-positions" claim ignores arrangement truncation
Reason: Mathematical correction derivable from CV-IN's existing admissibility clauses and the V-position counting facts from S8-depth (ASN-0036). The fix (qualify the count or separate the two claims) follows from the ASN's own structure without needing design-intent clarification or implementation evidence.

## Issue 4: CV-PRED's "valid V-position" predicate is implicitly restricted to D-SEQ★ form
Reason: Pure formulation fix. The choice between explicitly scoping CV-PRED to `V_S(d)` or defining `v − j` as the tumbler-level shift inverse via TS2 is derivable from the ASN's existing references (D-SEQ★ in ASN-0047, TS2 in ASN-0034).

## Issue 5: Self-comparison admissibility derivation is informal
Reason: Derivation is mechanical unpacking of CV-IN's clauses under `d_a = d_b`. All required facts (V-set equality, depth collapse, vacuous single-literal caveat) are derivable from CV-IN as stated; no external channel needed.

## Issue 6: CV-PROV-FORGOTTEN's "exactly one" claim leans on S7 without invoking attribution-uniqueness
Reason: Citation refinement requiring lookup of S7's labeled postconditions in ASN-0036, which is already a cited reference in this ASN. The specific postconditions to cite are derivable from ASN-0036's own structure.

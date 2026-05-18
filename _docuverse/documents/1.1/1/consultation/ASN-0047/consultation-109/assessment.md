# Channel Assignment — ASN-0047 review-109

**Date:** 2026-05-18 10:03

## Issue 1: NodeRegistryBootstrap "Scope note" is defensive prose
Reason: Pure prose-trimming task — collapse defensive meta-paragraphs into one sentence and move forward-looking pointer to Open Questions. The required structure is derivable from the existing axiom content and ASN organisation; no design or implementation question is at stake.

## Issue 2: K.μ⁻ "Per-subspace suffix pattern" precondition is redundant with derived lemma
Reason: Logical-structure correction internal to the ASN — D-CTG★/D-MIN★/D-SEQ★ are already stated as post-state invariants, and the lemma's derivation already shows the suffix shape follows from them. Choosing which side bears the obligation (precondition vs. derived consequence) is a presentation decision derivable from the ASN's own apparatus.

## Issue 3: A_v(d) case-split duplicated across sections
Reason: Organisational deduplication — state the case-split once at the definition site, cite by name at the discharge site. The substantive content is unchanged; both sections already say the same thing using the same T10a.6 argument.

## Issue 4: Sub-case labels (i)(ii)(iii) collide with K.δ top-level case labels
Reason: Pure notation/labeling issue — relabel the t-identity sub-sub-cases (e.g., A/B/C) to disambiguate from K.δ's top-level (i)/(ii). No design or implementation question involved.

## Issue 5: Fork example Step 3 mischaracterises S8-depth
Reason: The fix is a precise restatement using definitions already in this ASN and ASN-0036 — S8-depth is uniform-depth-within-subspace, subspace identity is `subspace(v)`. Separating the two properties is derivable from the existing definitions.

## Issue 6: K.μ~ partial-suffix admissibility "iff" claim overstated under sharing
Reason: Logical correction internal to the ASN — S5 (UnrestrictedSharing, ASN-0036) is already in scope, and both repair routes (weaken to "if", or restate as value-preservation iff) follow from the existing K.μ⁺ value-preservation clause and S5. The fix is purely a sharpening of the existing argument.

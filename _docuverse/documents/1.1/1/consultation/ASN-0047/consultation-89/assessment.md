# Channel Assignment — ASN-0047 review-89

**Date:** 2026-05-17 20:31

## Issue 1: P5 supersession by P3★ not made explicit in prose
Reason: Editorial fix derivable from the ASN itself — P3★'s body and table footnote already establish that it extends P5's monotonicity statement to L. Adding the explicit supersession clause needs no external evidence; the relationship is internal to the document.

## Issue 2: Allocator names A_C(d), A_L(d), A_v(d) used without formal definition
Reason: The content and link sub-allocators are already structurally specified via b_C(d), b_L(d), and SubAllocatorAxiom; naming them A_C(d) and A_L(d) is internal formalisation. A_v(d) for version allocation is referenced but never anchored — confirming its existence in the implementation grounds the formal definition.
Gregory question: Does udanax-green maintain a distinct per-document version allocator (analogous to the content and link sub-allocators) whose frontier is tracked across docreatenewversion emissions, or is version allocation dispatched through some other mechanism (e.g., a single global version frontier, or directly via inc on the prior version address)?

## Issue 3: "SubAllocatorAxiom.Namespace's structural commitment" references an unnamed sub-property
Reason: Pure internal editorial fix — SubAllocatorAxiom's body already specifies the structural form `[d.0.s_C.1]` / `[d.0.s_L.1]` and T4-validity is derivable from T4b applied to those forms. The fix is either adding a sub-clause label or replacing the dot notation with a direct citation, both derivable from existing content.

## Issue 4: K.μ⁻ admissible pattern has redundant disjunction
Reason: Internal — the suffix parameterisation `0 ≤ n'_S ≤ n_S` already subsumes full clearance at n'_S = 0, and the K.μ⁻ exhaustiveness lemma right below confirms this unification. Pure editorial rephrasing.

## Issue 5: Allocator hierarchy section's introduction enumerates downstream consumers
Reason: Style-only fix derivable from the ASN itself — replace consumer enumeration with an object-naming orientation sentence. No external evidence required.

# Revision Categorization — ASN-0063 review-21

**Date:** 2026-03-22 01:58

## Issue 1: CL0 — Element-level tightness proof incomplete for I-addresses
Category: INTERNAL
Reason: The prefix-matching argument is already shown in full for V-positions in the same proof. The I-address case is structurally identical — the fix is adding the symmetric two-step argument using the same T1(i) reasoning already present.

## Issue 2: Cross-origin span disjointness — "T10 gives disjointness directly" oversimplifies
Category: INTERNAL
Reason: The ordering argument extending T10 point disjointness to interval disjointness uses only T1 and the property that start and reach share a prefix — all already available in the ASN and referenced definitions. No design intent or implementation evidence needed.

## Issue 3: K.μ~ fixity proof — intermediate-state notation
Category: INTERNAL
Reason: The proof logic is correct; the issue is notational precision about which state the frame condition references. The fix is chaining through M_int using facts already established in the same paragraph (r = 0, K.μ⁻ preserves values).

## Issue 4: K.μ⁺_L — misleading parenthetical
Category: INTERNAL
Reason: The formal precondition is correct. The fix is rephrasing a parenthetical clarification to avoid implying K.λ must immediately precede K.μ⁺_L — a wording change derivable from the transition framework's own compositionality rules.

## Issue 5: VSpanImage definition — "gaps" conflicts with D-CTG
Category: INTERNAL
Reason: D-CTG is already stated in the ASN's own references. The contradiction between "gaps from prior content removal" and D-CTG's contiguity guarantee is resolvable by correcting the informal description to match the formal invariant.

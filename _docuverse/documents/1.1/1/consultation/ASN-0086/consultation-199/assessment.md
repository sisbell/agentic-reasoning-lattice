# Channel Assignment — ASN-0086 review-199

**Date:** 2026-06-01 14:37

## Issue 1: "the converse fails" is mis-cited and possibly false
Reason: Fully derivable from the ASN. The cited witness (NestedLinkWitness) is non-conforming, so it cannot support a converse-failure claim, and the ASN's own R7a plus the `→ ≡ K.σ ∪ K.α ∪ K.λ` completeness assertion point toward the converse actually holding — so the clause should be dropped. No external intent or implementation evidence is needed to resolve the internal mis-citation.

## Issue 2: a_emit "formula, not a commitment" — defensive meta-prose with forward deferral
Reason: Pure editorial deletion. `a_emit`'s totality is already stated in the definition, and the frontier/commitment relationship is established at Emit_K; removing the defensive paragraph requires no design intent or implementation fact.

## Issue 3: the non-frontier / NestedLinkWitness case is re-explained in four separate sections
Reason: Internal restructuring. The canonical statement (Remark — NestedLinkWitness) and the genuine wp invocations already exist in the ASN; consolidating to remove the duplicative a_emit/Emit_K restatements is derivable from the note's own content.

## Issue 4: Emit_K introduction explains notation rather than advancing meaning
Reason: Editorial removal. The indexed signature line already conveys that K is a family index, so deleting the notation commentary needs no external input.

# Channel Assignment — ASN-0086 review-201

**Date:** 2026-06-01 14:54

## Issue 1: Emit_K partiality passage restates and forward-defers rather than advancing
Reason: Pure editorial compression — the required rewrite, the P0f predicate, the NestedLinkWitness construction, and `a_emit`'s totality all already live in the ASN; no design intent or implementation evidence is needed to delete restatement and directional framing.

## Issue 2: wp Result explains why a conjunct is absent rather than stating the wp
Reason: Removing meta-prose about the wp's free variables is internal to the note; the fact that `K` is an index rather than a free variable is already stated in the Result, so the fix is derivable from the ASN alone.

## Issue 3: wp Case 1 "Domain of quantification" re-exposits the partial-operation convention
Reason: Deletion of scaffolding already carried by the P0-drop case in the load-bearingness paragraph; the partial-operation semantics are stated elsewhere in the ASN, so no channel consultation is required.

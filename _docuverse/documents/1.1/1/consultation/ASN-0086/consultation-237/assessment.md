# Channel Assignment — ASN-0086 review-237

**Date:** 2026-06-01 20:44

## Issue 1: "into but not onto" overstates — addr is onto when the store holds only triples
Reason: The fix is internal — the ASN's own TypedRelation definition (the `|Σ.L(a)| = 3` conjunct) and L3 (NEndsetStructure, ASN-0043, permitting higher-arity links) already establish that surjectivity is state-dependent; rewording the clause needs no external channel.

## Issue 2: Nullify's *Effect* defers its own semantics forward to wp Case 1 (forward-reference meta-prose)
Reason: The fix is internal — Nullify's effect is fully specified by its own definition (`Emit_R` composition), R0, R5.1, and R-Scope already present in the ASN; restating the effect self-contained and removing the meta-prose is a pure prose restructuring.

## Issue 3: relational layer / layer-reachable restate the same discipline commitment in different words
Reason: The fix is internal — both definitions are the ASN's own and assert identical content; consolidating to a single statement with a by-name reference is pure deduplication requiring no design intent or implementation evidence.

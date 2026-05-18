# Channel Assignment — ASN-0086 review-54

**Date:** 2026-05-18 06:10

## Issue 1: R7a proof — class-(i) admissibility argument is incomplete
Reason: The fix is a definitional choice between (a) stating class-(i) Frame as freshness + T4-valid + zeros = 2 with T10a-conformance treated as opaque, or (b) extending the replay vocabulary. Both paths can be discharged from ASN-0036 plus ASN-0086's own framing of class (i); no external channel is needed.

## Issue 2: R0a-Cor2 discussion is essay content
Reason: Trim or remove a "aligns with / matches" paragraph. Purely a stylistic revision derivable from the ASN's own content.

## Issue 3: Emit_K Definition's A_K membership paragraph duplicates WP Case 2
Reason: Deduplicate two paragraphs covering identical regimes. Structural revision internal to the ASN.

## Issue 4: "Dependency chain" pattern repetition
Reason: Establish the dependency-chain recipe once and reference. Pure structural revision within the ASN.

## Issue 5: Implementation Notes use-site inventory duplicates per-claim citations
Reason: Delete the inventory and rely on per-claim citations already present. Internal cleanup.

## Issue 6: R6c-Corollary parenthetical is defensive prose
Reason: Delete one parenthetical that explains what is not being used. Internal.

## Issue 7: Emit_K Definition has accumulated structural slots
Reason: Reduce the Definition to signature + precondition + frame; move function-ness to a lemma and A_K-membership to the WP section. Structural refactor derivable from the ASN's own content.

## Issue 8: R0 Step 2 case-exhaustiveness not stated
Reason: Add one sentence noting binary exhaustiveness of the split. Internal.

## Issue 9: Sparse forward references to ASN-0047
Reason: State once near Setup which substrate baseline ASN-0086 builds on. The author's existing citations (S3 not S3★; L0–L14 without V-position references) already indicate the ASN-0036+ASN-0043 baseline; making this explicit is an internal positioning statement.

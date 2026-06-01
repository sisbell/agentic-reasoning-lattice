# Channel Assignment — ASN-0086 review-98

**Date:** 2026-05-31 19:19

## Issue 1: The `→` definition is stated three times in different words
Reason: Pure deduplication — consolidate the identity `→ ≡ K.σ ∪ K.α ∪ K.λ` to one location and point the table row at it. No design intent or implementation evidence needed; the content is unchanged.

## Issue 2: FreshLinkKeyDisjointness carries a use-site inventory
Reason: Mechanical deletion of a downstream-consumer sentence; the lemma's content is untouched and consuming proofs already cite it by name. Internal.

## Issue 3: Observe_K's "Pattern domain" note re-proves decidability twice, then a third time
Reason: Collapse three statements of one decidability fact into one sentence. The retained justification (finiteness of `F̂`, per-span containment via T2, ghost queries via L9/L4) is all already in the ASN. Internal.

## Issue 4: wp Case 2's closing paragraph restates regimes (i)/(ii)/(iii)
Reason: Delete a redundant summary paragraph already covered by the regime definitions and the specialization paragraph. Internal.

## Issue 5: Repeated cross-section deferral to "WP Case 2"
Reason: Restructure cross-references so the crafted-span consequence is stated locally and WP Case 2 is the single authoritative site. Purely an organizational edit within the ASN. Internal.

## Issue 6: R6b mislabeled as a pure consequence of the `nullified` definition
Reason: The split (within-state flatness is definitional; cross-state persistence cites R3) is fully visible in R6b's own justification text, which already invokes R3. Relabeling and dependency-list correction are derivable from the ASN alone. Internal.

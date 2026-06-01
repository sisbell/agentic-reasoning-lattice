# Channel Assignment — ASN-0086 review-178

**Date:** 2026-06-01 10:48

## Issue 1: "Unit-depth retraction discipline" used as a state predicate but defined only as a layer property
Reason: Purely internal — the fix introduces a per-state predicate by lifting the per-state condition already used inside the wp Case 2 derivation and redefines the layer-level discipline in terms of it. No design intent or implementation evidence is required; all material is present in the ASN.

## Issue 2: The substrate-conformance / off-chain-edge necessity rationale is restated in four locations
Reason: Purely internal — consolidating four restatements of the same off-chain-edge/conformance-necessity rationale into the Remark and replacing the others with citations is a prose-deduplication edit fully determined by the ASN's own content.

## Issue 3: wp Case 2 "discipline alone is insufficient" reconstructs the NestedLinkWitness construction rather than citing it
Reason: Purely internal — folding the `b' ≼ a` extension into the Remark as a reusable sub-claim (or reducing the paragraph to a citation plus the single new nesting-inheritance step) is a structural consolidation derivable entirely from the existing NestedLinkWitness construction.

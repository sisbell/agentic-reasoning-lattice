# Channel Assignment — ASN-0070 review-78

**Date:** 2026-06-03 03:54

## Issue 1: "Frame" slots in F-persist and F-state carry commentary, not frame conditions
Reason: Internal — the fix follows directly from F1's frame `Σ' = Σ` (already in the ASN), which establishes `follow` writes no state, so no object-level frame condition exists to state; deleting the two commentary slots is mechanical and the transition context already lives in each lemma's pre/postconditions.

## Issue 2: The "an empty component arises two ways" point is stated three times
Reason: Internal — a pure deduplication of prose already present in the ASN; consolidating to the Config 6 Vacuous-subspace bullet and trimming the F-multidoc and F-empty restatements requires no external design intent or implementation evidence.

## Issue 3: F-canonical Step 0 re-derives the vacuous emptiness already established in the convention
Reason: Internal — both the Vacuous-subspace convention and Step 0 already contain the identical `R(d, e)|_S ⊆ V_S(d) = ∅` derivation; replacing the re-walk with a citation to the convention is a self-contained restructuring derivable from the ASN's own content.

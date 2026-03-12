# Revision Categorization — ASN-0030 review-1

**Date:** 2026-03-11 23:52

## Issue 1: A7a contradicts A8
Category: INTERNAL
Reason: The contradiction is between two properties stated within the same ASN. The fix — adding a precondition to A7a or quantifying over `endset(L) ∩ dom(Σ.I)` — is derivable from the definitions already present.

## Issue 2: A3(c) — transclusion cannot recover truly unreferenced content
Category: BOTH
Reason: The ASN claims transclusion recovers unreferenced content, but no defined operation creates a V-space mapping to an I-address absent from all V-spaces. Nelson's "historical backtrack functions" are cited as the intended mechanism but never specified. Gregory's implementation may reveal a code path not yet considered.
Nelson question: What mechanism did you intend for recovering content that has been deleted from all documents and versions — the "historical backtrack functions" mentioned in Literary Machines?
Gregory question: Is there any code path in udanax-green that creates a V-space (POOM) mapping to an existing I-address without reading that address from another document's V-space — i.e., a direct I-address-to-POOM insertion?

## Issue 3: `reachable(a, d)` defined independently of foundation `refs(a)`
Category: INTERNAL
Reason: The equivalence `reachable(a, d) ≡ (E p : (d, p) ∈ refs(a))` follows directly from expanding the definitions already in ASN-0026 and ASN-0030. No external evidence needed.

## Issue 4: No concrete example
Category: INTERNAL
Reason: A worked example uses only the operations and definitions already in the ASN. The scenario (create, delete, verify partition transitions) is constructible from existing formal content.

## Issue 5: A4a (REARRANGE) asserted from implementation evidence, not derived
Category: INTERNAL
Reason: The fix is presentational — relabel A4a as a specification requirement on REARRANGE rather than a derived theorem. The distinction between "required postcondition" and "known property" is an editorial decision within the ASN's own framework.

## Issue 6: A5 (COPY) introduced without preconditions
Category: INTERNAL
Reason: The missing preconditions (valid documents, in-range positions, k ≥ 1) follow the pattern of P9 (ValidInsertPos) already established in ASN-0026. No external evidence needed.

## Issue 7: A9 and A10 listed alongside formal invariants
Category: INTERNAL
Reason: The fix is structural — reclassify A9 and A10 as design remarks or move them to a discussion section. This is an editorial decision about how to organize the properties table.

# Channel Assignment — ASN-0086 review-195

**Date:** 2026-06-01 14:05

## Issue 1: Remark — NestedLinkWitness mutually forward-defers with Emit_K
Reason: Purely structural relocation — confine the Remark to the antichain-violating witness and move Emit_K's undefinedness statement to its own definition. The content already exists in the ASN; this is text reorganization with no design-intent or implementation question.

## Issue 2: wp Case 2 load-bearingness restates its derivation as a preview
Reason: Editorial deletion of a redundant preview sentence already stated verbatim in the Derivation. No external evidence needed; the fix is internal to the ASN's own prose.

## Issue 3: Definition — relational layer digresses into "sufficient not equivalent"
Reason: Editorial trimming — replace the sufficient-vs-equivalent excursion with a plain statement that the layer routes R-typed emission through P1-confined Nullify. Derivable from the layer's existing definition; no channel required.

# Channel Assignment — ASN-0086 review-96

**Date:** 2026-05-31 19:04

## Issue 1: WP Case 1 inconsistently drops Nullify's precondition P2 from the weakest precondition
Reason: The fix is a methodological/presentational consistency choice between two options the review already spells out, and all the relevant material — P2's status, the arity-3 scope rationale, the "well-formed Emit_R" remark, Case 2's guard-inclusion standard — is already present in the ASN. No design intent or implementation evidence is required.

## Issue 2: R0a-Cor1 postcondition (a) derivation stated twice
Reason: Pure deduplication of a derivation that appears twice within the ASN; the content is self-contained and the fix is editorial.

## Issue 3: Forward-consumer prose in R0a-Cor1
Reason: Editorial removal of placement-justifying meta-prose; nothing external is needed to state the two consequences directly.

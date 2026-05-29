# Channel Assignment — ASN-0040 review-46

**Date:** 2026-05-28 21:01

## Issue 1: B0a restates the same partition three times
Reason: Pure editorial deletion of redundant restatements; the operative two-clause partition is retained verbatim from the ASN, so the fix is internal.

## Issue 2: B4 carries formalization-choice and implementation-status meta-prose
Reason: Removing the framing-justification and implementation disclaimer requires only the ASN's existing B4 statement and its B7-derived per-namespace scope; no design-intent or implementation evidence is needed to delete prose.

## Issue 3: The wp section re-derives Bop and the invariant proofs
Reason: The freshness, B1, and B10 arguments already exist in full within Bop's proof, §B1, and §B10; cutting or replacing with citations is internal.

## Issue 4: B3's prose restates the classification table
Reason: The table and the `Occupied(t, s) ⟹ t ∈ s.B` forward requirement already carry the content; deleting the essay paragraphs is internal.

## Issue 5: Redundant foundation citation in B7
Reason: S(p, d)'s own postconditions establish `#cₙ = #p + d`; swapping the T10a.1 citation for the local postcondition is fully internal to the ASN.

## Issue 6: Gregory-evidence inventory in the depth/field section
Reason: The retained formal point (the `.0.` separator produced by `inc(p, 2)`'s TA5(d) separator) is already derived in B5; trimming the enumerated implementation confirmations needs no fresh evidence-channel input.

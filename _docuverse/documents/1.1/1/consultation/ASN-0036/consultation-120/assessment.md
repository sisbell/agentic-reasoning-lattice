# Channel Assignment — ASN-0036 review-120

**Date:** 2026-05-28 21:40

## Issue 1: Triple-redundant restatement of T4b projection well-definedness in S7a
Reason: Pure editorial deduplication — the fix is to state the well-definedness claim once and let the Depends entries name contributions. No design intent or implementation evidence is needed; the redundancy is internal to the contract.

## Issue 2: "Specific value of m is not fixed by the strand model" restated four times
Reason: Editorial deduplication of one design decision already stated in the ASN; consolidating to the empty-case definition and removing duplicates is fully internal. The retained Nelson hook (LM 4/31) is already cited in-text, requiring no new theory input.

## Issue 3: S3 contract carries a forward-reference to Open Questions as meta-prose
Reason: The fix is simply to delete the parenthetical; the Open Question already owns the temporal-scope question. Wholly internal — no channel needed.

## Issue 4: Implementation-cost essay prose around S8 does not advance any invariant
Reason: The fix is to cut narration to the load-bearing S1-monotonicity sentence (or relocate to an Open Question); the retained claim is already established within the ASN. No external evidence is required to remove duplicated prose.

## Issue 5: S8 run-corollary is non-vacuous only for decompositions the theorem never constructs
Reason: The fix is a logical scoping correction derivable from the ASN's own proof, which constructs only the singleton decomposition — state the corollary conditionally on a hypothesized non-trivial run or defer it. No design intent or implementation fact is needed to recognize the phantom guarantee.

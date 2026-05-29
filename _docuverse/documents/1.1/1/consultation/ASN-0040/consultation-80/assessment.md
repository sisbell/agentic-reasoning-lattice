# Channel Assignment — ASN-0040 review-80

**Date:** 2026-05-29 01:33

## Issue 1: B4 states its justification twice
Reason: Pure editorial deduplication — remove the redundant lead-in paragraph and collapse the repeated parenthetical to a single citation. The atomicity content and its provenance (B0a + foundation Σ signature) are already fully present in the ASN; no design-intent or implementation evidence is needed.

## Issue 2: S0 reproves a foundation result
Reason: The fix is a spec-internal cross-reference decision — cite T10a.7 (a foundation result already characterized in the review) or justify non-invocation via the `allocated(s) ⊆ s.B` open question, which is itself internal to this ASN. Whether S(p,d) is treated as an allocator domain is derivable from the ASN's own stated open questions and the foundation's property list, not from Nelson's intent or Gregory's code.

## Issue 3: B6 condition-(i) paragraph is "why the axiom is needed" framing
Reason: Editorial restructuring only — keep the aliasing example, trim the meta-rationale, and relocate the example to B7's well-posedness. All content (the alias pair, the disambiguation role) is already present in the ASN.

## Issue 4: Trace Step 4 misnames the increment parameter
Reason: Pure notational correction — reword to reserve `k` for TA5's depth parameter. The correct usage is fully determined by TA5's signature as already referenced in the ASN.

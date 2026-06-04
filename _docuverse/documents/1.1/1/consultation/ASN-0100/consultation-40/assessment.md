# Channel Assignment — ASN-0100 review-40

**Date:** 2026-06-04 13:32

## Issue 1: Non-circularity defense is meta-prose restated in two locations
Reason: Pure editorial deletion — the underlying logic already exists in the ASN; removing the meta-commentary and the §Atomicity mirror restatement requires no design intent or implementation evidence.

## Issue 2: "established once and decomposition-independently" contradicts its own proof
Reason: The fix is choosing accurate phrasing for an argument already present in the ASN; both the proof structure and the correct description are derivable from the text alone.

## Issue 3: I3-citation inventory is a use-site enumeration
Reason: Reducing the lemma roster to the load-bearing fact (I3-C `Σ'.C = Σ.C` fails because INSERT allocates and inserts) is derivable from the ASN's own content — the reason I3's whole-post-state characterizations don't hold is already stated.

## Issue 4: wp-calculus applicability commentary is explanatory padding
Reason: Straight deletion of methodology rationale; the assumption's statement and closing sentence already stand on their own in the ASN.

## Issue 5: The S8-depth / K.μ⁻-empties point is stated three times
Reason: Deduplication to the table row; the fact itself is unchanged and present in all three locations, so consolidation is internal.

## Issue 6: Repeated forward deferrals to §Atomicity
Reason: Replacing forward pointers with inline one-line consequences uses facts (uniqueness of Σ', K.α-before-K.ρ ordering) already established within the ASM's §Atomicity section.

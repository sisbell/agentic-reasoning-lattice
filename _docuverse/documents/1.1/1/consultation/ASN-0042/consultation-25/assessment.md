# Channel Assignment — ASN-0042 review-25

**Date:** 2026-05-13 23:06

## Issue 1: AccountField intro miscites T6 instead of T4(b)
Reason: Citation correction internal to the ASN — T4(b) defines the field projections, T6 only decides containment. The foundation labels are unambiguous; no design intent or implementation evidence is at stake.

## Issue 2: Informal "fields(a)" used as if it were a foundation function
Reason: Terminology cleanup — either bind "fields(a)" as a local abbreviation or expand to N(a), U(a), D(a), E(a). The choice is editorial and derivable from the existing foundation references.

## Issue 3: O10 existence proof imprecise in zeros(pfx(π)) = 0 case
Reason: Proof refinement using only the prefix relation (T5), field structure (T4), and O1a — all already cited in the ASN. The two sub-delegate forms are distinguished by the foundation's own prefix mechanics; no new design or implementation input is needed.

## Issue 4: O5 omits explicit π ∈ Π_Σ membership
Reason: Pure formal tightening to match O16's quantifier discipline; derivable from the ASN's own conventions around pfx being defined only on Π.

## Issue 5: O7 postcondition (a) proof asserts three-case exhaustion without justification
Reason: The covering-chain argument is already proved within O2 of this ASN; the fix is a one-sentence cross-reference. No external channel needed.

## Issue 6: O3 corollary "monotonic refinement" stated without derivation
Reason: The missing case (ω preserved) follows immediately from O13 (PrefixImmutability), which is already stated as an axiom in this ASN. Internal derivation only.

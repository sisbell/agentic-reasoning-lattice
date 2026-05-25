# Channel Assignment — ASN-0098 review-1

**Date:** 2026-05-24 19:10

## Issue 1: LP20 claim incorrect in extended state
Reason: The fix is purely notational — the review cites the relevant foundation claims (S3★ in ASN-0047, L4(c) in ASN-0043) and provides the corrected formula. Derivable from the ASN's own framework.

## Issue 2: Worked trace uses K.μ⁻ inconsistently with its definition
Reason: The fix is to use K.μ⁻ as defined in ASN-0047 (prefix-retention only). The trace can be reconstructed using either K.μ~+K.μ⁻ or a last-position removal scenario. Derivable from cited foundations.

## Issue 3: K.μ⁺_L not addressed in K.μ family analysis
Reason: ASN-0047 already defines K.μ⁺_L; the fix is to mechanically add analogous claims following the same proof patterns. The semantics are established in the foundation. Derivable from the ASN.

## Issue 4: Coverage definition restated with malformed notation
Reason: Pure citation fix — ASN-0043 already gives the correct three-part quantifier form. Derivable from cited foundation.

## Issue 5: LP19 is either trivial or unsupported
Reason: The decision to remove LP19 vs. formalize "tight endset construction" hinges on whether boundary-insertion exclusion was an intentional design guarantee with a corresponding construction discipline, and whether the implementation reflects any such discipline.
Nelson question: Was boundary-insertion exclusion (newly allocated content not extending a link's reach into its coverage) an intentional design guarantee, and was there a specific discipline for endset/span construction intended to enforce it?
Gregory question: Does udanax-green's span or endset construction follow any convention — e.g., tight coverage matching the I-addresses resident at construction time — that ensures K.α-allocated addresses fall outside existing endset coverage?

## Issue 6: LP18 proof miscites LP9
Reason: Pure citation fix — replace LP9 invocation with direct appeal to project's definition. Derivable from the ASN.

## Issue 7: LP18 cites wrong invariant for coverage permanence
Reason: Pure citation fix — LP1 → LP3. Derivable from the ASN.

## Issue 8: LP13 introduces informal vocabulary
Reason: The decision to remove the informal terms or promote them to formal definitions tied to the standard-triple convention is editorial. Neither option requires external input. Derivable from the ASN.

## Issue 9: LP1 restates L12 verbatim
Reason: Pure structural fix — remove LP1, have LP2's proof cite L12 directly. Derivable from the ASN and ASN-0043.

## Issue 10: LP4 proof does not connect to coverage invariance
Reason: Pure proof completeness fix — note that coverage(e) is a function of e and e is fixed across the comparison. Derivable from the ASN.

## Issue 11: Empty-endset and empty-arrangement edge cases unaddressed
Reason: The behavior under degenerate cases follows mechanically from project's definition (coverage(∅)=∅, dom(M(d))=∅ ⟹ projection=∅) and L3 already establishes which slots may be empty. Derivable from the ASN.

## Issue 12: LP14, LP15 are observations, not lemmas
Reason: The choice to fold into prose or strengthen to constructive independence claims is editorial. Both options are derivable from the ASN.

# Channel Assignment — ASN-0040 review-20

**Date:** 2026-05-11 09:14

## Issue 1: The Σ.B = allocated(Σ) identification is asserted but not supported
Reason: Fix is internal. The open question already defers the parent prerequisite; aligning the prose to that deferral (option b — weaken to one-sided inclusion plus conditional) requires no external input. The stronger option would reopen settled design questions.

## Issue 2: B0 stated as a corollary of T8 under the same unsupported identification
Reason: Fix is internal and textual. The properties table already classifies B0 as a design requirement; the prose simply needs to drop or qualify the corollary framing to match that standing. No design intent or implementation evidence is needed.

## Issue 3: B9's quantifier and Bop's domain do not match
Reason: Fix is internal. This is a consistency alignment driven by the same deferred parent-prerequisite question as Issues 1/2; widening B9 with a note (or restricting Bop) is a mechanical choice that follows from how Issues 1/2 are resolved.

## Issue 4: B7's Case 2 is proved abstractly but never traced concretely
Reason: Fix is internal. The reviewer specifies the concrete witness (namespaces ([1], 2) and ([2], 2)) and the divergence position; constructing the trace draws only on TA5(d), T1, and arithmetic already established in this ASN.

## Issue 5: Proofs invoke B4 with event-based vocabulary that the framework section retires
Reason: Fix is internal and textual. The framework section already defines the transition vocabulary and the reviewer supplies the replacement phrasing; this is a mechanical rewording with no semantic change.

## Issue 6: TA5a citation reformulated without acknowledgment
Reason: Fix is internal. TA5a's actual statement is in ASN-0034 (already accessible) and the reviewer quotes it directly; the fix is to either quote TA5a verbatim and derive the uniform form, or annotate the reformulation as the author's restatement.

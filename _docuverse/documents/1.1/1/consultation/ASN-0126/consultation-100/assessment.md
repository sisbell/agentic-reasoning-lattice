# Channel Assignment — ASN-0126 review-100

**Date:** 2026-06-10 10:48

## Issue 1: The gate never binds K to the deposited value's type slot
Reason: The fix is a one-clause formal binding (K = e₃ via StandardTriple's slot-3 convention, ASN-0043), fully specified by the review and derivable from definitions the note already cites. No design intent or implementation evidence bears on it.

## Issue 2: RegisteredAdmissible skips the step from `ℓ > 0` to non-empty coverage
Reason: The fix must cite or derive a tumbler-arithmetic monotonicity fact (`ℓ > 0 ⟹ s < s ⊕ ℓ`) for arbitrary well-formed spans, and before the note leans on it the property should be confirmed against what the arithmetic actually does, including carry and normalization edge cases — evidence territory, not design intent.
Gregory question: Does udanax-green's tumbler addition (tumbleradd) guarantee a result strictly greater than its first operand whenever the addend is nonzero, or are there carry/normalization/exponent-shift cases where `s ⊕ ℓ ≤ s` despite `ℓ > 0`?

## Issue 3: The abutting-spans divergence claim is asserted without a witness
Reason: The review supplies a complete witness, and verifying it needs only OrdinalShift and PrefixSpanCoverage (ASN-0043) plus the same TumblerAdd monotonicity fact Issue 2's consultation establishes — once that fact is in hand, the check (or the existential-hedge fallback) is internal derivation.

## Issue 4: Defensive acceptability prose in the retraction section
Reason: The fix is a deletion: the load-bearing (a)–(c) content and the LM citations to retain are already present in the paragraph, and the review specifies exactly what stays and what goes. No new design-intent or implementation input is required to cut the acceptability argument.

## Issue 5: Duplicated claims and advance-organizer prose
Reason: Pure deduplication of the note's own prose — the review names both removal sites and what survives at each claim's home. Entirely internal editing.

## Issue 6: Open Question 3 presupposes registry state this note excludes
Reason: The fix is a local rephrasing or deletion of a dangling reference, with the exact successor-state wording supplied by the review; the open-questions section is explicitly speculative, so neither design intent nor implementation evidence is needed to repair it.

# Channel Assignment — ASN-0051 review-63

**Date:** 2026-05-17 17:36

## Issue 1: (m ≥ 3, p ≥ 3) attainment lacks a concrete witness
Reason: The fix is constructive — exhibit explicit tumbler values, block I-extents, and span coverages using the ASN's own (m=2, p=3) nesting pattern with larger block sizes. All machinery (T-arithmetic, M7/M12 block decomposition, span coverage, S5 sharing) is already developed in the ASN; no design intent or implementation evidence is required.

## Issue 2: Worked Example's "discover_from({a₃}) = {b}" assumes no other links
Reason: The discover_s definition is stated in the ASN; the fix is pure prose precision — either qualify as membership (b ∈ discover_from({a₃})) or state the scoping assumption. No external channel needed.

## Issue 3: The "Reordering that changes locate" K.μ~ swap admissibility is implicit
Reason: The K.μ~ decomposition into K.μ⁻ + K.μ⁺ with D-SEQ upward-tail enforcement is specified by ASN-0047 (already cited extensively) and the prior worked example's Step 1 already exhibits the pattern. The fix is editorial — add a parallel admissibility sentence using rules already in scope.

## Issue 4: SV6 precondition lists "T12-well-formed" redundantly with "in an existing endset"
Reason: The ASN already resolves the framing question via its "Note on 'newly allocated'" — declaring SV6 structural rather than tied to endset membership. The fix is internal consistency: reconcile the SV6 statement and precondition list with the proof's actual scope.

## Issue 5: SV2-SV5 proofs cite L12 for coverage invariance but the argument is more general
Reason: This is a logical-scope tightening of citations. The set-theoretic fact that coverage(e) is a function of a fixed endset value e is derivable from the endset/coverage definitions in the ASN; the L12 citation should be repositioned as covering only the existing-link instantiation. No external channel needed.

## Issue 6: The four-case structural lemma's case (IIIb) j* = n_{k₁} branch handling
Reason: The case-elimination follows from the lemma's own uniformity argument applied case-by-case. The fix is to make the implicit reasoning explicit with a one-sentence note in the existing proof. Internal.

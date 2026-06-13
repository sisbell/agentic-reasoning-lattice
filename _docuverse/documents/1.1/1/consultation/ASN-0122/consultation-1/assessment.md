# Channel Assignment — ASN-0122 review-1

**Date:** 2026-06-12 17:21

## Issue 1: X2's reachability construction is not assembled from valid composites
Reason: The fix is bookkeeping against the spec series' own composite-validity rules (J0, J1★, K.α/K.μ⁺/K.ρ/K.δ), and the review already names the exact packaging required; neither design intent nor implementation evidence bears on it.

## Issue 2: X9's justification overstates what the discarded pairs reveal
Reason: The proof's three sub-arguments (CL-OWN, S3★+SD, CL-UNIQ) are already in the ASN and the review supplies the corrected gloss nearly verbatim; this is a precision rewrite of the lead-in and conclusion, internal to the note.

## Issue 3: R3 conflates determinism with canonicity, and the conformance clause then retracts R3
Reason: The defect is contract structure — a mislabeled postcondition and an internally inconsistent conformance paragraph — and the review prescribes the exact separation into binding requirements versus reference presentation. The ASN's own implementation observations already document the granularity and ordering facts the restructuring must accommodate, so no new evidence is needed.

## Issue 4: Empty-document and empty-region boundaries are unstated, and σ_full carries an implicit nonemptiness precondition
Reason: The review itself notes the empty cases all follow from the ASN's definitions and dictates the paragraph's content (`(d, ∅)`, `corr = ∅`, `CANON = ⟨⟩`, vacuous X11); pure internal derivation.

## Issue 5: No concrete worked example
Reason: The review specifies the example arrangements, the expected relation elements, the maximal pairs, and which claims to verify (X4, X8(c), the X11 tie-break); executing it is computation over the ASN's own definitions.

## Issue 6: X6(b)'s composition premises are unstated, and X7's wp formulas are silently one-sided
Reason: Both fixes are formal — stating the endpoint-frame and composed-position-map premises, and displaying the two-sided wp forms — and are derivable from X-T and the edit transitions' clauses the ASN already cites.

## Issue 7: X10(a) cites TS2 for distinctness across shift amounts
Reason: A citation swap among foundation shift lemmas whose correct chain (TS3+TS4, or TS5 with TS4 for the base case) the review spells out; internal.

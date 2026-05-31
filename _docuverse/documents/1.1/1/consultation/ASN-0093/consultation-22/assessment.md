# Channel Assignment — ASN-0093 review-22

**Date:** 2026-05-31 04:49

## Issue 1: TA5a's k=1 branch misstated as having "no zero-count side condition"
Reason: The corrected wording is fully specified by the review itself, which cites TA5a's actual contract (`k = 1 ∧ zeros(t) ≤ 3`); the fix is a wording substitution derivable from the ASN's own k=2 contrast, needing no design-intent or implementation evidence.

## Issue 2: "(equivalently L14 at the pre-state)" conflates the invariant with fresh-key disjointness
Reason: The inconsistency is internal — the note's own FirstEmissionFreshness proof already establishes that the new key is uncommitted, so L14-at-Σ cannot apply; dropping or restating the parenthetical is derivable from the ASN's existing reasoning.

## Issue 3: Triple repetition of "no commitment about implementation realisation"
Reason: Pure editorial deduplication within one section; no design-intent or implementation evidence is required to delete two of three identical disclaimers.

## Issue 4: Duplicate factoring rationale in the introduction
Reason: Editorial merge of two paragraphs asserting the same `E_doc → dom(M)` substitution fact; derivable from the ASN's own content.

## Issue 5: Defensive existence-justification around an axiom
Reason: Editorial removal of meta-prose narrating an omission; the ASN already establishes chain existence from B6-validity, so silently dropping the narration is internal.

## Issue 6: Repeated deferral to the same downstream location
Reason: Editorial consolidation of two forward pointers into one cross-reference; no external channel needed.

## Issue 7: L14 discharge-matrix cells restate a near-identical derivation
Reason: Editorial — collapse the redundant restatement under the existing "symmetric" label using the content↔link substitution rule already present elsewhere in the note; fully internal.

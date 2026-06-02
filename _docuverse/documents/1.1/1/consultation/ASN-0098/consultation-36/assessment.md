# Channel Assignment — ASN-0098 review-36

**Date:** 2026-06-02 13:35

## Issue 1: Fabricated citation and incorrect depth claim in LP9
Reason: The review already supplies the correct ASN-0047 content (depth `m_L(d) ≥ 2`, chosen not fixed, no `LinkVPositionDepthAxiom`); the fix is a citation/text correction against a sibling ASN, which is neither design intent nor implementation evidence.

## Issue 2: Fabricated citation `ChainUniformLength` (ASN-0093)
Reason: The review specifies the actual supporting lemmas (`FirstEmission` + `ChainDiscipline` + TA5(c)); replacing the fabricated name with the real derivation is internal to the spec corpus.

## Issue 3: Fabricated namespacing `SubAllocatorAxiom.*` in LP12b
Reason: The review names the real lemmas (`FirstEmission`, `ChainDiscipline`, `ChainMembershipForOrigin` + `L1a` + `M0`); de-namespacing the citations is a mechanical correction needing no channel.

## Issue 4: Verbatim duplicated conclusion across LP12a and LP12b
Reason: Pure deletion of a duplicated sentence; fully internal.

## Issue 5: Forward-reference accretion in "Working reference frame"
Reason: Cutting the frame-descent inventory and stating only the operating frame is an editorial trim derivable from the ASN's own scope.

## Issue 6: LP-Comp is a use-site inventory, not a claim
Reason: Removing the operation→lemma roster from the claims slot and optionally folding one line into prose is internal restructuring.

## Issue 7: Defensive justification + retained redundant sub-cases in achievability
Reason: The LP-Fin Corollary (already proved in-ASN) subsumes the cross-chain sub-proofs; deleting them plus the two-reason defense while keeping the emission-frontier argument is derivable from the ASN's own content.

## Issue 8: Numbering note is a revision-history essay
Reason: Reducing to the absent-label facts (LP1, LP15 unused; LP14 reclaimed) is an internal edit; the rotting rationale is removed, not relocated within the spec.

## Issue 9: Triangular deferral to the same downstream discharge
Reason: Collapsing three deferral pointers to a single LP12a→LP12b reference is an internal cross-reference cleanup.

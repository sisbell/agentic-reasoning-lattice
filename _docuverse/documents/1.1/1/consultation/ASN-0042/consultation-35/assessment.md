# Channel Assignment — ASN-0042 review-35

**Date:** 2026-05-14 03:32

## Issue 1: Unilateral O10★ trajectory length is over-specified without justification
Reason: The choice between "fork creates element-level content-bearing address" and "fork creates any owned address" turns on design intent (what is a fork's target meant to be?) and on what the implementation actually produces. Both channels can ground the depth commitment.
Nelson question: When a principal creates a fork in response to non-ownership of target content, must the new address be a content-bearing element-level address (the inclusion-link endpoint), or does the design admit forks at any level within the principal's domain?
Gregory question: When `docreatenewversion` routes a fork through `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)`, what depth tumbler does the resulting allocation produce — document-level, element-level, or something else — and does the trajectory involve one allocation call or multiple?

## Issue 2: O10's existence and unilateral proofs use inconsistent non-coverage conditions
Reason: Pure proof-tightening internal to ASN-0042. The unilateral construction with `u = hwm_0 + 1` and `u ∉ S'` (via O18 + baptismal coupling) already subsumes the existence argument; folding them together uses only facts already in the ASN.

## Issue 3: Worked example's "Self-ownership at the prefix" wording understates O18
Reason: O18 is already an axiom of this ASN with both the inductive clause and the bootstrap companion. The fix is to align the worked-example wording with the axiom — purely internal rewording.

## Issue 4: O17 (AllocatedAddressValidity) duplicates ASN-0040's B10
Reason: B10 (T4ValidityInvariant) is a derived invariant of ASN-0040, which is the project's own foundation. The fix is to check ASN-0040's content and either recast O17 as a citation to B10 or remove it — no external channel needed.

## Issue 5: O10's per-baptism authorization verifies O5 but not B6
Reason: B6 (ValidDepth) is a precondition of `Bop` in ASN-0040. Verifying that the trajectory's depth choices stay within B6's bound requires only recomputing `zeros(p) + (d − 1)` at each baptism step using facts already in ASN-0042. Internal fix.

## Issue 6: O15's condition labels skip (iii)
Reason: Pure presentation/numbering issue. Renumbering contiguously or inlining condition (iii) is an editorial choice with no external content dependence.

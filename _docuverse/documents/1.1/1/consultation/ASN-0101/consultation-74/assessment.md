# Channel Assignment — ASN-0101 review-74

**Date:** 2026-06-05 03:20

## Issue 1: P4a discharge in the D11 boundary derivation relies on a single-step argument at a multi-step composite boundary
Reason: The fix restructures an internal proof: P4a at the composite boundary must be discharged using validity clause (2)'s J1'★ (already in the ASN) to show every new `(a,d) ∈ R' \ R` has a surviving content-subspace witness at `B_{j+1}`, rather than the single-DEL N2 argument. All needed pieces (J1'★, the induction frame, P2) are present in the ASN.

## Issue 2: Wrong claim reference in the worked-example verification of D10
Reason: Purely textual correction — "each D11 wp" should read "each D10 wp," since the wps are D10's and D11 introduces no wp. Derivable from the ASN alone.

## Issue 3: Defensive vocabulary-provenance prose in D11
Reason: Editorial deletion of an accreted scoping sentence; the vocabulary list already carries the information. No external channel needed.

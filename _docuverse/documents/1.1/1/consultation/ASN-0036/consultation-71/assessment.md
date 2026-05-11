# Channel Assignment — ASN-0036 review-71

**Date:** 2026-05-10 21:16

## Issue 1: Within-subspace uniqueness proof omits divergence-position lower bound
Reason: Pure proof-clarification fix. The j ≥ 2 lower bound follows from the same-subspace hypothesis already in the proof, and the m = 2 corollary is immediate from the case structure.

## Issue 2: S5 cross-document construction has ambiguous "distinct V-positions"
Reason: Author intent clarification. The pair-counting works under either reading, so the fix is a choice about wording that is derivable from the existing formal counting expression.

## Issue 3: S8 existence postcondition is satisfied trivially; architectural intent diverges from formal claim
Reason: Choosing between options (a)/(b)/(c) depends on whether the implementation maintains a canonical run form. Gregory's evidence about the abandoned consolidation function is already cited and bears directly on whether `#runs(d)` is well-defined operationally; sharper evidence will tell us whether to formalize canonicality or defer it.
Gregory question: Does udanax-green's enfilade representation maintain a canonical (e.g., maximal-merged) run decomposition, or can the same arrangement be represented by multiple decompositions of different cardinality — and does the abandoned consolidation function suggest the implementation tolerates non-canonical forms?

## Issue 4: OrdAddHom postcondition (b) derivation is one sentence
Reason: Pure proof expansion. The reviewer has already supplied the derivation steps; the fix is to move them from the contract block into the proof body.

# Channel Assignment — ASN-0101 review-9

**Date:** 2026-05-27 16:32

## Issue 1: Composite-substitute enumeration includes vacuous or redundant cases
Reason: The fix requires reconsidering the enumeration against K.μ~'s admissibility conditions (from ASN-0047) and K.μ⁻'s suffix-truncation effect — both already characterised in the ASN's own references. Determining whether a transposition is always admissible when |V_{s_C}(d)| ≥ 2 follows from checking K.μ~'s precondition list against subspace-preserving permutations, which is derivable from established invariants.

## Issue 2: No explicit weakest precondition analysis
Reason: Computing wp(DEL[d, σ], Q) for any chosen postcondition Q reduces to inverting D0's effect and frame — a mechanical exercise using D0 and D9 (both already established in the ASN). No external information is needed.

## Issue 3: Worked example covers only single-document case
Reason: Constructing a two-document transclusion example requires only the abstract specification: a pre-state where M(d)(v) = M(d')(v') = a, then applying D0/D2/D3/D5/D9. The mechanics of how transclusion is established (J4 ForkComposite from ASN-0047) are referenced in the ASN itself.

## Issue 4: Σ_mid distinguishability argument under-specified
Reason: The simpler "π ≠ id ⟹ ∃v : M_mid(d)(v) ≠ M_pre(d)(v)" argument follows directly from K.μ~'s π ≠ id clause (which the ASN already cites) and the definition of state equality. Pure internal logical simplification.

## Issue 5: D8 Group (i) S2 disjointness argument compressed
Reason: Noting that Q's last-component range {p, ..., n_S−n} is empty iff n = n_S−p+1 is elementary integer arithmetic against the containment precondition already stated in D0. The two discharge routes (vacuous vs. non-vacuous) are derivable from the existing D0 setup.

## Issue 6: S9 (TwoStreamSeparation) not explicitly addressed
Reason: S9's statement is established in ASN-0036, and its discharge under DEL is "by D2" — already proven in the ASN. The fix is purely additive bookkeeping in D8's Group (iii) listing.

## Issue 7: ChainEnumerationInjectivity and substrate invariants from ASN-0093
Reason: The named lemmas are established in ASN-0093 and are structural properties of dom(C) and dom(L). With D2 (`dom(C') = dom(C)`) and D3 (`dom(L') = dom(L)`) already proven, the chain-discipline lemmas inherit pointwise. The fix is a bookkeeping addition to D8 Group (ii).

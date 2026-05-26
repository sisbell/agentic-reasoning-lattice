# Channel Assignment — ASN-0091 review-4

**Date:** 2026-05-26 14:41

## Issue 1: dom(Σ.M) preservation not explicit in RA-frame
Reason: The fix is a formal closure of the abstract-class definition — either add a fifth RA-frame conjunct or derive `dom(Σ'.M) = dom(Σ.M)` from `Σ'.E = Σ.E` plus foundation invariants (P6 of ASN-0047, substrate semantics `dom(M) = E_doc`). All needed material is already in the ASN's framework and cited foundations.

## Issue 2: "Covering exactly the I-addresses" misstates coverage type
Reason: This is a precision issue against ASN-0098's coverage definition. The corrected statement (coverage as tumbler set, intersection with `dom(C) ∪ dom(L)` via LP-Fin Corollary) is derivable from the foundation lemma the ASN already invokes; no design intent or implementation evidence required.

## Issue 3: RE-sub verification in worked example is vacuous
Reason: The fix is to extend the worked example with a link-subspace V-position (e.g., `[s_L, 1] ↦ a_link`). The link-subspace structure is fully specified by foundation S3★ (ASN-0036) and the cut-subspace pinning is supplied by ASN-0084's CS3/R-FRAME-P/S(a). Construction is internal.

## Issue 4: RE-trans★ omits the home-arrangement clause without comment
Reason: Pure logical clarification of how the three single-step clauses compose across n steps. The home-arrangement clause (iii) clearly fails when some step targets `origin(a)` — this can be observed directly from RE-other's quantification structure. No external consultation needed.

## Issue 5: π = id exclusion attribution is muddled
Reason: Pure attribution precision against ASN-0084's K.μ~ admissibility clauses, which are cited in the ASN. The fix separates clause (ii)'s role (excluding identity) from the existence precondition's role (ensuring non-identity permutations exist). Internal.

## Issue 6: π non-uniqueness under shared I-addresses not addressed
Reason: Shared I-addresses are licensed by foundation S5/UnrestrictedSharing (ASN-0036), already a citation point in the ASN. The fix is to acknowledge that RA-π's bijection is not unique when M(d) has duplicate values, and that RE-proj is parameterised by the witnessing π. Pure formal precision, derivable from already-cited foundation.

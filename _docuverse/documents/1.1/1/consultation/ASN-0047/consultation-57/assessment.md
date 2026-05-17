# Channel Assignment — ASN-0047 review-57

**Date:** 2026-05-16 20:17

## Issue 1: Forward reference to D-SEQ★ in K.μ⁻ amendment
Reason: Pure structural reorganization — D-SEQ★ is defined later in the same ASN, and either moving its definition or stating it inline at K.μ⁻ resolves the forward reference. Fully derivable from the ASN's own content.

## Issue 2: Conflicting characterization of J0 as axiom vs. derived theorem
Reason: The ASN already contains both the Nelson design-intent quote and the formal proof chain; the fix is to pick the orientation that matches P7a's actual proof (which uses J0 as a premise, making J0 axiomatic). Internal logical reconciliation.

## Issue 3: Layer-decomposition table conflates value immutability with set monotonicity
Reason: Technical correction — E is a set with no value structure, so the "values immutable" characterization is type-incorrect. Pure presentation fix derivable from the ASN's own definitions.

## Issue 4: Structural sufficiency caveat stated four times
Reason: Pure editorial consolidation — the caveat content is identical at all four sites, and the dedicated section already exists to host it. Internal.

## Issue 5: K.μ~ Case 1 subcase split adds verbosity without analytic content
Reason: Pure editorial cleanup — both subcases conclude with the same "zero steps, M unchanged, vacuous preservation" outcome. Merge derivable from the existing prose.

## Issue 6: K.μ~ "derived contract" relationship to its decomposition is circular in presentation
Reason: The contract content is fully present in the ASN; the fix is to state it independently at the definition site rather than calling it "derived from the decomposition." Pure structural reorganization.

## Issue 7: ExtendedReachableStateInvariants inductive step for K.μ⁺_L misses an explicit CL-UNIQ case
Reason: Pure addition — the CL-UNIQ proof for K.μ⁺_L already exists in the *Link-subspace ownership* section; the fix is to add a one-line citation in the inductive prose. Internal.

## Issue 8: Two paragraphs of P3 vs P3★ commentary belie a definitional ambiguity
Reason: Pure labeling/naming choice within the ASN — both the qualitative P3 and the quantitative monotonicity conjunction are present; the fix is to choose a naming convention that distinguishes them. Internal.

## Issue 9: Worked example "fork with subsequent insertion" verifies J1', not J1'★
Reason: Pure editorial consistency fix — the J1'/J1'★ relationship is already established (they coincide in the four-component subspace). Internal.

## Issue 10: The cross-document T10a chain is correct but stated three times verbatim
Reason: Pure editorial consolidation — the chain content is identical at all three sites, and a single canonical statement with backward citations would suffice. Internal.

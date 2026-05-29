# Channel Assignment — ASN-0036 review-113

**Date:** 2026-05-28 20:17

## Issue 1: Duplicated closing sentence in the two state-component justifications
Reason: Pure editorial deduplication — both sentences already appear in the ASN; the fix is to state the joint-constitution claim once. No design intent or implementation evidence is at issue.

## Issue 2: Reclamation-rule inventory adds nothing
Reason: The general statement "any rule removing some `a ∈ dom(C)` contradicts S0" is already present in the ASN and subsumes the enumerated cases. Replacement is internal compression.

## Issue 3: "Why the axiom is needed" prose imagining excluded cases (S7c, S7d, S8a)
Reason: The axiom content (`#E(a) ≥ 2`, document-tumbler discipline, `#v ≥ 2`) is already stated in each block; removing the counterfactual justifications and consumer lists is internal trimming.

## Issue 4: Document-structure / placement justifications (ShiftPreservation, S8 corollary)
Reason: The deleted prose is meta-commentary about where content sits; the formal contracts already carry the dependency structure. Purely internal.

## Issue 5: Excluded `m = 1` case re-imagined twice
Reason: S8a's precondition `#v ≥ 2` already excludes `m = 1`; removing the digressions follows directly from the ASN's own precondition.

## Issue 6: Repeated forward deferrals to ShiftPreservation
Reason: ShiftPreservation is defined within this ASN; consolidating the citations to its Depends line is an internal cross-reference cleanup.

## Issue 7: S9 self-justification
Reason: The directional reading is already captured in the contract and properties table; reducing the self-justifying prose is internal.

## Issue 8: Over-derived triviality in ShiftPreservation conclusion (i)
Reason: The needed fact `a_{#a} + k > 0` follows from `a_{#a} ≥ 1` and `k ≥ 1`, both already established in the proof; simplifying the chain uses only ASN-internal facts (NAT axioms already cited).

## Issue 9: Redundant double-derivation in OrdAddS8a
Reason: Both derivations and the OrdAddHom connection are already in the proof; collapsing to one derivation is internal editing.

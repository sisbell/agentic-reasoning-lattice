# Channel Assignment — ASN-0042 review-60

**Date:** 2026-05-14 12:46

## Issue 1: Inconsistent count of structural axioms
Reason: Internal classification/bookkeeping issue — the ASN already contains the inductive preservation arguments and the axiom statements; the fix is to reconcile the intro count, the table labels, and the inductive-derivation status using material already present.

## Issue 2: ω(a) definition omits state subscript
Reason: Pure notational cleanup — the state-relativization convention is already documented in the notation paragraph; the fix is to lift `Π_Σ` and the domain restriction into the formal definition itself.

## Issue 3: O8 proof relies tacitly on trajectory including the witnessed delegation
Reason: Internal proof-structure fix — the historical/structural double reading of `delegated_Σ` is already defined alongside O15; the fix is to invoke the historical reading explicitly in O8's hypothesis or to argue the trajectory's introducing transition coincides with the witnessed one.

## Issue 4: Covering-chain lemma not in Properties Introduced
Reason: Pure table completeness — the lemma is fully stated and proved inline; the fix is to add the row with its derivation provenance and consumer list.

## Issue 5: O3's "no spontaneous activation" hypothesis structure
Reason: Internal proof expansion — the explicit two-line argument already appears in OwnershipDomainPermanence Step 2; the fix is to lift that expansion into O3's body using the same Prefix-definition + O1b machinery already in scope.

## Issue 6: O7(c) chain construction skips the k=0→k=1 boundary
Reason: Internal construction repair — the boundary step's verification uses T4, T4a, the prefix relation, and delegation conditions (i),(iv),(v), all already established; the fix is either to restrict the chain to `k ≥ 1` or to verify `[1] ≺ [1, 0, 1]` and its T4/zeros properties separately.

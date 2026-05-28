# Channel Assignment — ASN-0095 review-1

**Date:** 2026-05-28 10:30

## Issue 1: PC6 (⊇) direction hand-waves Observe_K pattern reduction
Reason: This is an internal algebraic-closure question — whether arbitrary Observe_K patterns reduce to the catalog's base atoms, or whether new primitives must be admitted. The fix is mathematical and derivable from ASN-0086's Observe_K signature and ASN-0094's catalog rows already cited.

## Issue 2: PC2 admits substrate primitives (addr) in chains, but the closure says otherwise
Reason: Resolution is purely algebraic — choose among extending V_atom, restating PC2, or adding a bridge lemma. All three options operate within the ASN's own definitional vocabulary; no external evidence needed.

## Issue 3: PC1 does not handle empty quantification domains
Reason: Standard meta-mathematical convention (empty ∀ = ⊤, empty ∃ = ⊥). Internal definitional clarification.

## Issue 4: PC2's ⊥-dispatch introduces an if-then-else construct not in PC0–PC2
Reason: Pure algebraic-structure question about which composition primitives to admit. All three resolution options are internal choices about the closure's vocabulary.

## Issue 5: Set-theoretic operators at PL level are not formally admitted
Reason: Internal decision about whether set comprehensions are first-class PL operators or scoped to atomic template bodies per Sh5(b). Derivable from ASN-0094's catalog discipline.

## Issue 6: PC3 META status conflicts with its mathematical consequences
Reason: Classification/labeling issue between META design statements and LEMMA mathematical content. Internal restructuring; PC4's own proof already discharges the substantive claim.

## Issue 7: AtomicPredicate examples reference K's whose registration is not exhibited
Reason: The examples are illustrative; needed registrations (shapes + disciplines) are all from ASN-0094's catalog. Just add a registration prologue stating which K carries which shape and discipline.

## Issue 8: PC2 proof's appeal to Sh4 is imprecise
Reason: Reference precision — name FDD/SHCD instead of Sh4 generically. Directly derivable from ASN-0094's per-K discipline definitions.

## Issue 9: Definition — Signature lists T_cat as an input domain but Codom omits it
Reason: Internal asymmetry acknowledgement. The design rationale (templates consume but don't return type-indices) is already implicit in ASN-0094's catalog rows.

## Issue 10: Definition — SubstrateEvaluable depends on PL for QD-derived sets
Reason: Make the mutual-induction structure between QD, PL, and SubstrateEvaluable explicit. Internal definitional cleanup; the well-founding argument (depth) is already gestured at in the QD definition.

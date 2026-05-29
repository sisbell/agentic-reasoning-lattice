# Channel Assignment — ASN-0040 review-40

**Date:** 2026-05-28 20:00

## Issue 1: S2 breaks at the singleton zero tumbler
Reason: Pure formal boundary fix — T0 (cited in the ASN) requires #p ≥ 1, so p′ = [] ∉ T forces excluding p = [0]; adding `#p ≥ 2` is derivable from the ASN's own definitions and downstream call sites.

## Issue 2: The "Relationship to ASN-0034's allocated set" section is a deferral essay
Reason: Editorial reduction — the load-bearing statement (`allocated(Σ) ⊆ Σ.B` conditional on future activation discipline) and the prose to cut are both already present in the ASN; no design intent or implementation evidence is needed to trim deferral prose.

## Issue 3: B0 labeling justification is meta-prose
Reason: Internal editorial removal of meta-commentary about labeling; B0 and its B0a-derivation are stated within the ASN, so the fix is purely structural.

## Issue 4: B4 placement justification is meta-prose
Reason: Internal editorial deletion of a slot-placement sentence; the assertion of B4 stands on its own within the ASN.

## Issue 5: The "mutually recursive / joint induction" scaffolding in Bop is unnecessary
Reason: The claimed clean stratification (B_fin → B10 → B1 → Bop) is verifiable from the ASN's own proof sections; reorganizing the citation order requires no external input.

## Issue 6: B9 quantifier defends against an out-of-scope concern
Reason: Internal editorial removal — the parent-prerequisite question is already flagged as open in the ASN, so deleting the defensive prose needs no design or implementation input.

## Issue 7: Bop's frame condition is stated twice
Reason: Internal de-duplication; both passages are present in the ASN and the fix is to keep one.

## Issue 8: B6(iii) uniform-form parenthetical is a defense of notation
Reason: Internal editorial — TA5a's case-based bound is cited in the ASN itself, so replacing the parenthetical with direct per-d citations is derivable without external channels.

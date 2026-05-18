# Channel Assignment — ASN-0051 review-70

**Date:** 2026-05-17 20:39

## Issue 1: Editorial note's SV-label list incomplete
Reason: Purely editorial fix — update the parenthetical to include SV14, which is already defined in the body and listed in Properties Introduced. Derivable from the ASN's own content.

## Issue 2: Single-block precondition gap for SV11 fragment cover formula
Reason: Internal derivation rigor — the step from B1's V-coverage to I-extent union via the per-block V→I mapping rule (M0/M3 from ASN-0058) is already cited in the ASN; just needs explicit articulation. No external input required.

## Issue 3: SV11 attainment proof's "fragment count ≤ non-empty term count" not derived
Reason: Internal proof rigor — the surjection argument (each non-empty term lies in exactly one fragment, so image cardinality ≤ domain cardinality) is a one-line set-theoretic derivation from definitions already present.

## Issue 4: (m=1, p≥4) generalization recipe under-specified
Reason: Internal combinatorial verification — the question is whether 2p+1 siblings suffice with an appropriate excision schedule, or whether the count needs adjustment. This is a finite combinatorial question over the witness recipe; the resolution depends on working through block-size dynamics under iterated excision, all using machinery already in the ASN (M12, K.μ~+K.μ⁻ composite, SV11 attainment conditions).

## Issue 5: SV5 proof's "ran-equality from K.μ~" assertion needs scope qualifier
Reason: Editorial restructuring — add an endpoint-only qualifier at first use, or reorder the composite-level scope subsection to precede the proof. Internal organization fix.

## Issue 6: SV6 proof's element-level restriction timing
Reason: Internal proof restructuring — choice between retaining generality with a note or deriving the contrapositive directly. No new content required from theory or implementation.

## Issue 7: SV13(e) bullet on M-frame transitions misses K.μ⁺_L distinction context
Reason: Editorial restructuring — reorder so the K.μ⁺_L parallel precedes the M-frame list, or add an inline cross-reference. Internal organization fix.

## Issue 8: Witness shape W(m, 2) ambiguity at m=2
Reason: Internal combinatorial verification or claim removal — either verify the W(m,2)-shape m=2 → W(3,2) lift under (α_2) using SV11 attainment conditions, or simply drop the "either base would suffice" claim and anchor (α_2) at W(3, 2). Both options are derivable from the ASN's own lift machinery without external input.

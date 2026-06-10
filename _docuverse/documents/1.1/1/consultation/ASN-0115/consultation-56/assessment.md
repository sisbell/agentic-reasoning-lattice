# Channel Assignment — ASN-0115 review-56

**Date:** 2026-06-10 05:52

## Issue 1: The repeatability/citation rationale claims editing never mutates an existing arrangement — contradicting the substrate and this ASN's own R11
Reason: Internal. The ASN already adopts the mutable-arrangement model it needs — its substrate section cites P3 (ArrangementMutabilityOnly) and ASN-0047's K.μ⁻/K.μ⁺/K.μ~, R11's worked instance demonstrates in-place K.μ⁻ contraction, and R7's formal hypothesis is already correctly conditioned on `Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧`. The corrected R4/R7 prose (arrangement is mutable, delivery is of current `Σ.M(d)`, permanence belongs to S0/I-addresses) is derivable from content already present; the contradiction is a loose prose claim versus the ASN's own formal model.

## Issue 2: The override rationale asserts it "only bites shallow" without justifying the deep-start case
Reason: Internal. The missing deep-case argument uses only machinery already established in the ASN — the Confinement lemma (proven here), S8-depth (cited), and T1 case (ii) (ASN-0034) — and the reviewer has already written out the full proof. No design intent or implementation evidence is involved.

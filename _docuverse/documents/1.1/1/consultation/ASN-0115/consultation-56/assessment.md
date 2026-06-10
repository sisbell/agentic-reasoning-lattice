# Channel Assignment — ASN-0115 review-56

**Date:** 2026-06-10 05:52

## Issue 1: The repeatability/citation rationale claims editing never mutates an existing arrangement — contradicting the substrate and this ASN's own R11
Reason: Internal. The contradiction and its resolution are both already present in the ASN: it cites ASN-0047's K.μ⁻/K.μ⁺/K.μ~ and P3 (ArrangementMutabilityOnly) as substrate, its own R11 worked instance demonstrates in-place K.μ⁻ mutation, R7's formal hypothesis already conditions on the unchanged restriction, and S0 already carries the permanent-citation guarantee — so the prose can be aligned to the formal content without any external evidence or design ruling.

## Issue 2: The override rationale asserts it "only bites shallow" without justifying the deep-start case
Reason: Internal. The missing deep-case argument is a pure derivation from material already in the ASN — the Confinement lemma, S8-depth, and T1 case (ii) (ASN-0034) — and the review itself supplies the complete one-paragraph proof, so no design intent or implementation evidence is required.

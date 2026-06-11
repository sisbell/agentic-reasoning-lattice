# Channel Assignment — ASN-0120 review-22

**Date:** 2026-06-11 05:22

## Issue 1: The ρ=∅ / one-sided-link boundary is treated three times, with the same deferral issued twice
Reason: This is structural consolidation of content the ASN has already settled — the boundary's definedness, unique record, L3 legality, and ML9 inertness are all proved in-note. No new design intent or implementation evidence is required to merge three treatments into one.

## Issue 2: ML2 overstates representation independence — the model does expose decomposition-sensitive observables
Reason: The counterexamples come from the ASN's own citations (L5 membership, L6 value equality, Observe_K's raw triples), and the required fix is to rescope the claim to the enumerated coverage-based observables already proved. The correction is derivable entirely from material the note already holds.

## Issue 3: The one-sided slot convention's normative status is unsettled
Reason: Choosing between normative-precondition and informative-commentary turns on what Nelson intended the LM 4/48 slot convention to be — a rule the system enforces or a usage description. Gregory is not needed: the implementation note already establishes that CREATELINK takes the same silent path for both non-type slots, so the implementation enforces no slot convention.
Nelson question: In the one-sided link's design (LM 4/48), is "use the first endset to designate the matter pointed at" a constraint the system is meant to enforce on link creation, or a usage convention left to the link author — i.e., is a one-sided link with an empty first endset and populated second endset meant to be rejected?

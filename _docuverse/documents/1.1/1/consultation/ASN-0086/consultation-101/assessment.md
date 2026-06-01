# Channel Assignment — ASN-0086 review-101

**Date:** 2026-05-31 19:46

## Issue 1: Clause (b) of substrate-conforming layer enumerates consumers and argues its own necessity
Reason: Purely editorial trim — delete the consumer inventory and the `a*` independence essay, keeping the frontier-emission obligation. The retained content is already stated in the clause; no design intent or implementation evidence is needed.

## Issue 2: substrate-conforming state def carries a convoluted dual-state justification with forward reference
Reason: Structural cleanup derivable from the ASN's own text — state clauses (a)/(b) once and relocate the clause-coincidence assertion to the layer definition. No external channel needed.

## Issue 3: R0a-Cor1 substantive-postcondition (b) and the #E=2 narrowing are each stated in multiple places
Reason: Deduplication only — drop the redundant postcondition (b) and consolidate the L1b-narrowing framing to R0a-Cor2 plus Open Questions. The factual content (#E=2 via R0a-Cor2) and the design question already exist in-note; nothing new is decided.

## Issue 4: R6c's "Consequence" attributes a transitive-closure claim to single-step R3 without the induction
Reason: The inductive lift from `→` to `→*` is already performed explicitly in R6c's own proof; qualifying or naming the corollary is internal bookkeeping requiring no design intent or code evidence.

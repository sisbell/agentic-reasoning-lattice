# ASN-0057 Formal Statements

*Source: ASN-0057-tumbler-algebra-0.md (revised 2026-03-19) — Extracted: 2026-03-19*

## Definition — DisplacementFormula

Given tumblers a, b with k = divergence(a, b):

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

This is w = b ⊖ a (TumblerSub). The result has length max(#a, #b).

## D0 — DisplacementWellDefined (PRE, requires)

a < b, and the divergence k of a and b satisfies k ≤ #a.

Ensures: the displacement b ⊖ a is a well-defined positive tumbler, and TA0 is satisfied for a ⊕ (b ⊖ a) (displacement is positive, action point k ≤ #a).

## D1 — DisplacementRoundTrip (LEMMA, lemma)

For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

## D2 — DisplacementUnique (COROLLARY, lemma)

Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b):

  if a ⊕ w = b  then  w = b ⊖ a

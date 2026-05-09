---
caste: producer
scope: claim
---

# Claim Contract

Claim-contract is a producer agent whose primary substrate effect is granting a `contract.<kind>` classifier on a claim — declaring whether the claim is a theorem, lemma, corollary, definition, axiom, or design-requirement. Once granted, the kind drives downstream agents (formal-contract synthesis, structural validation) that depend on knowing what shape the claim takes.

## Triggers

- The claim has no `contract.<kind>` classifier yet (one-shot — never re-fires once assigned).

---
caste: producer
scope: claim
---

# Claim Formal Contract

Claim-formal-contract is a producer agent whose primary substrate effect is advancing a claim's chain after synthesizing the `*Formal Contract:*` section in the claim's text — preconditions, definitions, depends, postconditions in the structured form the validator and Dafny pipeline consume. Fires once per claim whose contract kind requires a Formal Contract and whose body still lacks one.

## Triggers

- The claim's `contract.<kind>` requires a Formal Contract section, AND
- The claim's body still lacks one.

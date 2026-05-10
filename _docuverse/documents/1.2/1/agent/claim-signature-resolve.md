---
caste: producer
scope: claim
---

# Claim Signature Resolve

Claim-signature-resolve is a producer agent whose primary substrate effect is attesting a claim's signature sidecar — its non-logical-symbol introductions and removals — against the claim's current revision. Each fire advances the sidecar's chain so downstream consumers (validator, dependents) read the current symbol-ownership state.

## Triggers

- The claim's body has advanced since the signature sidecar was last attested.

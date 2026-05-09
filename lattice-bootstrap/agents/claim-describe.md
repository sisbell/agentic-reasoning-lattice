---
caste: producer
scope: claim
---

# Claim Describe

Claim-describe is a producer agent whose primary substrate effect is attesting a claim's description sidecar — a one-to-three-sentence summary of what the claim says — against the claim's current revision. Each fire advances the sidecar's chain so downstream consumers (assembly, observability, navigation) read the current summary.

## Triggers

- The claim's body has advanced since the description sidecar was last attested.

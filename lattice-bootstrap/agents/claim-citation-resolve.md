---
caste: producer
scope: claim
---

# Claim Citation Resolve

Claim-citation-resolve is a producer agent whose primary substrate effect is typing the claim-label references in a claim's prose: emitting `citation.depends` and `citation.forward` per typed reference, `retraction` for stale ones, and an attestation on the references sidecar. Materializes the typed citation graph the validator and downstream reviewers consume.

## Triggers

- The claim's body has been edited since the references sidecar was last attested.

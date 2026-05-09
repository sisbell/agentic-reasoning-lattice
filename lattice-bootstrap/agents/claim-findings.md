---
caste: producer
scope: claim
---

# Claim Findings

Claim-findings is a producer agent whose primary substrate effect is decomposing a review's verdicts into per-finding substrate: emitting a `finding` classifier per item, `comment.<kind>` linking the finding to its target claim, and `provenance.derivation` from the review. Stages the review's content for the refiner to close.

## Triggers

- A `review.content` doc exists on the ASN whose findings haven't yet been decomposed into per-finding comments (one-shot per review).

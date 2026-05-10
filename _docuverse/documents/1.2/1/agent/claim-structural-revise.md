---
caste: refiner
scope: claim
---

# Claim Structural Revise

Claim-structural-revise is a refiner agent whose primary substrate effect is closing open `comment.violation` findings on a claim: emitting `resolution.edit` per addressed finding, plus `retraction` for RETRACT decisions on the claim's citations, after multi-pass edits to the claim's files. Drives the claim's structural state toward `is_claim_structurally_clean`.

## Triggers

- The claim has unresolved structural-violation findings open against it.

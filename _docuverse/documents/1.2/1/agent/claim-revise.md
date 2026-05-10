---
caste: refiner
scope: claim
---

# Claim Revise

Claim-revise is a refiner agent whose primary substrate effect is closing one open `comment.revise` on a claim by emitting `resolution.edit` or `resolution.reject` after editing the claim's text. Transforms the claim's open-finding state toward quiescence.

## Triggers

- An open `comment.revise` link targets the claim (per-comment).

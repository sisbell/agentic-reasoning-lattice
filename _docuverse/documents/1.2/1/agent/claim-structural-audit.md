---
caste: scout
scope: claim
---

# Claim Structural Audit

Claim-structural-audit is a scout agent whose primary substrate effect is making structural-invariant violations on a claim auditable: running the validator inside the agent and emitting a `review.structural` audit doc plus `comment.violation` per detected issue. Surfaces structural defects so the structural-revise refiner can close them.

## Triggers

- No structural audit exists for the claim yet, OR
- The latest audit's violations have all been resolved and the post-fix state needs re-auditing.

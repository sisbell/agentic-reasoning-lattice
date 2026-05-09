---
caste: producer
scope: claim
---

# Claim Patch

Claim-patch is a producer agent whose primary substrate effect is granting a `patch.claim` classifier and a patch-scoped review covering the targeted claim files: applying the operator-authored patch to disk and emitting findings as substrate. The findings flow into the standard claim-revise refinement chain.

## Triggers

- Operator-invoked, after dropping a patch md targeting one or more claim files.

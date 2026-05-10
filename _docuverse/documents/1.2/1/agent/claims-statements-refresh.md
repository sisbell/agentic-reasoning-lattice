---
caste: producer
scope: claim
---

# Claims Statements Refresh

Claims-statements-refresh is a producer agent whose primary substrate effect is advancing the `claims.statements` aggregate — a derived view of an ASN's formal claim statements — and emitting citation anchors per derived claim. Keeps the aggregate's substrate state in step with the per-claim state downstream consumers read.

## Triggers

- A derived claim has advanced past the aggregate's last attestation, AND
- Every derived claim is confirmed.

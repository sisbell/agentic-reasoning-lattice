---
caste: producer
scope: claim
---

# Cone Review

Cone-review is a producer agent whose primary substrate effect is a new `review.content` covering an apex claim and its same-ASN dependencies. Its findings drive downstream tightening of the apex's argument.

## Triggers

- The apex claim has a Formal Contract.
- Its dependencies are settled.
- No other agent is holding any of the cone's claims (apex + same-ASN deps) for review.
- The claim is either not yet cone-reviewed, or has gone cascade-stale (an upstream advanced past the cone's last coverage).

---
caste: producer
scope: note
---

# Note Clone

Note-clone is a producer agent whose primary substrate effect is granting a new note identity that clones an existing ASN: emitting a `note` classifier on the new doc, a `clone` classifier, and `provenance.clone(origin → clone)`. The clone evolves independently from its origin.

## Triggers

- Operator-invoked, when the operator wants to duplicate an ASN as an independently-evolving peer.

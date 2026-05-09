---
caste: producer
scope: note
---

# Note Consult

Note-consult is a producer agent whose primary substrate effect is gathering targeted consultations on each open `comment.revise` against a note: emitting `consultation.assessment`, `consultation.answer.<role>`, and `consultation.coverage` per finding. The coverage feeds note-revise so it can address each finding with the relevant evidence in context.

## Triggers

- The note has open `comment.revise` findings that don't yet have consultation coverage.

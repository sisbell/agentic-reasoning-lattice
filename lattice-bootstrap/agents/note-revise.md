---
caste: refiner
scope: note
---

# Note Revise

Note-revise is a refiner agent whose primary substrate effect is closing the open `comment.revise` findings on a note: emitting `resolution.edit` (or `resolution.reject` with rationale) per finding after editing the note's text. Drives the note's open-finding state toward quiescence.

## Triggers

- The note has open `comment.revise` findings, AND
- Every open revise has consultation coverage.

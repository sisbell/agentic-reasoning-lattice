---
caste: producer
scope: note
---

# Note Review

Note-review is a producer agent whose primary substrate effect is a new `review` covering a note plus per-finding `comment.<kind>` linking to the note. Its findings drive downstream refinement of the note's text via note-revise.

## Triggers

- An active non-retired note has unreviewed content — typically after the note has been edited and the latest review no longer covers the current content.

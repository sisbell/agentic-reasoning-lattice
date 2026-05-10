---
caste: producer
scope: note
---

# Note Patch

Note-patch is a producer agent whose primary substrate effect is granting a `patch.note` classifier and a patch-scoped review covering the targeted note: applying the operator-authored patch to disk and emitting findings as substrate. The findings flow into the standard note-revise refinement chain.

## Triggers

- Operator-invoked, after dropping a patch md targeting a note.

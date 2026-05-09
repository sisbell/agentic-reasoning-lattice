---
caste: producer
scope: note
---

# Note Statements

Note-statements is a producer agent whose primary substrate effect is attesting a note's `statements` sidecar — a formal-statements extraction of the note's content — once the note is confirmed. The sidecar serves as the artifact downstream `claim-decompose` consumes when deriving per-claim files.

## Triggers

- The note is confirmed, AND
- The statements sidecar is stale relative to the note's content.

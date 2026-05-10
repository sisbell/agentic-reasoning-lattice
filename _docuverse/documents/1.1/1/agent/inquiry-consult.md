---
caste: producer
scope: inquiry
---

# Inquiry Consult

Inquiry-consult is a producer agent whose primary substrate effect is gathering theory and evidence consultations against an inquiry: emitting `consultation.questions`, `consultation.answer.<role>` per Q/A, and `consultation.coverage`. Stages the consultation answers that note-draft will synthesize into a note.

## Triggers

- The inquiry has no consultation answers covering it yet.

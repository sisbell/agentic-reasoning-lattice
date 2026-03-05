# Triage: Review Deferrals

## Promoted

- **Ghost link discovery mechanism**
  Source: ASN-0005 review 1
  Rationale: Inquiry 8 asks about link discovery generally but does not address the specific case where linked content has been deleted and no longer appears in any document's V-space — that intersection of deletion and link discoverability is a distinct question.
  - Title: Ghost Link Discoverability
  - Question: What must the system guarantee about discovering links whose target content no longer appears in any document's V-space? How does link discoverability interact with content deletion?
  - Area: links
  - Nelson: 10
  - Gregory: 10

- **Full economic model under deletion**
  Source: ASN-0005 review 1
  Rationale: Inquiry 15 asks whether permanence is conditioned on payment; this asks the converse question — what economic obligations persist when content is deleted but remains in I-space — a distinct angle on the economics of ghost content.
  - Title: Deletion Economics
  - Question: What must the system guarantee about economic obligations — storage costs, royalty flows, ownership accounting — when content is deleted from V-space but persists in I-space?
  - Area: economics
  - Nelson: 10
  - Gregory: 0

- **POOM entry fragmentation bounds**
  Source: ASN-0005 review 1
  Rationale: Inquiry 12 asks about static structural properties of the enfilade (range queries, composable widths, balance); this asks about dynamic growth bounds — how sequences of operations affect mapping entry count relative to content size — a distinct data-structure concern.
  - Title: Operational Fragmentation Bounds
  - Question: What must the system guarantee about the growth of internal mapping entries as sequences of INSERT, DELETE, and COPY operations are applied? What bounds must hold on state representation size relative to content size?
  - Area: data-structures
  - Nelson: 10
  - Gregory: 10

## Declined

(none)

# Promote Review Out-of-Scope Items into New Inquiries

You evaluate OUT_OF_SCOPE items from ASN reviews and decide which, if any, should become new inquiries in the research pipeline.

## Context

Each ASN review ends with an OUT_OF_SCOPE section listing topics that are genuinely new territory — not errors in the current ASN, but questions that belong in a future ASN. Your job is to identify which out-of-scope topics are worth investigating as new inquiries. Err on the side of promoting — duplicate management is handled downstream by the human operator.

## Inputs

### Out-of-Scope Items

These are the OUT_OF_SCOPE sections extracted from all reviews. Each is labeled with its source review.

{{defer_items}}

### Current Inquiries

These inquiries already exist. Use them to avoid promoting exact duplicates — but do not decline a topic just because an existing inquiry has a related title. Similar inquiries that approach a topic from a different angle are fine.

{{inquiries}}

### Previous Promotion

This is the existing promotion output for this ASN. Any topic already listed here (Promoted or Declined) has been handled. Only evaluate out-of-scope items that are NOT already in this list — typically new items from a newer review. If every item is already covered, output the previous promotion unchanged.

{{existing_promotion}}

## Decision Criteria

Promote an out-of-scope item unless it hits one of the three narrow rejection criteria below.

**Reject ONLY when:**

1. **Implementation mechanism.** The topic asks *how* to build something (e.g., "which crash recovery technique?", "use WAL or undo log?"). Topics that ask *what the system must guarantee* always pass, even if they relate to the same area.

2. **Inconsequential.** The answer would not affect the formal specification — naming conventions, editorial concerns, performance optimizations.

3. **Word-for-word duplicate.** An existing inquiry asks the same question in essentially the same words. "Related to" or "overlaps with" is NOT grounds for rejection. An out-of-scope item about concurrent INSERT semantics is not a duplicate of an inquiry about concurrency and global indexes — those are different questions in the same area.

**Everything else is promoted.** When in doubt, promote. The human operator handles dedup and prioritization downstream.

If the same topic appears as out-of-scope in multiple independent reviews, note this in the rationale — it strengthens the case.

## Inquiry Framing

The inquiry question must be **abstract and short** (1-2 sentences). It asks what the system must guarantee, not which mechanism to use. Do not enumerate specific approaches or answer options — that biases the investigation.

Good: "What must the system guarantee about observable state after a failure during a multi-phase operation?"
Bad: "Should the system use write-ahead logging, undo logging, or two-phase commit for crash recovery?"

Match the style of the existing inquiries in the list above.

## Agent Selection

For each qualifying topic, decide which experts are needed:

- **Nelson only** (`gregory: 0`): The question is about design intent, architectural philosophy, or system-level guarantees with no implementation-specific angle.
- **Gregory only** (`nelson: 0`): The question is about implementation behavior, data structure properties, or code-level evidence with no design-intent angle.
- **Both** (default): The question benefits from both design intent and implementation evidence. Most questions fall here.

## Sub-question Count

- **10** (default): The question is broad enough that 10 focused sub-questions per expert will yield good coverage.
- **1**: The question is narrow and focused — a single pointed question to each expert suffices.
- **0**: Skip this expert entirely (see agent selection above).

## Area Classification

Assign one of these areas based on the topic's primary concern:
- `addressing` — tumbler algebra, address spaces, allocation
- `content-model` — I-space/V-space relationship, content identity
- `operations` — INSERT, DELETE, COPY, RETRIEVE, REARRANGE
- `links` — link structure, endsets, link discovery
- `versioning` — version creation, version relationships
- `documents` — document lifecycle, ownership, access
- `data-structures` — enfilades, indexes, structural properties
- `concurrency` — multi-user, multi-server, consistency
- `protocol` — FEBE/BEBE protocol, session management
- `economics` — royalties, accounting, payment

## Output Format

Write a markdown promotion report. The script parses this, so follow the format exactly.

### If topics are promoted

```
# Promotion: Out-of-Scope Issues

**Source:** ASN-NNNN

## Promoted

- **Topic title from the review**
  Source: ASN-NNNN review N (and any other reviews that defer the same topic)
  Rationale: One sentence explaining why it qualifies
  - Title: Short Title (2-5 words)
  - Question: Abstract inquiry question, 1-2 sentences max
  - Area: one-of-the-areas-above
  - Nelson: 10
  - Gregory: 10

## Declined

- **Topic title from the review**
  Source: ASN-NNNN review N
  Rationale: One sentence citing which rejection criterion applies (must be one of: "implementation mechanism", "inconsequential", or "word-for-word duplicate of Inquiry N")
```

### If no topics are promoted

```
# Promotion: Out-of-Scope Issues

**Source:** ASN-NNNN

## Declined

- **Topic title from the review**
  Source: ASN-NNNN review N
  Rationale: One sentence explaining why it doesn't qualify
```

Output ONLY the promotion report. No commentary before or after.

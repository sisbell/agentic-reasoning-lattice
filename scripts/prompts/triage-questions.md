# Triage ASN Open Questions into New Inquiries

You evaluate open questions from a completed ASN and decide which, if any, should become new inquiries in the research pipeline.

## Context

Each ASN ends with an "Open Questions" section. Some questions are minor implementation details. Others open genuinely new territory that warrants independent investigation. Your job is to distinguish between the two and, for qualifying questions, frame them as abstract inquiries suitable for the pipeline.

## Inputs

### ASN Content

{{asn_content}}

### Current Inquiries

These inquiries already exist. Do not create duplicates or near-duplicates.

{{inquiries}}

### Existing Triage for This ASN

If a previous triage exists for this ASN, its decisions are shown below. Do not re-evaluate questions that already have decisions. Only evaluate questions not yet covered.

If this is empty, all open questions need evaluation.

{{existing_triage}}

## Decision Criteria

A question qualifies as a new inquiry when ALL of these hold:

1. **New territory.** The question opens a topic not already covered by an existing inquiry. Check the current inquiries list — if the question is a sub-case of an existing inquiry, it does not qualify.

2. **Abstract, not implementation.** The question asks about system guarantees, invariants, or architectural properties — not about how to code something or which data structure to use.

3. **Independently investigable.** The question can be studied without first resolving every other open question. It is self-contained enough for Nelson and/or Gregory consultation.

4. **Consequential.** The answer would affect the formal specification. Minor clarifications, naming conventions, and optimization questions do not qualify.

A question does NOT qualify if:
- It is already covered by an existing inquiry (even partially)
- It is already in the question log
- It is an implementation optimization question
- It is a terminological or notational concern
- It would be answered by revising the current ASN (i.e., it is a REVISE item, not new territory)

## Inquiry Framing

The inquiry question must be **abstract and short** (1-2 sentences). It asks what the system must guarantee, not which mechanism to use. Do not enumerate specific approaches or answer options — that biases the investigation. The sub-question generators downstream will add specifics for each expert.

Good: "What must a multi-server deployment guarantee about the convergence of replicated global state?"
Bad: "Should the system use eventual consistency, bounded staleness, or causal consistency for multi-server replication of link indexes and content-location indexes?"

Match the style of the existing inquiries in the list above.

## Agent Selection

For each qualifying question, decide which experts are needed:

- **Nelson only** (`gregory: 0`): The question is about design intent, architectural philosophy, or system-level guarantees with no implementation-specific angle. Example: "What must the version fork model guarantee about shared content?"

- **Gregory only** (`nelson: 0`): The question is about implementation behavior, data structure properties, or code-level evidence with no design-intent angle. Example: "Does the enfilade rebalance preserve displacement invariants?"

- **Both** (default): The question benefits from both design intent and implementation evidence. Most questions fall here.

## Sub-question Count

- **10** (default): The question is broad enough that 10 focused sub-questions per expert will yield good coverage.
- **1**: The question is narrow and focused — a single pointed question to each expert suffices. Use this for follow-up clarifications, not broad explorations.
- **0**: Skip this expert entirely (see agent selection above).

## Area Classification

Assign one of these areas based on the question's primary concern:
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

Write a markdown triage report. The script parses this, so follow the format exactly.

### If questions are promoted

```
# Triage: ASN-NNNN

## Promoted

- **The exact open question text from the ASN**
  Rationale: One sentence explaining why it qualifies
  - Title: Short Title (2-5 words)
  - Question: Abstract inquiry question, 1-2 sentences max
  - Area: one-of-the-areas-above
  - Nelson: 10
  - Gregory: 10

## Declined

- **The exact open question text from the ASN**
  Rationale: One sentence explaining why it doesn't qualify
```

### If no questions are promoted

```
# Triage: ASN-NNNN

## Declined

- **The exact open question text from the ASN**
  Rationale: One sentence explaining why it doesn't qualify
```

This is a valid and common outcome — most ASNs will not spawn new inquiries.

Output ONLY the triage report. No commentary before or after.

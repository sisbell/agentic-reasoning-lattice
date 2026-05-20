## Question 8 [theory]

> For Coverage-shaped relations whose templates (`latest_K_for_addr`) do not consume the from-slot, what was the from-slot intended to identify — the witness/reviewer document, the home document, or something else — and why is it required rather than `c_F = 0`?

I have what I need. The question uses project-specific terminology not from Literary Machines, but the project's own rationale document (ASN-0047) explicitly answers it.

## The from-slot identifies the **witness/asserter document** (the K-document)

Project rationale `_docuverse/documents/1.1/1/rationale/ASN-0047/1.1.0.1.0.9632.0.2.3.md:23-29` states this directly:

> "Reverse-direction Coverage-shaped relations (REVIEWED_addr, REVISED_addr) project the slot K-doc from the from-slot of their underlying review/revision links."
>
> "Note: For these relations, K is recovered from the from-slot rather than the to-slot because review/revision links are directed from the witnessing K-document to the source it reviews/revises."

So the answer to your question:

- **What does the from-slot identify?** The K-document — the witness/reviewer document making the coverage assertion (e.g., the review-127 document asserting that something reviewed addr X).
- **Not the home document.** Home and from-set are distinct in Nelson's model. The home indicates ownership/where the link lives; the from-set is one of three semantic endsets.

## Why the template doesn't appear to "consume" it

The template name `latest_K_for_addr` is misleading. Both slots are consumed:
- `K` ← from-slot (the witness/reviewer document)
- `addr` ← to-slot (the subject being covered)
- "latest" ← temporal ordering across instances

The from-slot is the *source* of K. You cannot have `latest_K_for_addr` without a from-slot, because K *is* what the from-slot supplies.

## Why required rather than `c_F = 0`

Nelson's link model is explicit on this point — every link has three endsets, and each is an arbitrary span-set pointing somewhere:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" — LM 4/42

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse." — LM 4/43

A link with `c_F = 0` (no from-set) would be a one-sided link — Nelson treats those as a special case for designators where directionality is degenerate (LM 4/48). Review/revision relations are *not* degenerate: they have an asserter and a subject. The directionality carries provenance — without the from-slot, you cannot answer "which K-document asserted this coverage?" which destroys the auditability the Coverage shape exists to provide.

The semantic convention chosen — directed *from* the witnessing K-document *to* the source it reviews/revises — is a deliberate design decision (consistent with my principle that "what 'from' and 'to' mean depend on the specific case"). The from-slot is required because the relation's grounding depends on identifying the witness, even when the template's surface form names only the projected K.

# Channel Assignment — ASN-0130 review-26

**Date:** 2026-06-13 05:43

## Issue 1: View handling is fragmented across forward deferrals to PR-VIEW
Reason: Pure editorial consolidation — delete a bare cross-reference pointer in PR3 and move the view-polymorphism rationale to its owning section (PR-VIEW). The view semantics are already fully established in the ASN's own PR-VIEW; no design intent or implementation evidence is at stake, only where the existing prose lives.

## Issue 2: Editorial design-rationale in operation slots
Reason: Trimming rhetorical justification ("would be a lie", the non-predicate elaboration) whose operative content is already stated by the explicit reject-with-no-tuple clauses and the cross-reference to ASN-0128's S3. The enforce-by-rejection stance is internal to the note and already pinned; nothing about the system's intended behavior or the implementation is in question.

## Issue 3: "What this note commits" previews duplicate the body
Reason: Purely a prose-organization fix — collapse the seven duplicative preview bullets to a bare roadmap or cut them. The body already carries the content; deciding what the roadmap retains is internal to the note and needs no external channel.

# Channel Assignment — ASN-0069 review-85

**Date:** 2026-06-03 01:14

## Issue 1: Verbatim duplication of shared K.δ precondition discharges across sub-cases A and B
Reason: Purely a structural deduplication of proof prose. The three shared discharges (T10a.4, `zeros=2≠3`, V1+P8) are already established in the ASN and sub-case-independent; hoisting them needs no design intent or implementation evidence.

## Issue 2: Defensive justifications and document-convention meta-prose in structural slots
Reason: Pure prose deletion — removing a naming rationale, a notational-convention paragraph, and a forward deferral. The retained content (V2's statement, the `d_op` first-use clause, the quantifier-domain principle) is all already present in the ASN, so the fix is internal.

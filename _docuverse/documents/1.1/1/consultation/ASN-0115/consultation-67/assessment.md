# Channel Assignment — ASN-0115 review-67

**Date:** 2026-06-10 08:06

## Issue 1: R8's distinctness annotation is asymmetric between its sub-cases
Reason: Internal — the ASN already scopes the link sub-case to "distinct" positions, already handles the degenerate `v = v'` (one position, two overlapping specs) case separately in the same section, and already frames the guarantee as "once per V-position." Adding `v ≠ v'` to the box premise and content sub-case is a consistency fix derivable from the ASN's own reasoning; no design intent or implementation evidence is in question.

## Issue 2: R8 and R9 forward-reference R10 for a fact the `item` definition already establishes
Reason: Internal — the `⟨ref, a⟩`/address-carrying fact is defined upstream by the `item` definition in "What a spec-set is, and what delivery is," and both the citing locations (R8, R9) and the correct antecedent live within this ASN. Redirecting the citation from R10 to the `item` definition is a purely structural correction needing neither channel.

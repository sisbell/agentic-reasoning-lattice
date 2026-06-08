# Channel Assignment — ASN-0100 review-107

**Date:** 2026-06-07 22:24

## Issue 1: Unresolvable external references (Q1, Q3, Q5, Q8)
Reason: The Q-labels cite Nelson's question taxonomy on design intent (fresh-identity allocation, cross-document independence); to inline their substance or restate the requirement directly, we need what Nelson actually intended these operations to guarantee.
Nelson question: For INSERT, what does the design require regarding (a) fresh content identity — that inserted content always gets new I-addresses never aliased to existing ones — and (b) cross-document independence — that inserting into one document never alters another document that transcludes its content?

## Issue 2: Anti-bloat — vocabulary inventory and re-narration around the decomposition
Reason: Purely editorial cuts (defensive "not a primitive" sentence, the 7-element vocabulary list, and the re-narrated shift paragraph in §Effect Three); the load-bearing content all remains elsewhere in the ASN, so the fix is internal.

## Issue 3: No concrete example exercises m_C ≥ 3
Reason: Adding an m_C = 3 worked instance is a mechanical instantiation of the ASN's own closed-interval reduction and D-CTG★/D-MIN★/D-SEQ★ proofs; all needed machinery is already present in the text.

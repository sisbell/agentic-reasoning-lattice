# Channel Assignment — ASN-0114 review-16

**Date:** 2026-06-09 22:56

## Issue 1: F0's stated content does not match its "three clauses" billing, and duplicates F1
Reason: Internal fix. F0, F1, and F4 all already exist in the note; the defect is purely expository — the "three clauses" roadmap names a frame clause F0 does not carry, and the coverage equation is stated in both F0 and F1. Realigning the billing (or relocating the clauses) is a restructuring decision derivable from the note's own content, with no dependence on design intent or implementation evidence.

## Issue 2: The "single term" licensing for the multi-valued `followlink` is scoped too narrowly for its own uses
Reason: Internal fix. The review itself notes the licensing facts are already present — `⟨⟩` is the unique empty-coverage span-set (F7's first S2 collapse) and `⊥` is fixed by F0 — so widening the meta-statement to sanction the bare-term equalities in F7 and the worked instance is a self-contained logical adjustment requiring neither Nelson nor Gregory.

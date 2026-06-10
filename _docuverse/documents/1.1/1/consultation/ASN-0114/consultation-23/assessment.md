# Channel Assignment — ASN-0114 review-23

**Date:** 2026-06-10 00:33

## Issue 1: F4's frame enumerates a strict subset of the state it ranges over
Reason: Internal fix. The decision is purely a bookkeeping/consistency choice between two state models already cited in the note — ASN-0093's `(C, L, M)` and the ASN-0098/ASN-0047 extended `(C, L, E, M, R)` reachability that F5's LP13 and the worked instance's LP-Fin already draw on. The pure-read status of FOLLOWLINK is settled, so `E` and `R` are trivially fixed; the reviewer has spelled out both repair paths (restrict to the ASN-0093 projection, or complete the enumeration). No design intent or implementation evidence is required to pick and apply one.

## Issue 2: F6 discussion carries evidence-weighing meta-prose (anti-bloat)
Reason: Internal fix. This is a prose-trimming edit over content already present in the note — keep the abstract coverage-only limit, reduce the bounded-query evidence (Q12, Q18, already cited) to a single corroborating clause, and drop the "does not strengthen F6" evidence-weighing tail. No new evidence or design intent is needed to cut existing meta-prose.

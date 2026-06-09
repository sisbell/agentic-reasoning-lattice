# Channel Assignment — ASN-0116 review-30

**Date:** 2026-06-09 09:43

## Issue 1: P5 (DocumentIsolation) is false for documents with link-subspace arrangements
Reason: Fully internal — the fix swaps the superseded S3 for S3★ (already referenced in the note), states P5 per-subspace, and wires in K.α's whole-store freshness `A_new ∩ (dom(C) ∪ dom(L)) = ∅`, which the composite section already establishes. No design intent or implementation evidence is in question.

## Issue 2: Same S3-vs-S3★ imprecision in the left/shifted referential-integrity discharge
Reason: Internal — identical correction, citing S3★ (ASN-0047) instead of S3 and restricting the range bound to content-subspace positions; the argument's substance is unchanged and derivable from the note's own state model.

## Issue 3: Duplicated interval-disjointness fact under two names
Reason: Internal editorial consolidation — state the interval fact once and reference it from both sites; no external input needed.

## Issue 4: Rhetorical "This is the answer to X" framings recur as essay scaffolding
Reason: Internal editorial deletion of framing clauses; the technical statements stand on their own.

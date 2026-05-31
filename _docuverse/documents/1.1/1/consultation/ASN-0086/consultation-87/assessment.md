# Channel Assignment — ASN-0086 review-87

**Date:** 2026-05-31 15:54

## Issue 1: The `↦` / `↝` arrangement-transition machinery is inert (or contradicts) the stated ASN-0093 foundation
Reason: The contradiction is between two cited foundations (ASN-0036 admits arrangement modification; ASN-0093 M2 forbids non-empty arrangements), and resolving which substrate the note should target turns on whether mutable document arrangements are part of the intended design — a design-intent question for Nelson. Gregory is not needed: the conflict is between spec invariants, not implementation behavior.
Nelson question: Is document arrangement modification (non-empty, mutable `Σ.M(d)`) intended to be part of the substrate this relational layer sits on, or is the empty-arrangement constraint (M2) a permanent design commitment?

## Issue 2: R5-Cor (EmitContentUniformity) is a restatement of R0, not a new lemma
Reason: Fully derivable from the ASN — R0 already universally quantifies `F, G ∈ Endset` and `K ∈ T_admissible` with no coverage restriction, so demoting R5-Cor to a remark on R0 and citing R0 directly is an internal editorial change requiring no external evidence.

## Issue 3: R6b is stated, re-justified, and then re-derived at length — three times for one claim
Reason: Purely internal restructuring — collapse the redundant statements of the audit-slice quantification point into one location and let the Worked Sketch compute rather than re-narrate; no design intent or implementation evidence is involved.

## Issue 4: Meta-prose and forward-reference accretion (anti-bloat classifier)
Reason: Editorial deletion of placement/deferral prose and proof-structure narration, all derivable from the ASN's own content; no external channel needed.

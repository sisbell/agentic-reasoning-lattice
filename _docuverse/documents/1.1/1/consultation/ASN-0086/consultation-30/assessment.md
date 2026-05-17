# Channel Assignment — ASN-0086 review-30

**Date:** 2026-05-17 05:05

## Issue 1: R6c-Corollary's frame derivation has a small layering inconsistency
Reason: This is a prose-internal reconciliation: the ASN already states "This frame is part of ASN-0036's definition of the arrangement-modifying transition class and is inherited here without re-derivation," so the contradicting derivation in the same paragraph can be fixed by either dropping the L12/L12a citations or recasting them as consistency invariants. No external evidence required.

## Issue 2: Worked Sketch Step 5.2 silently introduces an unspecified arrangement-modifying transition
Reason: The fix has two paths — either populate Σ.M(d) with concrete entries and an explicit INSERT (semantics already defined in ASN-0036 / editing-operation ASNs and visible in the codebase) or state explicitly that 5.2 is a structural argument with concrete realization deferred. Both paths are derivable internally; the latter is purely a prose-level qualification.

## Issue 3: R0 Step 2 Case A's `s_L`-th sibling sweep deserves an explicit T4-validity invocation
Reason: The argument is already sound — TA5a (ASN-0034) is unconditional for k=0, and the seed `d.0.1` is T4-valid. The fix is adding one sentence noting the iterated preservation by induction on the iteration index. Fully derivable from ASN-0034 invariants already in scope.

## Issue 4: The "consequences" sections lack a typology marker
Reason: This is a presentation/classification issue — the writer needs to mark each consequence as {COROLLARY, POLICY, ARCHITECTURE} or restructure the paragraphs. The classification is determined by the consequences' own content (whether each is a formal corollary, a policy observation, or architectural commentary) and requires no external consultation.

## Issue 5: The R7 headline's conditionality is hedged in the body but not the abstract
Reason: Pure abstract-update task: add one sentence acknowledging that R7's reduction is the conjunction of R7a (proven) and R7b (stipulated), paralleling the hedging language already present for R0–R6 in the same abstract. No external evidence needed.

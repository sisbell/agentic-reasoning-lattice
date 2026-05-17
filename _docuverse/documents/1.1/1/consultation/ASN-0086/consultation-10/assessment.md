# Channel Assignment — ASN-0086 review-10

**Date:** 2026-05-16 19:30

## Issue 1: R5 Setup-tag inconsistency
Reason: The fix is a choice between two internal options (retag vs. rewrite as pure admissibility), and both options are decidable by inspecting R5's own proof structure and its dependence on R0's L14a-preservation step. No external evidence or design intent is required.

## Issue 2: T10a.1 citation missing for equal-length siblings
Reason: This is a cross-reference correction verifiable from ASN-0034's already-cited theorem catalog (T10a.1 is named in the foundation spec ASN-0086 already draws on for T10a.2/T10a.4/T10a.6/T10a.7/T10a.8). No external channels needed.

## Issue 3: T_cat^Σ definition asymmetry with L_K^Σ
Reason: The asymmetry is between two definitions in this note, and both proposed fixes (redefine T_cat^Σ in coverage-class form, or rephrase RetractionType) are internal definitional choices. The note's own Rationale paragraph already commits to coverage-equivalence as the operative semantics.

## Issue 4: Sub-document caveat introduces undefined concept
Reason: The fix is to delete a forward-reference to an undefined concept. ASN-0036's flat-document model is part of the foundation already cited; removing the parenthetical requires no new claim about design or implementation.

## Issue 5: R6a needs explicit `a ∈ A_rel^{Σ'}` step
Reason: Pure proof patching — the missing step is supplied by L12a (already cited in ASN-0086 elsewhere) applied to a precondition already in hand. No external context needed.

## Issue 6: Worked sketch does not link to R5
Reason: An editorial cross-reference between two sections of the same note. No design or implementation evidence required.

## Issue 7: R0a Case 1 partition wording
Reason: A presentational restructuring that makes an already-correct partition explicit; no new claims are introduced. Derivable from the existing proof's own logical structure.

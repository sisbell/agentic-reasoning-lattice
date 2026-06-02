# Channel Assignment — ASN-0047 review-339

**Date:** 2026-06-02 06:37

## Issue 1: J2's P4★ justification asserts the bound at intermediate states where it is declared able to fail
Reason: Purely a logical-statement fix internal to the ASN — replacing an overstated inclusion chain with the monotonicity fact (`Contains_C(Σ') ⊆ Contains_C(Σ)`, `R' = R`) that K.μ⁻'s own frame and effect already establish. No design intent or implementation evidence bears on it.

## Issue 2: K.μ⁻ contraction-shape semantics are restated in four separate locations
Reason: An anti-bloat consolidation of four redundant descriptions of one mechanism already fully specified in the ASN; deciding canonical-statement-plus-pointers is an editorial judgment requiring no external channel.

## Issue 3: NodeBaptism axiom is surrounded by rationale and restated, mixing "why" with "what"
Reason: The load-bearing facts (T10, CrossNodeAccountBase, SSGU consumers) are all derived within the ASN; trimming self-justifying non-circularity asides and the duplicate table restatement is internal editing, not a question of design intent or code behavior.

## Issue 4: "V-position depth (operational)" and "Clause (i)'s scope" carry defensive essay prose in structural slots
Reason: The substantive content (re-pin can change depth; clause-(i) scope) is already present and correct; cutting the surrounding meta-prose and folding the scope note into the clause is an internal prose-discipline fix.

# Channel Assignment — ASN-0094 review-91

**Date:** 2026-05-28 10:35

## Issue 1: Cross-ASN references to non-foundation ASNs
Reason: Editorial/structural fix derivable from project conventions and the local scaffolding clauses already present in the ASN. The reviewer notes the scaffolding already does the work locally; removing the cross-references is a documentation hygiene call, not a design or evidence question.

## Issue 2: SubstrateConformingLayer definition overlaps with foundation
Reason: Naming-collision fix between ASN-0094's local notion and ASN-0086's foundation definition. The choice (rename locally vs. strengthen to match foundation) is a stylistic/structural decision derivable from the two definitions in front of us.

## Issue 3: "Sh-conf binds Emit_K, not K.λ" repeated multiple times
Reason: Anti-bloat editorial fix. Consolidating a repeated clarification to a single canonical location requires no external input.

## Issue 4: Gate Ordering content appears in two locations
Reason: Editorial restructuring — replace forward-reference essay with a tight pointer. Internal to the ASN's prose organization.

## Issue 5: Terminology inconsistency for layer disciplines
Reason: Pure terminology consolidation across "contract" / "commitment" / "discipline". Reviewer already recommends "contract"; this is an editorial pick applied uniformly.

## Issue 6: Dead-content case in SHCD preservation
Reason: Removing a vacuous case from an induction that is already monotone by R3. Internal proof hygiene, derivable from ASN-0086's R3 and the existing case structure.

## Issue 7: Sh4HoldsAtFDDRegisteredK preconditions reference forward
Reason: Local reordering within the FDD subsection — either move the corollary past the preservation theorem or drop the "(below)" pointer. Pure structural fix.

## Issue 8: "Structural gates" prose duplicates Gate Ordering content
Reason: Anti-bloat fix — delete or compress to a cross-reference. The Gate Ordering section already specifies the clause-to-gate mapping.

## Issue 9: Definitions section has scope-clarification meta-prose
Reason: Remove a contrastive rationale parenthetical, citing CoverageEqualityDecidability instead. Editorial trim derivable from the existing lemma.

## Issue 10: Sh-conf rejection patterns numbered 1–5 don't match gate numbers
Reason: Numbering-scheme consistency between rejection patterns and Gate Ordering. Reviewer offers two paths (renumber by gate, or drop pattern numbering and cite by gate+clause); both are internal editorial choices.

## Issue 11: CoverageEqualityDecidability proof has scope-justification prose
Reason: Remove defensive paragraph anticipating reader confusion; treat spans uniformly as bounded T1-intervals per T12 + PrefixSpanCoverage. Internal proof cleanup derivable from existing axioms already cited.

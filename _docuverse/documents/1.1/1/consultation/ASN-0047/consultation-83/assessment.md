# Channel Assignment — ASN-0047 review-83

**Date:** 2026-05-17 17:00

## Issue 1: K.δ ghost-base versioning relationship to S7d unclear
Reason: The fix is derivable from the ASN's own ghost-base discipline at K.δ (Path 2 + TA5 determinism is already documented), combined with the precedent set by D-CTG★/D-MIN★/S3★/P4★ for refining ASN-0036 properties in the extended state. The choice between "justify" and "weaken S7d★" is a formal alignment internal to this ASN.

## Issue 2: K.μ⁻ "derived precondition" annotation is confusing
Reason: Stylistic contract cleanup — either move to "Consequences," drop, or commit to as a real precondition. Internal to the ASN.

## Issue 3: K.μ⁻ admissibility precondition contains redundancy
Reason: Structural consolidation of overlapping precondition clauses. Internal to the ASN.

## Issue 4: K.μ~ admissibility constraints reference post-state properties
Reason: Formal contract clarification — separating preconditions from postconditions is a structural fix derivable from the ASN.

## Issue 5: Defensive meta-prose accretion in Cross-document disjointness lemma
Reason: Removal of meta-prose justifying proof structure. Internal cleanup.

## Issue 6: Defensive "Shift-lemma applicability" paragraph in K.μ⁺_L
Reason: Compression of defensive paragraph to a citation. Internal cleanup.

## Issue 7: Reviser drift in J4 V-position preservation rationale
Reason: Removal of prior-formulation discussion. Internal cleanup.

## Issue 8: Multiple paragraphs defer to the same withdrawal-mechanism open question
Reason: Consolidation of duplicate defer-to-open-question text. Internal cleanup.

## Issue 9: Missing concrete worked example for K.δ case (ii) k=2 descent
Reason: The K.δ case (ii) k=2 specification is fully present in the ASN; producing a worked example exercises existing preconditions on concrete addresses. Internal.

## Issue 10: SubAllocatorAxiom explanatory prose redundancy
Reason: Consolidation of three-form explanation (axiom prose, post-axiom paragraph, dispatch table). Internal cleanup.

## Issue 11: K.μ~ "all valid π yield the same post-state" derivation is over-explained
Reason: Compression of essay-style derivation to a brief existential-witness note. Internal cleanup.

## Issue 12: L1b derivation chain not tight
Reason: Tightening "by construction" to a direct T4b citation — purely a foundation-citation rigor fix. Internal.

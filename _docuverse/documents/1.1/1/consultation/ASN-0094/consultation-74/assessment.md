# Channel Assignment — ASN-0094 review-74

**Date:** 2026-05-25 14:44

## Issue 1: Sh4 contract's "Without the conditional hypothesis" sub-paragraph is imagined-case meta-prose
Reason: Editorial fix — the reviewer has identified an imagined-case pattern and supplied the exact replacement text. No design intent or implementation evidence needed; the simplification is derivable from Sh2 alone (slot_addrs(F_τ) ⊆ A^Σ).

## Issue 2: Initial-State Baseline section bloats one assumption into four overlapping paragraphs
Reason: Pure consolidation of overlapping meta-prose into one paragraph plus one sentence. The substantive content is already stated; the fix is editorial.

## Issue 3: Caller-side rejection classification duplicates the Gate Ordering enumeration
Reason: Deduplication of two enumerations describing the same gate sequence. Picking one as primary is a structural editorial choice; the framework's gate semantics are unchanged.

## Issue 4: RetractionSelfFreshness's *Use sites* paragraph enumerates downstream consumers
Reason: Editorial removal of downstream-consumer enumeration and document-ordering justification. The lemma's content stands on its own; no external evidence needed.

## Issue 5: No concrete walkthrough exercises FDD or SHCD
Reason: The worked example exercises the framework's own definitions (FDD's `K_target_of` + suppression; or SHCD's `latest_K_for_addr` + `emission_order`). All machinery is internal to the ASN; example construction is derivable from the contract definitions and existing walkthrough patterns.

## Issue 6: Sh5 is labeled META but has no operational content
Reason: Demoting an editorial convention from labeled-property status. The change is structural/naming only; no external content involved.

## Issue 7: Decidability of coverage-equality is essay content embedded in TypedRelationCatalog Definition
Reason: Extract algorithm into a separate lemma. The algorithm's content and citations (T1/T2/T12/TumblerAdd/TA0/T5/PrefixSpanCoverage) are already established; the fix is purely restructural.

## Issue 8: Framework-wide commitment paragraph is meta-prose
Reason: Fold the identification into the subspace partition scaffolding clauses themselves. The content is preserved; the fix is editorial relocation.

## Issue 9: Lifetime constancy paragraph explains why the axiom is needed rather than what it says
Reason: Replace justification-as-content with a one-sentence axiom and relocate the inductive-baseline argument to Sh0's proof preamble. Both the axiom and its consumption site already exist in the ASN.

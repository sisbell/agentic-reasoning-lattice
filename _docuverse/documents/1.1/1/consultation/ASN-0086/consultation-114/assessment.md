# Channel Assignment — ASN-0086 review-114

**Date:** 2026-05-31 21:51

## Issue 1: Properties table contradicts the R0 proof on cross-home freshness
Reason: Internal — the proof body already gives the correct home-projection (T4b field-extraction) distinctness argument and explicitly disavows T10; the fix is to make the table match the proof it summarizes. No design-intent or implementation evidence needed.

## Issue 2: R0's first-emission branch relies on a →*-scoped lemma while the lemma is asserted over the full ↝*-reachable state space
Reason: Internal — the required conformance-free derivation (`[d.0.s_L.1] ∉ dom(Σ.L)` via the empty-homed-set predicate + `home(·)=d` contradiction; `∉ dom(Σ.C)` via SC-NEQ + T7) uses only lemmas already cited in the ASN, paralleling the existing subsequent-emission branch.

## Issue 3: R0a-Cor1 verbatim restates the ConformingHomedContiguity sub-lemma
Reason: Internal — purely a structural consolidation of two co-extensive set equalities under one label; no external input required.

## Issue 4: R7a's clause-(b) contingency is stated in three places
Reason: Internal — collapsing the triplicated contingency into a single clause of the lemma statement is an editorial deduplication using the ASN's own content.

## Issue 5: ConformingHomedContiguity proves a composite multi-key-at-one-home case no operation exercises
Reason: Internal — the note's operation set (Emit_K, Observe_K, Nullify) is fixed within the ASN and every operation deposits one key per home per step, so the decision to restrict the sub-lemma to the single-key case is derivable from the ASN's own scope.

# Review of ASN-0070

## REVISE

### Issue 1: The vacuous-subspace convention is restated four times
**ASN-0070, The Setting / V-restricted denotation / F1 / F-canon-form**: the fact "`V_S(d) = ∅ ⟹ m_S(d) undefined ⟹ Σ_V^S = ⟨⟩`" is asserted in (a) The Setting ("When `V_S(d) = ∅`, `m_{s_L}(d)` is undefined … the next insertion re-pins it"), (b) the V-restricted denotation definition ("When `m_S(d)` is undefined … `R(d, e)|_S = ∅` unconditionally … the only admissible span-set … is `⟨⟩`"), (c) F1's postcondition ("when `V_S(d) = ∅` … `Σ_V^S = ⟨⟩` by the V-restricted denotation convention"), and (d) F-canon-form ("When `m_S(d)` is undefined … the canonical form is `Σ_V^S = ⟨⟩`").
**Problem**: Two+ passages in different sections say the same thing in different words — the precise reader re-derives the same convention four times. This is the "two paragraphs say the same thing" accretion pattern.
**Required**: State the convention once (in the V-restricted denotation definition, where `⟦⟨⟩⟧_V := ∅` is fixed) and have F1, F-canon-form, and The Setting cite it rather than re-deriving the empty-subspace outcome.

### Issue 2: Organizational meta-prose in "Discussion: System Guarantees"
**ASN-0070, Discussion**: "we collect those readings here rather than appending one to each lemma body."
**Problem**: This is prose justifying document layout, not advancing any claim — the "prose justifies document ordering / placement" pattern. The Nelson readings themselves are admissible interpretive content, but the sentence explaining *why they were relocated* is noise the reader must skip.
**Required**: Drop the placement justification; open the section with the first reading directly.

### Issue 3: Rhetorical forward-pointers that carry no content
**ASN-0070, end of F0 section**: "From this single relation, the entire specification of FOLLOWLINK follows." Also F0's intro "Coverage may reach the arrangement fully, partially, or not at all; the inverse image handles all three uniformly, the empty set among them (formalised as F-empty)."
**Problem**: Both are signposting flourishes that defer to downstream material (F-empty, the rest of the note) without advancing the definition's meaning. The second enumerates a downstream consumer of F0 in place of object-level content.
**Required**: Remove the flourish; if the fully/partially/not-at-all observation is wanted, state it as the object-level fact (`coverage(e) ∩ ran(M(d))` may be any subset, including ∅) without the F-empty forward pointer.

## OUT_OF_SCOPE

### Topic 1: Multi-home endset resolution coherence; concurrency semantics; transclusion-lineage relationships
**Why out of scope**: These are the note's own Open Questions and belong in successor ASNs — they concern cross-document/cross-state relationships the present query operation does not need to specify. No error here.

The mathematics is sound: Step 1's action-point case split correctly excludes `k < m_S(d)` by finiteness (via T0(a) unboundedness) and the maximal-run construction in Step 2a sidesteps the S7 covering-vs-exact gap by building the span-set directly from contiguous runs rather than invoking S7. Edge cases (empty arrangement, both subspaces vacuous, cross-subspace straddle, multiplicity, state contraction) are each exercised against a concrete configuration. The remaining issues are residual prose accretion, not correctness.

META: not applicable — the ASN defines a state-pure query, its postcondition, and its invariants abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE

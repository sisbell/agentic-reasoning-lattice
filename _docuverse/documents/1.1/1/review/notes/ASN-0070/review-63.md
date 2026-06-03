# Review of ASN-0070

## REVISE

### Issue 1: F-slot restates its own postcondition

**ASN-0070, F-slot (SlotUniformity)**: The Postcondition reads "The resolution mechanism applies identically across slots; differing results reflect differing endsets, not differing routing." The paragraph after **Depends** then reads "The resolution mechanism is slot-independent: the type endset e₃ resolves by the same inverse-image definition as any other slot, and differing results across slots reflect differing endsets, not differing routing."

**Problem**: The post-Depends paragraph's first sentence duplicates the Postcondition's last sentence almost verbatim ("differing results … reflect differing endsets, not differing routing"). The construction-vs-resolution point is *also* already carried by the Depends line ("L3's asymmetric well-formedness … constrains link construction, not resolution"). This is the anti-bloat pattern: two passages in the same claim saying the same thing in different words.

**Required**: Delete the redundant restatement. The only non-duplicated content in that paragraph is the empty-endset observation ("R(d, eᵢ) = ∅ is uniformly admissible whether the cause is eᵢ = ∅ or coverage that misses the arrangement"); keep that single sentence and drop the rest.

### Issue 2: Defensive/label meta-prose in structural slots

**ASN-0070, Claims table, F-frame row**: "the frame clause Σ' = Σ of F1 (named handle for downstream citation)".
**ASN-0070, F-empty Postcondition**: the parenthetical "(A ⟨⟩ component here means coverage misses a populated subspace; this is distinct from a vacuous subspace V_S(d) = ∅, where ⟨⟩ is forced by the Vacuous-subspace convention.)"

**Problem**: The F-frame parenthetical justifies *why the row exists* (citation handle) rather than advancing the claim — a use-site rationale. The F-empty parenthetical re-explains the coverage-miss vs vacuous-subspace distinction that the "Vacuous-subspace convention" paragraph already defines and that Configurations 1 and 6 already exercise; it is defensive clarification restated outside its defining slot.

**Required**: Drop the "(named handle for downstream citation)" parenthetical — the frame clause stands on its own. Remove the F-empty distinction parenthetical; the distinction lives in the Vacuous-subspace convention and is exercised in the worked examples, so it need not be re-stated inside the lemma postcondition.

## OUT_OF_SCOPE

### Topic 1: Multi-home reconciliation and concurrency semantics
**Why out of scope**: Both Open Questions (relationship between `follow(ℓ,d,i)` and `follow(ℓ,d',i)` over shared homes; concurrency semantics under concurrent modification) are correctly deferred — they concern cross-document reconciliation and transaction isolation, distinct future territory rather than gaps in this query's specification.

The proofs themselves are sound: F-canonical's existence/uniqueness (the maximal-run construction, the consecutivity characterisation, and the V-restricted ↔ full denotation bridge) is carried through both inclusions with boundary cases (empty X, vacuous subspace, single-component last position) handled; the worked examples exercise interior-offset clipping (j>0, c<n), within-document multiplicity, cross-subspace straddle, and state-dependence concretely; and the wp analysis is non-trivial. No rigor defect found — the remaining issues are residual meta-prose.

VERDICT: REVISE

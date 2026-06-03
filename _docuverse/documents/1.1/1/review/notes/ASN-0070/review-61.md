# Review of ASN-0070

I checked F-canonical (both inclusions of Step 1, the consecutivity Characterisation of Step 2, the existence construction of Step 3, and the V-restricted↔full bridge with right- and left-closure of Step 4), the F-contig contiguity claim, F-subspace, F-empty's representational argument, and all five worked configurations including the P-depth/P-alloc premises. The mathematics is sound: edge cases (empty endset, empty arrangement, ghost references, partial/total emptiness, interior-offset clip `j>0,c<n`, cross-subspace straddle) are genuinely handled, the weakest-precondition analysis is non-trivial, and concrete examples verify the postcondition. No correctness gaps found, no foundation reinvention, no scope drift.

The remaining issues are anti-bloat / redundancy patterns, which the review-mode classifier asks me to surface.

## REVISE

### Issue 1: F-frame restates F1's frame clause verbatim

**ASN-0070, F-frame (INV) vs F1 (DEF)**: F1 already states "Frame. `Σ' = Σ`. No component of state is modified." F-frame then re-states "Postcondition. `Σ' = Σ`. Specifically: `C' = C`, `M' = M`, `L' = L`, `E' = E`, `R' = R`," with derivation "Definition of `follow` as a query (no effect clause)" and Frame "The frame condition itself."

**Problem**: This is the same claim in two structural slots, with a circular/vacuous derivation. It matches the "two paragraphs say the same thing in different words" trigger. The component enumeration adds nothing F1's frame did not already entail.

**Required**: Collapse F-frame into a table-row pointer to F1's frame clause, or delete it. If a named handle is wanted for downstream citation, keep the table entry but drop the lemma body and the vacuous derivation/Frame lines.

### Issue 2: F1 Remark is forward-looking explanatory prose in a DEF slot

**ASN-0070, F1 Remark**: "`Σ_V^S = ⟨⟩` arises from two distinct sources: (a) `V_S(d) = ∅`... or (b) `V_S(d) ≠ ∅` but `R(...)|_S = ∅`... Source (b) shows `Σ_V^S = ⟨⟩` does not imply the subspace is vacuous."

**Problem**: The (a)/(b) distinction is already captured structurally by the Vacuous-subspace convention (which forces `⟨⟩` for source (a)) and demonstrated operationally by worked Configuration 1 ("Partial emptiness", source (b)). It sits in the operation's definition slot as commentary the reader must parse before reaching the actual postcondition.

**Required**: Either remove the Remark (the convention + F-empty + the worked example carry it) or relocate it as a one-line note adjacent to F-empty, where the empty-result case is actually treated.

## OUT_OF_SCOPE

### Topic 1: Multi-home transclusion relationship across documents
**Why out of scope**: The first Open Question (relationship between `follow(ℓ,d,i)` and `follow(ℓ,d',i)` when coverage spans multiple homes) is genuinely new territory — it concerns inter-document resolution semantics, not the single-document inverse image this note defines.

### Topic 2: Concurrency semantics under concurrent modification
**Why out of scope**: The second Open Question belongs with the replication/inter-server protocol, explicitly excluded from this ASN.

VERDICT: REVISE

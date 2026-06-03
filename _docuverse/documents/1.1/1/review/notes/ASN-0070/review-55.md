# Review of ASN-0070

The mathematics here is genuinely rigorous — the F-canonical existence/uniqueness proof handles its cases, the contiguity claim is properly grounded in M1 + T12 order-convexity, and the six worked configurations each exercise a distinct postcondition correctly. I verified the per-block intersections in Configurations 1, 5, and 6 against the stated arrangements and they hold. My findings are presentational, concentrated in the structural-slot and duplication patterns the anti-bloat classifier targets.

## REVISE

### Issue 1: F-subspace proves its postcondition inside the Depends slot

**ASN-0070, F-subspace (IOSubspaceCorrespondence)**: The **Depends.** paragraph ends with "By S3★-aux, `subspace(v) ∈ {s_C, s_L}`. In the `s_C` case, S3★ gives `M(d)(v) ∈ dom(C)` and L0 gives `subspace_I(M(d)(v)) = s_C = subspace(v)`; in the `s_L` case... Either case yields `subspace_I(M(d)(v)) = subspace(v)`."

**Problem**: The lemma's main postcondition proof lives in the Depends slot. Every other lemma in this note (F-det, F-sound, F-complete, F-empty, F-multi) uses a dedicated **Derivation.** slot; F-subspace's main postcondition has no such slot, while its *corollary* gets one ("**Consequence.** ... *Derivation.*"). A reader following the lemma must extract the proof from the dependency inventory. Essay/proof content in a structural (Depends) slot.

**Required**: Move the postcondition proof out of Depends into a **Derivation.** slot. Leave Depends as a citation list only (the three "X — claim" entries), matching the convention used by the other lemmas.

### Issue 2: "d need not be the home document" stated in three places

**ASN-0070, F1, F-multidoc, and the F1 prose**: F1's prose enumerates non-requirements — "There is no requirement that `d` be `ℓ`'s home document. There is no requirement that any I-address in the endset's coverage be arranged in `d`. There is no requirement that the link have been resolved before..." — and each is then formalized as a separate downstream lemma (F-multidoc for the home point, F-empty/F-persist for reach and prior-resolution).

**Problem**: This is the "definition's introduction enumerates downstream consumers" pattern: F1 previews F-multidoc, F-empty, and F-persist in prose, and each lemma then restates the same content formally. F-multidoc's postcondition ("`home(ℓ)` ... plays no privileged role") and F1's "There is no requirement that `d` be `ℓ`'s home document" are the same claim in two voices.

**Required**: Drop the four "There is no requirement that..." sentences from F1. The Weakest Precondition Analysis already proves the precondition set is minimal (so nothing is silently required), and F-multidoc/F-empty/F-persist carry the formal statements. F1 should state its preconditions and stop.

### Issue 3: The "coverage, not decomposition" point is stated twice

**ASN-0070, The Setting and F0**: The Setting says "An endset records *which addresses* a link reaches; the specific span decomposition is a representational choice, not a semantic one." F0 says "It does not depend on the order or structure of spans within `e`. Two endsets with the same coverage produce the same `R(d, e)`."

**Problem**: Two paragraphs in different sections asserting the same fact (resolution depends on coverage, not span decomposition). The Setting's version is anticipatory prose for a property F0 then establishes definitionally.

**Required**: Keep the statement at F0 (where it is a property of the definition) and remove the anticipation from The Setting, or vice versa — one location, not two.

### Issue 4: Defensive exhaustiveness restatement in F-canonical Step 1

**ASN-0070, F-canonical Step 1**: "Since `actionPoint(ℓ) ∈ [1, #ℓ]` (ActionPoint postcondition, ASN-0034) and `#ℓ = m_S(d)`, the cases `1 ≤ k < m_S(d)` and `k = m_S(d)` are jointly exhaustive, and `k > m_S(d)` cannot arise."

**Problem**: "and `k > m_S(d)` cannot arise" is already entailed by the cited bound `actionPoint(ℓ) ≤ #ℓ = m_S(d)`. The clause restates the bound's consequence defensively after the bound has been given.

**Required**: Delete "and `k > m_S(d)` cannot arise" — the bound `k ∈ [1, m_S(d)]` already makes the two-case split exhaustive.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics for `follow` against a concurrently-modified document
The note's second Open Question raises this. Correctly deferred — transition interleaving is not this query's concern.

### Topic 2: Cross-home and transclusion-lineage resolution relationships
The first and third Open Questions. These require multi-document relational machinery this note does not (and need not) develop.

VERDICT: REVISE

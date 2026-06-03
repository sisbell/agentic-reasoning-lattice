# Review of ASN-0070

## REVISE

### Issue 1: F-canon-form definition states what a downstream proof *does* instead of stating the shape

**ASN-0070, F-canon-form clause (i)**: "The width is *not* pre-stipulated: F-canonical Step 1 derives that the finiteness and subspace-confinement of `⟦σ⟧_V` force each width to be an ordinal displacement `δ(c, m_S(d)) = [0, ..., 0, c]` of depth `m_S(d)`."

**Problem**: This is forward-reference meta-prose inside a definition. A reader working to understand the canonical form's *shape* reads clause (i), reaches this sentence, and is told only what a later theorem (F-canonical Step 1) establishes — not what the shape is. To learn the width constraint the reader must hold this sentence and jump to Step 1. That is precisely the "skip past meta-prose to follow the claim" pattern. The necessity argument (finiteness ⇒ action point = m ⇒ width is `δ(c,m)`) belongs in F-canonical, not in the definition. The definition should simply state the admissible width shape (each component is `(s, δ(c, m_S(d)))`, `c ≥ 1`) and let F-canonical prove that no other level-uniform span matches a finite `R(d,e)|_S`.

The same meta-prose is then echoed in the Claims Introduced table, F-canon-form row: "(its width is *not* stipulated — F-canonical Step 1 derives it must be an ordinal displacement `δ(c, m_S(d))`)". A table row should be a terse claim statement; the parenthetical restating the derivation is duplicate commentary, not claim content.

**Required**: In F-canon-form, state the width shape directly as part of the definition. Remove the "not pre-stipulated / F-canonical Step 1 derives…" justification from the definition body and from the table row, leaving the necessity argument to live once, in F-canonical Step 1.

### Issue 2: F-subspace Consequence restates its own formula in prose

**ASN-0070, F-subspace, Consequence (closing paragraph)**: "The `s_C`-component of the result picks out the content-subspace portion of coverage; the `s_L`-component picks out the link-subspace portion. An endset whose coverage straddles both I-subspaces (admissible by L4, ASN-0043) contributes to both result components; an endset confined to one I-subspace contributes only to that component."

**Problem**: The two displayed equalities `R(d,e)|_{s_C} = M(d)⁻¹(coverage(e) ∩ dom(C))` and the `s_L` analogue already carry this content exactly. The paragraph re-says the formula in words and adds nothing the equalities do not. This is the "two paragraphs say the same thing in different words" pattern — the straddle/confined observation is the visible consequence of intersecting coverage with `dom(C)` vs `dom(L)`.

**Required**: Delete the restatement, or compress to a single clause if the L4-admissibility pointer is worth keeping.

## OUT_OF_SCOPE

### Topic 1: Cross-document resolution relationship under shared homes
The first Open Question (relationship between `follow(ℓ, d, i)` and `follow(ℓ, d', i)` when coverage spans multiple homes) is correctly posed as future work; F-multidoc establishes that the present model forces no such relationship.

### Topic 2: Multi-server / BEBE traversal consistency
The second Open Question is replication territory, explicitly excluded by the scope note. Raising it as an open question (not a claim) is acceptable.

VERDICT: REVISE

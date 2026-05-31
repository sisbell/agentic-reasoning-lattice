# Review of ASN-0043

## REVISE

### Issue 1: The `Σ' ⊒ Σ` (StateExtension) discharge is duplicated verbatim across L9 and L11b
**ASN-0043, L9 and L11b, "*Discharge of `Σ' ⊒ Σ` (StateExtension)*"**:

L9: "`Σ'.C = Σ.C` and `Σ'.M = Σ.M` give equality — hence trivially monotone growth with agreement — on the shared domains of `C` and `M`; `Σ'.L = Σ.L ∪ {a ↦ ℓ}` with `a ∉ dom(Σ.L)` grows `L` only at the fresh address, so `dom(Σ.L) ⊆ dom(Σ'.L)` with `Σ'.L(b) = Σ.L(b)` for every `b ∈ dom(Σ.L)`. All three conjuncts hold, hence `Σ' ⊒ Σ`."

L11b: identical sentence, differing only in `{a ↦ ℓ}` vs `{a' ↦ Σ.L(a)}`.

**Problem**: This is the same derivation written twice (the "two paragraphs saying the same thing" accretion pattern). Both call sites are fresh-sibling extensions whose common construction — `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.L = Σ.L ∪ {fresh ↦ payload}` — is exactly FSP's construction. FSP already establishes the construction and discharges every state-local invariant plus L12/L12a, but it stops short of concluding `Σ' ⊒ Σ`, forcing each caller to re-derive StateExtension from facts FSP already has in hand (`a ∉ dom(Σ.L)` is FSP's h1; the `C`/`M` equalities are FSP's construction).
**Required**: Add `Σ' ⊒ Σ` to FSP's conclusion (it has all three conjuncts already), and replace both paragraphs with a one-line citation "`Σ' ⊒ Σ` by FSP."

### Issue 2: L8 "Consequences" expands a trivial inheritance into three formula-bullets that do no work
**ASN-0043, L8, "*Consequences*"**: "The defining biconditional is set-equality on coverage, so `same_type` inherits the three closure properties of `=` on sets immediately: *Reflexive.* ... — `coverage(...) = coverage(...)` by reflexivity of set equality. *Symmetric.* ... — by symmetry of set equality. *Transitive.* ... — by transitivity of set equality."

**Problem**: Each bullet restates an instance of `X = X` / symmetry / transitivity and justifies it with "by [property] of set equality." There is no case analysis and no step beyond the one-sentence lead-in. The three bullets do not advance the reasoning past the claim that already precedes them ("inherits the three closure properties of `=`").
**Required**: Condense to a single line, e.g. "Since the criterion is set equality on coverage, `same_type` inherits reflexivity, symmetry, and transitivity, hence is an equivalence relation partitioning `dom(Σ.L)` into type classes."

## OUT_OF_SCOPE

### Topic 1: Cross-store consistency under transclusion, compound-link well-formedness, allocation ordering of links vs. content
**Why out of scope**: These are raised in the ASN's own Open Questions and concern interactions (transclusion mechanics, operation ordering, compound-link constraints) that belong to later operation/arrangement ASNs, not to the static link-model state and its invariants. The ASN correctly defers rather than specifying them.

VERDICT: REVISE

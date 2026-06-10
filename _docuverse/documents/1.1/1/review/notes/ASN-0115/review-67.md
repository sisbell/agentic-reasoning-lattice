# Review of ASN-0115

The mathematics is sound. I verified the load-bearing proofs: the Confinement lemma (correct application of T5 with `p ≼ s`, `p ≼ reach(σ)`, `s ≤ t ≤ reach(σ)`); the `act` override's deep-case emptiness argument (proper-prefix contradiction via S8-depth + T1 case (ii)); R6's no-interior-hole/terminal-overrun result (canonical-start derivation from `act ≠ ∅` + D-SEQ★ frontier, with the deeper-than-`m_S` and `act = ∅` cases correctly scoped); and R7's repeatability (active-set agreement across the depth-compat/shallow-override/empty cases, with the comparability requirement correctly justified against divergent reachable branches). Boundaries — empty spec-set, empty active set, `S ∉ {s_C, s_L}`, depth mismatch, orphaning — are all covered. The findings below are precision and structure items, not correctness gaps.

## REVISE

### Issue 1: R8's distinctness annotation is asymmetric between its sub-cases

**ASN-0115, R8 (box and content sub-case)**: "If two active positions `v, v'` (within one spec or across specs) resolve to the same address … the operation performs no deduplication, so the shared content appears once per V-position."

**Problem**: The link sub-case explicitly scopes to "two **distinct** active link positions"; the box premise and the content sub-case omit `v ≠ v'`. The guarantee "once per V-position" and the whole transclusion framing presume distinct positions. The note itself shows that one position can be named by two overlapping specs ("a single bound V-position named by two overlapping specs … delivers the identical reference `⟨ref, a⟩` … twice"), so "two active positions" does **not** entail distinctness in this model — and in that degenerate `v = v'` case the same V-position yields two items, contradicting "once per V-position." The content side has the same exposure (two overlapping content specs naming one bound position).

**Required**: State `v ≠ v'` in R8's premise and content sub-case, matching the link sub-case, and let the `v = v'` (one position, multiple specs) phenomenon remain the separately-handled case it already is.

### Issue 2: R8 and R9 forward-reference R10 for a fact the `item` definition already establishes

**ASN-0115, R8 box**: "delivers the identical reference `⟨ref, a⟩` (R10) twice"
**ASN-0115, R9 box**: "a **link** item carries the address `a` itself (R10)"

**Problem**: Two claims in two earlier sections (R8, R9) both defer to the downstream R10 for the bare fact that a link position yields `⟨ref, a⟩` carrying the address. That fact is *defined upstream* by the `item` definition in "What a spec-set is" (`item(v, ρ, Σ) = ⟨ref, a⟩ if subspace(v) = s_L`). R10's genuine contribution is the *observability* claim (the boundary is visible as a change of item kind); its first half merely restates the `item` definition. Forward-citing R10 for the item form — when the definition is the actual antecedent and R10 is not yet established at these points — is exactly the "multiple paragraphs defer to the same downstream location" pattern, with the deferred content available earlier.

**Required**: Cite the `item` definition (or the definitions section) for the bare `⟨ref, a⟩`/address-carrying fact in R8 and R9; reserve the R10 citation for R10's observability claim. This removes the forward dependency and the latent duplication between R10's first half and `item`.

VERDICT: REVISE

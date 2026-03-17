# Review of ASN-0047

## REVISE

### Issue 1: J4 fork definition is ill-formed for empty-source case

**ASN-0047, Elementary transitions / J4**: "**Definition (Fork).** A *fork* of d_src to d_new is a composite transition Σ → Σ', with *precondition* d_src ∈ E_doc, consisting of: (i) K.δ creating d_new..., (ii) K.μ⁺ populating M'(d_new) with ran(M'(d_new)) ⊆ ran(M(d_src)), (iii) K.ρ recording provenance for each a ∈ ran(M'(d_new)), and no other elementary steps."

**Problem**: When dom(M(d_src)) = ∅, step (ii) is contradictory. K.μ⁺ requires dom(M'(d)) ⊃ dom(M(d)) (strict superset), so at least one new mapping must be added, giving ran(M'(d_new)) ≠ ∅. But the constraint ran(M'(d_new)) ⊆ ran(M(d_src)) = ∅ forces ran(M'(d_new)) = ∅. A function with non-empty domain has non-empty range — contradiction. The surrounding text handles this correctly ("K.μ⁺ and K.ρ are vacuous — the fork reduces to K.δ alone"), but the formal definition says the fork *consists of* all three steps, and K.μ⁺ cannot fire when the source is empty.

**Required**: Add `dom(M(d_src)) ≠ ∅` (or equivalently `M(d_src) ≠ ∅`) to the fork's precondition. The definition then applies cleanly to the non-empty case. The empty case is already handled: it is K.δ alone, structurally identical to ex nihilo creation and not a fork.

## OUT_OF_SCOPE

### Topic 1: Link arrangement invariants
**Why out of scope**: The ASN includes links in E_doc, asserting they "participate identically in transitions." But links and documents differ structurally — endset semantics, subspace layout (subspace 0 vs. ≥ 1). Whether S8a, S8-depth, and the text-subspace framing of S8 apply uniformly to link arrangements is a question for a future ASN on link structure. The ASN explicitly defers this: "belongs to a separate analysis."

### Topic 2: Provenance under transitive transclusion
**Why out of scope**: If document d₁ transcludes content a from d₂, which itself transcluded a from d₃, the provenance relation records (a, d₁), (a, d₂), and (a, d₃) independently as separate J1 events. Whether the system must support provenance *chain* queries (tracing the transclusion path) or only flat membership is a question about provenance semantics beyond the append-only recording defined here. Listed in the ASN's own open questions.

VERDICT: REVISE

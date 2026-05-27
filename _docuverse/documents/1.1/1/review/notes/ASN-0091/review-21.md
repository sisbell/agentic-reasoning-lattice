# Review of ASN-0091

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Cross-document transclusion under cut-induced span splitting
**Why out of scope**: The "Open Questions" section explicitly identifies this as future territory. The ASN establishes RE-trans (joint reference preservation across fragmentation) which is sufficient for this ASN's scope; finer-grained guarantees about how the split pieces relate as a *single* transclusion relationship belong in a follow-on ASN.

### Topic 2: Link-subspace REARRANGE semantics
**Why out of scope**: The "Open Questions" section flags this. CS3 of ASN-0084 fixes the cut subspace at s_C; a link-subspace rearrangement operation would be a distinct operation with its own preconditions and invariants. CL-OWN/CL-UNIQ preservation arguments here only need the s_C restriction.

### Topic 3: Observational equivalence at discoverability level (vs arrangement equality)
**Why out of scope**: Open question listed; would require a coarser equivalence relation than the bijection-class characterisation in this ASN. Belongs to a future ASN on link-layer semantics.

### Topic 4: Upper bound on run-decomposition cardinality increase per invocation
**Why out of scope**: Open question listed; the ASN establishes the existential RE-frag/coal/eq trichotomy. Tight bounds (e.g., O(n) in cut count) would be a quantitative refinement appropriate for a follow-on.

### Topic 5: Decomposition of arbitrary bijections of dom(M(d)) into cut-sequence rearrangements
**Why out of scope**: Open question listed; this is a reachability/expressiveness result about REARRANGE_K, distinct from the soundness/preservation results established here.

### Topic 6: Mixed sequences interleaving REARRANGE with K.α/K.λ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.δ/K.σ/K.ρ
**Why out of scope**: The multi-step composition section explicitly restricts to pure REARRANGE sub-sequences. Mixed-sequence treatment belongs to a cross-operation integration ASN, with each operation kind governed by its own ASN-0098 lemma (LP-Comp's case analysis catalogues them).

VERDICT: CONVERGED

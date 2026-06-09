# Review of ASN-0120

I checked the load-bearing derivations against the foundations: the subspace-confinement step (ordinal displacement + T5 → `t₁ = s_C`), the exact `#E = 2` content-address argument and its two uses (creation-state equality ML1/ML2 and stability under later K.α in ML8), the faithful-recovery equality `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)` including the merged-span case, and the ML9 weakest-precondition composition (LP12 + Fact (a) subspace disjointness + Fact (b) including the `d' = d` home boundary). Each holds. Edge cases the rubric flags — partial spans, empty type resolution, self-homed links, the home-document boundary in the wp — are all addressed or explicitly deferred to Open Questions.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Endsets referencing the link subspace (link-to-link)
**Why out of scope**: The ASN restricts spec-sets to content-subspace spans and defers links whose endsets point at other links to an Open Question. This is new territory (resolution through the link subspace would need a separate confinement argument), correctly deferred, not an error here.

### Topic 2: Empty from/to resolution semantics
**Why out of scope**: ML6 fixes the type-endset precondition (`ρ(R₃,Σ) ≠ ∅`); the meaning of an empty non-type endset is properly left to an Open Question rather than forced into this ASN.

The confinement re-derivation (rather than leaning on ASN-0058 C0/C0a, which only covers well-formed references) is the correct move given ρ admits partial spans, and the ASN flags it. Implementation material is consistently quarantined in marked notes with the abstract claim stated separately — no drift.

VERDICT: CONVERGED

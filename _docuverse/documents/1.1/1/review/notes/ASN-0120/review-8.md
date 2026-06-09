# Review of ASN-0120

I read the ASN, checked each of ML0–ML10 against its cited foundations, and verified the load-bearing arguments (subspace confinement, the `#E = 2` exactness, the ML9 weakest-precondition derivation including the `d' = d` boundary, and stability of endset content-coverage under later `K.α`).

## REVISE

(none)

The proofs hold up under scrutiny:

- **Confinement step** (ρ ⊆ dom(C)). The ordinal-displacement requirement `ℓ_j = δ(n_j, m)` is correctly shown to pin `t₁ = s_C` for every `t ∈ ⟦σ_j⟧` via T5 — the half-open endpoint `t ≤ u_j ⊕ ℓ_j` is within T5's `a ≤ b ≤ c` range, and `#p = m−1 ≥ 1` is justified. The deliberate divergence from ASN-0058's `resolve` (partial spans, confinement re-derived rather than borrowed from C0/C0a) is flagged and discharged.
- **`#E = 2` exactness** (ML1/ML2/ML8). Derived from chain membership + first-emission `#E = 2` + `inc(·,0)` length preservation, not merely C1b's `#E ≥ 2`. The dependence is used correctly in both the creation-state equality and its stability under future allocation.
- **ML9 wp.** Fact (a) (coverage/store trace = ρ, with the link-half emptiness shown by the `s_C ≠ s_L` prefix contradiction) and Fact (b) (range agreement, including the `d' = d` boundary where the added link address is shown inert) are both explicit. The `enabled` conjunct and the deliberate omission of source-document allocation from `enabled` are reasoned, not hand-waved.

Boundary cases are covered: empty type resolution (rejected by ML6), partial/all-deleted source spans (ρ filters to active positions; from/to may resolve empty), home-as-own-discovery-source (`d' = d`), and `V_{s_L}(d)` empty vs. non-empty for the `K.μ⁺_L` position. The worked example checks ML0/ML1/ML2/ML9 concretely. No non-foundation cross-references appear in the body. Implementation notes are marked as such and the abstract claim is stated separately each time.

## OUT_OF_SCOPE

### Topic 1: Endsets that reference the link subspace (link-to-link)
**Why out of scope**: The ASN explicitly defers this (Open Question 3) and the spec-set definition restricts arguments to the content subspace. A link whose endset points at another link is new territory requiring a different confinement argument, not an error here.

### Topic 2: Empty non-type endset semantics, and inter-run ordering within an endset
**Why out of scope**: Both are correctly carried as Open Questions, not as unstated claims. They concern meaning the abstract operation need not fix to record connection faithfully.

VERDICT: CONVERGED

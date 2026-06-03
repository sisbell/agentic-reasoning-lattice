# Review of ASN-0068

I checked the proofs of CV-MAX (existence and uniqueness), the precondition necessity argument CV-IN-N, the degenerate-case cluster (CV-LINK-DEGEN, CV-LINK-SELF, CV-SELF), and all five worked examples against the foundation claims. The reasoning is sound and the cited material (ASN-0034/0036/0047/0053/0058) is all from the foundation set, so the citations are permitted.

Specific checks that pass:
- **CV-IN-N**: the divergence argument is correct — for any `t = [S,1,...,1,j]` with `j ≥ s_m`, divergence with `reach(σ)` occurs at position `k < m_σ` regardless of `j`, so `t < reach(σ)` is unbounded in `j`. Verified.
- **CV-MAX uniqueness, Case δ > 0**: `v²_a − 1 = v¹_a + (δ−1)` with `0 ≤ δ−1 < n¹` correctly yields a left-extension of `R²`, contradicting left-maximality. The left-region run reconstruction via M-aux + predecessor inverse is rigorous, not hand-waved.
- **Edge cases**: empty arrangement (`V_S = ∅ ⟹ R = ⟨⟩ ⟹` empty via CV-EMPTY), self-comparison (CV-SELF `D ∪ X`), link subspace (CL-OWN/CL-UNIQ degeneracy), differing depths (Example 4), and restriction-induced fragmentation (Example 5) are all handled and the example arithmetic checks out.
- **CV-IN "equivalently"**: `actionPoint(width)=m_σ ⟺ width=δ(n,m_σ)` is sound because the level-uniform clause (`#width=m_σ`) is conjoined in the same precondition.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace comparison
CV-IN requires a single common subspace `S`. Comparing `s_C` of one document against `s_L` of another is excluded by precondition rather than proven empty (it would be, by L14 store disjointness). This is an appropriate scoping decision, not a defect — a future ASN could relax the precondition and discharge the emptiness explicitly.

### Topic 2: Concurrency and replication invariants
The Open Questions correctly defer mid-comparison arrangement mutation, replica equivalence, and multi-document correspondence composition. These are genuinely new territory, not gaps in this note.

Anti-bloat note: I looked specifically for forward-reference accretion, use-site inventories, and "deferred to X" chains. The worked-example interpretive closers (Examples 4, 5) and the CV-RO transition-vocabulary enumeration are heavier than strictly necessary, but they fall under protected categories — concrete examples and statements of what the operation does/does not do — so I am not flagging them. The necessity claim CV-IN-N follows the established T10a-N genre and advances a substantive structural fact (unbounded V-extent), so it is content, not meta-prose.

VERDICT: CONVERGED

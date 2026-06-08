# Review of ASN-0110

I read this as a specification of a pure query operation (RETRIEVEENDSETS): it fixes what state is read (`Σ.L` and the region alone), the touching relation, the role-separated return shape, and the operation's invariants (determinism, monotonicity, survivability, additivity, anonymity). I checked each proof, the boundary cases, and the worked instance.

## Findings

I could not find a correctness defect, a skipped case, or an unproven multi-step claim. Specifically:

- **Boundaries are covered.** Empty region (RE-zero → `⟨∅,…,∅⟩` of length `N_max`, not `⟨⟩`), empty store (`N_max = 0`, RE-arity/RE-conform), empty endset (`coverage(∅)=∅`, never touches), boundary contact (half-open denotation, RE-overlap), empty interior slot (reported in position), higher-arity links (RE-conform's concrete RE-complete obligation on `j > 3`), and the empty-store Gregory divergence (`⟨⟩` vs `⟨∅,∅,∅⟩`) are each addressed explicitly and honestly.
- **The touch/return asymmetry is correct and load-bearing.** Touching is keyed on coverage (RE-touch), the returned family is keyed on endset *value* (RE-result), so coverage-equal/representation-distinct endsets both appear — correctly contrasted with L8's coverage-keyed `same_type`. RE-full's "whole, not clipped" choice is justified structurally (L12) and semantically.
- **Decidability/termination discharged.** RE-decide reduces to finite double-disjunction of T2 comparisons over finite `dom(Σ.L)` (L-fin), finite arities, finite endsets, finite `I ∈ 𝒫_fin(T)`. RE-Vside's `image ⊆ ran(Σ.M(d))` finiteness (S8-fin) holds for arbitrary `R`.
- **Proofs verified.** RE-mono (LP13 + LP3★, genuinely multi-step), RE-wp (case split on fresh vs prior link, freshness from the sub-allocator lemmas, gated on allocated value alone), RE-add, RE-empty, RE-anon (L11b construction, lengths match), and the worked instance (the `F₁` touching/non-touching span split and the cross-role reuse exercise RE-full and RE-role exactly) all check out.
- **Anonymity bound is sound.** Each `|Eᵢ|` ≤ distinct slot-`i` links, so `max_i |Eᵢ|` lower-bounds distinct contributing links; the exact count is undetermined (RE-anon). The RE-reveal pairing-recovery claim is carefully hedged as state-level, conditioned on out-of-band knowledge, and deferred to OQ3.
- **No illicit cross-references.** All citations are to foundation ASNs (0034, 0036, 0043, 0047, 0086, 0093, 0098, 0099); the region domain is explicitly `𝒫_fin(T)`, so the "content-region" framing is descriptive shorthand, not an under-specified precondition.

The ASN defines state-reading discipline, an operation, and its abstract guarantees at a level any alternative implementation must satisfy. It has not drifted into implementation mechanics; implementation evidence is used to verify conformance, as expected.

## OUT_OF_SCOPE

### Topic 1: V-space presentation/clipping of returned endsets
**Why out of scope**: How an endset's I-coverage is projected back into a querying document's V-coordinates (and the resulting silent clipping of unmapped I-addresses) is a distinct, lossy presentation contract. The ASN correctly returns endsets whole (RE-full) and defers the presentation contract to its first Open Question.

### Topic 2: Sub-region/super-region invariants beyond additive union; tighter distinct-link bounds; deletion-history indistinguishability
**Why out of scope**: These are the ASN's own deferred Open Questions, each genuinely new territory rather than a gap in the present claims.

VERDICT: CONVERGED

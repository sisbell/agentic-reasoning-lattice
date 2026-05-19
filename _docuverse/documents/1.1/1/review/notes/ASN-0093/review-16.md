# Review of ASN-0093

## Strengths Verified

The dependency ordering for chain lemmas is explicit and load-bearing — proving ChainElementT4Validity → ChainUniformLength → ChainEnumerationInjectivity → ChainUniformZeroCount → DisjointSubAllocatorChains → ChainPrefixExtension prevents nested-induction circularity at each step.

The simultaneous-induction framing for transition-indexed properties (M0–M1, C0–C2, C-fin, L0–L14, L-fin, ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness) is sound. Each step cites only IH at Σ, never the conclusion at Σ' being derived.

The worked example exercises both first-emit and subsequent-emit branches for K.α/K.λ across three documents, verifies Cross-document disjointness in both Case A (prefix-comparable, Step 5) and Case B at equality (Step 9, real example) and B.i at strict inequality (Step 9, hypothetical d_alt') and B.ii (Step 9). FirstEmission's structural form is verified by component inspection.

The base case at Σ₀ holds: all quantifier-restricted invariants are vacuous over empty stores/dom(M); L14/L-fin/C-fin trivially hold.

## Spot-checks on subtle points

**Origin preservation under inc(·, 0):** For ℓ = inc(ℓ_prev, 0), TA5-SigValid pins sig(ℓ_prev) = #ℓ_prev = #d + 3 (by ChainUniformLength). The increment modifies position #d + 3 only; the third zero at position #d + 1 and earlier prefix are preserved by TA5(b), so origin(ℓ) = origin(ℓ_prev) = d. ✓

**Cross-document Case A at #d_1 + 1 = #d_2:** When d_2 has length exactly one more than d_1, d_2[#d_1 + 1] = d_2[#d_2] ≠ 0 by T4's positive-endpoint clause on d_2 (rather than by the zero-count argument). The proof's M0-at-both argument still applies because zeros(d_2) = 2 forces no additional zeros, but the positive-endpoint route also closes this boundary. ✓

**ChainPrefixExtension step soundness:** TA5(b) at k=0 preserves positions 1..#t_n except at sig(t_n) = #d + 3. Since #b_C(d) = #d + 2 < #d + 3, the anchor sits entirely in the preserved range. ✓

**FirstEmissionFreshness against dom(L):** The proof correctly avoids circularity by using FirstEmission's structural form (rather than L0 at Σ') for E(a)₁ = s_C, and L0 at Σ for E(ℓ)₁ = s_L. T7 closes via SC-NEQ. ✓

**SubspaceConventionAxiom load-bearing in L1c:** The L1c chain step inc(b_C(d), 0) = b_L(d) requires s_L = s_C + 1 (since sig at position #d + 2 advances value s_C to value s_C + 1). The axiom pins s_C = 1, s_L = 2, satisfying this. ✓

**ChainMembershipForOrigin contiguous-prefix at K.α subsequent-emit:** ChainEnumerationInjectivity gives strict monotonicity, so the lex-order max of {t_1, ..., t_{m_d}} is t_{m_d}, matching a_prev. ChainDiscipline closure gives a = t_{m_d + 1}. ✓

**K.σ cross-store freshness automatic:** d has zeros = 2 by precondition; C1/L1 force zeros = 3 for content/link addresses; anchors b_C(d')/b_L(d') have zeros = 3. So d collides with none. ✓

## Possible Concerns Checked

- "Symmetric to K.α (content↔link)" annotations in the matrix point to lemma proofs above that contain explicit link branches (FirstEmissionFreshness has "Link case against dom(L)" and "Link case against dom(C)" explicitly proved). These are pointer shorthand, not proof-by-similarity.

- The Definition's "T10a-discipline-satisfying chain" terminology is deliberately weaker than T10a's full discipline; the Caveat paragraph addresses this and proofs cite only the structural fragment.

- Cross-document disjointness uses M0 + T4 + T10 + Prefix directly rather than T10a.5, because the substrate's K.σ admits document addresses without requiring T10a allocator-tree embedding. The lemma's proof handles this without circularity.

- The substrate deliberately weakens S7d (no T10a allocation discipline on documents); higher-layer ASNs are expected to tighten K.σ's precondition.

- Open Questions properly defers concurrency, link withdrawal, higher-arity discipline, and document-address discipline.

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED

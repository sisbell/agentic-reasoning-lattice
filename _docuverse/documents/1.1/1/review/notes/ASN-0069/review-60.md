# Review of ASN-0069

I worked through the proofs claim by claim, with particular attention to the operation's preconditions, the boundary cases (empty source, link-only source, fork chains, sibling forks), and the frame/coupling discharges in the composite verification.

## Findings

**Identity (V1, V2).** The Document-level and parent-equality inductions on `A_v(d_src)`'s emission count correctly combine K.δ-ID.zeros/parent preservation with P1-supplied membership at each step; the base/step split for both the first-fork (`k=1`) and subsequent-fork (`k=0`) sub-cases is complete. The `d_src ≼ d_new` argument with its nested length induction (`#· = #d_src + 1`) is genuinely distinct from the outer prefix induction and is carried out, not waved.

**Content & arrangement (V3–V6, V8).** V4/V4b are honestly flagged as design commitments strengthening J4's `φ`-up-to-bijection; the K.μ⁺-amendment argument correctly yields only `⊆ s_C`, with full domain equality acknowledged as committed, not derived. V6's CL-OWN contradiction is sound. The non-injectivity of `M(d_op)` (S5 sharing) is correctly handled by counting `n = |ran|`, not `|dom|`, in both V0 and the K.ρ verification.

**Frame discipline (V5a, V8b).** The per-elementary-transition enumeration covers every member of ASN-0047's vocabulary including K.μ~ via decomposition; the two corollaries are instantiated with explicit operand assignments (no free label-swap). V8b's non-monotonicity and the K.μ⁺_L neutrality argument (`F ⊆ s_C`, so `v ≠ v_ℓ`) are correct.

**Composite verification.** Both the K.δ+K.μ⁺+K.ρ×n shape and the K.δ-alone empty shape discharge ValidComposite★ (intra-composite preconditions and J0/J1★/J1'★ couplings, the latter vacuously in the empty case). Freshness in both K.δ sub-cases is established against all three collision sources (at-most-once spawn, within-allocator injectivity, cross-allocator disjointness). V12(d)'s reliance on P4★ as a composite-boundary property correctly justifies that Σ is a boundary.

**Edge cases.** Empty source (V7), link-only source (third vignette), deepest-deletion (`n'=0` → subsequent empty fork), fork-of-fork (V11), and sibling forks (V10) are all covered. The worked example checks V1–V9 against a concrete depth-2 arrangement.

**Cross-ASN references.** All citations are to foundation ASNs (34, 36, 40, 47); no non-foundation references appear in the body.

I found no hand-waved cases, no proof-by-checkmark, and no unaddressed invariant conjunct. The ASN stays at the abstract state-transition level throughout, with implementation observations correctly quarantined as non-normative.

VERDICT: CONVERGED

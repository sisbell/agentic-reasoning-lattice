# Review of ASN-0115

I checked the substrate dependencies (all genuine foundations — ASN-0034/0036/0043/0045/0047/0053/0058/0082/0086/0093 — so no improper cross-ASN references), and verified the load-bearing proofs. The Confinement lemma (T5 application) is correct. R6's no-interior-hole argument is rigorous and honestly bounded to the bindable slice. R7's repeatability proof correctly handles the non-trivial point that `act`'s depth-compatibility branch reads whole-subspace state beyond the equated restriction, and correctly insists on comparability (`Σ →* Σ'`) rather than mere common-ancestor reachability. R8's subspace-sharing dispatch (S3★ + SD + S3★-aux) and link-vacuity argument (CL-OWN + CL-UNIQ) are sound. Worked instances and the R11 wp are present and check out. I found one rigor gap.

## REVISE

### Issue 1: The override's safety justification is an unproven derived claim
**ASN-0115, §"What a spec-set is, and what delivery is"** (the `act` rationale paragraph): "A spec stale against a re-pinned subspace should deliver nothing rather than vacuum its re-pinned content; so the override only *bites* when the start has gone too shallow (`#s < m_S(d)`), forcing empty lest the intersection capture deeper content the citation never named."

**Problem**: "the override only bites when `#s < m_S(d)`" is a checkable behavioral assertion — it is the *safety* argument for force-empty (it claims the override never discards content named at the current depth, only stale-shallow citations). But it is stated as obvious when it requires a multi-step argument: from a bound `v ∈ dom(M(d)) ∩ ⟦σ⟧`, Confinement forces `v₁ = s₁` so `v ∈ V_S(d)` with `#v = m_S(d)` (S8-depth); Confinement's prefix `p = [s₁,…,s_{#s−1}] ≼ v` forces `#v ≥ #s−1`, and the `#v = #s−1` case is excluded because then `v` is a proper prefix of `s`, hence `v < s`, contradicting `v ∈ ⟦σ⟧`; so `#v ≥ #s`, and with `#s ≠ m_S(d)` this gives `#s < m_S(d)`. The claim is *true* (I verified it), but as written it is exactly the "claim derived in one sentence that requires a multi-step argument" the standards reject — and it sits in rationale prose the anti-bloat pass is meant to scrutinize. The neighbouring "harmless rather than special-cased" paragraph shows its steps (S3★-aux, Confinement); this sentence does not, an asymmetry worth resolving.

**Required**: Either attach the one-clause justification (e.g., "since `#s > m_S(d)` forces the geometric intersection empty: any bound `v ∈ ⟦σ⟧` would lie in `V_S(d)` at depth `m_S(d)` (S8-depth) yet agree with `s` on its first `#s−1` components (Confinement), which is impossible when `#s > m_S(d)`") or soften the assertion to remove the unsupported behavioral over-claim. The anti-bloat-compatible fix is the brief parenthetical, not a new paragraph.

## OUT_OF_SCOPE

The five Open Questions (inline provenance, outright-failure conditions, dangling references under relaxed S3★, channel faithfulness, subspace-straddling spans) correctly defer genuine future territory and are consistent with the in-body scoping (single boundary-crossing spans explicitly excluded; channel correctness disclaimed as a frame limit on R2). No topic is mis-scoped, and the ASN defines none of the harness-listed out-of-scope operations.

VERDICT: REVISE

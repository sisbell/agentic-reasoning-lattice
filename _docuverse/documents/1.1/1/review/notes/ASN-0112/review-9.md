# Review of ASN-0112

I reviewed every claim (V0–V18), the well-definedness arguments, the worked examples, and the wp analysis against the foundation contracts.

## Verification performed

**V2 well-definedness and coverage.** Checked both depth regimes. For `#origin_d ≤ #reach_d`, D1's preconditions (`origin_d < reach_d`, `divergence ≤ #origin_d`, `#origin_d ≤ #reach_d`) are all met, giving `r⋆ = reach_d`. For `#origin_d > #reach_d`, D0's `#a > #b → a ⊕ (b ⊖ a) ≠ b` is correctly invoked and the actual reach computed directly. The `divergence ≤ #origin_d` step is sound in both the equal-length (S8-depth, case (i)) and cross-subspace (`k = 1`) cases. Coverage is established without assuming level-uniformity, as claimed.

**V3 tightness.** The inline proof that `max O(d).0` is a strictly smaller upper bound than `reach_d`, and that `reach_d` is the least *same-depth* strict upper bound, is correct (T1 case (i)/(ii) applied properly). The "same-depth" qualifier is necessary and correctly stated — the unqualified claim would be false, and the ASN flags this explicitly.

**V5/V6 exact-cover vs bounding-box dichotomy.** Single-subspace exactness routes through D-SEQ★/D-CTG★/D-MIN★; cross-subspace strict containment is forced by `s_C < s_L`. The depth subtlety (`m_C ≠ m_L`) is handled honestly, with coverage preserved and only reach-equality/tightness gated on the endpoint condition.

**Boundary cases.** Empty document (V11, distinguished `⟨⟩`, not a zero-width span — correctly excluded via TA6/T12), single-element occupancy (covered by the general argument), link-only documents (single-subspace at `s_L`), full content clearance with surviving links (V18 origin migration, the one transition V8 excludes). All accounted for.

**Worked examples.** Recomputed both the standard report (`1.1 for 1.2`) and the depth-divergent variant (`origin=[1,1,1]`, `reach_d=[2,2]`, `extent=[1,2,0]`, `r⋆=[2,2,0]`). Both check out, including the proper-prefix `reach_d < r⋆` and membership of `[2,1]` in `⟦σ_d⟧`.

**wp analysis.** `wp(·, Exact) = single-subspace occupancy` is genuinely both-directions (V5 forward, V6 converse, exhaustive over 0/1/2 subspaces). The companion reach-equality wp factors along the orthogonal endpoint axis. Non-trivial, correctly derived.

**Foundation usage.** S3★ (over S3) is correctly chosen to admit link V-positions; V14 splits permanence by subspace (S0/P0 for content, L12 for links) — the split is necessary and right. No foundation notation is reinvented; "endpoint-level-compatible" is carefully distinguished from S6's level-uniformity. All cross-references are to foundation ASNs (0034, 0036, 0043, 0047, 0053).

No scope violations: insertion/deletion appear only as characterizations of how the query value responds to state (V9/V10/V18), not as operation definitions; version semantics are deferred to Open Questions.

## REVISE

None.

## OUT_OF_SCOPE

None improperly included.

VERDICT: CONVERGED

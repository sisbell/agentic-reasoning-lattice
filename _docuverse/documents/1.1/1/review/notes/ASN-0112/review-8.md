# Review of ASN-0112

I worked the proofs and the arithmetic of every worked case rather than trusting the prose. Findings below.

## Verification performed

**V2 (covering + well-formedness).** Checked the D0 applicability in both depth regimes. Single-subspace: S8-depth forces `#origin_d = #reach_d`, equal-length distinct tumblers diverge within shared length (case (ii) of Divergence is impossible), so `k ≤ #origin_d`. Cross-subspace: divergence at position 1. D0 then discharges `Pos(extent_d)` and `actionPoint = k ≤ #origin_d` without any level-uniformity assumption. Coverage split (D1 closes round-trip when `#origin_d ≤ #reach_d`; direct TumblerAdd computation of `r⋆` as zero-padded `reach_d` when `#origin_d > #reach_d`) is sound — `r⋆ ≥ reach_d > max O(d)` holds in both. Correct.

**V3 (tightness).** The restriction to "least *same-depth* upper bound" is the right one — the proof correctly excludes the smaller zero-extension successor `max O(d).0` as breaking level-uniformity, and the component-wise case split (`j = m` vs `j < m`) is complete. This is a genuine correction of the naive "least reach over all of T" claim that would be false.

**Arithmetic of worked cases.** Re-derived each: eleven chars → `[1,1] for [0,11]` ✓; three-content+one-link → `[1,1] for [1,2]` with `r⋆=[2,2]` ✓; depth-divergent variant `m_C=3,m_L=2` → `extent=[1,2,0]`, `r⋆=[2,2,0]`, `reach_d=[2,2]` a proper prefix (so `reach(σ_d)≠reach_d` but coverage holds) ✓. All confirm the claims they illustrate.

**Edge cases.** Empty (V11, ⟨⟩ with TA6 sentinel argument distinguishing from a forbidden zero-width span), singleton, link-only (V5 link instance via D-SEQ★ at `s_L`), full content clearance with surviving links (V18 origin migration via D-MIN★ at `s_L`), and the m_C≠m_L divergence are each handled. V10/V18's `extent_after = shift(extent_before, n)` checks out in the dense regime, and the content-maximal ⟺ link-empty ⟺ single-subspace equivalence is correctly used.

**Other obligations.** Concrete examples present (two). Non-trivial wp analysis present (`wp(·, Exact) = single-subspace occupancy`, derived through V5/V6/V7 with exhaustive 0/1/2-subspace case split). Pure query, so state-invariant preservation is trivial and the burden correctly rests on the returned value, which is covered exhaustively. No cross-ASN references outside the foundation set (0034/0036/0043/0047/0053); ASN-0113 appears only in the scope exclusion note. No invented notation duplicating a foundation concept — "endpoint-level-compatible" is a new, clearly-named distinction explicitly tied to S6, not a reinvention.

## OUT_OF_SCOPE

None to flag — the ASN correctly defers per-subspace exact reporting (V7, Open Questions) and authorization (precondition section notes the BERT gate as a deployment concern outside the value semantics) without defining claims for them.

No REVISE items: every multi-case proof shows its cases, boundaries are covered, and the careful level-uniform/endpoint-compatible distinction is maintained consistently throughout.

VERDICT: CONVERGED

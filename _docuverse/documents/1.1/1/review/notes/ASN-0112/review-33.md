# Review of ASN-0112

The note is rigorous on its core obligations: V0–V2's well-formedness and covering proofs correctly avoid assuming level-uniformity, handle both the single-subspace (equidepth) and cross-subspace (`k = 1`) cases via D0/D1, and the worked example plus the depth-divergent variant check out arithmetically (`2.1 for 0.1`, `1.1 for 1.2`, `[1,2,0]`/`[2,2,0]` all verify). The wp analysis is non-trivial and the case splits are exhaustive by S3★-aux. The cross-ASN references are all to foundation ASNs. My findings are confined to the anti-bloat patterns this note is flagged for.

## REVISE

### Issue 1: Meta-justification of foundation-fact selection in V8
**ASN-0112, "The origin is permanent..." (V8 parenthetical)**: "S8-depth alone is per-state and would not supply this cross-state constancy."
**Problem**: The first parenthetical sentence is load-bearing — it establishes via ASN-0047's `m_S(d)` re-pinning discipline that `m_C` is constant within a content-present regime, which is what pins the literal tumbler `[s_C,1,…,1]` across states. But the closing sentence explains *why a different foundation fact (S8-depth) is insufficient* rather than advancing V8. This is the meta-prose pattern (justifying which fact is needed instead of stating what V8 says); a reader following V8 must skip it.
**Required**: Delete the "S8-depth alone..." sentence. The re-pinning sentence alone discharges the depth-constancy obligation.

### Issue 2: Orthogonality note plus implementation digression embedded in the V6 structural discussion
**ASN-0112, "Exact cover within a subspace; a bounding box across subspaces" (paragraph following the V6 golden case)**: "The bounding-box reading of V6 holds independent of the endpoint depth relation (V2). The implementation in fact realizes only `m_C = m_L`: content and link V-positions are placed at the same depth — both depth 2 ... (consultation Q2: `findvsatoappend`, `findnextlinkvsa`, and `setlinkvsas` all emit depth-2 V-addresses), so the cross-subspace endpoints are level-compatible and `reach(σ_d) = reach_d` exactly."
**Problem**: V6's claim is purely structural ("bounding box, not exact cover"). This paragraph interrupts it with (a) a cross-claim orthogonality note about V2 and (b) an implementation digression naming specific functions, neither of which advances V6. The substantive content — that the reach is tight in practice because `m_C = m_L` — belongs with the V2 reach biconditional, not in the V5/V6 exact-vs-enclosure discussion. A reader following the structural argument must skip past it.
**Required**: Move the `m_C = m_L` / reach-tightness observation to the V2 reach-biconditional discussion (or the implementation-remark section), and drop the standalone "holds independent of the endpoint depth relation (V2)" sentence, whose orthogonality content is already implicit in V2 and V6 being separate claims.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-to-count invariant (Open Question 1)
**Why out of scope**: Per-subspace extent reporting is RETRIEVEDOCVSPANSET / ASN-0113 territory; posing it as an open question here is appropriate and not a defect in this ASN.

VERDICT: REVISE

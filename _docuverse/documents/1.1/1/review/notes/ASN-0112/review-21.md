# Review of ASN-0112

I checked the operation's value semantics, every introduced claim (V0–V18), the boundary cases, the foundation citations, and the depth/subspace case analysis. The note is a pure query specification that stays abstract and uses foundations correctly.

## REVISE

None.

The areas I scrutinized most closely all hold:

- **V2 coverage** is proved in both depth-relation cases. The `#origin_d > #reach_d` branch is computed directly via TumblerAdd (k=1): `r⋆` equals `reach_d` zero-padded, so `reach_d` is a proper prefix of `r⋆` and `max O(d) < reach_d < r⋆`. Coverage survives without assuming level-uniformity. The reach biconditional (`reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`) is derived inline from D1 (⟸) and D0's `#a > #b → a⊕(b⊖a) ≠ b` (⟹), not asserted.
- **V3 tightness** correctly establishes `sig(w) = #w` from S8a + TA5-SIG (not TA5-SigValid, which would require T4-validity V-positions don't have), then cites TA5's "smallest same-length tumbler strictly greater" property. The same-depth qualifier is load-bearing and stated, and the leap from witness `reach_d` to `σ_d` is gated on `reach(σ_d) = reach_d`.
- The **tightness-domain (`m_C ≤ m_L`) vs level-uniformity (`m_C ≥ m_L`)** distinction — the subject of the last revision — is correct and the disambiguation earns its place rather than being conflation-warning bloat.
- **Boundary cases** are covered: empty (`⟨⟩` via V11, with the zero return read as sentinel not address per TA6), single position, link-only single-subspace, cross-subspace bounding box, and a depth-divergent (`m_C=3>m_L=2`) variant. The worked example checks out (`extent = [2,2]⊖[1,1] = [1,2]`).
- **V8/V18** properly bound origin permanence at the content-occupancy toggle; **V14** correctly splits permanence by subspace (S0/P0 for content, L12 for links) and restricts to occupied positions, excluding the V6 inter-subspace void.
- The **wp(Exact)** analysis is non-trivial and the exhaustiveness (zero/one/two subspaces) is sound.

No improper non-foundation cross-references in the ASN body; Q-number citations are implementation evidence, not ASN references. No forward-reference accretion patterns (no "see below," no circular-dependency justifications, no downstream-consumer inventories in definitions).

VERDICT: CONVERGED

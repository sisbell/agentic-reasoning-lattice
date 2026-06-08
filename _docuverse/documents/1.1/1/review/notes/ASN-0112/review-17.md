# Review of ASN-0112

The mathematics is sound. I checked the load-bearing arguments — V2 coverage (both depth cases via D0/D1), V3 same-depth tightness via TA5/`inc(·,0)`, the cross-subspace bounding box (V6), insertion/deletion monotonicity (V10/V18), and the empty-result handling (V0/V11/V17). The derivations hold, edge cases (empty document, single subspace, content clearance with surviving links, m_C ≠ m_L endpoints) are covered, and there is a concrete worked report plus a non-trivial wp analysis. My findings are about accreted meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: V3 narrates the argument instead of making it
**ASN-0112, "The span is the tightest covering bound among same-depth reaches"**: "We are deliberately careful about the qualifier, because without it the claim is false. ... We do not redevelop the arithmetic; the foundation supplies it." and "This is the most the reach argument proves: it fixes `reach_d` against `max O(d)` alone and says nothing about `#origin_d`."
**Problem**: The *qualifier* (least upper bound among same-depth tumblers, not globally — `w.0` is smaller but deeper) is genuine, load-bearing precision and must stay. But these three sentences are reviser narration *about* the argument — defensive justification of the care taken, a disclaimer that the arithmetic is not redeveloped, and a meta-statement of what the argument does not prove. A precise reader must skip past them to reach the TA5 content that actually settles tightness.
**Required**: Keep the same-depth/level-uniform distinction and the TA5 derivation; delete the process narration. State the qualifier as a condition, not as an account of the reviser's diligence.

### Issue 2: the reach biconditional is established in V2 and re-derived in V6
**ASN-0112, V2** establishes: "the **reach biconditional** `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d` (D1 closes the round-trip when `#origin_d ≤ #reach_d`; D0 makes it fail when `#origin_d > #reach_d`)." **V6's "subtlety of depth" paragraph** then re-derives the same fact: "the V2 reach biconditional settles it directly: `reach(σ_d) = reach_d` exactly when `#origin_d ≤ #reach_d` ... while when `m_C > m_L` the actual reach `r⋆` strictly exceeds `reach_d` (it is `reach_d` zero-padded to depth `m_C`)."
**Problem**: The "zero-padded to depth `m_C`" mechanism is precisely V2's second covering case, restated in different words one section later. Two paragraphs say the same thing.
**Required**: In V6, apply the V2 biconditional by citation (it covers `m_C ≠ m_L` already) rather than re-deriving the padding mechanism. Reduce the paragraph to the one new fact V6 needs — that the realized case is `m_C = m_L` (Q2), so the endpoints are level-compatible and `reach(σ_d) = reach_d` exactly.

### Issue 3: the V6 claims-table row re-litigates the level relations
**ASN-0112, Claims table, V6**: "the endpoints are level-compatible iff the subspaces share a depth (`m_C = m_L`...), while the span is level-uniform under the weaker `m_C ≥ m_L`; coverage holds in all cases (even `m_C ≠ m_L`)."
**Problem**: The row now restates the level-compatible / level-uniform / coverage three-way distinction already carried by V2 and V3. A claims-table row should state the claim, not re-run the qualifier analysis that the body section owns.
**Required**: Trim the row to V6's actual claim (`O(d) ⊊ ⟦σ_d⟧` strictly when occupied positions span two subspaces — a bounding box, not an exact cover); leave the depth-relation bookkeeping to V2/V3.

## OUT_OF_SCOPE

None. The note correctly defers per-subspace exact reporting, content delivery, region reads, and version comparison to future ASNs, and its Open Questions name them without defining claims for them.

VERDICT: REVISE

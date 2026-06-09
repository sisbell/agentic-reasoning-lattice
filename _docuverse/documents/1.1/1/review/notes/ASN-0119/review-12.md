# Review of ASN-0119

I verified the operation's structural backbone, the S3★ inheritance argument (revised to route through π⁻¹), and every worked numerical example.

## Verification performed

**Pivot example** (`ABCDE ↦ ACDEB`, cuts ord 2,3,6): R-P1 gives `M'([s_C,2..4]) = a₃,a₄,a₅`; R-P2 gives `M'([s_C,5]) = a₂`; R-EXT keeps `a₁`. Destination ordinals `{2,3,4}∪{5}∪{1}` tile `{1..5}` disjointly — P2, P1, P3 all confirmed.

**Swap example** (`ABCDEF ↦ AEFCDB`, cuts ord 2,3,5,7): widths `w_α=1, w_μ=2, w_β=2`; middle net displacement `+1 = w_β−w_α`. Destinations `{2,3}∪{4,5}∪{6}∪{1}` tile `{1..6}`. Confirmed.

**Atomicity composite**: Move 1 (cuts 2,3,5) → `ACDBE`; Move 2 (cuts 4,5,6) → `ACDEB`. Final matches atomic pivot (P8a); intermediate `M_mid([s_C,4])=a₂ ≠ a₄ ≠ a₅` confirms P8b divergence.

**Footprint examples**: all three behaviors check out under `π` — `{B,C,D,E}` stays contiguous (`{2,3,4,5}↦{2,3,4,5}`); `{A,B}` fragments via exterior-meets-region (`{1,2}↦{1,5}`); `{B,C}` fragments via partial coverage (`{2,3}↦{2,5}`); `{B,E}` *gains* contiguity (`{2,5}↦{4,5}`). The P7c sufficiency-not-necessity framing is precise and well-defended.

**S3★ revision**: the π⁻¹ routing is sound — `M'(d)(v) = M(d)(π⁻¹(v))`, `π⁻¹(v)` is again a text position because R-PPERM/R-SPERM map each subspace onto itself, and pre-state S3★ discharges the inclusion. The note correctly avoids the false claim that an individual key keeps its image (the worked pivot exhibits `M'([s_C,2])=a₃ ≠ a₂=M([s_C,2])`).

## Assessment

Every system-level obligation from the consultation is discharged: content permanence (P0), identity correspondence (P1), extent conservation (P3), discoverability (P5), link survival (P6/P7a/P7b), atomicity (P8a/P8b), isolation (P9). Boundary cases (empty subspace, single position, zero-width region) are correctly placed outside the partial operation's domain via R-PRE. The contiguity invariants are inherited verbatim because `V_{s_C}(d)` is unchanged as a set. Foundation references are all to verified ASNs (0034/0036/0043/0047/0058/0084/0098). The five open questions are genuine future territory.

No REVISE items remain. The depth requirements — concrete examples for both operation modes, non-trivial wp analysis (P7c is the sole arrangement-conditional postcondition), and derived consequences — are all met.

VERDICT: CONVERGED

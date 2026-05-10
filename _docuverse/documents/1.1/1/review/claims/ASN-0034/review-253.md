# Cone Review — ASN-0034/TS1 (cycle 2)

*2026-04-18 07:04*

### TA1-strict and TS1 both rely on Divergence's exhaustiveness but neither cites T3

**Foundation**: Divergence's exhaustiveness postcondition ("exactly one of case (i) or case (ii) applies") is discharged via T3: "For exhaustiveness, suppose neither case applies — all shared components agree and `#a = #b`. Then by T3, `a = b`, contradicting `a ≠ b`." Divergence's own Depends accordingly lists T3.

**ASN**: Both downstream consumers rule out Divergence case (ii) and conclude case (i) applies without citing T3:
- TA1-strict, proof opening: "Both sub-cases fail, so case (ii) cannot apply, and we are in Divergence case (i)…"
- TS1 precondition check (viii): "since #v₁ = #v₂ = m, Divergence case (ii) (prefix divergence) is excluded… Since v₁ < v₂ implies v₁ ≠ v₂, Divergence case (i) applies…"

Neither TA1-strict's Depends nor TS1's Depends includes T3.

**Issue**: The step "case (ii) excluded + `a ≠ b` ⟹ case (i) applies" consumes Divergence's exhaustiveness postcondition, which is load-bearing on T3. TA1-strict's own Depends prose articulates the per-step citation discipline precisely for this situation — "requires T0 to be listed here rather than left to flow transitively through Divergence, T1, ActionPoint, TumblerAdd, or TA0, so that a reviser tightening T0 … has Depends-backed visibility into TA1-strict's consumption sites." Under that same discipline, a reviser tightening T3's canonical-representation semantics (the mechanism that converts "all shared components agree + equal lengths" into "a = b") would have no Depends-backed visibility into either TA1-strict's or TS1's consumption sites at the case-(i)-must-apply step, while every other transitively-reachable foundation (T0, T1, TA-Pos, NAT-order, NAT-wellorder) is cited. The omission is a consistency gap within the per-step discipline the ASN documents.

**What needs resolving**: Either T3 must be cited at TA1-strict's and TS1's case-(ii)-exclusion step (matching the per-step discipline's treatment of T0/T1/TA-Pos/NAT-order/NAT-wellorder), or the per-step discipline must be narrowed in a way that explains why T3's transitive reachability through Divergence's exhaustiveness is exempt when the other foundations' transitive reachabilities are not.

# Regional Review — ASN-0034/TumblerAdd (cycle 8)

*2026-04-20 14:34*

### T0 declares the subcarrier ℕ⁺ but no claim in the ASN consumes it
**Foundation**: T0 (CarrierSetDefinition) — the axiom introduces the carrier T and a companion subcarrier ℕ⁺.
**ASN**: T0 body: "Write `ℕ⁺ = {n ∈ ℕ : n > 0}` for the strictly positive naturals." T0 formal contract: "The subcarrier `ℕ⁺ = {n ∈ ℕ : n > 0}` denotes the strictly positive naturals." Scanning the remaining claims — T1, T3, TA-Pos, ActionPoint, the seven stated NAT-* axioms, and TumblerAdd — no body text or formal contract references ℕ⁺. ActionPoint's "`w_{actionPoint(w)} ≥ 1`" postcondition, TumblerAdd's "`wₖ ≥ 1`" fact, and the components of T are all stated against ℕ, not ℕ⁺.
**Issue**: ℕ⁺ is introduced as named content in T0's axiom and re-committed in T0's formal contract, yet no consumer in this ASN predicates anything on ℕ⁺-membership. This mirrors the prior finding about the set **Z** introduced in TA-Pos's formal contract with no in-ASN consumer: both are reified notations whose formal-contract presence is not anchored to any use-site. The "precision reader" test — does the formal contract commit to more than any consumer needs? — fails here the same way. Unlike `ℕ`, `#·`, and `·ᵢ`, which are load-bearing across every downstream claim, ℕ⁺ sits as a dangling definitional artifact.
**What needs resolving**: Either remove ℕ⁺ from T0's formal contract (and the accompanying prose) until a consumer in this ASN actually quantifies over or tests membership in ℕ⁺, or identify the stated claim that consumes `n ∈ ℕ⁺` (or the equivalent) and surface that dependence explicitly in its Depends list so T0's ℕ⁺ clause is anchored to an in-ASN use-site.

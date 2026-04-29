# Cone Review — ASN-0034/T7 (cycle 1)

*2026-04-25 22:47*

Reading the ASN as a system. The core finding is a slot-citation error in T7 referencing a contract slot that does not exist on T4.

### T7 cites "T4's Axiom" but T4 has no Axiom slot
**Class**: REVISE
**Foundation**: T4's Formal Contract has slots Definition, Consequence, Preconditions, Depends — no Axiom.
**ASN**: T7 proof: *"By T4's Axiom, every non-separator component is strictly positive: `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present"* and again *"strictly positive by T4's Axiom (its `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` clauses at non-separator positions)"*. Also T7's Depends entry: *"T4 (HierarchicalParsing) — ... and its Axiom's `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` clauses supply strict positivity of non-separator components."*
**Issue**: T4's contract carries no Axiom slot. The `0 < Nᵢ, …` clauses live inside T4's *Definition* (the Canonical written form clause "with `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present"), and the strict-positivity fact is *derived* in T4's prose from NAT-zero applied to T0's typing plus the non-separator distinction `tᵢ ≠ 0`. Citing "T4's Axiom" three times mis-routes the citation to a non-existent slot, and additionally elides that the strict-positivity content rests on NAT-zero rather than being posited by T4.
**What needs resolving**: T7 must cite the actual source — either T4's Definition (Canonical written form) or NAT-zero applied at the non-separator position with `tᵢ ∈ ℕ` from T0 — and the Depends entry for T4 must be corrected accordingly. If T4 is intended to package this as an exported axiomatic fact, that slot must be added to T4's contract; otherwise downstream citations must route through the actual delivery mechanism.

### T4 prose "purely definitional" overstates
**Class**: OBSERVE
**Foundation**: —
**ASN**: T4 prose: *"T4 is purely definitional: it characterises T4-valid as a predicate on T (the four-conjunct conjunction above) without asserting which `t ∈ T` satisfy it"*.
**Issue**: T4 also exports an Exhaustion Consequence (`zeros(t) ∈ {0,1,2,3}` under the bound). Calling T4 "purely definitional" while it carries a derived Consequence is mildly inaccurate framing; consumers reading "purely definitional" might miss the Consequence available at the citation site.

VERDICT: REVISE

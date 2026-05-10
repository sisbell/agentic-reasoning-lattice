# Regional Review — ASN-0034/ActionPoint (cycle 6)

*2026-04-21 23:18*

### T0 uses `≥` in its formal contract but no axiom defines the relation
**Foundation**: NAT-order (NatStrictTotalOrder) — formal contract introduces `<` (irreflexivity, transitivity, trichotomy) and defines `≤` via `m ≤ n ⟺ m < n ∨ m = n`. No clause introduces `≥`.
**ASN**: T0 body: "For each `a ∈ T`, write `#a` for the length of `a` (so `#a ≥ 1`)". T0 formal contract: "`#· : T → ℕ` satisfying `#a ≥ 1` for all `a ∈ T`".
**Issue**: T0's formal contract asserts `#a ≥ 1` using the symbol `≥`, but `≥` is not defined by any axiom in the ASN. NAT-order defines `<` and `≤`; it is silent on `≥`. A prior cycle flagged the same undefined-`≥` issue in ActionPoint's postcondition, which has since been rewritten into `≤`-form (`1 ≤ w_{actionPoint(w)}`), but T0's two uses of `≥` were not converted. T0 is also structurally prior to the NAT-* axioms in the enumeration it publishes, so even if `≥` were defined downstream, T0's own contract would rest on a symbol established later. This is the only remaining site in the ASN where `≥` appears; consumers citing T0's length bound inherit a symbol the ASN does not license.
**What needs resolving**: Either extend NAT-order's formal contract to introduce `≥` as defined notation for the reversed `≤`, or rewrite T0's length bound to use the `≤`-form already supplied (e.g., `1 ≤ #a`), matching the rewrite applied to ActionPoint's postcondition so every symbol in T0's contract resolves against stated axiom content.

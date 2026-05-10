# Regional Review — ASN-0034/T4a (cycle 4)

*2026-04-22 01:45*

### NAT-addcompat cited but never stated
**Foundation**: structural — claims cited in Depends and invoked in proofs must have a stated axiom/definition somewhere in scope
**ASN**: T4c Injectivity: "NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}`, yields `0 < 1`, `1 < 2`, and `2 < 3`". T4c Depends: "NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}` to supply the base links `0 < 1`, `1 < 2`, `2 < 3` in injectivity's chain."
**Issue**: NAT-addcompat is the load-bearing citation for the pairwise distinctness of `0, 1, 2, 3` (explicitly added after the earlier finding flagged that NAT-zero/NAT-discrete/NAT-order cannot establish `n ≠ n + 1`). Yet no NAT-addcompat claim appears anywhere in this ASN, the declared depends list is empty, and the Foundation Statements block is "(none)". NAT-discrete already uses `m + 1` without `+` being axiomatized — the intended home for addition is presumably NAT-addcompat, but it has no body in this document. The chains `0 < 1 < 2 < 3` (Injectivity) and `zeros(t) ∈ {0, 1, 2, 3}` (Exhaustion) therefore rest on an unstated axiom; T4c's proof obligation is not discharged.
**What needs resolving**: Either include a NAT-addcompat (NatAdditionOrderAndSuccessor) claim in this ASN with an explicit axiom that grounds `n < n + 1` (and whatever else T4c needs — including membership of the numerals `1, 2, 3` in ℕ via `+`), declare it as an external dependency with its statement quoted, or recast Injectivity and Exhaustion so they do not depend on an unstated claim.

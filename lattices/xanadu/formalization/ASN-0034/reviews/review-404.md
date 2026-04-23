# Regional Review — ASN-0034/T4c (cycle 2)

*2026-04-23 00:57*

### NAT-zero Consequence derivation uses substitution-of-equals-under-`<` that the rest of the ASN disallows
**Class**: REVISE
**Foundation**: NAT-zero (NatZeroMinimum) — Consequence derivation paragraph; NAT-order disjointness clause `(A m, n ∈ ℕ : m < n : m ≠ n)`
**ASN**: NAT-zero prose deriving `¬(n < 0)`: *"In the second case, `0 = n` rewrites `n < 0` to `0 < 0`, again contradicting irreflexivity."* The step "rewrites `n < 0` to `0 < 0`" is substitution of equals under `<`. But T4c's Exhaustion explicitly states *"substitution of equals under `<` is not among NAT-order's stated properties,"* and the previous REVISE cycle removed analogous reasoning from T4c's Injectivity in favor of the disjointness axiom clause. NAT-order's own exactly-one Consequence derivation likewise avoids this rewriting and routes through disjointness for `¬(m < n ∧ m = n)` and `¬(m = n ∧ n < m)`.
**Issue**: NAT-zero relies on a property the rest of the ASN has been careful to avoid. The two postures are incompatible: either substitution of equals under `<` is available everywhere (and T4c's note plus NAT-order's disjointness-routed derivations are over-cautious), or it is not available anywhere (and NAT-zero's second case is unjustified). The ASN currently commits to the latter for trichotomy and T4c but the former for NAT-zero.
**What needs resolving**: Rework NAT-zero's second case to use NAT-order's disjointness axiom (from `n < 0` derive `n ≠ 0`, equivalently `0 ≠ n` by symmetry of `=`, contradicting `0 = n`), and add NAT-order's disjointness clause to NAT-zero's Depends bullet. Alternatively, if substitution-of-equals under `<` is taken as logical (a property of `=`) rather than a NAT-order property, declare this explicitly once in the ASN and make it consistently available — then the T4c Exhaustion caveat should be withdrawn.

### "T4-valid" is used as a predicate without a point-of-definition
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: The term "T4-valid" appears in T4's Consequence prose (*"every T4-valid tumbler"*), in T4c's domain statement (*"On the T4-valid subset of `T`"*), in T4c's Preconditions, and in T4c's Postconditions. Neither T4's Axiom nor any Definition slot introduces "T4-valid" as a named predicate; it is implicitly "satisfies T4's Axiom clauses".
**Issue**: A predicate used across claim boundaries has no single declaration site. Minor; adding `T4-valid(t) := zeros(t) ≤ 3 ∧ …` once (in a Definition slot or adjacent to the Axiom) would remove the implicit unfold.

### T4 Axiom slot carries a definition of "field separator"
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4's Axiom bullet includes *"T4 stipulates that a position `i` of `t` is a field separator iff `tᵢ = 0`."* This is a terminological definition (biconditional introducing a name), not a constraint on valid address tumblers.
**Issue**: Slot mismatch — NAT-order keeps notational definitions (`≤`, `≥`, `>`) in a dedicated Definition slot. T4's "field separator" definition belongs in a Definition slot rather than inside the Axiom.

### T4 Axiom's per-`k` schema restates Consequences inside the Axiom
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4's Axiom closes with the four canonical forms for `k ∈ {0, 1, 2, 3}`, including the strict-positivity conditions `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ`. T4's own prose derives these strict positivities from NAT-zero + NAT-discrete at non-separator positions (*"NAT-zero together with NAT-discrete (at m = 0) force every non-zero component to be strictly positive"*). The exhaustion of `k ∈ {0, 1, 2, 3}` is the Consequence paragraph, yet the schema assumes that exhaustion to enumerate four cases.
**Issue**: The schema mixes axiomatic content (the field-separator adjacency, endpoint constraints, `zeros(t) ≤ 3`) with what the ASN treats as derived (strict positivity of components; exhaustion of `k`). Either promote the schema to the Consequence slot, or state only the axiomatic clauses in the Axiom and derive the schema afterward.

VERDICT: REVISE

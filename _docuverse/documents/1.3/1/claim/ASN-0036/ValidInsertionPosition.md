**ValidInsertionPosition (ValidInsertionPosition).** For a document `d` with `V_1(d) ≠ ∅`, the *binary* predicate `ValidInsertionPosition(d, v)` is satisfied when:

- The common V-position depth `m` of V_1(d) is fixed by S8-depth. By S8a, `m ≥ 2`.
- Setting `N = |V_1(d)|`, the predicate holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.

*Proof.* By D-MIN, `min(V_1(d)) = [1, 1, ..., 1]` of depth `m`. By OrdinalShift (ASN-0034), `shift([1, ..., 1], j)` leaves the leading `m − 1` components unchanged and advances the last component to `1 + j`, so `shift([1, ..., 1], j) = [1, ..., 1, 1 + j]` for `j ≥ 1`; at `j = 0` the position is `v = min(V_1(d)) = [1, ..., 1]` by D-MIN. Every component is then `≥ 1` — the leading `m − 1` equal 1, the last `1 + j ≥ 1` — so `zeros(v) = 0` with componentwise positivity, and OrdShiftHom (a) fixes `v₁ = 1` as the text subspace identifier. For `j ≠ j'` in `{0, ..., N}` the last components `1 + j ≠ 1 + j'` (NAT-order, ASN-0034), so the length-`m` tumblers diverge at position `m` and are distinct by T3 (ASN-0034), giving exactly `N + 1` positions. ∎

*Formal Contract:*

- *Preconditions:* `V_1(d) ≠ ∅`; the common V-position depth `m` of `V_1(d)` is fixed by S8-depth and satisfies `m ≥ 2` by S8a.
- *Definition:* With `N = |V_1(d)|`, `ValidInsertionPosition(d, v)` holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`. By D-MIN, `min(V_1(d)) = [1, ..., 1]` of depth `m`, and by OrdinalShift (ASN-0034) `shift([1, ..., 1], j) = [1, ..., 1, 1 + j]`; equivalently the satisfying set is `{[1, ..., 1, 1 + j] : j ∈ {0, ..., N}}`.
- *Postconditions:* The satisfying set contains exactly `N + 1` pairwise-distinct positions (NAT-order and T3, ASN-0034). Each satisfying `v` has `v₁ = 1` as the text subspace identifier (OrdShiftHom) and `zeros(v) = 0` with every component `≥ 1` (componentwise positivity).

- *Depends:*
  - S8-depth (FixedDepthVPositions) — supplies the common V-position depth `m` of V_1(d) asserted in the preconditions and used throughout the proof to fix the tumbler length
  - S8a (ArrangementDomainRestriction) — supplies the `m ≥ 2` lower bound on depth, invoked in the preconditions, and the zero-free / componentwise-positive predicate verified on each satisfying `v` in the postconditions
  - D-MIN (VMinimumPosition) — supplies `min(V_1(d)) = [1, …, 1]` of depth `m`, the base position from which all satisfying `v` are constructed in both the definition and the proof
  - OrdinalShift (ASN-0034) — supplies the `shift` operator and its expansion `shift([1,…,1], j) = [1,…,1, 1+j]`, the key step in deriving the satisfying-set formula in the proof and formal contract
  - OrdShiftHom (OrdinalShiftPreservation) — supplies part (a) `subspace(shift(v, n)) = subspace(v)`, invoked to establish `v₁ = 1` as the text subspace identifier for every satisfying position (postcondition)
  - T3 (ASN-0034) — supplies the distinctness criterion for length-`m` tumblers that differ at any component, used to conclude the `N + 1` satisfying positions are pairwise distinct
  - NAT-order (ASN-0034) — supplies the strict total order on natural numbers, used to establish `1 + j ≠ 1 + j'` for `j ≠ j'`, driving the distinctness count in the proof and postconditions
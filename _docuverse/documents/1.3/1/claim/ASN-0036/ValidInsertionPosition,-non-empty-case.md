**Definition (ValidInsertionPosition, non-empty case).** For a document `d` with `V_1(d) ≠ ∅`, the *binary* predicate `ValidInsertionPosition(d, v)` is satisfied when:

- The common V-position depth `m` of V_1(d) is fixed by S8-depth. By S8a, `m ≥ 2`.
- Setting `N = |V_1(d)|`, the predicate holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.

*Formal Contract (ValidInsertionPosition, non-empty case).*
- *Signature:* `ValidInsertionPosition(d, v)` — a *binary* predicate on document `d` and V-position `v`. The common V-position depth `m` is determined by `d` via S8-depth and read from state.
- *Preconditions:* Document `d` with `V_1(d) ⊆ dom(M(d))` non-empty; D-CTG holds on V_1(d); D-MIN gives `min(V_1(d)) = [1, ..., 1]` and D-SEQ gives `V_1(d) = {[1, ..., 1, k] : 1 ≤ k ≤ N}` (both needed to discharge the explicit form (d)); `m ≥ 2` is the common depth of V_1(d) by S8-depth and S8a.
- *Definition:* `ValidInsertionPosition(d, v)` holds iff, writing `N = |V_1(d)|`, `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`.
- *Postconditions:* (a) `subspace(v) = 1` and `#v = m` (the state-fixed common depth). (b) `v` satisfies S8a: `zeros(v) = 0` and all components positive. (c) For fixed `d`, exactly `N + 1` values of `v` satisfy the predicate. (d) The explicit form is `v = [1, 1, ..., 1, 1 + j]` of depth `m`, with last component `1 + j` and all `m − 1` preceding components equal to 1 (matching the D-SEQ notation).
- *Derivation:* By D-MIN, `min(V_1(d)) = [1, 1, ..., 1]` of depth `m`. By OrdinalShift (ASN-0034), `shift([1, ..., 1], j)` leaves the leading `m − 1` components unchanged and advances the last component to `1 + j`, so `shift([1, ..., 1], j) = [1, ..., 1, 1 + j]` for `j ≥ 1`; at `j = 0` the position is `v = min(V_1(d)) = [1, ..., 1]` by D-MIN. This is (d). Every component is then `≥ 1` — the leading `m − 1` equal 1, the last `1 + j ≥ 1` — so `zeros(v) = 0` with componentwise positivity (b), and OrdShiftHom (a) fixes `v₁ = 1` as the text subspace identifier. For `j ≠ j'` in `{0, ..., N}` the last components `1 + j ≠ 1 + j'` (NAT-order, ASN-0034), so the length-`m` tumblers diverge at position `m` and are distinct by T3 (ASN-0034), giving exactly `N + 1` positions (c).
- *Depends:* D-MIN, D-CTG, D-CTG-depth, D-SEQ; S8a, S8-fin, S8-depth; OrdShiftHom (subspace and S8a preservation), OrdinalShift (last-component value, ASN-0034); T3 (ASN-0034).

- *Depends:*
  - S8-depth (Fixed-depth V-positions) — supplies the common depth `m` of V_1(d) consumed by the predicate signature, preconditions, all postconditions, and the derivation of the explicit form
  - S8a (Σ.M(d) domain restriction) — supplies the lower bound `m ≥ 2` and componentwise-positivity well-formedness constraint used throughout the derivation and postconditions (b) and (d)
  - D-CTG (VContiguity) — required as a precondition; contiguity of V_1(d) is needed to discharge the explicit form (d) via D-SEQ's proof
  - D-MIN (VMinimumPosition) — supplies `min(V_1(d)) = [1, …, 1]`, the base position from which every valid insertion position is constructed (`j = 0` case and anchor for OrdinalShift)
  - D-SEQ (SequentialPositions) — supplies the explicit enumeration `V_1(d) = {[1, …, 1, k] : 1 ≤ k ≤ N}` needed to establish the exactly `N + 1` count in postcondition (c)
  - D-CTG-depth (SharedPrefixReduction) — required as a precondition; guarantees that components 2 through `m − 1` are uniformly 1, enabling the explicit form (d)
  - S8-fin (Finite arrangement) — supplies finiteness of `dom(M(d))`, bounding the count to exactly `N + 1` positions in postcondition (c)
  - OrdShiftHom (OrdinalShiftPreservation) — supplies the shift-preservation lemma: `subspace(shift(v, n)) = subspace(v)` (postcondition (a)) and S8a-closure of `shift(v, n)` (postcondition (b))
  - OrdinalShift (ASN-0034) — supplies the `shift` operator and the last-component computation `shift([1, …, 1], j) = [1, …, 1, 1 + j]` used in the definition and derivation
  - T3 (CanonicalRepresentation, ASN-0034) — supplies tumbler distinctness from diverging component sequences, used to establish that the `N + 1` constructed positions are pairwise distinct (postcondition (c))
# Citation Resolve — ASN-0036/ValidInsertionPosition,-non-empty-case — run 1

*2026-06-25T02:06:33Z*
*Model: sonnet*

## Output

All referenced labels are confirmed real. Now I can classify them all — every reference in the prose supplies something the claim's definition, preconditions, or derivation consumes, so all are `depends`.

```
CLASSIFICATIONS:
- label: S8-depth
  direction: depends
  bullet: "- S8-depth (Fixed-depth V-positions) — supplies the common depth `m` of V_1(d) consumed by the predicate signature, preconditions, all postconditions, and the derivation of the explicit form"

- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies the lower bound `m ≥ 2` and componentwise-positivity well-formedness constraint used throughout the derivation and postconditions (b) and (d)"

- label: D-CTG
  direction: depends
  bullet: "- D-CTG (VContiguity) — required as a precondition; contiguity of V_1(d) is needed to discharge the explicit form (d) via D-SEQ's proof"

- label: D-MIN
  direction: depends
  bullet: "- D-MIN (VMinimumPosition) — supplies `min(V_1(d)) = [1, …, 1]`, the base position from which every valid insertion position is constructed (`j = 0` case and anchor for OrdinalShift)"

- label: D-SEQ
  direction: depends
  bullet: "- D-SEQ (SequentialPositions) — supplies the explicit enumeration `V_1(d) = {[1, …, 1, k] : 1 ≤ k ≤ N}` needed to establish the exactly `N + 1` count in postcondition (c)"

- label: D-CTG-depth
  direction: depends
  bullet: "- D-CTG-depth (SharedPrefixReduction) — required as a precondition; guarantees that components 2 through `m − 1` are uniformly 1, enabling the explicit form (d)"

- label: S8-fin
  direction: depends
  bullet: "- S8-fin (Finite arrangement) — supplies finiteness of `dom(M(d))`, bounding the count to exactly `N + 1` positions in postcondition (c)"

- label: OrdShiftHom
  direction: depends
  bullet: "- OrdShiftHom (OrdinalShiftPreservation) — supplies the shift-preservation lemma: `subspace(shift(v, n)) = subspace(v)` (postcondition (a)) and S8a-closure of `shift(v, n)` (postcondition (b))"

- label: OrdinalShift
  direction: depends
  bullet: "- OrdinalShift (ASN-0034) — supplies the `shift` operator and the last-component computation `shift([1, …, 1], j) = [1, …, 1, 1 + j]` used in the definition and derivation"

- label: T3
  direction: depends
  bullet: "- T3 (CanonicalRepresentation, ASN-0034) — supplies tumbler distinctness from diverging component sequences, used to establish that the `N + 1` constructed positions are pairwise distinct (postcondition (c))"

RETRACTIONS: []
```

# Citation Resolve — ASN-0036/ValidFirstInsertionPosition — run 1

*2026-06-25T02:40:21Z*
*Model: sonnet*

## Output

All labels are confirmed real claims. Now I have everything needed to produce the output.

```
CLASSIFICATIONS:
- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies the well-formedness constraint `zeros(v) = 0` and lower bound `m ≥ 2` consumed by the precondition and postcondition (b)"

- label: T0
  direction: depends
  bullet: "- T0 (ASN-0034) — supplies the equivalence `zeros(v) = 0` iff every component is positive, invoked in postcondition (b) for componentwise positivity of the all-ones tuple"

- label: S8-depth
  direction: forward
  bullet: "- S8-depth (Fixed-depth V-positions) — in the non-empty case, depth `m` is read from state via S8-depth; the empty-case predicate takes `m` as a free parameter and does not depend on this claim"

- label: D-CTG
  direction: forward
  bullet: "- D-CTG (VContiguity) — named in the non-empty example as a downstream invariant any successor state must satisfy; not consumed by the empty-case axiom"

- label: D-MIN
  direction: forward
  bullet: "- D-MIN (VMinimumPosition) — named in both examples as the constraint that forces `min(V₁(d)) = [1, 1]` once the subspace becomes non-empty; not consumed by the empty-case formal contract"

- label: T3
  direction: forward
  bullet: "- T3 (CanonicalRepresentation, ASN-0034) — cited in the empty-case example to note that depth-2 and depth-3 all-ones tumblers are distinct; illustrative, not load-bearing for the formal contract"

- label: ValidInsertionPosition
  direction: forward
  bullet: "- ValidInsertionPosition (non-empty case) — the companion binary predicate; named for contrast in the example section to show how the ternary empty-case predicate differs"

RETRACTIONS: []
```

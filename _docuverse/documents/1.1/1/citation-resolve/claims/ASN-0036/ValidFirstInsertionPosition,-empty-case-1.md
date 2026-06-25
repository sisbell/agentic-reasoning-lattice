# Citation Resolve — ASN-0036/ValidFirstInsertionPosition,-empty-case — run 1

*2026-06-25T02:33:44Z*
*Model: sonnet*

## Output

I have enough information to classify all label references. Here's my analysis:

- **S8a**: The formal contract explicitly states "Depends: S8a — for the lower bound m ≥ 2" and postcondition (b) invokes the S8a condition `zeros(v) = 0`. → `depends`
- **T0 (ASN-0034)**: Formal Depends section states "T0 (ASN-0034) — for componentwise positivity of the constant tuple"; confirmed by S8a.md which shows T0 supplies `zeros(t) = 0` ↔ every component positive. → `depends`
- **S8-depth**: Appears only in the non-empty example ("depth m = 2 is read from state via S8-depth"); the empty-case claim treats depth m as a free parameter — S8-depth is not consumed by the formal contract. → `forward`
- **D-CTG**: Appears only in the non-empty example as a constraint successor states must satisfy; not consumed by the empty-case axiom. → `forward`
- **D-MIN**: Appears in both examples as a downstream constraint; the formal contract doesn't invoke it. → `forward`
- **T3**: Appears in the empty-case example to note depth-2 and depth-3 give distinct tumblers; illustrative, not load-bearing for the formal contract. → `forward`
- **ValidInsertionPosition**: The non-empty companion predicate, named for contrast in the example section; the empty-case claim stands without it. → `forward`

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

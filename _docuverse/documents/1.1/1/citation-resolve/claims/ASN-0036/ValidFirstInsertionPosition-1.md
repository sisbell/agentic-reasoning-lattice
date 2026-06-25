# Citation Resolve — ASN-0036/ValidFirstInsertionPosition — run 1

*2026-06-25T20:08:12Z*
*Model: sonnet*

## Output

Now I have everything I need. Let me classify the five labels found in the prose.

**Reasoning through each:**

- **`ValidInsertionPosition`** — named in the heading "Non-empty case (binary predicate)" as the companion predicate that handles the non-empty case. The claim's own definition is the empty-case ternary predicate; `ValidInsertionPosition` is a parallel claim referenced for contrast/context. The current claim doesn't rest on its correctness. → `forward`

- **`S8-depth`** — "The depth `m = 2` is read from state via S8-depth." This appears inside the non-empty example illustrating `ValidInsertionPosition`, not the ternary predicate itself. The ternary predicate takes `m` explicitly as a parameter; S8-depth is explanatory context for how `m` is obtained in practice. → `forward`

- **`D-CTG`** — "Any successor state whose `V₁(d)` gains a position at, say, [1, 2] must still satisfy D-CTG and D-MIN." This points the reader toward constraints future (post-insertion) states must satisfy; D-CTG is not consumed to establish this claim's definition. → `forward`

- **`D-MIN`** — "D-MIN requires min(V₁(d)) = [1, 1] once the subspace becomes non-empty, so the position is exactly the one D-MIN demands." D-MIN supplies the axiom whose constraint is the direct motivation/justification for the claim's definition — the first insertion position is precisely the one D-MIN demands. → `depends`

- **`T3`** — "by T3, this is a different tumbler." Used as a proof step in the empty case example to establish that depth-3 `[1,1,1]` is distinct from depth-2 `[1,1]`. T3 (CanonicalRepresentation) supplies the tumbler-equality criterion invoked here. → `depends`

```
CLASSIFICATIONS:
- label: D-MIN
  direction: depends
  bullet: "- D-MIN (VMinimumPosition) — supplies the axiom that min(V₁(d)) = [1,…,1] once non-empty, establishing that the ternary predicate's choice of v is exactly the position D-MIN demands"

- label: T3
  direction: depends
  bullet: "- T3 (CanonicalRepresentation) — supplies tumbler equality (component-wise identity) used to confirm that depth-m [1,…,1] and depth-m' [1,…,1] are distinct tumblers when m ≠ m'"

- label: ValidInsertionPosition
  direction: forward
  bullet: "- ValidInsertionPosition (ValidInsertionPosition) — the non-empty companion binary predicate; illustrated in the examples as the parallel case this claim contrasts against"

- label: S8-depth
  direction: forward
  bullet: "- S8-depth (FixedDepthVPositions) — supplies the mechanism by which depth m is read from state in the non-empty companion predicate; referenced as explanatory context for how m is obtained in practice"

- label: D-CTG
  direction: forward
  bullet: "- D-CTG (VContiguity) — named as a successor-state constraint any post-insertion V₁(d) must satisfy; downstream obligation, not consumed by this claim's definition"

RETRACTIONS: []
```

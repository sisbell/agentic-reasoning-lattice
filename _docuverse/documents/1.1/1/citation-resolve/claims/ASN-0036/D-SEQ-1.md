# Citation Resolve — ASN-0036/D-SEQ — run 1

*2026-06-25T02:17:38Z*
*Model: sonnet*

## Output

All referenced claims are confirmed. Now I have everything I need to classify.

All seven labels in the prose are consumed by the proof steps — the claim's correctness rests on each one. None are forward/navigational references.

```
CLASSIFICATIONS:
- label: S8-depth
  direction: depends
  bullet: "- S8-depth (Fixed-depth V-positions) — supplies the common depth `m` of all V-positions in the text subspace; used throughout to treat V_1(d) as a set of fixed-length tuples"

- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies the lower bound `m ≥ 2` and componentwise positivity; used to verify that the intermediate witness `w` constructed in Step 3 lies in `dom(Σ.M(d))`"

- label: D-CTG
  direction: depends
  bullet: "- D-CTG (VContiguity) — supplies the gap-filling axiom invoked in Step 3 to conclude that every intermediate `w = [1, 1, …, 1, k]` between two attained positions lies in V_1(d)"

- label: D-CTG-depth
  direction: depends
  bullet: "- D-CTG-depth (SharedPrefixReduction) — supplies the shared-prefix result used in Step 1 Case `m ≥ 3` to show all positions in V_1(d) agree on components 2 through `m − 1`"

- label: D-MIN
  direction: depends
  bullet: "- D-MIN (VMinimumPosition) — supplies `min(V_1(d)) = [1, 1, …, 1]`; used in Step 2 to establish that k = 1 is attained, and in Step 1 Case `m ≥ 3` to pin the shared components to the value 1"

- label: S8-fin
  direction: depends
  bullet: "- S8-fin (Finite arrangement) — supplies finiteness of `dom(Σ.M(d))`; used in Step 4 to conclude the k-values form a finite range"

- label: T1
  direction: depends
  bullet: "- T1 case (i) (LexicographicOrder, ASN-0034) — supplies first-divergence comparison; used in Step 3 to order positions agreeing on components 1 through `m − 1` and differing at component `m`"

RETRACTIONS: []
```

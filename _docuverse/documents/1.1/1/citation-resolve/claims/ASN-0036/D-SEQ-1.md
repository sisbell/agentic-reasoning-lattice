# Citation Resolve — ASN-0036/D-SEQ — run 1

*2026-06-25T20:03:38Z*
*Model: sonnet*

## Output

All label references are verified. D-SEQ's prose cites seven labels, all consumed as proof-step inputs. Here are the classifications:

```
CLASSIFICATIONS:
- label: S8-depth
  direction: depends
  bullet: "- S8-depth (FixedDepthVPositions) — supplies the common-depth guarantee for V_1(d); the proof opens by fixing m as that common depth and invokes S8-depth to assert it exists"

- label: S8a
  direction: depends
  bullet: "- S8a (ArrangementDomainRestriction) — supplies the depth ≥ 2 lower bound (m ≥ 2); the claim states \"the derivation below relies on this lower bound\" and Step 3 re-invokes it to qualify the intermediate witness w"

- label: D-CTG-depth
  direction: depends
  bullet: "- D-CTG-depth (SharedPrefixReduction) — supplies the shared-prefix result (components 2 through m − 1 identical) used in Step 1 Case m ≥ 3 to pin all but the last component to 1"

- label: D-MIN
  direction: depends
  bullet: "- D-MIN (VMinimumPosition) — supplies min(V_1(d)) = [1, 1, …, 1]; Step 1 (Case m ≥ 3) uses it to fix the shared-prefix value to 1, and Step 2 uses it to establish k = 1 as an attained value"

- label: T1(i)
  direction: depends
  bullet: "- T1(i) (LexicographicOrder, ASN-0034) — supplies the lexicographic comparison rule; Step 3 invokes it twice to establish v₁ < v₂ and v₁ < w < v₂ from component-wise comparisons"

- label: D-CTG
  direction: depends
  bullet: "- D-CTG (VContiguity) — supplies the contiguity constraint; Step 3 applies it to conclude the intermediate witness w ∈ V_1(d), making the k-values a contiguous range"

- label: S8-fin
  direction: depends
  bullet: "- S8-fin (FiniteArrangement) — supplies the finiteness of dom(M(d)); Step 4 uses it to conclude V_1(d) is finite, bounding the k-value range"

RETRACTIONS: []
```

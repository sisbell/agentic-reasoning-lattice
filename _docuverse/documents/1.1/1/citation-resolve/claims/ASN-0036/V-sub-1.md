# Citation Resolve — ASN-0036/V-sub — run 1

*2026-06-28T02:54:09Z*
*Model: sonnet*

## Output

All four labels (`D-CTG`, `D-CTG-depth`, `D-MIN`, `D-SEQ`) appear in the prose as claims that *constrain* `V_1(d)` — they build on this definition, not the other way around. The already-classified entries (`subspace`, `Σ.M(d)`) remain correct.

```
CLASSIFICATIONS:
- label: D-CTG
  direction: forward
  bullet: "- D-CTG (VContiguity) — consumes V_1(d) as the set over which its contiguity quantifier ranges; this claim is what gives that set meaning"

- label: D-CTG-depth
  direction: forward
  bullet: "- D-CTG-depth (SharedPrefixReduction) — consumes V_1(d) as the text-subspace projection whose elements it proves share a common prefix; defined here"

- label: D-MIN
  direction: forward
  bullet: "- D-MIN (VMinimumPosition) — constrains min(V_1(d)) to the all-ones tuple; V_1(d) is the set defined here"

- label: D-SEQ
  direction: forward
  bullet: "- D-SEQ (SequentialPositions) — derives the sequential form of V_1(d) by composing D-CTG, D-CTG-depth, and D-MIN over the set defined here"

RETRACTIONS: []
```

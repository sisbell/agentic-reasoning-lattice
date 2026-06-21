# Citation Resolve — ASN-0053/WR — run 1

*2026-06-20T23:41:54Z*
*Model: sonnet*

## Output

I have all the information I need. Here are the classifications:

```
CLASSIFICATIONS:
- label: D2
  direction: depends
  bullet: "- D2 (DisplacementUnique, ASN-0034) — supplies the displacement uniqueness result `reach(σ) ⊖ start(σ) = ℓ` that is the claim's conclusion, once its preconditions are discharged for (a, b, w) = (s, reach(σ), ℓ)"

- label: T12
  direction: depends
  bullet: "- T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that qualifies the level-uniform span; the proof cites T12 to discharge D2's preconditions on ℓ"

- label: TA-strict
  direction: depends
  bullet: "- TA-strict (StrictIncrease, ASN-0034) — supplies `a ⊕ w > a` instantiated as s < reach(σ), discharging D2's precondition a < b"

- label: TA0
  direction: depends
  bullet: "- TA0 (WellDefinedAddition, ASN-0034) — supplies the result-length identity `#(s ⊕ ℓ) = #ℓ = #s` used to pin #reach(σ) = #s and to confirm TA0's own preconditions for the s ⊕ ℓ = reach(σ) step"

- label: WF
  direction: forward
  bullet: "- WF (WellFormedSpanFromEndpoints) — sibling claim whose proof contains the equal-length/divergence-type argument reproduced inline here; cited as a navigation pointer"

RETRACTIONS: []
```

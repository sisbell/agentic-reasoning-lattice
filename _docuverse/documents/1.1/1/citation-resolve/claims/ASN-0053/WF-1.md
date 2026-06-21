# Citation Resolve — ASN-0053/WF — run 1

*2026-06-20T23:17:14Z*
*Model: sonnet*

## Output

I now have everything I need. T12 is `SpanWellDefinedness` (ASN-0034) and D1 is `DisplacementRoundTrip` (ASN-0034). Both are `depends`:

- **T12** supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that the proof explicitly verifies and the claim's conclusion targets ("satisfying T12").
- **D1** supplies the identity a ⊕ (b ⊖ a) = b that the proof invokes directly to establish reach(γ) = s ⊕ (r ⊖ s) = r.

Neither is `forward` — WF does not name any downstream refinement or elaboration in its prose.

```
CLASSIFICATIONS:
- label: T12
  direction: depends
  bullet: "- T12 (SpanWellDefinedness, ASN-0034) — supplies the well-formedness predicate (Pos(ℓ) and actionPoint(ℓ) ≤ #s) that the proof verifies and the claim's conclusion targets"

- label: D1
  direction: depends
  bullet: "- D1 (DisplacementRoundTrip, ASN-0034) — supplies the identity a ⊕ (b ⊖ a) = b used in the proof step reach(γ) = s ⊕ (r ⊖ s) = r"

RETRACTIONS: []
```

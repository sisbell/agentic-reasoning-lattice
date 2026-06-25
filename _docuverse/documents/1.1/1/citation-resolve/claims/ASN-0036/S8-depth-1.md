# Citation Resolve — ASN-0036/S8-depth — run 1

*2026-06-25T20:14:46Z*
*Model: sonnet*

## Output

I have the information I need from the already-read files. The claim references two labels:

1. **`OrdinalShift` (ASN-0034)** — the `shift` operator and the `δ` displacement operator it defines are used directly in the claim's definition of consecutive V-positions and in the subject of the shift-preservation lemma. The claim's reasoning consumes these symbols.

2. **`S8a`** — the shift-preservation lemma says `shift(v, n)` "preserves... its S8a well-formedness." S8a (ArrangementDomainRestriction) defines exactly what well-formedness means (`zeros(t) = 0 ∧ #t ≥ 2`). The lemma's conclusion is stated in terms of S8a's predicate — S8a supplies the criterion being preserved.

Both are `depends`.

```
CLASSIFICATIONS:
- label: OrdinalShift
  direction: depends
  bullet: "- OrdinalShift (ASN-0034) — supplies the `shift(v, n)` operator and `δ` displacement operator used to define consecutive V-positions and as the subject of the shift-preservation lemma"

- label: S8a
  direction: depends
  bullet: "- S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate (`zeros(t) = 0 ∧ #t ≥ 2`) that the shift-preservation lemma claims `shift(v, n)` preserves"

RETRACTIONS: []
```

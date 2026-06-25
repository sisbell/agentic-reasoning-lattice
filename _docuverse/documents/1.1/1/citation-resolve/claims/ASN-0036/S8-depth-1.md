# Citation Resolve — ASN-0036/S8-depth — run 1

*2026-06-25T02:01:51Z*
*Model: sonnet*

## Output

Both labels verified. S8a.md exists as a standalone claim file. OrdinalShift is a cross-ASN reference (ASN-0034) whose file doesn't exist yet in the claim directory, but it's still referenced in the prose and needs classification.

The prose has two labels to classify:
- **S8a** — the postconditions invoke "by S8a" for the lower bound `m_s ≥ 2`, and the shift-preservation paragraph invokes "S8a well-formedness". Both uses consume the constraint S8a supplies. → `depends`
- **OrdinalShift** (ASN-0034) — the claim uses `shift(v, 1)` and `v ⊕ δ(1, #v)` defined by OrdinalShift to characterize consecutive V-positions, and the shift-preservation lemma takes OrdinalShift as its subject. → `depends`

```
CLASSIFICATIONS:
- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies the well-formedness constraint and lower bound m_s ≥ 2 used in the postconditions and the shift-preservation lemma"

- label: OrdinalShift
  direction: depends
  bullet: "- OrdinalShift (ASN-0034) — supplies the shift(v, n) operator and v ⊕ δ(1, #v) notation used to characterize consecutive V-positions and state the shift-preservation lemma"

RETRACTIONS: []
```

# Citation Resolve — ASN-0036/OrdShiftHom — run 1

*2026-06-25T02:15:12Z*
*Model: sonnet*

## Output

The ASN-0034 claims aren't in the 1.3 tree yet, but all five labels appear explicitly in the claim prose and the Formal Contract names their roles precisely. The classification is clear from the proof structure alone.

All five referenced labels are `depends` — each supplies a definition, operator, or condition that the proof steps directly invoke:

- **OrdinalShift** — supplies the definition `shift(v, n) = v ⊕ δ(n, m)` that the proof opens with
- **OrdinalDisplacement** — supplies `δ(n, m) = [0, ..., 0, n]` and the `actionPoint` value `m` used to justify well-definedness
- **TumblerAdd** — supplies the component-wise addition formula that drives the copy/increment split
- **TA0** — supplies length preservation `#r = m`, used throughout the proof
- **S8a** — supplies `vᵢ ≥ 1` for every `i`, which part (b) directly consumes

None of the references are downstream elaborations or navigation pointers; each is consumed by the proof.

```
CLASSIFICATIONS:
- label: OrdinalShift
  direction: depends
  bullet: "- OrdinalShift (ASN-0034) — supplies the definition `shift(v, n) = v ⊕ δ(n, m)` that the proof writes out in its opening step"

- label: OrdinalDisplacement
  direction: depends
  bullet: "- OrdinalDisplacement (ASN-0034) — supplies `δ(n, m) = [0, ..., 0, n]` with `actionPoint(δ(n, m)) = m`, used to establish well-definedness of the addition"

- label: TumblerAdd
  direction: depends
  bullet: "- TumblerAdd (ASN-0034) — supplies the component-wise addition formula that justifies the copy/increment split at the action point"

- label: TA0
  direction: depends
  bullet: "- TA0 (ASN-0034) — supplies length preservation `#shift(v, n) = m`, used in both parts of the proof"

- label: S8a
  direction: depends
  bullet: "- S8a (V-position well-formedness) — supplies `vᵢ ≥ 1` for every `i`, the premise that part (b) directly consumes"

RETRACTIONS: []
```

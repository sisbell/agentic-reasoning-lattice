# Citation Resolve — ASN-0036/OrdShiftHom — run 1

*2026-06-25T20:01:23Z*
*Model: sonnet*

## Output

I have all the information needed. Let me classify each label from the prose.

Labels found in the prose:
- **OrdinalShift** — defines `shift(v, n) = v ⊕ δ(n, m)`, the definition the proof expands
- **OrdinalDisplacement** — invoked "By OrdinalDisplacement, `actionPoint(δ(n, m)) = m`"; proof correctness rests on this fact
- **TumblerAdd** — "By TumblerAdd, the result is built component-wise"; the component rule (`rᵢ = vᵢ` for `i < m`, `rₘ = vₘ + n`) is the proof's backbone
- **TA0** — "(TA0, ASN-0034)" supplies `#(a ⊕ w) = #w`, used as `#r = m`
- **S8a** — the predicate whose preservation is being proved; its definition (`zeros(t) = 0`, `#t ≥ 2`, all components ≥ 1`) is consumed in the part (b) hypothesis

All five are `depends`: the claim's proof invokes each directly.

```
CLASSIFICATIONS:
- label: OrdinalShift
  direction: depends
  bullet: "- OrdinalShift (OrdinalShift) — supplies the `shift(v, n) = v ⊕ δ(n, m)` definition that the proof expands throughout."

- label: OrdinalDisplacement
  direction: depends
  bullet: "- OrdinalDisplacement (OrdinalDisplacement) — supplies `δ(n, m) = [0,...,0,n]` and the postcondition `actionPoint(δ(n, m)) = m` invoked to confirm well-definedness and to identify the action point in the component-wise expansion."

- label: TumblerAdd
  direction: depends
  bullet: "- TumblerAdd (TumblerAdd) — supplies the component-wise rule `rᵢ = vᵢ` for `i < m` and `rₘ = vₘ + n`; part (a) and part (b) are both built entirely on this expansion."

- label: TA0
  direction: depends
  bullet: "- TA0 (WellDefinedAddition) — supplies `#(a ⊕ w) = #w`, instantiated as `#r = #δ(n,m) = m` (depth preserved), used in the frame condition and the S8a verification."

- label: S8a
  direction: depends
  bullet: "- S8a (ArrangementDomainRestriction) — supplies the predicate definition (`zeros(t) = 0`, `#t ≥ 2`, all components ≥ 1`) consumed as the part (b) hypothesis and proved to hold on `shift(v, n)`."

RETRACTIONS: []
```

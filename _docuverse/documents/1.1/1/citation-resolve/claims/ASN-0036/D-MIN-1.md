# Citation Resolve — ASN-0036/D-MIN — run 1

*2026-06-25T02:34:41Z*
*Model: sonnet*

## Output

All three labels in the prose (`S8a`, `S8-depth`, `T1`) appear in the `*Depends:*` line and each supplies something the claim's axiom or preconditions rest on:

- **S8a** — supplies `m_1 ≥ 2` (the lower-bound precondition)
- **S8-depth** — supplies `m_1`, the common depth used in the axiom's tuple length
- **T1 (LexicographicOrder, ASN-0034)** — defines the `min` operator used in the axiom

```
CLASSIFICATIONS:
- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies the lower bound m_1 ≥ 2 used as a precondition on the common depth"

- label: S8-depth
  direction: depends
  bullet: "- S8-depth (Fixed-depth V-positions) — supplies the common depth m_1 that sets the tuple length in the axiom min(V_1(d)) = [1, 1, ..., 1]"

- label: T1
  direction: depends
  bullet: "- T1 (LexicographicOrder, ASN-0034) — defines the min operator applied to V_1(d) in the axiom"

RETRACTIONS: []
```

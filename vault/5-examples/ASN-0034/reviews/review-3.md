## Correctness

I redid every computation in all eleven scenarios. No correctness errors found — all arithmetic, definition applications, and notation are correct.

Spot checks of the most complex computations:

- **S10A**: a⊖w=[0,0,0,0,0,0,0,1], b⊖w=[0,0,0,0,0,0,0,4] — position 8: 1 < 4. ✓
- **S10B**: a⊖w=[0,0,0,0,1] (length 5), b⊖w=[0,0,0,0,1,0,1,2] (length 8) — proper prefix relation confirmed. ✓
- **S4 full-address round-trip failure**: r⊖w_full finds divergence at d=1 (r₁=1, w₁=0), producing r back unchanged. TA4's zero-prefix condition fails at position 1 (a₁=1≠0). Failure correctly attributed. ✓
- **S3 result-length identity**: #(a⊕w_deep)=8=#w_deep; #(a⊕w_shallow)=1=#w_shallow. ✓
- **S5 boundary**: zeros([1,0,1,0,1,0,1])=3, so k=2 blocked by TA5 T4 preservation constraint (zeros(t)≤2 required). ✓

---

## Coverage

Building the coverage matrix against the Properties Introduced table:

| Property | Scenario | Non-vacuous |
|----------|----------|-------------|
| T0(a) | S7 | ✓ |
| T0(b) | S7 | ✓ |
| T1 | S1, S3, S5, S8, S10 | ✓ |
| T2 | S1 | ✓ |
| T3 | S2, S8 | ✓ |
| T4 | S2, S5, S11 | ✓ |
| T5 | S1, S6 | ✓ |
| T6(a) | S5 | ✓ |
| T6(b) | S5 | ✓ |
| **T6(c)** | **none** | **✗** |
| T6(d) | S11 | ✓ |
| T7 | S8 | ✓ |
| T8 | S9 | ✓ |
| T9 | S5, S9 | ✓ |
| T10 | S5 | ✓ |
| T10a | S5 | ✓ |
| T12 | S6 | ✓ |
| TA0 | S3, S4, S6 | ✓ |
| TA1 (weak) | S3 op B | ✓ |
| TA1-strict | S3 op A | ✓ |
| TA-strict | S3, S6 | ✓ |
| TA2 | S4, S10 | ✓ |
| TA3 (weak) | S10 sub-B | ✓ |
| TA3-strict | S10 sub-A | ✓ |
| TA4 | S4 | ✓ |
| TA5 | S5, S7, S9 | ✓ |
| TA6 | S4 | ✓ |
| TA7a | S4, S8 | ✓ |

---

```
VERDICT: REVISE

## Coverage gaps

### Gap 1: T6(c) — same node, user, and document-lineage fields
**Missing**: T6(c) is absent from the coverage table and scenarios. It is listed in the
backlog but not yet promoted to a scenario.
**Needed**: Two element addresses sharing all three upper fields. The addresses already
exist in S9: a₁=[1,0,1,0,1,0,1,1] and a₂=[1,0,1,0,1,0,1,2]. Add an explicit T6(c)
step: parse both via fields(·), extract node=[1], user=[1], doc=[1] from each, confirm
the match, and state that the determination is computable from the addresses alone
without consulting any index or version graph. One sentence in S9 suffices; no new
scenario is required.
```
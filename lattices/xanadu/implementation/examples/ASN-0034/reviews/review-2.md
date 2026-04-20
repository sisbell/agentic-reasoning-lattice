## Correctness

### Issue 1: Variable name collision in Scenario 1, T5 step
**Scenario**: Scenario 1
**Property**: T5
**Step**: Properties exercised — T5 bullet
**Problem**: The setup defines `p = [1, 0, 3]` (a user address, zeros=1). The T5 bullet then writes "prefix p=[1,0,3,0,2,0,1]", reusing the same name for a length-7 common prefix of e₁ and e₂. A reader following the scenario has `p = [1, 0, 3]` in scope; the inline reassignment without renaming produces an ambiguous reading. The T5 verification is mathematically correct, but the notation is defective.
**Correction**: Rename the T5 prefix to a fresh identifier — `q = [1,0,3,0,2,0,1]` or `π` — and update the T5 bullet accordingly: "T5: prefix q=[1,0,3,0,2,0,1]; any x with e₁ ≤ x ≤ e₂ must extend q..."

All arithmetic across all ten scenarios checks out. No other correctness errors found.

---

## Coverage gaps

### Gap 1: T6(d) — structural subordination within a document family
**Missing**: T6(d) says that whether the document field of `a` is a *prefix* of the document field of `b` (structural subordination within a version family) is decidable from the addresses alone. This is architecturally distinct from the equality tests in T6(a)–(c). It requires a multi-component document field — e.g., address `[1,0,3,0,2,1,0,1,1]` with document field `[2,1]` — to demonstrate that document field `[2]` of another address is a prefix of `[2,1]`.

**Problem**: Every document field in every scenario is a single-component sequence (`[1]` or `[2]`). S5 demonstrates T6(a) (same node) and T6(b) (different users, decidably) but never reaches T6(d). No worked example features a version address.

**Needed**: Add a sub-step — either within Scenario 5 or as a standalone scenario — that introduces two addresses: one with document field `[d]` and one with document field `[d, v]` (a version). Show explicitly that `[d]` is extracted from the first address's parse, `[d, v]` from the second, and that `[d] ≼ [d, v]` (prefix check via the lexicographic order, length comparison) confirms structural subordination. Contrast with a pair where the document fields are `[d₁]` and `[d₂, v]` with `d₁ ≠ d₂`, which decidably fails T6(d). This exercises the prefix test on document fields rather than equality.

---

```
VERDICT: REVISE
```
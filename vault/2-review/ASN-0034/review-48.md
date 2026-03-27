# Proof Verification: TS5

**Checking TS5 (ShiftAmountMonotonicity)**

**Logical flow review:**

1. Define d = n₂ − n₁ ≥ 1 — correct, since n₂ > n₁ with both natural and n₁ ≥ 1.
2. TS3 invoked with (v, n₁, d): preconditions n₁ ≥ 1, d ≥ 1, #v = m all hold — gives `shift(shift(v, n₁), d) = shift(v, n₂)`. ✓
3. Length preservation: proof needs #shift(v, n₁) = m. It expands via "the definition of shift" (OrdinalShift) to get u = v ⊕ δ(n₁, m), then uses TA0's result-length identity and OrdinalDisplacement's #δ(n₁, m) = m. ✓ logically.
4. TS4 invoked with (u, d): preconditions d ≥ 1, #u = m both hold — gives `shift(u, d) > u`. ✓
5. Substitution chain: `shift(v, n₂) = shift(u, d) > u = shift(v, n₁)`. ✓
6. Formal contract matches the property statement exactly. ✓

**Dependency check:**

| Dependency | Declared? | Used? |
|---|---|---|
| TS3 | Yes | Yes — decomposition step |
| TS4 | Yes | Yes — strict increase on u |
| TA0 | Yes | Yes — result-length identity |
| OrdinalShift | **No** | **Yes** — "By the definition of shift, u = v ⊕ δ(n₁, m)" |
| OrdinalDisplacement | **No** | **Yes** — #δ(n₁, m) = m used to conclude #u = m |

The proof explicitly invokes OrdinalShift to expand `shift(v, n₁) = v ⊕ δ(n₁, m)` and OrdinalDisplacement to obtain `#δ(n₁, m) = m`. Neither is listed in the dependency block. Without these two definitions, the declared dependencies alone cannot establish `#shift(v, n₁) = m` — TS3's frame condition only covers the double-shift length, TS4 says nothing about length, and TA0 requires the ⊕/δ expansion to be applicable.

```
RESULT: FOUND

**Problem**: The proof uses OrdinalShift and OrdinalDisplacement without declaring
them as dependencies. Specifically, the sentence "By the definition of shift,
u = v ⊕ δ(n₁, m), and by TA0 (result-length identity), #u = #δ(n₁, m) = m"
requires OrdinalShift to expand shift into ⊕ and OrdinalDisplacement to know
that #δ(n₁, m) = m. Neither appears in the dependency list.

**Required**: Add OrdinalShift and OrdinalDisplacement to the declared dependencies
of TS5, with brief justifications (e.g., "Expands shift to tumbler addition for
length verification" and "Supplies #δ(n, m) = m for the length argument").
```

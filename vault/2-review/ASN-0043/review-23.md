## Foundation Consistency Check: ASN-0043

### 1. Stale Labels

All foundation citations exist in the current foundation statements:

- ASN-0034: T4, T7, T12, T9, T10, T10a, TA5(d), T3, T5, T6, T1, T2, T0(a), OrdinalDisplacement, OrdinalShift — all present ✓
- ASN-0036: S0, S1, S3, S4, S5, S7, S7a, S7b, origin() — all present ✓

(none)

### 2. Local Redefinitions

Checked each `introduced` entry against the full foundation:

- `GlobalUniqueness`: S4 (ASN-0036) covers only I-addresses; GlobalUniqueness generalizes to all element-level allocations. Distinct scope — correctly `introduced`.
- `home(a)`: `origin(a)` in ASN-0036 is defined for `dom(Σ.C)` only; `home(a)` applies the same formula to `dom(Σ.L)`. New function — correctly `introduced`.
- `PrefixSpanCoverage`, `coverage(e)`, `Endset`, `Link`, `L0–L14`: none of these appear in ASN-0034 or ASN-0036.

(none)

### 3. Structural Drift

Spot-checked all restated foundation content:

- T12 invocation in Endset definition: `ℓ > 0` and `k ≤ #s` — matches T12 exactly ✓
- T7 application in L0: `a.E₁ ≠ b.E₁ ⟹ a ≠ b` — matches T7 exactly ✓
- S3 restatement in L14: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — matches S3 exactly ✓
- OrdinalShift result in PrefixSpanCoverage: `shift(x, 1) = [x₁, ..., x_{#x−1}, x_{#x} + 1]` — consistent with OrdinalShift + TumblerAdd ✓
- S7 parallel in GlobalUniqueness section: "T9, T10, T10a + TA5(d) + T3" — matches S7's "Follows from" list (T4 is implicitly covered through `origin`'s field decomposition, which ASN-0043 inherits by citing `origin` directly) ✓

(none)

### 4. Missing Dependencies

Declared depends: ASN-0034, ASN-0036. Every cross-ASN citation in the body traces to one of these two. No references to any other ASN appear.

(none)

### 5. Exhaustiveness Gaps

Scanned all "all" claims:

- L14 claims `dom(Σ.C) ∪ dom(Σ.L)` is the complete set of stored entities — consistent with ASN-0036's two-component state `(Σ.C, Σ.M)` plus the new `Σ.L`; no third stored-entity component exists in the foundation ✓
- L3 claims `|Σ.L(a)| ≥ 2` — no foundation property imposes a conflicting bound ✓
- L12 transition claim covers all state transitions — no foundation operation escapes its scope ✓

(none)

### 6. Registry Mismatches

Checked each table entry for body/table consistency:

- `GlobalUniqueness | LEMMA | introduced`: body contains a derivation by analogy with S4 citing T9, T10, T10a, TA5, T3. Correctly `introduced` with local argument ✓
- `L4 | LEMMA | introduced`: body contains a formal statement plus design commentary on absences. Listed as `introduced`; body provides local formal content ✓
- `L9 | LEMMA | introduced`: body contains a full state-construction proof. Correctly `introduced` ✓
- `PrefixSpanCoverage | LEMMA | introduced`: body contains a complete proof. Correctly `introduced` ✓
- All other entries: table type and body content are consistent ✓

No property listed as `cited` that contains a local proof; no property listed as `introduced` that merely restates a foundation statement.

(none)

---

`RESULT: CLEAN`

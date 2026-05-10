## Foundation Consistency Check: ASN-0036

### 1. Stale Labels
(none)

All cited foundation labels — T0(a), T1, T2, T3, T4, T5, T8, T9, T10, T10a, TA5(c), TA7a — exist in the ASN-0034 foundation with matching names and content.

### 2. Local Redefinitions
(none)

All properties listed as `introduced` (S0–S9, D-CTG, D-MIN, D-SEQ, ValidInsertionPosition, Σ.C, Σ.M(d), etc.) are new to this ASN. The `origin(a)` function is constructed from T4's `fields(t)` but is not a redefinition of anything in the foundation. The "correspondence run" concept in S8 is structurally related to but distinct from T12 (SpanWellDefinedness).

### 3. Structural Drift
(none)

All foundation definitions are applied faithfully. TumblerAdd's result-length identity is used correctly. TA7a's subspace closure is applied as stated. T4's field hierarchy and zero-count correspondence are applied correctly in S7b and S8a.

### 4. Missing Dependencies
(none)

Every foundation citation points to ASN-0034, the only declared dependency.

### 5. Exhaustiveness Gaps
(none)

### 6. Registry Mismatches

**Finding — D-CTG-depth table entry omits foundation dependencies used in its proof.**

Properties table entry:
> `D-CTG-depth | Shared prefix reduction: at depth m ≥ 3, contiguity reduces to the last component | corollary from D-CTG, S8-fin, S8-depth`

Body proof (in the "Arrangement contiguity" section) explicitly cites two ASN-0034 properties by name:

- **T0(a) (UnboundedComponentValues):** `"By T0(a), unboundedly many values of n exist, yielding infinitely many distinct positions in V_S(d) — contradicting S8-fin."`
- **T1 (LexicographicOrder):** `"By T1(i), w > v₁"` and `"By T1(i), w < v₂"`

T0(a) is load-bearing: without the guarantee that arbitrarily large component values exist, the proof cannot produce infinitely many intermediates and the contradiction with S8-fin does not go through. T1 is the ordering principle invoked twice to establish the sandwich `v₁ < w < v₂`.

The table entry "corollary from D-CTG, S8-fin, S8-depth" implies the corollary follows from local properties only. The body contradicts this by citing two foundation properties explicitly.

---

`RESULT: 1 FINDING`

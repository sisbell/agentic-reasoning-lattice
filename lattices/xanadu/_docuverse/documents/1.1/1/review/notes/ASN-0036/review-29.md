## Foundation Consistency Check: ASN-0036

### 1. Stale Labels

All cited labels exist in the ASN-0034 foundation: T0(a), T1, T3, T4, T5, T8, T9, T10, T10a, TA5 (with subcases (c) and (d)), TA7a, OrdinalShift, TumblerAdd.

(none)

### 2. Local Redefinitions

No ASN-0036 `introduced` property duplicates a foundation statement. The closest candidates:
- **S1** (store monotonicity): the body notes it is "the content-store specialisation of T8," but T8 is about address persistence in the abstract address space; S1 adds the value-preservation requirement. Distinct statement, correctly `introduced`.
- **OrdinalShift / OrdinalDisplacement**: used throughout but cited from the foundation, not redefined locally.

(none)

### 3. Structural Drift

All restatements of foundation content are accurate:
- T4 field correspondence (`zeros = 0/1/2/3`) reproduced correctly in S7b and S8a.
- T8 (AllocationPermanence) characterised correctly as address-only persistence; S1 explicitly extends it to values.
- TA5(c)/(d) subcases cited correctly: (c) gives `#t' = #t` for siblings, (d) gives `#t' = #t + k` for children — matches the singleton-decomposition proof and S4 derivation.
- T10 (PartitionIndependence) applied correctly: [s₁] ⋠ [s₂] when s₁ ≠ s₂ since neither single-component tumbler is a prefix of the other.
- TA7a (SubspaceClosure) used for subspace-closure of ordinal displacement; the simplest case `[x] ⊕ [k] = [x+k]` follows from TumblerAdd's result-length identity and TA7a's closure guarantee.

(none)

### 4. Missing Dependencies

All property citations are to ASN-0034, the sole declared dependency. No other ASN's formal statements are invoked.

(none)

### 5. Exhaustiveness Gaps

The S4 proof covers three allocator-distinctness cases:
1. Same allocator — T9
2. Different allocators, non-nesting prefixes — T10
3. Different allocators, nesting prefixes (ancestor-descendant) — T10a + TA5(d) + T3

These three cases are exhaustive over all possible allocator relationships. Grandparent-grandchild depth differences are covered by the depth argument (TA5(d) is applied recursively through each spawning level), and T3 guarantees distinct tumblers of different depths. No foundation properties are omitted from the coverage.

(none)

### 6. Registry Mismatches

Cross-checking each properties-table status against the body:

- **S1** — table: `corollary of S0`; body: "S1 is a corollary of S0." ✓
- **S4** — table: `from T9, T10, T10a, TA5, T3 (ASN-0034)`; body derives it from exactly those properties (citing TA5(d) specifically, subsumed by TA5). ✓
- **S5** — table: `consistent with S0–S3 (witness construction)`; body gives a witness construction (explicit states Σ_N and Σ'_N). ✓
- **S6** — table: `corollary of S0`; body: "S6 is a consequence of S0." ✓
- **S7** — table: `from S7a, S7b, T4, T9, T10 (ASN-0034)`; body: "S7 follows from S7a... S7b... and T4... Since I-addresses are permanent (S0) and unique (S4)." ✓
- **S8** — table: `theorem from S8-fin, S8a, S2, S8-depth, T1, T5, T10, TA5(c), TA7a (ASN-0034)`; body contains a full local proof from exactly these. ✓
- **D-CTG-depth** — table: `corollary from D-CTG, S8-fin, S8-depth, T0(a), T1 (ASN-0034)`; body has a contradiction proof citing all of these. ✓
- **D-SEQ** — table: `corollary from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth`; body derivation uses these (ASN-0034 transitives captured in D-CTG-depth). ✓
- **S9** — table: `theorem from S0`; body: two-line proof citing only S0. ✓
- **S8-depth** — table: `design requirement`; body: "This is a design requirement, not a convention." ✓

(none)

---

`RESULT: CLEAN`

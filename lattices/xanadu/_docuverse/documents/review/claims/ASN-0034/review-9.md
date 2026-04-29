# Proof Review — ASN-0034 (cycle 2)

*2026-04-08 17:57*

32 properties (GlobalUniqueness, OrdinalShift, PartitionMonotonicity, PositiveTumbler, T10, T10a, T10a-N, T10a.1, T10a.2, T10a.3, T4, T4a, T4b, T4c, T5, T6, T7, T8, T9, TA-LC, TA-RC, TA5, TA5-SIG, TA5-SigValid, TA5a, TA6, TA7a, TS1, TS2, TS3, TS4, TS5)

### TA6

Looking at the proof of TA6 (ZeroTumblers) against the verification checklist:

**1. Precondition completeness** — The inputs (zero tumbler, tumbler with positive component) are fully stated. OK.

**2. Case coverage** — Conjunct 1 covers #t = 0 and #t ≥ 1 (exhaustive). Conjunct 2 covers k ≤ m and k > m (exhaustive), including the edge case where s is empty (m = 0 falls into Case 2 since k ≥ 1 > 0). OK.

**3. Postcondition establishment** — Both conjuncts are fully proved, reaching the claimed conclusions. However, there is an error in the justification chain (see below).

**4. All conjuncts addressed** — Both conjuncts proved. OK.

**5. Dependency correctness** — T1 is used in Conjunct 2 for the ordering definition. T4 is used in Conjunct 1 for the positive-component and non-empty field constraints. No undeclared or unused dependencies. OK.

**6. Formal contract** — Two postconditions matching the two conjuncts. Matches the property statement. OK.

**7. Missing guarantees** — None. The proof only relies on T1, T4, and properties of natural numbers. OK.

**Issue found in Conjunct 2, Case 1:**

The text states:

> "Since k ≤ m ≤ min(m, n), this is a divergence within the shared length."

The chain `k ≤ m ≤ min(m, n)` asserts `m ≤ min(m, n)`, which requires `m ≤ n`. Nothing in the case assumptions establishes `m ≤ n`.

Counterexample to the chain: let `s = [0, 0, 0, 0, 0]` (m = 5) and `t = [0, 1]` (n = 2). Then `k = 2`, and Case 1 applies since `k = 2 ≤ 5 = m`. The chain claims `2 ≤ 5 ≤ min(5, 2) = 2`, but `5 ≤ 2` is false.

The *conclusion* `k ≤ min(m, n)` is correct — it follows from `k ≤ m` (case assumption) and `k ≤ n` (by definition, since `k ∈ {1, …, n}`) — but the stated justification chain contains a false intermediate claim.

```
RESULT: FOUND

**Problem**: In Conjunct 2, Case 1, the inequality chain "k ≤ m ≤ min(m, n)" is
false when m > n. The step m ≤ min(m, n) requires m ≤ n, which is not given.
Concrete counterexample: s = [0,0,0,0,0] (m=5), t = [0,1] (n=2), k=2 — the
chain asserts 5 ≤ min(5,2) = 2, which is false.

**Required**: Replace "Since k ≤ m ≤ min(m, n)" with a correct derivation:
"Since k ≤ m (case assumption) and k ≤ n (by definition of k as an element
of {1, …, n}), we have k ≤ min(m, n)."
```

### T10a

## Verification

### Checklist Analysis

**1. Precondition completeness** — T10a is a design axiom constraining allocator behavior. The axiom statement is clear and complete. ✓

**2. Case coverage** — Three consequences plus necessity are enumerated and addressed. ✓

**3. Postcondition establishment** — T10a.1, T10a.2, T10a.3 are each argued. T10a-N asserts necessity but does not construct a concrete counterexample (e.g., a specific base `b` and siblings `s₁ = inc(b, 0)`, `s₂ = inc(b, 1)` where `s₁` is a prefix of `s₂`). The argument says relaxing "permits prefix nesting" without demonstrating a witness pair. Minor concern but not the primary issue.

**4. All conjuncts addressed** — T10a.1, T10a.2, T10a.3, T10a-N are all present. ✓

**5. Dependency correctness** — **Problem found.** The Dependencies section declares **(none)**, yet the proof explicitly invokes:
   - **TA5(c)**: `#inc(t, 0) = #t` — used in Consequence 1 (T10a.1)
   - **TA5(d)**: `#inc(t, k) = #t + k` for `k > 0` — used in Consequence 3 (T10a.3) and T10a-N
   - **T10** (PartitionIndependence): its precondition is what T10a.2 claims to satisfy
   - **Prefix** property: "tumblers of equal length are prefix-related only if identical" — used in Consequence 2 (T10a.2)

   Four dependencies are used but none are declared.

**6. Formal contract** — The contract correctly uses *Axiom* for the core constraint and *Postconditions* for the derived consequences. The fields match the narrative. ✓

**7. Missing guarantees** — Because TA5, T10, and Prefix are not provided as ground truth, the derived postconditions (T10a.1–T10a.3, T10a-N) cannot be verified against their stated foundations. The reasoning *appears* sound if those properties say what the proof claims, but this cannot be confirmed from the provided dependencies alone.

---

```
RESULT: FOUND

**Problem**: The proof derives T10a.1–T10a.3 and T10a-N using four properties
(TA5(c), TA5(d), T10, Prefix) that are not declared in the dependency list.
The dependency section states "(none)" while the justification text explicitly
invokes all four. Without these as declared and verified dependencies, the
derived postconditions rest on ungrounded appeals.

**Required**: Declare TA5, T10, and Prefix as dependencies of T10a so that
the derivations of T10a.1, T10a.2, T10a.3, and T10a-N can be verified
against their stated foundations.
```

### GlobalUniqueness

RESULT: FOUND

**Problem**: The proof attributes the child-spawning output `c₀ = inc(t, k')` to the parent allocator ("c₀ itself is the parent's output, not a child sibling output"), but Case 1 relies on T9, which is explicitly scoped to the sibling stream — the `inc(·, 0)` sequence. T9's proof defines `same_allocator(a, b)` as "both `a` and `b` appear in this sequence," referring to `t₀, t₁ = inc(t₀, 0), t₂ = inc(t₁, 0), …`. Child-spawning outputs are produced by `inc(·, k')` with `k' > 0` and are not in any allocator's sibling stream.

This leaves two classes of pairs uncovered by the case analysis:

1. **Child-spawning output vs. parent sibling** (e.g., `c₀ = inc([1], 2) = [1,0,1]` vs. parent sibling `[2]`): Both are attributed to the parent allocator → Case 1. But `same_allocator(c₀, [2])` is false under T9's definition, so T9 cannot establish ordering. The pair also doesn't qualify for Cases 2–4, which require *different* allocators.

2. **Two child-spawning outputs from the same parent** (e.g., `c₁ = inc([1], 2) = [1,0,1]` and `c₂ = inc([2], 2) = [2,0,1]`): Both attributed to the parent → Case 1. Again, neither is in the parent's sibling stream, so T9 does not apply.

These pairs are trivially distinct (by length for class 1, by TA5(b) and T3 for class 2), but the proof's case partition does not handle them.

**Required**: Reclassify `c₀` as the child allocator's base address (`t₀` in the child's sequence) rather than a parent output. T9 already includes `t₀` in the allocator's sequence and proves `t₀ < t₁` as its base case, so `c₀` vs. child siblings is covered by Case 1. Under this classification:

- `c₀` vs. parent siblings → different allocators (child vs. parent), nesting prefixes, and length separation (`γ + k'` vs. `γ`) gives `a ≠ b` by T3 via Case 4.
- Two child-spawning outputs from the same parent (now bases of different child allocators) → different allocators with non-nesting prefixes (they differ at position `γ`, inherited from distinct parent siblings via TA5(b)) → Case 2.

This also eliminates the need for the "separate treatment" paragraph: all child allocations (including `c₀`) have uniform length `γ + k'` by TA5(c)–(d), which differs from parent sibling length `γ`, so length separation in Case 4 covers every parent-vs-child pair without special cases.

The sentence to remove: "And `c₀` itself is the parent's output, not a child sibling output, so no double-counting occurs." Replace with a note that `c₀` is the child allocator's base address, produced by the parent's `inc(·, k')` and assigned as the child's `t₀`.

### OrdinalShift

## Verification of OrdinalShift

**Checking preconditions of TA0 application.** The proof invokes TA0 to establish that `shift(v, n) = v ⊕ δ(n, m) ∈ T`. TA0 requires four preconditions:

| TA0 Precondition | Checked in proof? |
|---|---|
| `a ∈ T` (i.e., `v ∈ T`) | Assumed from precondition ✓ |
| `w ∈ T` (i.e., `δ(n, m) ∈ T`) | **Not verified** |
| `w > 0` (i.e., `δ(n, m) > 0`) | **Not verified** |
| `actionPoint(w) ≤ #a` | Verified: "action point of δ(n, m) is m = #v, so k ≤ #v holds trivially" ✓ |

The proof only explicitly checks one of the four TA0 preconditions. The other two (`δ(n, m) ∈ T` and `δ(n, m) > 0`) are true but require reasoning from a definition of δ that is not among the provided dependencies.

**Checking dependency completeness.** The proof relies on properties of `δ(n, m)` — specifically its definition as `[0, ..., 0, n]` of length m, its membership in T, its positivity when `n ≥ 1`, its action point being m, and its length being m. Neither TA0 nor TumblerAdd defines or establishes any of these. The definition of δ is an undeclared dependency.

**Checking postconditions.** All four postconditions are established, assuming δ's properties hold:
- `shift(v, n) ∈ T` — via TA0 (if all preconditions met) ✓
- `#shift(v, n) = #v` — via TumblerAdd result-length identity: `#(v ⊕ δ(n,m)) = #δ(n,m) = m = #v` ✓
- `shift(v, n)ᵢ = vᵢ for i < m` — via TumblerAdd prefix copy rule ✓
- `shift(v, n)ₘ = vₘ + n ≥ 1` — via TumblerAdd action-point rule; `vₘ ≥ 0` (since `v ∈ T`) and `n ≥ 1` give `vₘ + n ≥ 1` ✓

**Checking formal contract.** The contract has Preconditions, Definition, and Postconditions — appropriate for this property. The contract matches the narrative. ✓

```
RESULT: FOUND

**Problem**: The proof depends on δ(n, m) — its definition, membership in T, positivity,
action point, and length — but δ is not defined in either declared dependency (TA0,
TumblerAdd) and is not listed as a dependency. Consequently, when applying TA0, the
preconditions δ(n, m) ∈ T and δ(n, m) > 0 are assumed without verification.

**Required**: Either (a) add the definition of δ (likely "DeltaDisplacement" or similar)
as an explicit dependency, so that δ(n, m) ∈ T, δ(n, m) > 0, actionPoint(δ(n, m)) = m,
and #δ(n, m) = m are established facts; or (b) inline the construction and verify these
properties within the OrdinalShift proof itself, explicitly checking all four TA0
preconditions before invoking it.
```

28 verified, 4 found.

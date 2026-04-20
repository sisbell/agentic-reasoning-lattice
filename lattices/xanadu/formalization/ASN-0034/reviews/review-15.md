# Proof Review — ASN-0034 (cycle 1)

*2026-04-08 22:51*

62 properties

### TumblerAdd

RESULT: FOUND

**Problem**: The definition pivots on "action point `k`" and the formal contract references `actionPoint(w)` in its precondition, but the action point function is never defined within this property section. The dependency list is "(none)", so no external definition is declared either. Without a formal definition of `k` (e.g., `k = min{i : wᵢ ≠ 0}`), the three-case construction cannot be evaluated and the precondition `actionPoint(w) ≤ #a` cannot be checked. This is a dependency used but not declared.

Additionally, the postcondition `a ⊕ w ∈ T` appears in the formal contract but is not established in the narrative. The result-length identity `#(a ⊕ w) = #w` is derived algebraically from the construction, but tumbler membership of the result is simply asserted — the proof does not verify that the constructed sequence satisfies whatever well-formedness constraints T requires.

**Required**:
1. Declare the action point definition as a dependency (or define it inline within this section).
2. Either derive `a ⊕ w ∈ T` from the construction — showing the result satisfies tumbler well-formedness — or remove it from the postconditions and establish it in a separate property that depends on TumblerAdd.

### PositiveTumbler

## Verification of PositiveTumbler

### Checklist Analysis

**1. Precondition completeness** — The definition is clear and complete: positive means `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`, zero tumbler means `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`. No missing assumptions.

**2. Case coverage** — The informal argument mentions two sub-cases ("smaller component" and "has run out of components") corresponding to T1 cases (i) and (ii), but does not separate them or verify the agreement precondition that T1 requires at all positions before the witness.

**3. Postcondition establishment** — The formal contract claims a postcondition `(A t ∈ T, z ∈ T : t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t)`, but the property section has **no `*Proof.*` block**. The only argument is one sentence:

> "if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (0 < tₖ) or has run out of components, either way placing it below `t`."

This does not constitute a proof. It does not specify that `k` must be the *first* nonzero component (needed to ensure `tᵢ = 0$ for `i < k`, matching `zᵢ = 0`). It does not verify the T1 agreement condition `(A i : 1 ≤ i < k : zᵢ = tᵢ)`. It does not distinguish the two T1 cases with explicit witnesses. The postcondition is asserted but not established.

**4. All conjuncts** — The definition conjunct is fine. The postcondition conjunct is unproved.

**5. Dependency correctness** — T1 is genuinely needed for the ordering claim. T3 is implicitly used (sequence equality). TA0 and TA4 are referenced only for motivational context ("The condition `w > 0` in TA0 and TA4 excludes...") and are not used in proving the postcondition — they are not true dependencies.

**6. Formal contract** — The contract structure (Definition + Postconditions) correctly matches the property's nature. The formulas match the narrative claims.

**7. Missing guarantees** — None. The postcondition follows from T1 and the definition; no additional properties are needed.

---

```
RESULT: FOUND

**Problem**: The postcondition `(A t ∈ T, z ∈ T : t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t)` is stated in the formal contract but has no `*Proof.*` block. The one-sentence informal argument does not construct a T1 witness, does not verify the agreement condition `(A i : 1 ≤ i < k : zᵢ = tᵢ)`, and does not specify that `k` must be the first nonzero component of `t`. Two cases need explicit treatment:
  - Case `#z ≥ k` (where `k` is the first nonzero position of `t`): witness `k` via T1 case (i), since `zᵢ = 0 = tᵢ` for `i < k` and `zₖ = 0 < tₖ`.
  - Case `#z < k`: witness `#z + 1` via T1 case (ii), since `zᵢ = 0 = tᵢ` for all `i ≤ #z` (because `#z < k` implies `tᵢ = 0` at those positions) and `#z + 1 ≤ k ≤ #t`.

**Required**: Add a `*Proof.*` block with explicit case analysis on the relationship between `#z` and the first nonzero position of `t`, constructing the T1 witness and verifying the agreement precondition in each case.
```

### PartitionMonotonicity

## Verification Analysis

**Checking the "Total ordering" section carefully.**

The proof's final combining argument claims:

> "Every address in the partition belongs to exactly one sub-partition — the unique sub-partition whose prefix it extends (uniqueness follows from non-nesting)."

This is false. The root prefix `p` of the partition satisfies `p ≼ p`, so `p` is in the set `{t ∈ T : p ≼ t}`, and `p` is an allocated address. But every sub-partition prefix `tᵢ` has `#tᵢ = #t₀ = #s + k > #p` (since `p ≼ s` gives `#s ≥ #p`, and `k > 0` gives `#t₀ > #s ≥ #p`). Since `#tᵢ > #p`, no `tᵢ` can be a prefix of `p`, so `p` does not extend any sub-partition prefix. The root address `p` belongs to the partition but to no sub-partition.

The "Total ordering" argument only compares pairs where both addresses belong to some sub-partition `tᵢ` or `tⱼ`. It never considers a comparison between `p` and any other allocated address `a` in the partition. Consequently, the proof does not establish that `p` is comparable with every other allocated address.

The inductive step handles this situation correctly for inner levels — it explicitly shows "the root address `tᵢ` precedes every other address in the sub-partition" via T1 case (ii). But the top-level "Total ordering" section has no analogous treatment for `p`.

```
RESULT: FOUND

**Problem**: The "Total ordering" paragraph claims "Every address in the partition
belongs to exactly one sub-partition," but the partition root `p` is in `{t ∈ T :
p ≼ t}` and does not extend any sub-partition prefix `tᵢ` (since `#tᵢ > #p`).
The combining argument only handles pairs where both addresses belong to sub-
partitions, so comparisons involving `p` are never established. The total ordering
claim is incomplete.

**Required**: Add a root-address case to the "Total ordering" section, mirroring
the pattern already used in the inductive step: for any allocated `a ≠ p` with
`p ≼ a`, the proper prefix relation `p ≺ a` (hence `#p < #a`) gives `p < a` by
T1 case (ii). Then partition the remaining pairs into the existing sub-partition
cases.
```

### T0(b)

RESULT: FOUND

**Problem**: The formal contract labels T0(b) as an *Axiom*, but the property is derived from T0, not posited. The narrative itself states "T0(b) follows from T's definition as the set of all finite sequences over ℕ," and a full proof is given. An axiom is "a fundamental assertion by definition or design, not derived" — T0(b) is derived. Additionally, the contract content embeds proof reasoning ("Since there is no upper bound on the length of finite sequences, for any `n ≥ 1`, the constant sequence of `n` ones is a member of T with `#t = n ≥ n`") rather than stating a clean guarantee. Compare with T0(a), which correctly uses *Postcondition* for an analogous derived property.

**Required**: Replace the formal contract with a *Postcondition* field containing a clean statement of the guarantee, parallel to T0(a)'s contract:

```
*Formal Contract:*
- *Postcondition:* For every `n ∈ ℕ` with `n ≥ 1`, there exists `t ∈ T` with `#t ≥ n`.
```

58 verified, 4 found.

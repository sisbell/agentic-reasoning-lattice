# Contract Review — ASN-0034 (cycle 1)

*2026-04-08 18:40*

### PartitionMonotonicity

- `INACCURATE: The precondition says "sub-partition prefixes t₁, t₂, ... produced by the child-level allocator's sibling stream via inc(·, 0) starting from t₀," implicitly excluding t₀ from the set of sub-partition prefixes. But the proof treats t₀ as the first sub-partition prefix throughout. The non-nesting argument is applied to the full sequence t₀, t₁, t₂, ... ("Applying this inductively from t₀ ... we obtain #tₙ = #t₀ for all n ≥ 0"). The cross-partition ordering section says "Take two sibling sub-partition prefixes tᵢ and tⱼ with i < j" using i ranging over all n ≥ 0. The total ordering section likewise iterates over sub-partitions tᵢ for all i ≥ 0. Since t₁ = inc(t₀, 0) has the same length as t₀ (TA5(c)), t₀ and t₁ are non-nesting, and t₀ heads its own distinct sub-partition. The precondition should read "sub-partition prefixes t₀, t₁, t₂, ... where t₀ is the initial child prefix and tₙ₊₁ = inc(tₙ, 0) for n ≥ 0"; postconditions (1) and (2) should correspondingly be understood to cover i ≥ 0.`

### PositiveTumbler

`

- `MISSING_POSTCONDITION: PositiveTumbler proof section asserts: every positive tumbler is strictly greater (under T1) than every zero tumbler of any length — formally (A t ∈ T, z ∈ T : t > 0 ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t). This ordering consequence is not captured in the contract.`

### T10a

**

- `INACCURATE: T10a.3 states #c ≥ m + k' and #output ≥ m + k'₁ + … + k'_d, but the proof establishes exact equality throughout. T10a.1 gives exact length preservation for siblings (#sibling = #base, via TA5(c): #inc(t, 0) = #t), and TA5(d) gives the exact spawning length (#inc(t, k') = #t + k'). Combining these, child outputs have length exactly m + k', and the multi-level case is #output = m + k'₁ + … + k'_d. The proof says "the separation is additive," characterizing an exact value, not a bound. The contract should use = throughout in T10a.3.`

3 mismatches.

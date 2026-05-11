# Review of ASN-0036

## REVISE

### Issue 1: S8 contract's S8a precondition is incompletely restated

**ASN-0036, S8 Formal Contract, Preconditions**: "`(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1)` (S8a)"

**Problem**: S8a is stated earlier as a three-conjunct property: `zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : 1 ≤ i ≤ #v : vᵢ > 0)`. The contract's inline summary omits `#v ≥ 2` (the depth bound) and replaces componentwise positivity with `v₁ ≥ 1`. The S8 proof relies on the full S8a, particularly `#v ≥ 2`:
- The within-subspace incompatibility lemma's case split forces `j ≥ 2` (using positive first component) and then proceeds with `m ≥ 2`.
- The cross-subspace uniqueness argument explicitly notes "`shift(v, 1)` also extends `[S₁]`: ... since `m ≥ 2`, this includes position 1".
- The argument that `shift(v, 1)` preserves the subspace identifier requires `#v ≥ 2`.

**Required**: Either drop the inline summary and reference S8a by label alone (matching how S8-fin, S2, S3, S8-depth are referenced), or restate the full three-conjunct form. The current partial summary may mislead a reader who treats the contract as authoritative without consulting S8a's definition.

### Issue 2: S8 dependency listing includes TA5 but the proof does not use TA5

**ASN-0036, Properties Introduced table, S8 row**: "theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034)"

**Problem**: The S8 proof explicitly invokes TumblerAdd's three-region component formula, OrdinalShift (for `shift(v, 1) = v ⊕ δ(1, m)`), OrdinalDisplacement, and TS4 (`v ≤ shift(v, 1)`), plus T1, T3, T5, T10, and NAT-discrete (for the `v_m + 1` reasoning in the case `j = m`). TA5 (HierarchicalIncrement) is the `inc(t, k)` operator and appears nowhere in S8's proof. TA5(c) is mentioned only in motivational prose about why non-trivial runs arise operationally — that prose is not a proof step.

For comparison, OrdShiftHom's row in the same table correctly cites "OrdinalShift, OrdinalDisplacement"; TA5 is not analogously listed there. The S8 entry is the only spurious citation.

**Required**: Replace "TA5" with the operators actually consumed — `TumblerAdd`, `OrdinalShift`, `OrdinalDisplacement`, `TS4` — or drop TA5 if the table's intent is "tumbler-arithmetic family" without enumeration.

## OUT_OF_SCOPE

No additional out-of-scope items beyond those already enumerated in the Open Questions and Scope sections.

VERDICT: REVISE

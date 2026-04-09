# Proof Review — ASN-0034 (cycle 4)

*2026-04-08 18:20*

8 properties (GlobalUniqueness, PartitionMonotonicity, T10a, T10a.1, T10a.2, T10a.3, T8, T9)

### T10a

## Verification of T10a (AllocatorDiscipline)

**Checklist 1–4 (Logic):** The reasoning is sound. Each consequence follows correctly from the stated premises:

- **T10a.1**: `inc(·, 0)` + TA5(c) → uniform length. ✓
- **T10a.2**: Equal length + Prefix → incomparability. ✓
- **T10a.3**: Single-level case from TA5(d); multi-level by induction. ✓ (induction is implicit but straightforward)
- **T10a-N**: Concrete counterexample correctly applies TA5(b) + TA5(d) to invoke T1 case (ii), establishing a₁ ≺ a₂. ✓

**Checklist 6 (Formal contract):** Axiom + Postconditions structure is appropriate for a design constraint with derived consequences. All four sub-properties are listed. ✓

**Checklist 5 (Dependency correctness):** The proof explicitly invokes five external properties — **TA5** (subclauses b, c, d), **T10** (PartitionIndependence), **T1** case (ii), and **Prefix** (PrefixRelation) — but the declared dependency list is empty.

```
RESULT: FOUND

**Problem**: The proof uses five undeclared dependencies. The justification
explicitly relies on TA5(b) (prefix agreement for k > 0), TA5(c) (#inc(t,0) = #t),
TA5(d) (#inc(t,k) = #t + k for k > 0), T10 (PartitionIndependence precondition),
T1 case (ii) (proper-prefix definition), and Prefix (PrefixRelation — equal-length
tumblers are prefix-related only if identical). None of these appear in the
Dependencies section, which lists "(none)".

**Required**: Declare TA5, T1, T10, and Prefix (PrefixRelation) as dependencies
of T10a. All four are load-bearing: TA5 supplies the length postconditions used
in every consequence; T1 and Prefix supply the prefix logic for T10a.2 and T10a-N;
T10 is the property whose precondition T10a is designed to satisfy.
```

7 verified, 1 found.

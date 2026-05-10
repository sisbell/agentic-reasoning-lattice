# Review of ASN-0001

Based on Dafny verification — modeling-1 (30 properties)

## REVISE

### Issue 1: TA3 strict order preservation is too strong

The ASN claims TA3 holds strictly and unconditionally:

> **TA3 (Order preservation under subtraction).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)`.

And later emphasizes:

> "The strict form of TA3 holds without additional preconditions — unlike TA1, there is no weak/strict split."

The Dafny verification found a counterexample that disproves strict preservation. When zero-padding causes both operands to coincide with `w`, the subtraction maps both to the same zero tumbler:

- `a = [1, 0]`, `b = [1, 0, 0]`, `w = [1, 0, 0, 0]`
- `a` padded to length 4: `[1, 0, 0, 0]` = `w` padded to length 4. Result: `[0, 0, 0, 0]`.
- `b` padded to length 4: `[1, 0, 0, 0]` = `w` padded to length 4. Result: `[0, 0, 0, 0]`.
- `a < b` (prefix rule), `a ⊖ w = b ⊖ w` (equality, not strict).

The gap is in the ASN's proof, Case 0. The proof states:

> "If `max(#a, #w) = max(#b, #w)`, then `#a < #b ≤ #w`, and zero-padding makes `a` and `b` differ at position `#a + 1` (where `a` pads to 0 and `b_{#a+1}` is a genuine component)."

The phrase "genuine component" implicitly assumes `b_{#a+1} ≠ 0`, but `b`'s extension can consist entirely of zeros (as in `b = [1, 0, 0]`). When `b`'s components beyond `#a` are all zero, the padded `a` and padded `b` are identical over the range where both are defined, and if `w` is long enough to pad both to the same length, the subtraction produces the same zero tumbler.

**Proposed fix:** Weaken TA3 to match TA1's structure — weak preservation universally, strict under a tighter condition:

> **TA3 (Order preservation under subtraction, weak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

> **TA3-strict.** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

The equal-length precondition eliminates the prefix case entirely (two tumblers of the same length cannot be in a prefix relationship unless equal). For the editing use case — single-component ordinals `[x]` and `[y]` subtracted by `[n]` — `#a = #b = 1` always holds, so TA3-strict applies and editing correctness is unaffected.

The verification section of TA3 and the paragraph beginning "The strict form of TA3 holds without additional preconditions" must be revised accordingly. The claim that "subtraction's zeroing of positions before the divergence point cannot erase the distinction between `a` and `b`" is wrong — when both operands equal `w` after padding, there is no divergence point, and both map to the zero tumbler.

The formal summary table should update TA3's statement to reflect the weak/strict split.

## QUALITY

### File: GlobalUniqueness.dfy — SIMPLIFY

Duplicate include on lines 1-2:

```dafny
include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
```

Remove one.

### File: StrictOrderPreservation.dfy — SIMPLIFY

Bridge lemmas `LessThanFromWitness` and `LessThanImpliesLessAt` are duplicated verbatim in `WeakOrderPreservation.dfy`. Extract into a shared utility module (e.g., `LessThanBridge.dfy`) and import from both.

### File: WeakOrderPreservation.dfy — SIMPLIFY

Same duplication as above — `LessThanFromWitness` and `LessThanImpliesLessAt` should be imported from a shared module.

### File: ZeroTumblerInvalid.dfy — SIMPLIFY

`CompareSeq` and `CompareSound` duplicate the identical functions in `LexicographicOrder.dfy`. Import from `LexicographicOrder` instead.

### File: SubtractionPreservesOrder.dfy — SIMPLIFY

`PadAgreesOnW` (line ~170) has an empty proof body and a trivially provable ensures clause. If the solver doesn't need it as a trigger, remove it. If it is needed, add a one-line comment explaining why.

The `ka < kb` branch at the end of `SubPreservesOrder_General` uses `assert false` without explanation. Add a brief comment documenting why this case is unreachable (a diverges from w before b does, but Subtractable requires a >= w at the divergence while a < b and b still matches w, forcing a < w — contradiction).

### File: SubtractionPreservesOrder.dfy (bridge lemmas) — SIMPLIFY

`LessThanFromWitness` and `LessThanFromPrefix` are also defined here, adding a third copy of `LessThanFromWitness`. These should come from the shared bridge module.

### All other files — PASS

The remaining 24 files are clean and well-structured:

- **AddressPermanence, ForwardAllocation, PartitionIndependence, PartitionMonotonicity, PrefixOrderingExtension, AllocatorDiscipline** — State-based predicates and lemmas, minimal proof bodies, clear structure.
- **CanonicalRepresentation, ContiguousSubtrees, MutualInverse, ReverseInverse, StrictIncrease, SpanWellDefined** — Trivial proof bodies where the solver handles everything. Appropriately sparse.
- **LexicographicOrder** — Verbose but each helper (CompareSeq/Sound/Complete/Equal/Transitive) serves a distinct proof obligation. The four classical order properties are established cleanly.
- **IntrinsicComparison** — Bidirectional equivalence proof is well-decomposed.
- **HierarchicalIncrement** — Good use of the LessThanByPrefix bridge lemma for the child case.
- **HierarchicalParsing, DecidableContainment** — Well-structured predicate hierarchies. FindZero is clean.
- **DualSpaceSeparation** — Good: models both Insert and Delete, proves frame for each, proves transitivity.
- **SubspaceClosure** — Clean single-component closure proofs.
- **SubspaceDisjointness** — HasKZeros/KthZero pattern is complex but necessary for locating the third separator.
- **SubspaceFrame** — Clean frame condition proofs.
- **UnboundedComponents** — Good use of WithComponent as a named constructor for witnesses.
- **OrthogonalDimensions** — Clean decomposition with independence lemmas.
- **WellDefinedAddition, WellDefinedSubtraction** — Trivial, appropriately so.

## SKIP

### Divergence: GlobalUniqueness — prefix-ownership structure

The divergence notes that the ASN "does not specify the prefix-ownership structure explicitly." The ASN does establish this implicitly through T10 (non-nesting prefixes guarantee distinctness) and T10a (allocator discipline constrains prefix creation). The Dafny formalization makes the implicit structure explicit as a `PrefixOwnership` precondition — this is a proof artifact of translating prose reasoning into a formal precondition. The ASN's Global Uniqueness proof covers the same ground through its case analysis. No spec change needed.

### Divergence: OrthogonalDimensions — predicate signature

The proof index recorded `predicate(Displacement)` but the Dafny formalization uses `predicate(Displacement2D, Displacement2D)`. This is a proof-index mapping artifact. The ASN text for TA8 clearly states the property in terms of pairs of displacements. The property is correctly formalized. No spec change needed.

### 27 clean verifications

AddressPermanence, AllocatorDiscipline, CanonicalRepresentation, ContiguousSubtrees, DecidableContainment, DualSpaceSeparation, ForwardAllocation, HierarchicalIncrement, HierarchicalParsing, IntrinsicComparison, LexicographicOrder, MutualInverse, PartitionIndependence, PartitionMonotonicity, PrefixOrderingExtension, ReverseInverse, SpanWellDefined, StrictIncrease, StrictOrderPreservation, SubspaceClosure, SubspaceDisjointness, SubspaceFrame, UnboundedComponents, WeakOrderPreservation, WellDefinedAddition, WellDefinedSubtraction, ZeroTumblerInvalid — all verified without divergence, confirming the ASN properties as stated.

VERDICT: REVISE

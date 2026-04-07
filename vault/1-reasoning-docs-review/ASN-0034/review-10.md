# Review of ASN-0034

Based on Dafny verification — 31 properties, 1 divergence reported

## REVISE

No genuine spec issues found.

## QUALITY

### File: AllocatorDiscipline.dfy — SIMPLIFY

Defines `LastSigRec`, `LastSig`, and `Inc` independently from HierarchicalIncrement.dfy. Both files model TA5's increment operation with separate implementations. AllocatorDiscipline should import `Inc` and `LastSig` from HierarchicalIncrement rather than re-defining them.

```dafny
// AllocatorDiscipline.dfy — lines 12-42: independent LastSig/Inc
function LastSigRec(s: seq<nat>, i: nat): nat ...
function LastSig(t: Tumbler): nat ...
function Inc(t: Tumbler, k: nat): Tumbler ...
```

```dafny
// HierarchicalIncrement.dfy — lines 9-40: same concepts, different implementation
function LastSigRec(s: seq<nat>, i: nat, top: nat): nat ...
function LastSig(t: Tumbler): nat ...
function Inc(t: Tumbler, k: nat): (t': Tumbler) ...
```

Suggested fix: Define `LastSig` and `Inc` once in HierarchicalIncrement (or in a shared helpers module). AllocatorDiscipline imports and uses them. The `LastSigIs` helper lemma in AllocatorDiscipline is specific to that proof and can stay.

### File: SubspaceDisjoint.dfy — SIMPLIFY

Defines `FindZero` identically to DecidableContainment.dfy (same signature, same logic, same postconditions).

```dafny
// SubspaceDisjoint.dfy — lines 8-18
function FindZero(s: seq<nat>, start: nat): nat ...

// DecidableContainment.dfy — lines 9-19
function FindZero(s: seq<nat>, start: nat): nat ...
```

Suggested fix: Extract `FindZero` into a shared field-parsing helpers module. Both SubspaceDisjoint and DecidableContainment import it.

### File: SubtractionStrictOrder.dfy — SIMPLIFY

Defines `SubComponent` helper lemma identically to SubtractionWeakOrder.dfy (same signature, same body, same postcondition).

```dafny
// SubtractionStrictOrder.dfy — lines 13-33
lemma SubComponent(x: Tumbler, w: Tumbler, i: nat) ...

// SubtractionWeakOrder.dfy — lines 17-37
lemma SubComponent(x: Tumbler, w: Tumbler, i: nat) ...
```

Suggested fix: Extract `SubComponent` into a shared subtraction helpers module. Both strict and weak order proofs import it.

### File: SubtractionWeakOrder.dfy — SIMPLIFY

The `SubPrefixCase` lemma (~80 lines) has dense assertion chains with nested conditionals. The structure is sound but some intermediate assertions restate what the solver already knows from earlier bindings. For example:

```dafny
// lines 173-178
forall i | 0 <= i < la
  ensures ra.components[i] == rb.components[i]
{
  assert ra.components[i] == rac[i] == rb.components[i];
}
```

This pattern appears three times in the method. The `forall` wrapper is needed, but the inner assertion body is a single chain the solver can likely close without the explicit intermediate. Similarly, the `rac` padding array (line 155) introduces a proof-only intermediate that forces manual index reasoning for ~30 lines. Consider whether the proof can compare `ra` and `rb` directly using `SubResultsAgreeAtI` and `SubResultZeroBeyondA` without materializing `rac`.

### Remaining files — PASS

AdditionAssociative, AdditionStrictOrder, AdditionWeakOrder, AllocationPermanence, CanonicalRepresentation, ContiguousSubtrees, DecidableContainment, ForwardAllocation, GlobalUniqueness, HierarchicalIncrement, IncrementPreservesValidity, IntrinsicComparison, LexicographicOrder, PartialInverse, PartitionIndependence, PartitionMonotonicity, PrefixOrderingExtension, ReverseInverse, SpanWellDefined, StrictIncrease, SubspaceClosure, SubtractionStrictOrder (logic), UnboundedComponents, UnboundedLength, ValidAddress, WellDefinedAddition, WellDefinedSubtraction, ZeroTumblerSentinel — all clean, appropriately sparse, good decomposition.

## SKIP

### GlobalUniqueness divergence — proof artifact

The Dafny model captures the structural core of GlobalUniqueness: given any of three discriminants (strict ordering, non-nesting prefixes, or length difference), `a ≠ b` follows. The ASN's four-case proof reduces to these three discriminants (Cases 3 and 4 both reduce to length difference). The exhaustiveness argument — that every pair of distinct allocation events satisfies at least one discriminant — is a system-level invariant depending on T9, T10, and T10a as ongoing properties of the allocation state machine. Dafny cannot express "for all allocation events that have ever occurred or will occur" without modeling the full allocation history. The structural core is what matters for the algebra; the exhaustiveness is an allocation-layer argument that the ASN already provides in prose. No spec change needed.

### 30 clean verifications — no action needed

All 30 non-divergent properties verified without requiring any change to the ASN's stated properties. The Dafny preconditions match the ASN's stated conditions (modulo 0-indexing vs 1-indexing). Helper lemmas (e.g., `LessThanIntro`, `LessThanAt`, `SubComponent`) are proof machinery that decompose verification steps — they introduce no independent content beyond the ASN properties they serve.

VERDICT: SIMPLIFY

# Review of ASN-0026

Based on Dafny verification — 18/18 verified, no divergences reported.

## REVISE

No genuine spec issues found. All 18 proved statements faithfully encode the ASN properties.

## QUALITY

### File: FreshInjective.dfy — SIMPLIFY
### File: FreshPositions.dfy — SIMPLIFY
### File: InsertLength.dfy — SIMPLIFY
### File: LeftUnchanged.dfy — SIMPLIFY
### File: RightShifted.dfy — SIMPLIFY

**Missing abstraction (repeated definition).** All five P9 files independently define the same `InsertV` function:

```dafny
function InsertV(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>): ...
{
  v[..p-1] + newAddrs + v[p-1..]
}
```

Each copy attaches different `ensures` clauses. This is five sources of truth for the same operation. If INSERT semantics change, all five files need updating.

**Fix:** Define `InsertV` once in a shared module (e.g., `InsertOps.dfy`) with no `ensures` clauses. Each property file imports it and states its guarantee as a separate lemma:

```dafny
module InsertOps {
  function InsertV(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>): seq<IAddr>
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
  { v[..p-1] + newAddrs + v[p-1..] }
}
```

Then e.g. `LeftUnchanged.dfy` becomes a lemma about `InsertOps.InsertV` rather than a re-definition with a bespoke ensures clause. This separates the operation definition from the property claims — matching the ASN's own structure where P9's four clauses are independent statements about a single operation.

### File: NonInjective.dfy — PASS

The assertion chains in `SelfTransclusionPermitted` and `CrossTransclusionPermitted` are verbose but necessary. They guide the solver through `WellFormed` → `TextOrdinals` → `RangeSet` for the constructed witnesses. Existence proofs with set-comprehension predicates typically need this level of guidance. The structure is mechanical but not redundant.

### File: MappingExact.dfy — PASS

The `Retrieve` equality within `MappingExact` is tautological by definition (`Retrieve` is defined as `s.iota[s.vmap[d][q]]`, then the predicate asserts it equals `s.iota[s.vmap[d][q]]`). However, the predicate also checks `s.vmap[d][q] in Allocated(s)`, which is non-trivial, and the tautology is architecturally intentional — P3 constrains the system to use exactly this retrieval path. The encoding correctly captures the ASN's intent.

### File: CreationBasedIdentity.dfy — PASS
### File: CrossDocVIndependent.dfy — PASS
### File: ISpaceExtension.dfy — PASS
### File: ISpaceImmutable.dfy — PASS
### File: ISpaceMonotone.dfy — PASS
### File: NoAddressReuse.dfy — PASS
### File: NoRefCounting.dfy — PASS
### File: RefStability.dfy — PASS
### File: ReferentiallyComplete.dfy — PASS
### File: ValidInsertPos.dfy — PASS
### File: ViewerIndependent.dfy — PASS

These are clean. Predicate definitions match ASN statements directly. Derived lemmas (NoAddressReuse, NoRefCounting, ISpaceExtension, RefStability, CreationBasedIdentity) have empty bodies — the solver handles them from their preconditions. ViewerIndependent's encoding via a structurally-unused `Viewer` parameter is a clean way to express a negative architectural constraint.

## SKIP

### Proof artifacts: seq-based V-space modeling

The P9 files model V-space as `seq<IAddr>` rather than Foundation's `map<VPos, IAddr>`. Each file notes the isomorphism with Foundation's representation under J1 (dense ordinals). This is a standard Dafny modeling choice — sequences give native support for slicing and concatenation, which maps directly to INSERT's semantics. The isomorphism is stated informally; a formal bridging lemma is not needed at this stage since the seq encoding faithfully represents the ASN's `[1..n_d] -> Addr` total function.

### Clean verifications

All 18 properties verified without requiring additional preconditions, weakened conclusions, or structural changes to the ASN statements. The predicate encodings (P0, P1, P2, P3, P7, P11) map one-to-one with the ASN's mathematical formulations. The derived properties (NO-REUSE, P8, +_ext, REF-STABILITY) follow from their parent axioms as the ASN claims. P4 delegates to ASN-0001's GlobalUniqueness as specified. P5's existence witnesses construct valid states demonstrating both self-transclusion and cross-document transclusion.

VERDICT: SIMPLIFY

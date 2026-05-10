# Review of ASN-0035

Based on Dafny verification — 19/19 properties verified

## REVISE

No genuine spec issues found. All three divergences are proof artifacts (see SKIP).

## QUALITY

### File: AllocationAuthority.dfy — PASS
Minimal precondition predicate with axiom-declared `authorized`. Clean.

### File: AlwaysValidStates.dfy — SIMPLIFY

`ZeroCountAllPositive` is duplicated verbatim in UniformNodeType.dfy (both prove `forall i :: s[i] > 0 ==> ZeroCount(s) == 0`). `ZeroCountImpliesAllPositive` (the converse) is also only needed here but is the natural companion. Both should live in a shared helper — either in TumblerHierarchy.dfy or a dedicated ZeroCountLemmas module — and be imported by both AlwaysValidStates and UniformNodeType.

```dafny
  // In AlwaysValidStates.dfy:
  lemma ZeroCountAllPositive(s: seq<nat>)
    requires forall i :: 0 <= i < |s| ==> s[i] > 0
    ensures TumblerHierarchy.ZeroCount(s) == 0

  // In UniformNodeType.dfy — identical:
  lemma ZeroCountAllPositive(s: seq<nat>)
    requires forall i :: 0 <= i < |s| ==> s[i] > 0
    ensures TumblerHierarchy.ZeroCount(s) == 0
```

Factor into a single shared location and import.

Otherwise the module is well-structured: the four BaptizePreserves* lemmas have empty bodies where the solver suffices (SingleRoot, NodeTree) and minimal bodies where hints are needed (BaptizedNodes, SequentialChildren). The SequentialChildren preservation proof has appropriate case structure — the non-trivial branch (new node `n`) is the only one with a body.

### File: AuthorityPermanence.dfy — PASS
Design constraint as subset predicate on authorization grants. Clean.

### File: BaptismMonotonicity.dfy — PASS
Subset predicate. Clean.

### File: BaptizedNodes.dfy — PASS
Genesis validity proved with one helper call. Clean.

### File: CoordinationFreeDisjointness.dfy — PASS
Empty body — solver derives from NonNesting and AllExtend. Ideal.

### File: ForwardReferenceAdmissibility.dfy — PASS
Single delegation to SpanNonEmpty. Clean.

### File: GhostElement.dfy — PASS
One assert hint for the witness `Tumbler([1])`. Minimal.

### File: IdentityByAssignment.dfy — PASS
Single delegation to CanonicalRepresentation. Clean.

### File: LocalSerializationSufficiency.dfy — PASS
Three helper lemmas (UniqueParent, DistinctParentsDistinctChildren, ChildrenUnchanged) build to the main commutativity result. All have empty bodies. Good decomposition.

### File: NoNodeMutableState.dfy — PASS
Extensional equivalence predicate, universally true by construction. Empty proof body. Clean.

### File: NodeTree.dfy — PASS
Minimal predicate. Clean.

### File: PrefixPropagation.dfy — PASS
Empty body. Clean.

### File: SequentialChildren.dfy — PASS
Minimal predicate. Clean.

### File: SingleRoot.dfy — PASS
Minimal predicate. Clean.

### File: StructuralOrdering.dfy — PASS
Two lemmas, each one-line body calling LessThanIntro at the divergence point. Sparse, correct.

### File: SubtreeContiguity.dfy — PASS
Empty body — T5 falls out of prefix semantics. Ideal.

### File: SubtreeDisjointness.dfy — PASS
Empty body — contradiction from non-nesting prefixes. Ideal.

### File: UniformNodeType.dfy — SIMPLIFY
`ZeroCountAllPositive` duplicated from AlwaysValidStates (see above). Remove and import from shared location.

## SKIP

### Artifact 1: AllInvariants omits N6 (AlwaysValidStates divergence)

The ASN explicitly derives N6 from N3 and N5 by structural induction. The Dafny model correctly omits N6 from AllInvariants because preserving N3 and N5 is sufficient — N6 is a consequence, not an independent invariant. No spec change needed.

### Artifact 2: Only spans formalized for N7 (ForwardReferenceAdmissibility divergence)

Links and type addresses are not yet modeled in the Dafny formalization. The ASN states all three reference types share the same argument: well-formedness is arithmetic, not state-dependent. The proof for spans demonstrates the pattern; the other two will follow identically once links are modeled. Incomplete coverage of a correct spec property, not a spec issue.

### Artifact 3: Inductive-step obligations only for N6 (StructuralOrdering divergence)

The Dafny model verifies the two key lemmas — prefix precedes descendant, earlier-sibling subtree precedes later-sibling subtree — that constitute the inductive step of the N6 proof. The full biconditional requires formalizing DFS traversal over a finite node set, which is a Dafny encoding challenge, not a spec gap. The ASN's proof sketch uses exactly these two obligations. No spec change needed.

### Clean verifications (16 properties)

AllocationAuthority, AuthorityPermanence, BaptismMonotonicity, BaptizedNodes, CoordinationFreeDisjointness, GhostElement, IdentityByAssignment, LocalSerializationSufficiency, NoNodeMutableState, NodeTree, PrefixPropagation, SequentialChildren, SingleRoot, SubtreeContiguity, SubtreeDisjointness, UniformNodeType — all verified without divergence. The spec properties are faithfully encoded and the proofs are clean.

VERDICT: SIMPLIFY

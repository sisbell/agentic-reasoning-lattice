// Shared definitions for two-space architecture (ASN-0036). Content store,
// arrangement, state, and helper predicates used by all property proofs.
module TwoSpace {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // ---------------------------------------------------------------------------
  // Val — opaque content value type
  // ---------------------------------------------------------------------------

  type Val(==)

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  // Full two-space state: content store + per-document arrangements + known documents
  datatype TwoSpaceState = TwoSpaceState(
    C: map<Tumbler, Val>,
    M: map<Tumbler, map<Tumbler, Tumbler>>,
    documents: set<Tumbler>
  )

  // ---------------------------------------------------------------------------
  // ContentImmutability — transition invariant on C
  // ---------------------------------------------------------------------------

  ghost predicate ContentImmutability(s: TwoSpaceState, s': TwoSpaceState) {
    forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  }

  // ---------------------------------------------------------------------------
  // ReferentialIntegrity — all V-references resolve
  // ---------------------------------------------------------------------------

  ghost predicate ReferentialIntegrity(s: TwoSpaceState) {
    forall d, v :: d in s.M && v in s.M[d] ==> s.M[d][v] in s.C
  }

  // ---------------------------------------------------------------------------
  // AllPositive — all tumbler components strictly positive
  // ---------------------------------------------------------------------------

  ghost predicate AllPositive(t: Tumbler) {
    |t.components| >= 1 &&
    forall i :: 0 <= i < |t.components| ==> t.components[i] > 0
  }

  // ---------------------------------------------------------------------------
  // Origin — document-level prefix N.0.U.0.D
  // ---------------------------------------------------------------------------

  function Origin(a: Tumbler): Tumbler
    requires TumblerHierarchy.HasElementField(a)
    ensures IsPrefix(Origin(a), a)
  {
    Tumbler(a.components[..TumblerHierarchy.E1Pos(a) - 1])
  }
}

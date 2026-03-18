include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// Arrangement invariants lemma — ArrangementInvariantsPreserved
// Every valid composite transition preserves S2, S3, S8a, S8-depth, S8-fin.
// Each elementary transition preserves these per-state properties; composition
// follows by induction over any finite sequence of elementary steps.
module ArrangementInvariantsPreserved {
  import opened TumblerAlgebra

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
  )

  function GetArrangement(M: map<Tumbler, Arr>, d: Tumbler): Arr {
    if d in M then M[d] else map[]
  }

  // DIVERGENCE: S2 (functionality) and S8-fin (finiteness) are structural in
  // Dafny's map model — map<Tumbler, Tumbler> is inherently functional and
  // finite. The invariant below captures S3 (referential integrity) and
  // S8a + S8-depth (V-position well-formedness), abstracted into a single
  // per-V-position predicate VPosValid.

  ghost predicate VPosValid(v: Tumbler) {
    |v.components| >= 1 && PositiveTumbler(v)
  }

  ghost predicate ArrangementOk(arr: Arr, C: map<Tumbler, nat>) {
    (forall v :: v in arr ==> arr[v] in C) &&
    (forall v :: v in arr ==> VPosValid(v))
  }

  ghost predicate ArrInv(s: State) {
    forall d :: ArrangementOk(GetArrangement(s.M, d), s.C)
  }

  // ---------------------------------------------------------------------------
  // Per-elementary-transition preservation
  // ---------------------------------------------------------------------------

  // K.α: content allocation — M in frame, C grows
  lemma AlphaPreservesArrInv(s: State, s': State, a: Tumbler, val: nat)
    requires ArrInv(s)
    requires a !in s.C
    requires s'.C == s.C[a := val]
    requires s'.M == s.M
    ensures ArrInv(s')
  { }

  // K.δ: entity creation — M and C in frame
  lemma DeltaPreservesArrInv(s: State, s': State)
    requires ArrInv(s)
    requires s'.C == s.C
    requires s'.M == s.M
    ensures ArrInv(s')
  { }

  // K.μ⁺: arrangement extension — preconditions establish invariants for new entries
  lemma ExtensionPreservesArrInv(s: State, s': State, d: Tumbler)
    requires ArrInv(s)
    requires s'.C == s.C
    requires forall v :: v in GetArrangement(s.M, d) ==>
      v in GetArrangement(s'.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]
    requires forall v :: v in GetArrangement(s'.M, d).Keys - GetArrangement(s.M, d).Keys ==>
      GetArrangement(s'.M, d)[v] in s.C
    requires forall v :: v in GetArrangement(s'.M, d).Keys - GetArrangement(s.M, d).Keys ==>
      VPosValid(v)
    requires forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d')
    ensures ArrInv(s')
  { }

  // K.μ⁻: arrangement contraction — restriction preserves invariants
  lemma ContractionPreservesArrInv(s: State, s': State, d: Tumbler)
    requires ArrInv(s)
    requires s'.C == s.C
    requires forall v :: v in GetArrangement(s'.M, d) ==>
      v in GetArrangement(s.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]
    requires forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d')
    ensures ArrInv(s')
  { }

  // K.ρ: provenance recording — M and C in frame
  lemma RhoPreservesArrInv(s: State, s': State)
    requires ArrInv(s)
    requires s'.C == s.C
    requires s'.M == s.M
    ensures ArrInv(s')
  { }

  // Composition: the per-transition lemmas compose by induction over any finite
  // sequence of elementary steps. Each step produces a state satisfying ArrInv,
  // which serves as the pre-state for the next step.
}

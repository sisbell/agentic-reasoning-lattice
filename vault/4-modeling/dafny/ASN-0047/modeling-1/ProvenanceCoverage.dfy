include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// P7a — ProvenanceCoverage
module ProvenanceCoverage {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: set<Tumbler>,              // dom(C): allocated content addresses
    E: set<Tumbler>,              // entity addresses
    M: map<Tumbler, Arr>,         // arrangements per document
    R: set<(Tumbler, Tumbler)>    // provenance relation (address, document)
  )

  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  function GetArrangement(M: map<Tumbler, Arr>, d: Tumbler): Arr {
    if d in M then M[d] else map[]
  }

  function RanM(s: State, d: Tumbler): set<Tumbler> {
    GetArrangement(s.M, d).Values
  }

  // S3 — referential integrity: arranged addresses must be allocated
  ghost predicate S3(s: State) {
    forall d, a :: a in RanM(s, d) ==> a in s.C
  }

  // P7a — every allocated content address has provenance in some document
  ghost predicate ProvenanceCoverage(s: State) {
    forall a :: a in s.C ==> exists d :: (a, d) in s.R
  }

  // Base: dom(C₀) = ∅; vacuous
  lemma ProvenanceCoverageBase(s: State)
    requires s.C == {}
    ensures ProvenanceCoverage(s)
  { }

  // P7a — ProvenanceCoverage: inductive step
  // Derived from J0, J1, P0, P2
  lemma ProvenanceCoverageInductive(s: State, s': State)
    requires S3(s)
    requires ProvenanceCoverage(s)
    requires s.C <= s'.C                             // P0
    requires s.R <= s'.R                             // P2
    requires forall a :: a in s'.C - s.C ==>         // J0
               exists d :: d in E_doc(s') && a in RanM(s', d)
    requires forall d :: d in E_doc(s') ==>          // J1
               forall a :: a in RanM(s', d) - RanM(s, d) ==>
                 (a, d) in s'.R
    ensures ProvenanceCoverage(s')
  {
    forall a | a in s'.C
      ensures exists d :: (a, d) in s'.R
    {
      if a in s.C {
        var d :| (a, d) in s.R;
        assert (a, d) in s'.R;
      } else {
        assert a in s'.C - s.C;
        var d :| d in E_doc(s') && a in RanM(s', d);
        assert a !in RanM(s, d);
        assert (a, d) in s'.R;
      }
    }
  }
}

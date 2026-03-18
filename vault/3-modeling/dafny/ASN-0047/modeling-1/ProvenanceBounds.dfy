include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// P4 — ProvenanceBounds (ASN-0047)
// Contains(Σ) ⊆ R
// Derived from J1 (ExtensionRecordsProvenance) and P2 (ProvenancePermanence)
module ProvenanceBounds {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
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

  // DIVERGENCE: WF is an explicit precondition requiring arrangements exist only
  // for allocated documents. The ASN treats this structurally (M is total with
  // M(d) = ∅ for d ∉ E_doc), but the Dafny partial-map model needs it to link
  // pre-existing arrangement entries back to E_doc membership in the inductive step.
  ghost predicate WF(s: State) {
    forall d :: d in s.M ==> d in E_doc(s)
  }

  // P4 — Contains(Σ) ⊆ R
  ghost predicate ProvenanceBounds(s: State) {
    forall a, d :: d in E_doc(s) && a in RanM(s, d) ==> (a, d) in s.R
  }

  // Base case: (E₀)_doc = ∅ so Contains(Σ₀) = ∅
  lemma ProvenanceBoundsBase(s: State)
    requires s.M == map[]
    requires s.R == {}
    ensures ProvenanceBounds(s)
  { }

  // Inductive step: Contains(Σ) ⊆ R preserved by valid composite transitions
  lemma ProvenanceBoundsInductive(s: State, s': State)
    requires WF(s)
    requires ProvenanceBounds(s)
    requires s.R <= s'.R  // P2
    requires forall d :: d in E_doc(s') ==>
               forall a :: a in RanM(s', d) - RanM(s, d) ==>
                 (a, d) in s'.R  // J1
    ensures ProvenanceBounds(s')
  { }
}

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// J0 — AllocationRequiresPlacement
module AllocationRequiresPlacement {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arr = map<Tumbler, Tumbler>

  // State projection for J0: content allocation, entities, arrangements
  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>
  )

  function GetArrangement(M: map<Tumbler, Arr>, d: Tumbler): Arr {
    if d in M then M[d] else map[]
  }

  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  function RanM(s: State, d: Tumbler): set<Tumbler> {
    GetArrangement(s.M, d).Values
  }

  // ---------------------------------------------------------------------------
  // J0 — AllocationRequiresPlacement
  //
  // (A Σ → Σ', a : a ∈ dom(C') \ dom(C) :
  //   (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))
  //
  // Every freshly allocated I-address appears in some arrangement in the
  // post-state — the containing document may itself have been freshly
  // created by K.δ in the same composite transition.
  // ---------------------------------------------------------------------------

  ghost predicate AllocationRequiresPlacement(pre: State, post: State) {
    forall a :: a in post.C.Keys - pre.C.Keys ==>
      exists d :: d in E_doc(post) && a in RanM(post, d)
  }
}

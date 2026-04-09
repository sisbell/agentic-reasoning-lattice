include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.μ~ — ArrangementReordering (POST)
// For d ∈ E_doc, there exists a bijection π : dom(M(d)) → dom(M'(d))
// such that (A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))
// Composite: K.μ⁻ + K.μ⁺; bijection on V-positions
module ArrangementReordering {
  import opened TumblerAlgebra
  import TumblerHierarchy

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

  // π is a bijection from 'from' onto 'to'
  ghost predicate IsBijection(pi: map<Tumbler, Tumbler>, from: set<Tumbler>, to: set<Tumbler>) {
    pi.Keys == from &&
    pi.Values == to &&
    forall v1, v2 :: v1 in from && v2 in from && v1 != v2 ==> pi[v1] != pi[v2]
  }

  // ---------------------------------------------------------------------------
  // K.μ~ — ArrangementReordering
  //
  // For d ∈ E_doc, there exists a bijection π : dom(M(d)) → dom(M'(d)) with
  // (A v : v ∈ dom(M(d)) : M'(d)(π(v)) = M(d)(v))
  // Precondition: d ∈ E_doc
  // Frame: C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))
  // ---------------------------------------------------------------------------

  ghost predicate Post(s: State, s': State, d: Tumbler, pi: map<Tumbler, Tumbler>) {
    // pre: d is a document entity
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    // pi is a bijection from dom(M(d)) to dom(M'(d))
    IsBijection(pi, GetArrangement(s.M, d).Keys, GetArrangement(s'.M, d).Keys) &&
    // post: M'(d)(π(v)) = M(d)(v) for all v in dom(M(d))
    (forall v :: v in GetArrangement(s.M, d) ==>
      GetArrangement(s'.M, d)[pi[v]] == GetArrangement(s.M, d)[v]) &&
    // frame
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  // Corollary: reordering preserves the range (I-addresses)
  lemma ReorderingPreservesRange(s: State, s': State, d: Tumbler, pi: map<Tumbler, Tumbler>)
    requires Post(s, s', d, pi)
    ensures GetArrangement(s'.M, d).Values == GetArrangement(s.M, d).Values
  { }
}

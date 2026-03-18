include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// J3 — ReorderingIsolation
// K.μ~ as a distinguished composite satisfies:
// C' = C ∧ E' = E ∧ R' = R
// Reordering preserves ran(M(d)), so Contains(Σ') = Contains(Σ)
module ReorderingIsolation {
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

  ghost function ArrRange(m: Arr): set<Tumbler> {
    set v | v in m :: m[v]
  }

  // (a, d) ∈ Contains(Σ) iff d ∈ E_doc ∧ a ∈ ran(M(d))
  ghost predicate InContains(s: State, a: Tumbler, d: Tumbler) {
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    a in ArrRange(GetArrangement(s.M, d))
  }

  // K.μ~ postcondition: ran(M'(d)) = ran(M(d)), derived from bijection
  ghost predicate ReorderPost(s: State, s': State, d: Tumbler) {
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    // ran preserved
    ArrRange(GetArrangement(s'.M, d)) == ArrRange(GetArrangement(s.M, d)) &&
    // frame
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  // J3 — ReorderingIsolation
  lemma ReorderingIsolation(s: State, s': State, d: Tumbler)
    requires ReorderPost(s, s', d)
    ensures s'.C == s.C
    ensures s'.E == s.E
    ensures s'.R == s.R
    ensures forall a, d' :: InContains(s, a, d') <==> InContains(s', a, d')
  { }
}

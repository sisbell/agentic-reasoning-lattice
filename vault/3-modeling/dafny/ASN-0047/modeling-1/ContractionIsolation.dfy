include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// J2 — ContractionIsolation
// K.μ⁻ as an elementary transition satisfies:
// C' = C ∧ E' = E ∧ R' = R
// Contains(Σ') ⊆ Contains(Σ) ⊆ R = R'
module ContractionIsolation {
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

  // ran(M(d)): I-addresses referenced by an arrangement
  ghost function ArrRange(m: Arr): set<Tumbler> {
    set v | v in m :: m[v]
  }

  // (a, d) ∈ Contains(Σ) iff d ∈ E_doc ∧ a ∈ ran(M(d))
  ghost predicate InContains(s: State, a: Tumbler, d: Tumbler) {
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    a in ArrRange(GetArrangement(s.M, d))
  }

  // K.μ⁻ post-condition (mirrors ArrangementContraction.Post)
  ghost predicate ContractionPost(s: State, s': State, d: Tumbler) {
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    // domain strictly shrinks
    GetArrangement(s'.M, d).Keys < GetArrangement(s.M, d).Keys &&
    // surviving mappings preserved
    (forall v :: v in GetArrangement(s'.M, d) ==>
      v in GetArrangement(s.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]) &&
    // frame
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  // J2 — ContractionIsolation
  lemma ContractionIsolation(s: State, s': State, d: Tumbler)
    requires ContractionPost(s, s', d)
    // Frame preservation
    ensures s'.C == s.C
    ensures s'.E == s.E
    ensures s'.R == s.R
    // Containment can only shrink
    ensures forall a, d' :: InContains(s', a, d') ==> InContains(s, a, d')
  { }
}

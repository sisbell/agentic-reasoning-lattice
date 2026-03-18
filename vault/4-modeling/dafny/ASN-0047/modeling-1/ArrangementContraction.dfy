include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.μ⁻ — ArrangementContraction (POST)
// dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))
module ArrangementContraction {
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

  // ---------------------------------------------------------------------------
  // K.μ⁻ — ArrangementContraction
  //
  // dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))
  // Precondition: d ∈ E_doc
  // Frame: C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))
  // ---------------------------------------------------------------------------

  ghost predicate Post(s: State, s': State, d: Tumbler) {
    // pre: d is a document entity
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    // post: domain strictly shrinks
    GetArrangement(s'.M, d).Keys < GetArrangement(s.M, d).Keys &&
    // post: surviving mappings preserved
    (forall v :: v in GetArrangement(s'.M, d) ==>
      v in GetArrangement(s.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]) &&
    // frame
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  // Domain strictly shrinks
  lemma ContractionStrictlyShrinks(s: State, s': State, d: Tumbler)
    requires Post(s, s', d)
    ensures GetArrangement(s'.M, d).Keys < GetArrangement(s.M, d).Keys
  { }

  // Surviving mappings preserved
  lemma ContractionPreservesMappings(s: State, s': State, d: Tumbler, v: Tumbler)
    requires Post(s, s', d)
    requires v in GetArrangement(s'.M, d)
    ensures v in GetArrangement(s.M, d)
    ensures GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]
  { }

  // Frame: other documents unchanged
  lemma FrameOtherDocuments(s: State, s': State, d: Tumbler, d': Tumbler)
    requires Post(s, s', d)
    requires d' != d
    ensures GetArrangement(s'.M, d') == GetArrangement(s.M, d')
  { }

  // Frame: entities unchanged
  lemma FrameEntities(s: State, s': State, d: Tumbler)
    requires Post(s, s', d)
    ensures s'.E == s.E
  { }

  // Frame: content unchanged
  lemma FrameContent(s: State, s': State, d: Tumbler)
    requires Post(s, s', d)
    ensures s'.C == s.C
  { }

  // Frame: provenance unchanged
  lemma FrameProvenance(s: State, s': State, d: Tumbler)
    requires Post(s, s', d)
    ensures s'.R == s.R
  { }
}

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.μ⁺ — ArrangementExtension (POST)
// dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))
module ArrangementExtension {
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
  // K.μ⁺ — ArrangementExtension
  //
  // dom(M'(d)) ⊃ dom(M(d)) ∧ (A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))
  // Precondition: d ∈ E_doc; new mappings target dom(C)
  // Frame: C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R
  // ---------------------------------------------------------------------------

  ghost predicate Post(s: State, s': State, d: Tumbler) {
    // pre: d is a document entity
    d in s.E &&
    TumblerHierarchy.DocumentAddress(d) &&
    // post: domain strictly grows
    GetArrangement(s.M, d).Keys < GetArrangement(s'.M, d).Keys &&
    // post: existing mappings preserved
    (forall v :: v in GetArrangement(s.M, d) ==>
      v in GetArrangement(s'.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]) &&
    // post: new mappings target allocated content
    (forall v :: v in GetArrangement(s'.M, d).Keys - GetArrangement(s.M, d).Keys ==>
      GetArrangement(s'.M, d)[v] in s.C) &&
    // frame
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  // Domain strictly grows
  lemma ExtensionStrictlyGrows(s: State, s': State, d: Tumbler)
    requires Post(s, s', d)
    ensures GetArrangement(s.M, d).Keys < GetArrangement(s'.M, d).Keys
  { }

  // Existing mappings preserved
  lemma ExtensionPreservesMappings(s: State, s': State, d: Tumbler, v: Tumbler)
    requires Post(s, s', d)
    requires v in GetArrangement(s.M, d)
    ensures v in GetArrangement(s'.M, d)
    ensures GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]
  { }

  // New mappings reference allocated content
  lemma NewMappingsInContent(s: State, s': State, d: Tumbler, v: Tumbler)
    requires Post(s, s', d)
    requires v in GetArrangement(s'.M, d).Keys - GetArrangement(s.M, d).Keys
    ensures GetArrangement(s'.M, d)[v] in s.C
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

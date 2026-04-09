include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.δ — EntityCreation (POST)
// E' = E ∪ {e}, e fresh, ValidAddress(e), ¬IsElement(e)
module EntityCreation {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
  )

  // Arrangement accessor: absence from the map represents the empty arrangement
  function GetArrangement(M: map<Tumbler, Arr>, d: Tumbler): Arr {
    if d in M then M[d] else map[]
  }

  // ---------------------------------------------------------------------------
  // K.δ — EntityCreation
  //
  // E' = E ∪ {e} where e ∉ E ∧ ValidAddress(e) ∧ ¬IsElement(e)
  // Frame: C' = C; M' = M; R' = R
  //
  // DIVERGENCE: The ASN states "When IsDocument(e): M'(e) = ∅" as an explicit
  // postcondition. In the map model, M is unchanged (frame), and the empty-
  // arrangement condition follows from the convention that absence from the map
  // represents ∅. The NewDocumentEmpty lemma captures this consequence under
  // the well-formedness assumption that fresh entities have no prior arrangement.
  // ---------------------------------------------------------------------------

  ghost predicate Post(s: State, s': State, e: Tumbler) {
    e !in s.E &&
    TumblerHierarchy.ValidAddress(e) &&
    !TumblerHierarchy.ElementAddress(e) &&
    s'.E == s.E + {e} &&
    s'.C == s.C &&
    s'.M == s.M &&
    s'.R == s.R
  }

  // Entity set grows by exactly {e}
  lemma CreationExtendsEntities(s: State, s': State, e: Tumbler)
    requires Post(s, s', e)
    ensures s'.E - s.E == {e}
  { }

  // Existing entities preserved
  lemma CreationPreservesExisting(s: State, s': State, e: Tumbler, e2: Tumbler)
    requires Post(s, s', e)
    requires e2 in s.E
    ensures e2 in s'.E
  { }

  // New document has empty arrangement (from frame + map convention)
  lemma NewDocumentEmpty(s: State, s': State, e: Tumbler)
    requires Post(s, s', e)
    requires TumblerHierarchy.DocumentAddress(e)
    requires e !in s.M  // well-formedness: fresh entity has no prior arrangement
    ensures GetArrangement(s'.M, e) == map[]
  { }
}

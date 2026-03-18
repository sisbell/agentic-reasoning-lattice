include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerAllocation.dfy"

module EntityPermanence {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import TumblerAllocation

  // Minimal state projection: only the entity set is needed for P1
  datatype State = State(E: set<Tumbler>)

  // ---------------------------------------------------------------------------
  // P1 — EntityPermanence
  //
  // (A Σ → Σ' :: E ⊆ E')
  // Transition invariant; specialises T8 (ASN-0034 AddressPermanence)
  // ---------------------------------------------------------------------------

  ghost predicate EntityPermanence(s: State, s': State) {
    s.E <= s'.E
  }

  // Sub-properties: permanence per stratum

  lemma NodePermanence(s: State, s': State, e: Tumbler)
    requires EntityPermanence(s, s')
    requires e in s.E
    requires TumblerHierarchy.NodeAddress(e)
    ensures e in s'.E
  { }

  lemma AccountPermanence(s: State, s': State, e: Tumbler)
    requires EntityPermanence(s, s')
    requires e in s.E
    requires TumblerHierarchy.AccountAddress(e)
    ensures e in s'.E
  { }

  lemma DocumentPermanence(s: State, s': State, e: Tumbler)
    requires EntityPermanence(s, s')
    requires e in s.E
    requires TumblerHierarchy.DocumentAddress(e)
    ensures e in s'.E
  { }

  // Connection to T8: EntityPermanence is AddressPermanence applied to E
  lemma SpecialisesT8(s: State, s': State)
    requires EntityPermanence(s, s')
    ensures TumblerAllocation.AddressPermanence(s.E, s'.E)
  { }

  // Transitivity: permanence composes across transition sequences
  lemma EntityPermanenceTransitive(s1: State, s2: State, s3: State)
    requires EntityPermanence(s1, s2)
    requires EntityPermanence(s2, s3)
    ensures EntityPermanence(s1, s3)
  { }
}

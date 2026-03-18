include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module ExtensionRecordsProvenance {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Arrangement: partial map from V-addresses to I-addresses
  type Arrangement = map<Tumbler, Tumbler>

  // State components relevant to J1
  datatype State = State(
    entities: set<Tumbler>,
    arrangements: map<Tumbler, Arrangement>,
    provenance: set<(Tumbler, Tumbler)>
  )

  // E_doc: document entities in a state
  ghost function Docs(s: State): set<Tumbler> {
    set e | e in s.entities && TumblerHierarchy.DocumentAddress(e)
  }

  // ran(M(d)): I-addresses referenced by an arrangement
  ghost function ArrRange(m: Arrangement): set<Tumbler> {
    set v | v in m :: m[v]
  }

  // M(d) with totality: empty arrangement for documents not in the map
  function ArrOf(s: State, d: Tumbler): Arrangement {
    if d in s.arrangements then s.arrangements[d] else map[]
  }

  // J1 — ExtensionRecordsProvenance
  // Every I-address freshly placed in a document's arrangement
  // has provenance recorded in the post-state.
  ghost predicate ExtensionRecordsProvenance(s: State, s': State) {
    forall d, a ::
      d in Docs(s') &&
      a in ArrRange(ArrOf(s', d)) &&
      a !in ArrRange(ArrOf(s, d))
      ==> (a, d) in s'.provenance
  }
}

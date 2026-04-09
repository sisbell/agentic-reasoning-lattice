include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module ProvenanceRequiresExtension {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arrangement = map<Tumbler, Tumbler>

  datatype State = State(
    entities: set<Tumbler>,
    arrangements: map<Tumbler, Arrangement>,
    provenance: set<(Tumbler, Tumbler)>
  )

  ghost function Docs(s: State): set<Tumbler> {
    set e | e in s.entities && TumblerHierarchy.DocumentAddress(e)
  }

  ghost function ArrRange(m: Arrangement): set<Tumbler> {
    set v | v in m :: m[v]
  }

  function ArrOf(s: State, d: Tumbler): Arrangement {
    if d in s.arrangements then s.arrangements[d] else map[]
  }

  // J1' — ProvenanceRequiresExtension
  // New provenance (a,d) in R'\R requires a newly arranged in d:
  // a in ran(M'(d)) \ ran(M(d)).
  ghost predicate ProvenanceRequiresExtension(s: State, s': State) {
    forall a, d ::
      d in Docs(s') &&
      (a, d) in s'.provenance - s.provenance
      ==> a in ArrRange(ArrOf(s', d)) - ArrRange(ArrOf(s, d))
  }
}

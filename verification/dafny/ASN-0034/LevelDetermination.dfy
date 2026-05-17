// ASN-0034: T4c — LevelDetermination
// The mapping zeros(t) → hierarchical level is a bijection on {0, 1, 2, 3}:
// 0 ↔ node, 1 ↔ user, 2 ↔ document, 3 ↔ element.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"

module LevelDetermination {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing

  datatype Level = Node | User | Document | Element

  function LevelDetermination(t: Tumbler): Level
    requires InT(t)
    requires HierarchicalParsing.HierarchicalParsing(t)
    ensures Zeros(t) == 0 <==> LevelDetermination(t) == Node
    ensures Zeros(t) == 1 <==> LevelDetermination(t) == User
    ensures Zeros(t) == 2 <==> LevelDetermination(t) == Document
    ensures Zeros(t) == 3 <==> LevelDetermination(t) == Element
  {
    if Zeros(t) == 0 then Node
    else if Zeros(t) == 1 then User
    else if Zeros(t) == 2 then Document
    else Element
  }
}

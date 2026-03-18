include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// K.δ (pre) — EntityCreatable
// parent(e) ∈ E when ¬IsNode(e)
module EntityCreatable {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection: only the entity set
  datatype State = State(E: set<Tumbler>)

  // Entity: valid address with zeros ≤ 2 (excludes element-level addresses)
  ghost predicate IsEntity(e: Tumbler) {
    TumblerHierarchy.ValidAddress(e) &&
    TumblerHierarchy.ZeroCount(e.components) <= 2
  }

  // Parent of a non-node entity: truncate at last zero separator.
  // Account N.0.U → N; Document N.0.U.0.D → N.0.U.
  function Parent(e: Tumbler): Tumbler
    requires IsEntity(e)
    requires !TumblerHierarchy.NodeAddress(e)
  {
    var z0 := FindZero(e.components, 0);
    if TumblerHierarchy.AccountAddress(e) || z0 >= |e.components| then
      Tumbler(e.components[..z0])
    else
      var z1 := FindZero(e.components, z0 + 1);
      Tumbler(e.components[..z1])
  }

  // K.δ precondition: non-node entities require their parent in E
  ghost predicate EntityCreatable(s: State, e: Tumbler) {
    IsEntity(e) &&
    (TumblerHierarchy.NodeAddress(e) || Parent(e) in s.E)
  }
}

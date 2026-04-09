include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// P8 — EntityHierarchy
// (A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)
module EntityHierarchy {
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

  // P8 — EntityHierarchy: every non-node entity's parent is in E
  ghost predicate EntityHierarchy(s: State) {
    forall e :: e in s.E && IsEntity(e) && !TumblerHierarchy.NodeAddress(e)
      ==> Parent(e) in s.E
  }

  // Base case: E₀ = {n₀} with IsNode(n₀) — no non-nodes, vacuously true
  lemma EntityHierarchyBase(n0: Tumbler)
    requires TumblerHierarchy.NodeAddress(n0)
    ensures EntityHierarchy(State({n0}))
  { }

  // Inductive step: K.δ creates entity e; EntityCreatable requires parent(e) ∈ E
  // for non-nodes. P1 gives E ⊆ E ∪ {e}.
  lemma EntityHierarchyCreation(s: State, e: Tumbler)
    requires EntityHierarchy(s)
    requires IsEntity(e)
    requires e !in s.E
    requires !TumblerHierarchy.NodeAddress(e) ==> Parent(e) in s.E
    ensures EntityHierarchy(State(s.E + {e}))
  { }
}

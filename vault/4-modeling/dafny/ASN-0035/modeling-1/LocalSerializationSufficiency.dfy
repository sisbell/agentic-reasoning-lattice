include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module LocalSerializationSufficiency {
  import opened TumblerAlgebra

  // A node n is a child of p iff n extends p by exactly one component
  ghost predicate IsChildOf(n: Tumbler, p: Tumbler) {
    |n.components| == |p.components| + 1 &&
    n.components[..|p.components|] == p.components
  }

  // The set of children of p within a set of nodes
  ghost function Children(p: Tumbler, nodes: set<Tumbler>): set<Tumbler> {
    set n | n in nodes && IsChildOf(n, p)
  }

  // A node has exactly one parent
  lemma UniqueParent(n: Tumbler, p: Tumbler, q: Tumbler)
    requires IsChildOf(n, p)
    requires IsChildOf(n, q)
    ensures p == q
  { }

  // Children of distinct parents are distinct
  lemma DistinctParentsDistinctChildren(np: Tumbler, nq: Tumbler, p: Tumbler, q: Tumbler)
    requires p != q
    requires IsChildOf(np, p)
    requires IsChildOf(nq, q)
    ensures np != nq
  { }

  // Adding a child of q does not change children(p)
  lemma ChildrenUnchanged(p: Tumbler, q: Tumbler, nodes: set<Tumbler>, nq: Tumbler)
    requires p != q
    requires IsChildOf(nq, q)
    ensures Children(p, nodes + {nq}) == Children(p, nodes)
  { }

  // N12 — LocalSerializationSufficiency
  //
  // Two BAPTIZE operations targeting different parents commute:
  // each reads only its parent's children (BAPTIZE postcondition),
  // children of different parents are disjoint (derived from N10),
  // so neither operation affects the other's input or output.
  lemma LocalSerializationSufficiency(
    p: Tumbler, q: Tumbler,
    nodes: set<Tumbler>,
    np: Tumbler, nq: Tumbler
  )
    requires p != q
    requires IsChildOf(np, p)
    requires IsChildOf(nq, q)
    requires np !in nodes
    requires nq !in nodes
    ensures Children(p, nodes + {nq}) == Children(p, nodes)
    ensures Children(q, nodes + {np}) == Children(q, nodes)
    ensures np != nq
    ensures nodes + {np} + {nq} == nodes + {nq} + {np}
  { }
}

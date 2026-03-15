include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// N6 — StructuralOrdering
// For any a, b ∈ Σ.nodes: a < b under T1 ⟺ a ≺_dfs b
// Derived from N3, N5, T1.
//
// DIVERGENCE: The ASN states a biconditional between T1 order and DFS
// pre-order over the baptized node tree. The Dafny model verifies the two
// structural lemmas that are the proof obligations for the inductive step:
// (i) a proper prefix precedes its extensions, and (ii) descendants of an
// earlier sibling precede descendants of a later sibling. The full
// equivalence follows by structural induction over the finite tree (N3),
// applying these lemmas at each node. Formalizing the DFS traversal itself
// would require a recursive function over the tree's finite node set.
module StructuralOrdering {
  import opened TumblerAlgebra

  // Node address: non-empty, all components positive (zeros(n) = 0)
  ghost predicate NodeAddress(n: Tumbler) {
    |n.components| >= 1 &&
    forall i :: 0 <= i < |n.components| ==> n.components[i] > 0
  }

  // N6(i) — PrefixPrecedesDescendant
  // A proper prefix precedes all its extensions under T1 (case ii of T1).
  lemma PrefixPrecedesDescendant(p: Tumbler, d: Tumbler)
    requires IsPrefix(p, d)
    requires |p.components| < |d.components|
    ensures LessThan(p, d)
  {
    LessThanIntro(p, d, |p.components|);
  }

  // N6(ii) — InterSubtreeOrdering
  // For siblings ci = [p₁,...,pₐ,i] and cj = [p₁,...,pₐ,j] with i < j,
  // any extension of ci precedes any extension of cj under T1.
  // Divergence at position a (= |p|) with d[a] = ci[a] < cj[a] = e[a]
  // gives d < e by T1 case (i).
  lemma InterSubtreeOrdering(
    p: Tumbler, ci: Tumbler, cj: Tumbler, d: Tumbler, e: Tumbler
  )
    requires |ci.components| == |p.components| + 1
    requires |cj.components| == |p.components| + 1
    requires IsPrefix(p, ci)
    requires IsPrefix(p, cj)
    requires ci.components[|p.components|] < cj.components[|p.components|]
    requires IsPrefix(ci, d)
    requires IsPrefix(cj, e)
    ensures LessThan(d, e)
  {
    LessThanIntro(d, e, |p.components|);
  }
}

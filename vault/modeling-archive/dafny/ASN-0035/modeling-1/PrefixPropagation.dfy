include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module PrefixPropagation {
  import opened TumblerAlgebra

  // N16 — PrefixPropagation
  // For every address a allocated in the subtree rooted at node n:
  // n ≼ a. The first #n components of a are identical to those of n.
  //
  // Core step: AllocationInc(t, k) preserves any prefix n of t,
  // provided k > 0 (appending) or the last nonzero of t lies
  // beyond n's boundary (sibling increment doesn't touch n's components).

  lemma PrefixPropagation(n: Tumbler, t: Tumbler, k: nat)
    requires IsPrefix(n, t)
    requires PositiveTumbler(t)
    requires |t.components| > 0
    requires k == 0 ==> exists j :: |n.components| <= j < |t.components| && t.components[j] != 0
    ensures IsPrefix(n, AllocationInc(t, k))
  {
  }
}

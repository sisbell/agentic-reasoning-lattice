module SubspaceDisjointness {
  import opened TumblerAlgebra

  // ASN-0001 T7 — SubspaceDisjointness

  // s[i..] contains at least k zero-valued components
  predicate HasKZeros(s: seq<nat>, k: nat, i: nat)
    decreases |s| - i
  {
    if k == 0 then true
    else if i >= |s| then false
    else if s[i] == 0 then HasKZeros(s, k - 1, i + 1)
    else HasKZeros(s, k, i + 1)
  }

  // Position of the k-th zero in s, searching from index i (k is 1-indexed)
  function KthZero(s: seq<nat>, k: nat, i: nat): (pos: nat)
    requires k >= 1
    requires HasKZeros(s, k, i)
    ensures i <= pos < |s|
    ensures s[pos] == 0
    decreases |s| - i
  {
    if s[i] == 0 && k == 1 then i
    else if s[i] == 0 then KthZero(s, k - 1, i + 1)
    else KthZero(s, k, i + 1)
  }

  // T4-derived: an element address has at least 3 zero separators,
  // with the element field starting after the third zero
  predicate ElementAddress(t: Tumbler) {
    HasKZeros(t.components, 3, 0) &&
    KthZero(t.components, 3, 0) + 1 < |t.components|
  }

  // Subspace identifier: first component of the element field (E₁)
  function SubspaceId(t: Tumbler): nat
    requires ElementAddress(t)
  {
    t.components[KthZero(t.components, 3, 0) + 1]
  }

  // T7 — SubspaceDisjointness
  // The subspace identifier permanently separates the address space
  // into disjoint regions. (A a, b in T : a.E1 != b.E1 ==> a != b)
  // Corollary of T3 (canonical rep. = Dafny structural equality) and
  // T4 (well-defined field parsing via ElementAddress/SubspaceId).
  lemma SubspaceDisjointnessLemma(a: Tumbler, b: Tumbler)
    requires ElementAddress(a)
    requires ElementAddress(b)
    requires SubspaceId(a) != SubspaceId(b)
    ensures a != b
  { }
}

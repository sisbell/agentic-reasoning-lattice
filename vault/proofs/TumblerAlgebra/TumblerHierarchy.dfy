// Hierarchy properties (ASN-0034): T4, T5, T6, T7, PrefixOrderingExtension
module TumblerHierarchy {
  import opened TumblerAlgebra

  // ---------------------------------------------------------------------------
  // T4 — ValidAddress
  // ---------------------------------------------------------------------------

  function ZeroCount(s: seq<nat>): nat
    decreases |s|
  {
    if |s| == 0 then 0
    else (if s[0] == 0 then 1 else 0) + ZeroCount(s[1..])
  }

  predicate NoAdjacentZeros(s: seq<nat>) {
    forall i :: 0 <= i < |s| - 1 ==> !(s[i] == 0 && s[i + 1] == 0)
  }

  predicate ValidAddress(t: Tumbler) {
    |t.components| >= 1 &&
    ZeroCount(t.components) <= 3 &&
    t.components[0] != 0 &&
    t.components[|t.components| - 1] != 0 &&
    NoAdjacentZeros(t.components)
  }

  // ---------------------------------------------------------------------------
  // T5 — ContiguousSubtrees
  // ---------------------------------------------------------------------------

  lemma ContiguousSubtrees(p: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires IsPrefix(p, a)
    requires IsPrefix(p, c)
    requires LessEq(a, b)
    requires LessEq(b, c)
    ensures IsPrefix(p, b)
  { }

  // ---------------------------------------------------------------------------
  // T6 — DecidableContainment
  // ---------------------------------------------------------------------------

  function NodeField(t: Tumbler): seq<nat> {
    var z := FindZero(t.components, 0);
    t.components[..z]
  }

  function UserField(t: Tumbler): seq<nat> {
    var z0 := FindZero(t.components, 0);
    if z0 >= |t.components| then []
    else
      var z1 := FindZero(t.components, z0 + 1);
      t.components[z0+1..z1]
  }

  function DocField(t: Tumbler): seq<nat> {
    var z0 := FindZero(t.components, 0);
    if z0 >= |t.components| then []
    else
      var z1 := FindZero(t.components, z0 + 1);
      if z1 >= |t.components| then []
      else
        var z2 := FindZero(t.components, z1 + 1);
        t.components[z1+1..z2]
  }

  predicate SameNode(a: Tumbler, b: Tumbler) {
    NodeField(a) == NodeField(b)
  }

  predicate SameNodeUser(a: Tumbler, b: Tumbler) {
    NodeField(a) == NodeField(b) && UserField(a) == UserField(b)
  }

  predicate SameNodeUserDoc(a: Tumbler, b: Tumbler) {
    NodeField(a) == NodeField(b) && UserField(a) == UserField(b) && DocField(a) == DocField(b)
  }

  predicate SeqIsPrefix(a: seq<nat>, b: seq<nat>) {
    |a| <= |b| && a == b[..|a|]
  }

  predicate DocFieldIsPrefix(a: Tumbler, b: Tumbler) {
    SeqIsPrefix(DocField(a), DocField(b))
  }

  lemma DecidableContainment(a: Tumbler, b: Tumbler)
    ensures SameNodeUserDoc(a, b) ==> SameNodeUser(a, b)
    ensures SameNodeUser(a, b) ==> SameNode(a, b)
  { }

  lemma DocPrefixReflexive(t: Tumbler)
    ensures DocFieldIsPrefix(t, t)
  { }

  lemma DocPrefixTransitive(a: Tumbler, b: Tumbler, c: Tumbler)
    requires DocFieldIsPrefix(a, b)
    requires DocFieldIsPrefix(b, c)
    ensures DocFieldIsPrefix(a, c)
  { }

  lemma DocPrefixAntisymmetric(a: Tumbler, b: Tumbler)
    requires DocFieldIsPrefix(a, b)
    requires DocFieldIsPrefix(b, a)
    ensures DocField(a) == DocField(b)
  { }

  lemma SameDocImpliesMutualPrefix(a: Tumbler, b: Tumbler)
    requires DocField(a) == DocField(b)
    ensures DocFieldIsPrefix(a, b) && DocFieldIsPrefix(b, a)
  { }

  // ---------------------------------------------------------------------------
  // T7 — SubspaceDisjoint
  // ---------------------------------------------------------------------------

  function E1Pos(t: Tumbler): nat {
    var z0 := FindZero(t.components, 0);
    if z0 >= |t.components| then |t.components| + 1
    else
      var z1 := FindZero(t.components, z0 + 1);
      if z1 >= |t.components| then |t.components| + 1
      else
        var z2 := FindZero(t.components, z1 + 1);
        z2 + 1
  }

  predicate HasElementField(t: Tumbler) {
    E1Pos(t) < |t.components|
  }

  function E1(t: Tumbler): nat
    requires HasElementField(t)
  {
    t.components[E1Pos(t)]
  }

  lemma SubspaceDisjoint(a: Tumbler, b: Tumbler)
    requires HasElementField(a)
    requires HasElementField(b)
    requires E1(a) != E1(b)
    ensures a != b
  { }

  // ---------------------------------------------------------------------------
  // PrefixOrderingExtension
  // ---------------------------------------------------------------------------

  lemma PrefixOrderingExtension(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires LessThan(p1, p2)
    requires !IsPrefix(p1, p2)
    requires !IsPrefix(p2, p1)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures LessThan(a, b)
  {
    var k :| LessThanAt(p1, p2, k);
    LessThanIntro(a, b, k);
  }
}

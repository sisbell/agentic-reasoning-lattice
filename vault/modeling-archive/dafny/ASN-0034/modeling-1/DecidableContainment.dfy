include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T6 — DecidableContainment
module DecidableContainment {
  import opened TumblerAlgebra

  // ---------------------------------------------------------------------------
  // Field extraction — find zero separators, extract field subsequences
  // ---------------------------------------------------------------------------

  function FindZero(s: seq<nat>, start: nat): nat
    requires start <= |s|
    ensures start <= FindZero(s, start) <= |s|
    ensures FindZero(s, start) < |s| ==> s[FindZero(s, start)] == 0
    ensures forall i :: start <= i < FindZero(s, start) ==> s[i] != 0
    decreases |s| - start
  {
    if start == |s| then |s|
    else if s[start] == 0 then start
    else FindZero(s, start + 1)
  }

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

  // ---------------------------------------------------------------------------
  // Decidable predicates — all computable (non-ghost)
  // ---------------------------------------------------------------------------

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

  // ---------------------------------------------------------------------------
  // T6 — DecidableContainment
  // Containment hierarchy: (c) => (b) => (a)
  // Document prefix: partial order
  // ---------------------------------------------------------------------------

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
}

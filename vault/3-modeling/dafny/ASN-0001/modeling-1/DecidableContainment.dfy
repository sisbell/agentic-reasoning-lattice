include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "HierarchicalParsing.dfy"

module DecidableContainment {
  import opened TumblerAlgebra
  import opened HierarchicalParsing

  // T6 — DecidableContainment (corollary of T4)
  // For well-formed tumblers, field-sharing is decidable from addresses alone.
  // The four predicates below are non-ghost (computable); their existence
  // constitutes the decidability proof.

  // Find position of first zero at or after 'start'; returns |s| if none
  function FindZero(s: seq<nat>, start: nat): nat
    requires start <= |s|
    ensures start <= FindZero(s, start) <= |s|
    ensures FindZero(s, start) < |s| ==> s[FindZero(s, start)] == 0
    ensures forall j :: start <= j < FindZero(s, start) ==> s[j] != 0
    decreases |s| - start
  {
    if start == |s| then |s|
    else if s[start] == 0 then start
    else FindZero(s, start + 1)
  }

  // (a) Same node field
  predicate SameNodeField(a: Tumbler, b: Tumbler)
    requires ValidAddress(a) && ValidAddress(b)
  {
    a.components[..FindZero(a.components, 0)] ==
    b.components[..FindZero(b.components, 0)]
  }

  // (b) Same node and user fields
  predicate SameNodeUserField(a: Tumbler, b: Tumbler)
    requires ValidAddress(a) && ValidAddress(b)
  {
    var sa := a.components;
    var sb := b.components;
    var z0a := FindZero(sa, 0);
    var z0b := FindZero(sb, 0);
    if z0a >= |sa| || z0b >= |sb| then false
    else if sa[..z0a] != sb[..z0b] then false
    else sa[z0a+1..FindZero(sa, z0a+1)] == sb[z0b+1..FindZero(sb, z0b+1)]
  }

  // (c) Same node, user, and document fields
  predicate SameNodeUserDocField(a: Tumbler, b: Tumbler)
    requires ValidAddress(a) && ValidAddress(b)
  {
    var sa := a.components;
    var sb := b.components;
    var z0a := FindZero(sa, 0);
    var z0b := FindZero(sb, 0);
    if z0a >= |sa| || z0b >= |sb| then false
    else if sa[..z0a] != sb[..z0b] then false
    else
      var z1a := FindZero(sa, z0a + 1);
      var z1b := FindZero(sb, z0b + 1);
      if z1a >= |sa| || z1b >= |sb| then false
      else if sa[z0a+1..z1a] != sb[z0b+1..z1b] then false
      else sa[z1a+1..FindZero(sa, z1a+1)] == sb[z1b+1..FindZero(sb, z1b+1)]
  }

  // (d) Document field of a is a prefix of document field of b
  predicate DocFieldSubordination(a: Tumbler, b: Tumbler)
    requires ValidAddress(a) && ValidAddress(b)
  {
    var sa := a.components;
    var sb := b.components;
    var z0a := FindZero(sa, 0);
    var z0b := FindZero(sb, 0);
    if z0a >= |sa| || z0b >= |sb| then false
    else
      var z1a := FindZero(sa, z0a + 1);
      var z1b := FindZero(sb, z0b + 1);
      if z1a >= |sa| || z1b >= |sb| then false
      else
        var docA := sa[z1a+1..FindZero(sa, z1a+1)];
        var docB := sb[z1b+1..FindZero(sb, z1b+1)];
        |docA| <= |docB| && docA == docB[..|docA|]
  }

  // Field sharing is hierarchically nested
  lemma DecidableContainment(a: Tumbler, b: Tumbler)
    requires ValidAddress(a) && ValidAddress(b)
    ensures SameNodeUserDocField(a, b) ==> SameNodeUserField(a, b)
    ensures SameNodeUserField(a, b) ==> SameNodeField(a, b)
  { }
}

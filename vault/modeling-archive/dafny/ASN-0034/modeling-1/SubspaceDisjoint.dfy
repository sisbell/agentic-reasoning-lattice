include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// T7 — SubspaceDisjoint
module SubspaceDisjoint {
  import opened TumblerAlgebra

  // Find first zero in s from position start onward; returns |s| if none
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

  // Position of E₁: component immediately after the third zero separator
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

  // Tumbler has an element field (3rd zero exists with a component after it)
  predicate HasElementField(t: Tumbler) {
    E1Pos(t) < |t.components|
  }

  // First component of the element field
  function E1(t: Tumbler): nat
    requires HasElementField(t)
  {
    t.components[E1Pos(t)]
  }

  // T7: different subspace identifiers imply different tumblers
  lemma SubspaceDisjoint(a: Tumbler, b: Tumbler)
    requires HasElementField(a)
    requires HasElementField(b)
    requires E1(a) != E1(b)
    ensures a != b
  { }
}

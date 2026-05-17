// ASN-0034: T4b — UniqueParse
// The four partial functions N, U, D, E : T ⇀ T extract the node, user,
// document, and element sub-sequences of t, with domains fixed by zeros(t):
// N is defined on the T4-valid subdomain; U, D, E require zeros(t) ≥ 1, ≥ 2,
// = 3 respectively.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"

module UniqueParse {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing

  // Shift each index in s by 1 (used in ZeroIndices recursion).
  function Shift(s: seq<nat>): seq<nat>
    decreases |s|
    ensures |Shift(s)| == |s|
    ensures forall i :: 0 <= i < |s| ==> Shift(s)[i] == s[i] + 1
  {
    if |s| == 0 then []
    else [s[0] + 1] + Shift(s[1..])
  }

  // 0-indexed positions of all zeros in s, in strictly increasing order.
  function ZeroIndices(s: seq<Carrier>): seq<nat>
    decreases |s|
    ensures |ZeroIndices(s)| == CountZeros(s)
    ensures forall i :: 0 <= i < |ZeroIndices(s)| ==> ZeroIndices(s)[i] < |s|
    ensures forall i :: 0 <= i < |ZeroIndices(s)| ==> s[ZeroIndices(s)[i]] == 0
    ensures forall i, j :: 0 <= i < j < |ZeroIndices(s)| ==>
              ZeroIndices(s)[i] < ZeroIndices(s)[j]
    ensures |ZeroIndices(s)| > 0 && |s| > 0 && s[0] != 0 ==>
              ZeroIndices(s)[0] >= 1
    ensures |ZeroIndices(s)| > 0 && |s| > 0 && s[|s|-1] != 0 ==>
              ZeroIndices(s)[|ZeroIndices(s)|-1] < |s| - 1
  {
    if |s| == 0 then []
    else if s[0] == 0 then [0] + Shift(ZeroIndices(s[1..]))
    else Shift(ZeroIndices(s[1..]))
  }

  // Node-field projection: prefix of t.components before the first zero,
  // or all of t.components if no zero exists (Case k = 0).
  function N(t: Tumbler): (r: Tumbler)
    requires InT(t)
    requires HierarchicalParsing(t)
    ensures InT(r)
  {
    var zs := ZeroIndices(t.components);
    if |zs| == 0 then t
    else
      assert Component(t, 1) == t.components[0];
      assert t.components[0] != 0;
      assert zs[0] >= 1;
      Tumbler(t.components[..zs[0]])
  }

  // User-field projection: components between the first and second zero,
  // or from after the first zero to the end if only one zero exists.
  function U(t: Tumbler): (r: Tumbler)
    requires InT(t)
    requires HierarchicalParsing(t)
    requires Zeros(t) >= 1
    ensures InT(r)
  {
    var zs := ZeroIndices(t.components);
    if |zs| == 1 then
      assert Component(t, Length(t)) == t.components[|t.components|-1];
      assert t.components[|t.components|-1] != 0;
      assert zs[0] < |t.components| - 1;
      Tumbler(t.components[zs[0]+1..])
    else
      assert zs[0] < zs[1];
      assert t.components[zs[0]] == 0;
      assert t.components[zs[1]] == 0;
      assert zs[0] < |t.components| - 1;
      // HP at 1-indexed i = zs[0]+1 gives: !(Component(t, zs[0]+1)==0 && Component(t, zs[0]+2)==0)
      assert 1 <= zs[0]+1 < Length(t);
      assert Component(t, zs[0]+1) == t.components[zs[0]];
      assert Component(t, zs[0]+2) == t.components[zs[0]+1];
      assert t.components[zs[0]+1] != 0;
      assert zs[1] != zs[0] + 1;
      assert zs[1] >= zs[0] + 2;
      Tumbler(t.components[zs[0]+1..zs[1]])
  }

  // Document-field projection: components between the second and third zero,
  // or from after the second zero to the end if only two zeros exist.
  function D(t: Tumbler): (r: Tumbler)
    requires InT(t)
    requires HierarchicalParsing(t)
    requires Zeros(t) >= 2
    ensures InT(r)
  {
    var zs := ZeroIndices(t.components);
    if |zs| == 2 then
      assert Component(t, Length(t)) == t.components[|t.components|-1];
      assert t.components[|t.components|-1] != 0;
      assert zs[1] < |t.components| - 1;
      Tumbler(t.components[zs[1]+1..])
    else
      assert zs[1] < zs[2];
      assert t.components[zs[1]] == 0;
      assert t.components[zs[2]] == 0;
      assert zs[1] < |t.components| - 1;
      assert 1 <= zs[1]+1 < Length(t);
      assert Component(t, zs[1]+1) == t.components[zs[1]];
      assert Component(t, zs[1]+2) == t.components[zs[1]+1];
      assert t.components[zs[1]+1] != 0;
      assert zs[2] != zs[1] + 1;
      assert zs[2] >= zs[1] + 2;
      Tumbler(t.components[zs[1]+1..zs[2]])
  }

  // Element-field projection: components after the third zero.
  function E(t: Tumbler): (r: Tumbler)
    requires InT(t)
    requires HierarchicalParsing(t)
    requires Zeros(t) == 3
    ensures InT(r)
  {
    var zs := ZeroIndices(t.components);
    assert Component(t, Length(t)) == t.components[|t.components|-1];
    assert t.components[|t.components|-1] != 0;
    assert zs[2] < |t.components| - 1;
    Tumbler(t.components[zs[2]+1..])
  }
}

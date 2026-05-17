// ASN-0034: TA5-SIG — LastSignificantPosition
// sig(t) is the index of the rightmost nonzero component of t; when t has
// no nonzero component, sig(t) = #t by convention. Always 1 <= sig(t) <= #t.
include "./CarrierSetDefinition.dfy"

module LastSignificantPosition {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  // Constructive scan from index k downward, returning the largest index
  // i <= k with Component(t, i) != 0. The precondition guarantees such an
  // i exists, so termination at k == 1 only fires when Component(t, 1) != 0.
  function LastSignificantPositionFromIndex(t: Tumbler, k: nat): nat
    requires InT(t)
    requires 1 <= k <= Length(t)
    requires exists i :: 1 <= i <= k && Component(t, i) != 0
    ensures 1 <= LastSignificantPositionFromIndex(t, k) <= k
    ensures Component(t, LastSignificantPositionFromIndex(t, k)) != 0
    ensures forall j :: LastSignificantPositionFromIndex(t, k) < j <= k ==>
              Component(t, j) == 0
    decreases k
  {
    if Component(t, k) != 0 then k
    else LastSignificantPositionFromIndex(t, k - 1)
  }

  function LastSignificantPosition(t: Tumbler): nat
    requires InT(t)
    ensures 1 <= LastSignificantPosition(t) <= Length(t)
    ensures (exists i :: 1 <= i <= Length(t) && Component(t, i) != 0) ==>
              Component(t, LastSignificantPosition(t)) != 0 &&
              (forall j :: LastSignificantPosition(t) < j <= Length(t) ==>
                 Component(t, j) == 0)
    ensures (forall i :: 1 <= i <= Length(t) ==> Component(t, i) == 0) ==>
              LastSignificantPosition(t) == Length(t)
  {
    if exists i :: 1 <= i <= Length(t) && Component(t, i) != 0 then
      LastSignificantPositionFromIndex(t, Length(t))
    else
      Length(t)
  }
}

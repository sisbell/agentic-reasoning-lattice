// ASN-0034: TumblerSub — definition (DEF)
// Tumbler subtraction a ⊖ w, defined component-wise on padded sequences:
//   L = max(#a, #w); k = zpd(a, w);
//   k undefined ⇒ rᵢ = 0 for all i ∈ [1, L];
//   k defined   ⇒ rᵢ = 0 for i < k; rₖ = aₖ − wₖ (padded);
//                  rᵢ = aᵢ (padded) for k < i ≤ L.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./ZeroPaddedDivergence.dfy"

module TumblerSub {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened ZeroPaddedDivergence
  import opened NatCarrierSet

  // Saturating subtraction: returns x - y when x >= y, else 0. Keeps the result
  // total over ℕ; the spec relies on the precondition consequence that at
  // k = zpd(a, w) we have aₖ >= wₖ, making the saturation immaterial there.
  function SatSub(x: Carrier, y: Carrier): Carrier {
    if x >= y then x - y else 0
  }

  // Component i (1-indexed) of a ⊖ w under the case split on k = zpd(a, w).
  function SubComponent(a: Tumbler, w: Tumbler, k: nat, i: nat): Carrier
    requires InT(a) && InT(w)
    requires 1 <= i
  {
    if k == 0 then 0
    else if i < k then 0
    else if i == k then SatSub(PaddedComponent(a, k), PaddedComponent(w, k))
    else PaddedComponent(a, i)
  }

  // Construct the result sequence by indexing from 1 to L (built in reverse).
  function BuildSubSeq(a: Tumbler, w: Tumbler, k: nat, L: nat): (s: seq<Carrier>)
    requires InT(a) && InT(w)
    ensures |s| == L
    ensures forall i :: 0 <= i < L ==> s[i] == SubComponent(a, w, k, i + 1)
    decreases L
  {
    if L == 0 then []
    else BuildSubSeq(a, w, k, L - 1) + [SubComponent(a, w, k, L)]
  }

  function TumblerSub(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    ensures InT(r)
    ensures Length(r) == (if Length(a) >= Length(w) then Length(a) else Length(w))
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
              ==> (PositiveTumbler.PositiveTumbler(r)
                   && ActionPoint.ActionPoint(r) ==
                        ZeroPaddedDivergence.ZeroPaddedDivergence(a, w))
  {
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    Tumbler(BuildSubSeq(a, w, k, L))
  }
}

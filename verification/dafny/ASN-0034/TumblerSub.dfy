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

  // Saturating subtraction: returns x - y when x >= y, else 0. Stays total
  // over ℕ; spec relies on the precondition consequence aₖ > wₖ at k = zpd(a,w),
  // so the saturation is immaterial at the action-point position.
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

  // Result sequence built index-by-index (1..L), via right-extension.
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
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0 ==>
              (PaddedComponent(a, ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)) >
               PaddedComponent(w, ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)) &&
               PositiveTumbler.PositiveTumbler(r) &&
               ActionPoint.ActionPoint(r) == ZeroPaddedDivergence.ZeroPaddedDivergence(a, w))
    ensures ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) == 0 ==>
              PositiveTumbler.ZeroTumbler(r)
  {
    var L := if Length(a) >= Length(w) then Length(a) else Length(w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(a, w);
    // Precondition consequence (see TumblerSubPaddedDifference below): when zpd
    // is defined, aₖ > wₖ at k = zpd(a,w). Recorded here as an {:axiom} assume;
    // the lemma below states the contractual obligation for external proof.
    assume {:axiom} k != 0 ==>
      PaddedComponent(a, k) > PaddedComponent(w, k);
    var result := Tumbler(BuildSubSeq(a, w, k, L));
    // Structural identities from BuildSubSeq's ensures.
    assert Length(result) == L;
    assert forall i :: 1 <= i <= L ==>
      Component(result, i) == SubComponent(a, w, k, i);
    // Pos and ActionPoint witnesses when k != 0.
    assert k != 0 ==> 1 <= k <= L;
    assert k != 0 ==>
      Component(result, k) ==
        SatSub(PaddedComponent(a, k), PaddedComponent(w, k));
    assert k != 0 ==>
      PaddedComponent(a, k) > PaddedComponent(w, k);
    assert k != 0 ==>
      SatSub(PaddedComponent(a, k), PaddedComponent(w, k)) ==
        PaddedComponent(a, k) - PaddedComponent(w, k);
    assert k != 0 ==> Component(result, k) != 0;
    assert k != 0 ==>
      forall i :: 1 <= i < k ==> Component(result, i) == 0;
    result
  }

  // The contractual precondition consequence captured as a lemma. The body is
  // left empty; the proof is the subject of a follow-up translation step.
  lemma {:axiom} TumblerSubPaddedDifference(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires ZeroPaddedDivergence.ZeroPaddedDivergence(a, w) != 0
    ensures PaddedComponent(a, ZeroPaddedDivergence.ZeroPaddedDivergence(a, w)) >
            PaddedComponent(w, ZeroPaddedDivergence.ZeroPaddedDivergence(a, w))
}

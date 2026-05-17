// ASN-0034: TA6 — ZeroTumblers
// Corollary: every zero tumbler is (a) not a valid address (excluded by T4's
// first-component rule) and (b) strictly less than every positive tumbler
// under the lexicographic order.
include "./CarrierSetDefinition.dfy"
include "./HierarchicalParsing.dfy"
include "./PositiveTumbler.dfy"
include "./LexicographicOrder.dfy"

module ZeroTumblers {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalParsing
  import opened PositiveTumbler
  import opened LexicographicOrder
  import opened NatStrictTotalOrder

  function FirstNonzeroFrom(t: Tumbler, k: nat): nat
    requires InT(t)
    requires 1 <= k <= Length(t)
    requires exists i :: k <= i <= Length(t) && Component(t, i) != 0
    ensures k <= FirstNonzeroFrom(t, k) <= Length(t)
    ensures Component(t, FirstNonzeroFrom(t, k)) != 0
    ensures forall j :: k <= j < FirstNonzeroFrom(t, k) ==> Component(t, j) == 0
    decreases Length(t) - k
  {
    if Component(t, k) != 0 then k
    else FirstNonzeroFrom(t, k + 1)
  }

  lemma ZeroNotValidAddress(t: Tumbler)
    requires InT(t)
    requires ZeroTumbler(t)
    ensures !HierarchicalParsing.HierarchicalParsing(t)
  { }

  lemma LexOrderWitnessCase1(s: Tumbler, t: Tumbler, k: nat)
    requires InT(s) && InT(t)
    requires 1 <= k <= Length(s) && k <= Length(t)
    requires forall i :: 1 <= i < k ==>
               Component(s, i) == Component(t, i)
    requires Less(Component(s, k), Component(t, k))
    ensures LexicographicOrder.LexicographicOrder(s, t)
  {
    assert
      && 1 <= k
      && (forall i :: 1 <= i < k ==>
            i <= Length(s) && i <= Length(t) &&
            Component(s, i) == Component(t, i))
      && (k <= Length(s) && k <= Length(t) && Less(Component(s, k), Component(t, k)));
  }

  lemma LexOrderWitnessCase2(s: Tumbler, t: Tumbler)
    requires InT(s) && InT(t)
    requires Length(s) + 1 <= Length(t)
    requires forall i :: 1 <= i <= Length(s) ==>
               Component(s, i) == Component(t, i)
    ensures LexicographicOrder.LexicographicOrder(s, t)
  {
    var k := Length(s) + 1;
    assert
      && 1 <= k
      && (forall i :: 1 <= i < k ==>
            i <= Length(s) && i <= Length(t) &&
            Component(s, i) == Component(t, i))
      && (k == Length(s) + 1 && k <= Length(t));
  }

  lemma ZeroBelowPositive(s: Tumbler, t: Tumbler)
    requires InT(s) && InT(t)
    requires ZeroTumbler(s)
    requires PositiveTumbler.PositiveTumbler(t)
    ensures LexicographicOrder.LexicographicOrder(s, t)
  {
    var j := FirstNonzeroFrom(t, 1);
    if j <= Length(s) {
      LexOrderWitnessCase1(s, t, j);
    } else {
      LexOrderWitnessCase2(s, t);
    }
  }

  lemma ZeroTumblers(s: Tumbler, t: Tumbler)
    requires InT(s) && InT(t)
    requires ZeroTumbler(s)
    ensures !HierarchicalParsing.HierarchicalParsing(s)
    ensures PositiveTumbler.PositiveTumbler(t) ==>
              LexicographicOrder.LexicographicOrder(s, t)
  {
    ZeroNotValidAddress(s);
    if PositiveTumbler.PositiveTumbler(t) {
      ZeroBelowPositive(s, t);
    }
  }
}

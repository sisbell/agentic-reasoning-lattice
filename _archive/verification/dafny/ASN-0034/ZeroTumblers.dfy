include "./LexicographicOrder.dfy"
include "./HierarchicalParsing.dfy"

module ZeroTumblers {
  // TA6 — ZeroTumblers
  // (a) Zero tumblers are not valid addresses
  // (b) Zero tumblers are less than every positive tumbler under T1

  import LO = LexicographicOrder
  import HP = HierarchicalParsing
  import SE = SyntacticEquivalence
  import CD = CarrierSetDefinition

  ghost predicate AllZero(s: seq<nat>) {
    forall i :: 0 <= i < |s| ==> s[i] == 0
  }

  ghost predicate HasPositive(s: seq<nat>) {
    exists i :: 0 <= i < |s| && s[i] > 0
  }

  // (a) Zero tumblers are not valid addresses
  lemma ZeroNotValidAddress(t: SE.Tumbler)
    requires SE.ValidTumbler(t)
    requires AllZero(t.components)
    ensures !HP.ValidAddress(t)
  { }

  // (b) Zero tumblers are less than every positive tumbler under T1
  lemma ZeroLessThanPositive(s: CD.Tumbler, t: CD.Tumbler)
    requires CD.ValidTumbler(s)
    requires CD.ValidTumbler(t)
    requires AllZero(s.components)
    requires HasPositive(t.components)
    ensures LO.LessThan(s, t)
  {
    LO.LessThanTrichotomy(s, t);
  }
}

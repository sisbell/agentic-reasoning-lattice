include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// TA6 — ZeroTumblerSentinel
module ZeroTumblerSentinel {
  import opened TumblerAlgebra

  // A zero tumbler: every component is zero
  ghost predicate IsZeroTumbler(t: Tumbler) {
    forall i :: 0 <= i < |t.components| ==> t.components[i] == 0
  }

  // Part 1: No zero tumbler is a valid address.
  // ValidAddress (T4) requires components[0] != 0, which implies
  // PositiveTumbler. A zero tumbler has no nonzero components.
  lemma ZeroNotValidAddress(t: Tumbler)
    requires IsZeroTumbler(t)
    ensures !PositiveTumbler(t)
  { }

  // Part 2: Every zero tumbler is less than every positive tumbler.
  // Witness: if s is shorter than t's action point, s is a proper
  // prefix (all shared components are zero); otherwise, s diverges
  // at the action point where s[ap]=0 < t[ap].
  lemma ZeroLessThanPositive(s: Tumbler, t: Tumbler)
    requires IsZeroTumbler(s)
    requires PositiveTumbler(t)
    ensures LessThan(s, t)
  {
    var ap := ActionPoint(t);
    if |s.components| <= ap {
      LessThanIntro(s, t, |s.components|);
    } else {
      LessThanIntro(s, t, ap);
    }
  }
}

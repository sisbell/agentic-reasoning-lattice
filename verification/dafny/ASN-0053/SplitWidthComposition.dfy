// ASN-0053: S5 — SplitWidthComposition (LEMMA)
// Under the conditions of S4 (SplitPartition), the widths of the two
// parts compose to the original width: d ⊕ d' = ℓ.
include "SplitPartition.dfy"
include "../ASN-0034/AdditionAssociative.dfy"
include "../ASN-0034/LeftCancellation.dfy"

module SplitWidthComposition {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import SP = SplitPartition
  import AA = AdditionAssociative
  import LC = LeftCancellation

  // S5: SplitWidthComposition.
  // The widths of the two split parts compose to the original width: d ⊕ d' = ℓ.
  // ValidSpan/LevelUniform conjuncts appear first so their precondition-establishing
  // facts are available when the solver checks TumblerAdd's preconditions.
  lemma SplitWidthComposition(sigma: SP.SpanValue, p: Tumbler)
    requires SP.ValidSpan(sigma) && SP.LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, SP.Reach(sigma))
    ensures
      var lam := SP.SplitPartition(sigma, p).left;
      var rho := SP.SplitPartition(sigma, p).right;
      SP.ValidSpan(lam) && SP.ValidSpan(rho) && SP.LevelUniform(lam) &&
      (var ddd := TumblerAdd.TumblerAdd(lam.width, rho.width);
       ddd == sigma.width &&
       PositiveTumbler.PositiveTumbler(ddd) &&
       ActionPoint.ActionPoint(ddd) ==
         (if ActionPoint.ActionPoint(lam.width) <= ActionPoint.ActionPoint(rho.width)
          then ActionPoint.ActionPoint(lam.width)
          else ActionPoint.ActionPoint(rho.width)))
  {
    SP.SplitPartitionTheorem(sigma, p);
    var lam := SP.SplitPartition(sigma, p).left;
    var rho := SP.SplitPartition(sigma, p).right;
    var s   := sigma.start;
    var d   := lam.width;
    var dd  := rho.width;
    var ell := sigma.width;

    // AP(dd) ≤ Length(d): ValidSpan(rho) gives AP(dd) ≤ Length(rho.start) = Length(p);
    // LevelUniform(lam) gives Length(d) = Length(lam.start) = Length(s) = Length(p).
    assert Length(d) == Length(s);
    assert ActionPoint.ActionPoint(dd) <= Length(d);

    // Displacement chain: reach(lam)=p gives s⊕d=p; reach(rho)=reach(sigma) gives p⊕d'=s⊕ℓ.
    assert TumblerAdd.TumblerAdd(TumblerAdd.TumblerAdd(s, d), dd) == TumblerAdd.TumblerAdd(s, ell);

    // TA-assoc: (s⊕d)⊕d' = s⊕(d⊕d'), Pos(d⊕d'), AP(d⊕d') = min(AP(d),AP(d')).
    AA.AdditionAssociative(s, d, dd);
    var ddd := TumblerAdd.TumblerAdd(d, dd);
    assert TumblerAdd.TumblerAdd(s, ddd) == TumblerAdd.TumblerAdd(s, ell);

    // AP(ddd) ≤ Length(s) for TA-LC.
    if ActionPoint.ActionPoint(d) <= ActionPoint.ActionPoint(dd) {
      assert ActionPoint.ActionPoint(ddd) == ActionPoint.ActionPoint(d);
    } else {
      assert ActionPoint.ActionPoint(ddd) == ActionPoint.ActionPoint(dd);
      assert ActionPoint.ActionPoint(ddd) <= Length(s);
    }

    // TA-LC: s⊕(d⊕d') = s⊕ℓ ⟹ d⊕d' = ℓ.
    LC.LeftCancellation(s, ddd, ell);
  }
}

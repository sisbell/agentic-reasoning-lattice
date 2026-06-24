// ASN-0053: S5 — SplitWidthComposition (LEMMA/theorem)
// For a level-uniform span σ split at interior point p,
// the widths of the two parts compose to the original width:
//   TumblerAdd(p ⊖ start(σ), reach(σ) ⊖ p) = width(σ)
include "./SpanDefs.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "./LevelConstraint.dfy"
include "../ASN-0034/AdditionAssociative.dfy"
include "../ASN-0034/LeftCancellation.dfy"

module SplitWidthComposition {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import LO = LexicographicOrder
  import LC = LevelConstraint
  import WF = WellFormedSpanFromEndpoints
  import TS = TumblerSub
  import TA = TumblerAdd   // explicit alias: AdditionAssociative brings TumblerAdd as visible module
  import AP = ActionPoint  // explicit alias: same reason
  import AA = AdditionAssociative
  import LCan = LeftCancellation

  // S5: width(λ) ⊕ width(ρ) = width(σ), where λ and ρ are the two split parts.
  // ValidSpan ensures #1/#2 serve as well-formedness dischargers for the TumblerAdd
  // call in subsequent ensures (Dafny checks ensures preconditions from requires +
  // preceding ensures, not the body).  The contract postconditions are #3/#4/#5.
  lemma SplitWidthComposition(sigma: SpanEntry, p: Tumbler)
    requires ValidSpan(sigma)
    requires LC.LevelUniform(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(sigma.start, p)
    requires LO.LexicographicOrder(p, Reach(sigma))
    requires Length(p) == Length(sigma.start)
    ensures ValidSpan(SpanEntry(sigma.start, TS.TumblerSub(p, sigma.start)))
    ensures ValidSpan(SpanEntry(p, TS.TumblerSub(Reach(sigma), p)))
    ensures TA.TumblerAdd(TS.TumblerSub(p, sigma.start), TS.TumblerSub(Reach(sigma), p)) == sigma.width
    ensures PositiveTumbler.PositiveTumbler(TA.TumblerAdd(TS.TumblerSub(p, sigma.start), TS.TumblerSub(Reach(sigma), p)))
    ensures
      var d  := TS.TumblerSub(p, sigma.start);
      var d' := TS.TumblerSub(Reach(sigma), p);
      (AP.ActionPoint(d) <= AP.ActionPoint(d') ==> AP.ActionPoint(TA.TumblerAdd(d, d')) == AP.ActionPoint(d)) &&
      (AP.ActionPoint(d') <= AP.ActionPoint(d) ==> AP.ActionPoint(TA.TumblerAdd(d, d')) == AP.ActionPoint(d'))
  {
    var s := sigma.start;
    var w := sigma.width;
    var r := Reach(sigma);
    var w1 := TS.TumblerSub(p, s);
    var w2 := TS.TumblerSub(r, p);

    // w1 is valid: TumblerAdd(s, w1) = p, Pos(w1), AP(w1) <= Length(s)
    WF.WellFormedSpanFromEndpoints(s, p);
    assert TA.TumblerAdd(s, w1) == p;

    // Length(r) = Length(s) from LevelConstraint
    LC.LevelConstraint(sigma);
    assert Length(r) == Length(s);

    // w2 is valid: TumblerAdd(p, w2) = r, Pos(w2), AP(w2) <= Length(p)
    WF.WellFormedSpanFromEndpoints(p, r);
    assert TA.TumblerAdd(p, w2) == r;

    // AP(w2) <= Length(p) = Length(s) = Length(w1), so TumblerAdd(w1, w2) is well-formed
    assert AP.ActionPoint(w2) <= Length(w1);

    // Associativity: TumblerAdd(TumblerAdd(s, w1), w2) = TumblerAdd(s, TumblerAdd(w1, w2))
    AA.AdditionAssociative(s, w1, w2);
    var w12 := TA.TumblerAdd(w1, w2);

    // Chain: TumblerAdd(s, w12) = TumblerAdd(TumblerAdd(s, w1), w2) = TumblerAdd(p, w2) = r
    assert TA.TumblerAdd(s, w12) == r;

    // TumblerAdd(s, w) = r by definition of Reach
    assert TA.TumblerAdd(s, w) == r;

    // AP(w12) = min(AP(w1), AP(w2)) <= Length(s) in both branches
    if AP.ActionPoint(w1) <= AP.ActionPoint(w2) {
      assert AP.ActionPoint(w12) == AP.ActionPoint(w1);
    } else {
      assert AP.ActionPoint(w12) == AP.ActionPoint(w2);
    }
    assert AP.ActionPoint(w12) <= Length(s);

    // LeftCancellation: TumblerAdd(s, w12) = TumblerAdd(s, w) => w12 = w
    LCan.LeftCancellation(s, w12, w);
  }
}

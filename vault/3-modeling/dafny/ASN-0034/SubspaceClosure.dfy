include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"

module SubspaceClosure {
  // TA7a — SubspaceClosure
  // S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd
  import TS = TumblerSub

  // Definition: S — ordinals with all positive components
  ghost predicate InS(o: Tumbler) {
    ValidTumbler(o) && forall i :: 0 <= i < |o.components| ==> o.components[i] > 0
  }

  // Tail components of displacement are positive (after action point)
  ghost predicate TailPositive(w: Tumbler)
    requires ValidTumbler(w)
    requires IsPositive(w)
  {
    var k := TA.ActionPoint(w);
    forall i :: k < i < |w.components| ==> w.components[i] > 0
  }

  // Addition closure in T: o ⊕ w ∈ T, #(o ⊕ w) = #w
  lemma AdditionClosureInT(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |o.components|
    ensures ValidTumbler(TA.TumblerAdd(o, w))
    ensures |TA.TumblerAdd(o, w).components| == |w.components|
  { }

  // Addition closure in S: o ⊕ w ∈ S when tail components of w are positive
  lemma AdditionClosureInS(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TA.ActionPoint(w) < |o.components|
    requires TailPositive(w)
    ensures InS(TA.TumblerAdd(o, w))
  { }

  // Subtraction closure in T: o ⊖ w ∈ T
  lemma SubtractionClosureInT(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TS.GreaterOrEqual(o, w)
    ensures ValidTumbler(TS.TumblerSub(o, w))
  { }

  // ⊖ S-membership, Case k≥2: actionPoint ≥ 2 (1-indexed) and #w ≤ #o
  // Divergence at position 1 (1-indexed) since w₁=0 but o₁>0; result = o ∈ S
  lemma SubtractionSHighAP(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TS.GreaterOrEqual(o, w)
    requires TA.ActionPoint(w) >= 1  // actionPoint ≥ 2 in 1-indexed
    requires |w.components| <= |o.components|
    ensures TS.TumblerSub(o, w) == o
    ensures InS(TS.TumblerSub(o, w))
  {
    var len := TS.Max(|o.components|, |w.components|);
    var pa := TS.Pad(o.components, len);
    var pw := TS.Pad(w.components, len);
    assert w.components[0] == 0;
    assert pa[0] > 0 && pw[0] == 0;
    assert TS.FindDivergence(pa, pw, 0) == 0;
  }

  // ⊖ S-membership, Case k=1, d=1: actionPoint = 1 (1-indexed), o₁ ≠ w₁, #w ≤ #o
  // r₁ = o₁ - w₁ > 0, rᵢ = oᵢ > 0 for i > 1 → result ∈ S
  lemma SubtractionSLowAP_Div1(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TS.GreaterOrEqual(o, w)
    requires TA.ActionPoint(w) == 0  // actionPoint = 1 in 1-indexed
    requires o.components[0] != w.components[0]
    requires |w.components| <= |o.components|
    ensures InS(TS.TumblerSub(o, w))
  {
    var len := TS.Max(|o.components|, |w.components|);
    var pa := TS.Pad(o.components, len);
    var pw := TS.Pad(w.components, len);
    assert pa[0] != pw[0];
    assert TS.FindDivergence(pa, pw, 0) == 0;
    assert o != w;
    assert o.components[0] > w.components[0];
  }

  // ⊖ negative characterization, Case k=1, d>1: o₁ = w₁ → r₁ = 0, result ∈ T \ S
  lemma SubtractionNotInS_LowAP_HighDiv(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TS.GreaterOrEqual(o, w)
    requires TA.ActionPoint(w) == 0  // actionPoint = 1 in 1-indexed
    requires o.components[0] == w.components[0]
    ensures !InS(TS.TumblerSub(o, w))
  {
    var len := TS.Max(|o.components|, |w.components|);
    var pa := TS.Pad(o.components, len);
    var pw := TS.Pad(w.components, len);
    assert pa[0] == pw[0];
    var d := TS.FindDivergence(pa, pw, 0);
    assert d >= 1;
    var r := TS.TumblerSub(o, w);
    assert r.components[0] == 0;
  }

  // ⊖ negative characterization: #w > #o → trailing zeros, result ∈ T \ S
  lemma SubtractionNotInS_LongW(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TS.GreaterOrEqual(o, w)
    requires |w.components| > |o.components|
    ensures !InS(TS.TumblerSub(o, w))
  {
    var len := TS.Max(|o.components|, |w.components|);
    assert len == |w.components|;
    var pa := TS.Pad(o.components, len);
    var pw := TS.Pad(w.components, len);
    var d := TS.FindDivergence(pa, pw, 0);
    var r := TS.TumblerSub(o, w);
    assert pa[|o.components|] == 0;
    if d == 0 {
      assert r.components[|o.components|] == 0;
    } else {
      assert r.components[0] == 0;
    }
  }

  // ⊖ single-component: #o = 1, #w = 1 → result ∈ S ∪ Z
  lemma SubtractionSSingleComponent(o: Tumbler, w: Tumbler)
    requires InS(o)
    requires ValidTumbler(w)
    requires IsPositive(w)
    requires TS.GreaterOrEqual(o, w)
    requires |o.components| == 1
    requires |w.components| == 1
    ensures InS(TS.TumblerSub(o, w)) || IsZero(TS.TumblerSub(o, w))
  {
    var r := TS.TumblerSub(o, w);
    if o.components[0] == w.components[0] {
      assert IsZero(r);
    } else {
      SubtractionSLowAP_Div1(o, w);
    }
  }
}

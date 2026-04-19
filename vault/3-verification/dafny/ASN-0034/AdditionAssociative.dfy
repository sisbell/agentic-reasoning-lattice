include "./TumblerAdd.dfy"

module AdditionAssociative {
  // TA-assoc — AdditionAssociative

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd

  lemma AdditionAssociative(a: Tumbler, b: Tumbler, c: Tumbler)
    requires ValidTumbler(a) && ValidTumbler(b) && ValidTumbler(c)
    requires IsPositive(b) && IsPositive(c)
    requires TA.ActionPoint(b) <= |a.components|
    requires TA.ActionPoint(c) <= |b.components|
    ensures TA.ActionPoint(TA.TumblerAdd(b, c)) ==
            if TA.ActionPoint(b) <= TA.ActionPoint(c) then TA.ActionPoint(b) else TA.ActionPoint(c)
    ensures |TA.TumblerAdd(TA.TumblerAdd(a, b), c).components| == |c.components|
    ensures |TA.TumblerAdd(a, TA.TumblerAdd(b, c)).components| == |c.components|
    ensures TA.TumblerAdd(TA.TumblerAdd(a, b), c) == TA.TumblerAdd(a, TA.TumblerAdd(b, c))
  {
    var k_b := TA.ActionPoint(b);
    var k_c := TA.ActionPoint(c);
    var bc := TA.TumblerAdd(b, c);

    // Establish IsPositive(bc) and ActionPoint(bc) via case analysis
    assert IsPositive(bc);
    if k_b < k_c {
      assert bc.components[k_b] != 0;
      assert TA.ActionPoint(bc) == k_b;
    } else if k_b == k_c {
      assert bc.components[k_b] != 0;
      assert TA.ActionPoint(bc) == k_b;
    } else {
      assert bc.components[k_c] != 0;
      assert TA.ActionPoint(bc) == k_c;
    }
  }
}

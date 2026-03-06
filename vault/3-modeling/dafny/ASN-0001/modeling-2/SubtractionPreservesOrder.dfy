include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubtractionPreservesOrder {

  import opened TumblerAlgebra

  // TA3 — SubtractionPreservesOrder (POST, ensures)
  // (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)

  // Case: a equals w after padding, b does not
  lemma SubCase_AEqW(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires TumblerSubtract(a, w) != TumblerSubtract(b, w)
    requires Pad(a.components, Max(|a.components|, |w.components|)) ==
             Pad(w.components, Max(|a.components|, |w.components|))
    requires Pad(b.components, Max(|b.components|, |w.components|)) !=
             Pad(w.components, Max(|b.components|, |w.components|))
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var len_a := Max(|a.components|, |w.components|);
    var len_b := Max(|b.components|, |w.components|);
    var pb := Pad(b.components, len_b);
    var pw_b := Pad(w.components, len_b);
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);
    var kb := FirstDiff(pb, pw_b);

    assert ra == Tumbler(Zeros(len_a));
    assert pb[kb] >= pw_b[kb];
    assert pb[kb] != pw_b[kb];
    assert rb.components[kb] == pb[kb] - pw_b[kb];
    assert rb.components[kb] > 0;

    if kb < len_a {
      assert ra.components[kb] == 0;
      LessThanIntro(ra, rb, kb);
    } else {
      assert len_a <= kb;
      assert len_a < len_b;
      assert forall i :: 0 <= i < len_a ==> ra.components[i] == 0 && rb.components[i] == 0;
      LessThanIntro(ra, rb, len_a);
    }
  }

  // General case: both diverge from w
  lemma SubCase_General(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires TumblerSubtract(a, w) != TumblerSubtract(b, w)
    requires Pad(a.components, Max(|a.components|, |w.components|)) !=
             Pad(w.components, Max(|a.components|, |w.components|))
    requires Pad(b.components, Max(|b.components|, |w.components|)) !=
             Pad(w.components, Max(|b.components|, |w.components|))
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var len_a := Max(|a.components|, |w.components|);
    var len_b := Max(|b.components|, |w.components|);
    var pa := Pad(a.components, len_a);
    var pw_a := Pad(w.components, len_a);
    var pb := Pad(b.components, len_b);
    var pw_b := Pad(w.components, len_b);
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);
    var ka := FirstDiff(pa, pw_a);
    var kb := FirstDiff(pb, pw_b);
    assert pa[ka] >= pw_a[ka] && pa[ka] != pw_a[ka];
    assert pb[kb] >= pw_b[kb] && pb[kb] != pw_b[kb];

    if ka > kb {
      assert ra.components[kb] == 0;
      assert rb.components[kb] > 0;
      LessThanIntro(ra, rb, kb);
    } else if ka == kb {
      if pa[ka] < pb[ka] {
        assert ra.components[ka] < rb.components[ka];
        LessThanIntro(ra, rb, ka);
      } else {
        assert pa[ka] == pb[ka];
        assert ra.components[ka] == rb.components[ka];
        ghost var j: nat :|
          j <= |a.components| && j <= |b.components| &&
          (forall i :: 0 <= i < j ==> a.components[i] == b.components[i]) &&
          ((j < |a.components| && j < |b.components| && a.components[j] < b.components[j]) ||
           (j == |a.components| && j < |b.components|));
        assert j > ka;
        if j < |a.components| && j < |b.components| {
          assert ra.components[j] == pa[j];
          assert rb.components[j] == pb[j];
          assert j < len_a && j < len_b;
          assert pa[j] == a.components[j];
          assert pb[j] == b.components[j];
          LessThanIntro(ra, rb, j);
        } else {
          if j < len_a {
            assert ra.components[j] == pa[j];
            assert pa[j] == 0;
            assert rb.components[j] == pb[j];
            if pb[j] > 0 {
              LessThanIntro(ra, rb, j);
            } else {
              assert len_a <= len_b;
              if len_a == len_b {
                assert ra.components != rb.components;
                var d := FirstDiff(ra.components, rb.components);
                assert ra.components[d] == pa[d];
                assert pa[d] == 0;
                LessThanIntro(ra, rb, d);
              } else {
                assert len_a < len_b;
                if ra.components == rb.components[..len_a] {
                  LessThanIntro(ra, rb, len_a);
                } else {
                  var d := FirstDiff(ra.components, rb.components[..len_a]);
                  assert rb.components[..len_a][d] == rb.components[d];
                  assert ra.components[d] == pa[d];
                  assert pa[d] == 0;
                  LessThanIntro(ra, rb, d);
                }
              }
            }
          } else {
            assert len_a <= j;
            assert len_a < len_b;
            LessThanIntro(ra, rb, len_a);
          }
        }
      }
    } else {
      // ka < kb: impossible — a diverges from w before b does,
      // meaning a > w == b at position ka, contradicting a < b
      assert false;
    }
  }

  lemma SubtractionPreservesOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w)) ||
            TumblerSubtract(a, w) == TumblerSubtract(b, w)
  {
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);
    if ra == rb { return; }

    var len_a := Max(|a.components|, |w.components|);
    var len_b := Max(|b.components|, |w.components|);
    var pa := Pad(a.components, len_a);
    var pw_a := Pad(w.components, len_a);
    var pb := Pad(b.components, len_b);
    var pw_b := Pad(w.components, len_b);

    if pa == pw_a {
      if pb == pw_b {
        assert ra == Tumbler(Zeros(len_a));
        assert rb == Tumbler(Zeros(len_b));
        assert len_a != len_b;
        assert len_a < len_b;
        LessThanIntro(ra, rb, len_a);
      } else {
        SubCase_AEqW(a, b, w);
      }
    } else if pb == pw_b {
      var ka := FirstDiff(pa, pw_a);
      assert pa[ka] >= pw_a[ka];
      assert pa[ka] != pw_a[ka];
      assert false;
    } else {
      SubCase_General(a, b, w);
    }
  }

}

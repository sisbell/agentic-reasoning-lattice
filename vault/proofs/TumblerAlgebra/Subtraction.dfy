// Subtraction properties (ASN-0034): TA2, TA3-strict, TA3-weak, TA4, ReverseInverse
module Subtraction {
  import opened TumblerAlgebra

  // ---------------------------------------------------------------------------
  // TA2 — WellDefinedSubtraction
  // ---------------------------------------------------------------------------

  ghost predicate SubtractionPrecondition(a: Tumbler, w: Tumbler) {
    Subtractable(a, w)
  }

  lemma WellDefinedSubtraction(a: Tumbler, w: Tumbler)
    requires SubtractionPrecondition(a, w)
    ensures |TumblerSubtract(a, w).components| == Max(|a.components|, |w.components|)
  { }

  // ---------------------------------------------------------------------------
  // TA3-strict — SubtractionStrictOrder
  // (a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b → a ⊖ w < b ⊖ w)
  // ---------------------------------------------------------------------------

  lemma StrictAgreeAtI(a: Tumbler, b: Tumbler, w: Tumbler, k: nat, i: nat)
    requires LessThanAt(a, b, k)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires |a.components| == |b.components|
    requires 0 <= i < k
    ensures i < |TumblerSubtract(a, w).components|
    ensures i < |TumblerSubtract(b, w).components|
    ensures TumblerSubtract(a, w).components[i] ==
            TumblerSubtract(b, w).components[i]
  {
    var len := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, len);
    var pb := Pad(b.components, len);
    var pwa := Pad(w.components, len);

    SubtractResultAt(a, w, i);
    SubtractResultAt(b, w, i);

    assert pa[i] == pb[i] by {
      assert i < k <= |a.components|;
      assert a.components[i] == b.components[i];
    }

    if pa == pwa {
      if pb == pwa {
      } else {
        var db := FirstDiff(pb, pwa);
        if db < k {
          assert pa[db] == pb[db];
          assert pa[db] != pwa[db];
          assert false;
        }
      }
    } else {
      var da := FirstDiff(pa, pwa);
      if pb == pwa {
        if da < k {
          assert pa[da] == pb[da];
          assert pb[da] != pwa[da];
          assert false;
        }
      } else {
        var db := FirstDiff(pb, pwa);
        if da < k && db < k {
          if da < db {
            assert pb[da] == pwa[da];
            assert pa[da] == pb[da];
            assert pa[da] != pwa[da];
            assert false;
          } else if db < da {
            assert pa[db] == pwa[db];
            assert pa[db] == pb[db];
            assert pb[db] != pwa[db];
            assert false;
          }
        } else if da < k {
          if db >= k {
          }
        } else if db < k {
          if da >= k {
            assert pa[db] == pb[db];
            assert pa[db] == pwa[db] by {
              assert db < da;
            }
            assert pb[db] != pwa[db];
            assert false;
          }
        }
      }
    }
  }

  lemma StrictOrderAtK(a: Tumbler, b: Tumbler, w: Tumbler, k: nat)
    requires LessThanAt(a, b, k)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires |a.components| == |b.components|
    requires k < |a.components| && k < |b.components|
    ensures k < |TumblerSubtract(a, w).components|
    ensures k < |TumblerSubtract(b, w).components|
    ensures TumblerSubtract(a, w).components[k] < TumblerSubtract(b, w).components[k]
  {
    var len := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, len);
    var pb := Pad(b.components, len);
    var pw := Pad(w.components, len);

    SubtractResultAt(a, w, k);
    SubtractResultAt(b, w, k);

    assert pa[k] == a.components[k];
    assert pb[k] == b.components[k];
    assert a.components[k] < b.components[k];

    if pa == pw {
      assert pb != pw;
      var db := FirstDiff(pb, pw);
      if db < k {
        assert pa[db] == pb[db];
        assert pa[db] != pw[db];
        assert false;
      }
      assert db == k;
    } else {
      var da := FirstDiff(pa, pw);
      if pb == pw {
        if da < k {
          assert pa[da] == pb[da];
          assert pb[da] == pw[da];
          assert false;
        }
        assert da == k;
        assert pa[k] >= pw[k];
        assert pa[k] < pb[k];
        assert pb[k] == pw[k];
        assert false;
      } else {
        var db := FirstDiff(pb, pw);
        if da < k {
          assert pa[da] == pb[da];
          assert pb[da] == pw[da] || db <= da;
          if db > da {
            assert pb[da] == pw[da];
            assert pa[da] == pb[da];
            assert pa[da] != pw[da];
            assert false;
          }
          assert db == da;
        } else if da == k {
          if db < k {
            assert pa[db] == pb[db];
            assert pa[db] == pw[db];
            assert pb[db] != pw[db];
            assert false;
          }
          if db > k {
            assert pb[k] == pw[k];
            assert pa[k] < pb[k];
            assert pa[k] >= pw[k];
            assert false;
          }
          assert db == k;
        } else {
          assert pa[k] == pw[k];
          if db < k {
            assert pa[db] == pb[db];
            assert pa[db] == pw[db];
            assert pb[db] != pw[db];
            assert false;
          }
          if db > k {
            assert pb[k] == pw[k];
            assert pa[k] == pw[k];
            assert pa[k] == pb[k];
            assert a.components[k] < b.components[k];
            assert false;
          }
          assert db == k;
        }
      }
    }
  }

  lemma SubtractionStrictOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires |a.components| == |b.components|
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var k: nat :| LessThanAt(a, b, k);
    assert k < |a.components| && k < |b.components|;

    forall i | 0 <= i < k
      ensures TumblerSubtract(a, w).components[i] ==
              TumblerSubtract(b, w).components[i]
    { StrictAgreeAtI(a, b, w, k, i); }

    StrictOrderAtK(a, b, w, k);
    LessThanIntro(TumblerSubtract(a, w), TumblerSubtract(b, w), k);
  }

  // ---------------------------------------------------------------------------
  // TA3-weak — SubtractionWeakOrder
  // (a < b ∧ a ≥ w ∧ b ≥ w → a ⊖ w ≤ b ⊖ w)
  // ---------------------------------------------------------------------------

  lemma PadAgreesBeforeK(ac: seq<nat>, bc: seq<nat>, wc: seq<nat>, k: nat)
    requires k <= |ac| && k <= |bc|
    requires forall j :: 0 <= j < k ==> ac[j] == bc[j]
    ensures forall i :: 0 <= i < k ==>
      Pad(ac, Max(|ac|, |wc|))[i] == Pad(bc, Max(|bc|, |wc|))[i] &&
      Pad(wc, Max(|ac|, |wc|))[i] == Pad(wc, Max(|bc|, |wc|))[i]
  {
    forall i | 0 <= i < k
      ensures Pad(ac, Max(|ac|, |wc|))[i] == Pad(bc, Max(|bc|, |wc|))[i]
      ensures Pad(wc, Max(|ac|, |wc|))[i] == Pad(wc, Max(|bc|, |wc|))[i]
    {
      assert i < |ac| && i < |bc|;
    }
  }

  lemma DivergenceSameBeforeK(
    pa: seq<nat>, pwa: seq<nat>, pb: seq<nat>, pwb: seq<nat>, k: nat
  )
    requires |pa| >= k && |pwa| == |pa| && |pb| >= k && |pwb| == |pb|
    requires forall i :: 0 <= i < k ==> pa[i] == pb[i] && pwa[i] == pwb[i]
    requires pa != pwa && pb != pwb
    requires FirstDiff(pa, pwa) < k
    ensures FirstDiff(pb, pwb) == FirstDiff(pa, pwa)
  {
    var da := FirstDiff(pa, pwa);
    assert forall j :: 0 <= j < da ==> pb[j] == pwb[j];
    assert pb[da] != pwb[da];
  }

  lemma WeakAgreeAtI(a: Tumbler, b: Tumbler, w: Tumbler, k: nat, i: nat)
    requires LessThanAt(a, b, k)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires 0 <= i < k
    ensures i < |TumblerSubtract(a, w).components|
    ensures i < |TumblerSubtract(b, w).components|
    ensures TumblerSubtract(a, w).components[i] ==
            TumblerSubtract(b, w).components[i]
  {
    var la := Max(|a.components|, |w.components|);
    var lb := Max(|b.components|, |w.components|);
    var pa := Pad(a.components, la);
    var pwa := Pad(w.components, la);
    var pb := Pad(b.components, lb);
    var pwb := Pad(w.components, lb);

    PadAgreesBeforeK(a.components, b.components, w.components, k);
    SubtractResultAt(a, w, i);
    SubtractResultAt(b, w, i);

    assert pa[i] == pb[i];
    assert pwa[i] == pwb[i];

    if pa == pwa {
      if pb == pwb {
      } else {
        var db := FirstDiff(pb, pwb);
        if db < k {
          assert pa[db] == pb[db] && pwa[db] == pwb[db];
          assert pa[db] != pwa[db];
          assert false;
        }
      }
    } else {
      var da := FirstDiff(pa, pwa);
      if pb == pwb {
        if da < k {
          assert pa[da] == pb[da] && pwa[da] == pwb[da];
          assert pb[da] != pwb[da];
          assert false;
        }
      } else {
        var db := FirstDiff(pb, pwb);
        if da < k {
          DivergenceSameBeforeK(pa, pwa, pb, pwb, k);
          assert db == da;
        } else {
          if db < k {
            assert pa[db] == pb[db] && pwa[db] == pwb[db];
            assert pa[db] != pwa[db];
            assert da <= db;
            assert false;
          }
        }
      }
    }
  }

  lemma WeakOrderAtK(a: Tumbler, b: Tumbler, w: Tumbler, k: nat)
    requires LessThanAt(a, b, k)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires k < |a.components| && k < |b.components|
    ensures k < |TumblerSubtract(a, w).components|
    ensures k < |TumblerSubtract(b, w).components|
    ensures TumblerSubtract(a, w).components[k] < TumblerSubtract(b, w).components[k]
  {
    var la := Max(|a.components|, |w.components|);
    var lb := Max(|b.components|, |w.components|);
    var pa := Pad(a.components, la);
    var pwa := Pad(w.components, la);
    var pb := Pad(b.components, lb);
    var pwb := Pad(w.components, lb);

    PadAgreesBeforeK(a.components, b.components, w.components, k);
    SubtractResultAt(a, w, k);
    SubtractResultAt(b, w, k);

    assert pa[k] == a.components[k];
    assert pb[k] == b.components[k];
    assert a.components[k] < b.components[k];
    assert pwa[k] == pwb[k];

    if pa == pwa {
      assert pb != pwb;
      var db := FirstDiff(pb, pwb);
      if db < k {
        assert pa[db] == pb[db] && pwa[db] == pwb[db];
        assert pa[db] != pwa[db];
        assert false;
      }
      assert db == k;
    } else {
      var da := FirstDiff(pa, pwa);
      if da < k {
        if pb == pwb {
          assert pa[da] == pb[da] && pwa[da] == pwb[da];
          assert false;
        }
        DivergenceSameBeforeK(pa, pwa, pb, pwb, k);
      } else if da == k {
        if pb == pwb {
          assert pb[k] == pwb[k];
          assert pa[k] == pwa[k];
          assert false;
        }
        var db := FirstDiff(pb, pwb);
        if db < k {
          assert pa[db] == pb[db] && pwa[db] == pwb[db];
          assert pa[db] != pwa[db];
          assert da <= db;
          assert false;
        }
        if db > k {
          assert pb[k] == pwb[k];
          assert pa[k] < pb[k];
          assert pa[k] >= pwa[k];
          assert false;
        }
        assert db == k;
      } else {
        assert pa[k] == pwa[k];
        assert pb != pwb;
        var db := FirstDiff(pb, pwb);
        if db < k {
          assert pa[db] == pb[db] && pwa[db] == pwb[db];
          assert pa[db] != pwa[db];
          assert da <= db;
          assert false;
        }
        if db > k {
          assert pb[k] == pwb[k];
          assert false;
        }
        assert db == k;
      }
    }
  }

  lemma WeakZeroBeyondA(a: Tumbler, w: Tumbler, k: nat, m: nat)
    requires Subtractable(a, w)
    requires k == |a.components|
    requires k <= m < Max(|a.components|, |w.components|)
    ensures TumblerSubtract(a, w).components[m] == 0
  {
    var la := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, la);
    var pwa := Pad(w.components, la);

    assert pa[m] == 0;

    SubtractResultAt(a, w, m);

    if pa == pwa {
    } else {
      var da := FirstDiff(pa, pwa);
      if m < da {
      } else if m == da {
        assert pa[da] == 0;
        assert false;
      } else {
      }
    }
  }

  lemma WeakPrefixCase(a: Tumbler, b: Tumbler, w: Tumbler, k: nat)
    requires LessThanAt(a, b, k)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires k == |a.components| && k < |b.components|
    requires TumblerSubtract(a, w) != TumblerSubtract(b, w)
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var la := Max(|a.components|, |w.components|);
    var lb := Max(|b.components|, |w.components|);
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);

    assert la <= lb by {
      assert |b.components| > k == |a.components|;
    }

    if la <= k {
      forall i | 0 <= i < k
        ensures ra.components[i] == rb.components[i]
      { WeakAgreeAtI(a, b, w, k, i); }
      LessThanIntro(ra, rb, k);
    } else {
      var rac := ra.components + Zeros(lb - la);
      assert |rac| == lb;
      assert |rb.components| == lb;

      forall i | 0 <= i < k
        ensures rac[i] == rb.components[i]
      {
        WeakAgreeAtI(a, b, w, k, i);
        assert rac[i] == ra.components[i];
      }

      forall i | k <= i < lb
        ensures rac[i] == 0
      {
        if i < la {
          WeakZeroBeyondA(a, w, k, i);
          assert rac[i] == ra.components[i];
        }
      }

      if rac == rb.components {
        if la < lb {
          forall i | 0 <= i < la
            ensures ra.components[i] == rb.components[i]
          {
            assert ra.components[i] == rac[i] == rb.components[i];
          }
          LessThanIntro(ra, rb, la);
        } else {
          assert ra.components == rb.components;
          assert false;
        }
      } else {
        var m := FirstDiff(rac, rb.components);
        assert m >= k by {
          if m < k {
            assert false;
          }
        }
        assert rac[m] == 0;
        assert rb.components[m] > 0;

        if m < la {
          forall i | 0 <= i < m
            ensures ra.components[i] == rb.components[i]
          {
            if i < la {
              assert ra.components[i] == rac[i] == rb.components[i];
            }
          }
          assert ra.components[m] == rac[m];
          assert ra.components[m] == 0;
          LessThanIntro(ra, rb, m);
        } else {
          assert la <= m;
          assert la < lb by {
            assert m < lb;
          }
          forall i | 0 <= i < la
            ensures ra.components[i] == rb.components[i]
          {
            assert ra.components[i] == rac[i] == rb.components[i];
          }
          LessThanIntro(ra, rb, la);
        }
      }
    }
  }

  lemma SubtractionWeakOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    ensures LessEq(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var k: nat :| LessThanAt(a, b, k);
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);

    if ra == rb { return; }

    if k < |a.components| && k < |b.components| {
      forall i | 0 <= i < k
        ensures ra.components[i] == rb.components[i]
      { WeakAgreeAtI(a, b, w, k, i); }
      WeakOrderAtK(a, b, w, k);
      LessThanIntro(ra, rb, k);
    } else {
      WeakPrefixCase(a, b, w, k);
    }
  }

  // ---------------------------------------------------------------------------
  // TA4 — PartialInverse ((a ⊕ w) ⊖ w = a)
  // ---------------------------------------------------------------------------

  lemma PartialInverse(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) + 1 == |a.components|
    requires |w.components| == |a.components|
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    ensures Subtractable(TumblerAdd(a, w), w)
    ensures TumblerSubtract(TumblerAdd(a, w), w) == a
  { }

  // ---------------------------------------------------------------------------
  // ReverseInverse ((a ⊖ w) ⊕ w = a)
  // ---------------------------------------------------------------------------

  lemma ReverseInverse(a: Tumbler, w: Tumbler)
    requires PositiveTumbler(w)
    requires ActionPoint(w) + 1 == |a.components|
    requires |w.components| == |a.components|
    requires forall i :: 0 <= i < ActionPoint(w) ==> a.components[i] == 0
    requires Subtractable(a, w)
    ensures TumblerAdd(TumblerSubtract(a, w), w) == a
  { }
}

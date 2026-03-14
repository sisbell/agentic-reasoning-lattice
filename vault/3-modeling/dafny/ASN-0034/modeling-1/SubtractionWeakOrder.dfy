include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubtractionWeakOrder {
  import opened TumblerAlgebra

  // TA3 — SubtractionWeakOrder
  // (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)

  ghost predicate LessEqual(a: Tumbler, b: Tumbler) {
    a == b || LessThan(a, b)
  }

  // ---------------------------------------------------------------------------
  // Helper: characterize each component of TumblerSubtract
  // ---------------------------------------------------------------------------

  lemma SubComponent(x: Tumbler, w: Tumbler, i: nat)
    requires Subtractable(x, w)
    requires i < Max(|x.components|, |w.components|)
    ensures var len := Max(|x.components|, |w.components|);
            var px := Pad(x.components, len);
            var pw := Pad(w.components, len);
            TumblerSubtract(x, w).components[i] ==
              (if px == pw then 0
               else if i < FirstDiff(px, pw) then 0
               else if i == FirstDiff(px, pw) then px[i] - pw[i]
               else px[i])
  {
    var len := Max(|x.components|, |w.components|);
    var px := Pad(x.components, len);
    var pw := Pad(w.components, len);
    if px == pw {
    } else {
      var d := FirstDiff(px, pw);
      var result := Zeros(d) + [px[d] - pw[d]] + px[d+1..];
      assert TumblerSubtract(x, w) == Tumbler(result);
      if i < d {
      } else if i == d {
      } else {
        assert result[i] == px[i];
      }
    }
  }

  // ---------------------------------------------------------------------------
  // Helper: padded sequences agree before k
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

  // ---------------------------------------------------------------------------
  // Helper: divergence with w before k is at the same position for both
  // ---------------------------------------------------------------------------

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

  // ---------------------------------------------------------------------------
  // Results agree at position i < k
  // ---------------------------------------------------------------------------

  lemma SubResultsAgreeAtI(a: Tumbler, b: Tumbler, w: Tumbler, k: nat, i: nat)
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
    SubComponent(a, w, i);
    SubComponent(b, w, i);

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

  // ---------------------------------------------------------------------------
  // Component case: ra[k] < rb[k]
  // ---------------------------------------------------------------------------

  lemma SubResultOrderAtK(a: Tumbler, b: Tumbler, w: Tumbler, k: nat)
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
    SubComponent(a, w, k);
    SubComponent(b, w, k);

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
          assert pa[k] == pwa[k]; // wrong — da == k means pa[k] != pwa[k]
          assert false;
        }
        var db := FirstDiff(pb, pwb);
        if db < k {
          assert pa[db] == pb[db] && pwa[db] == pwb[db];
          assert pa[db] != pwa[db];
          assert da <= db;
          assert false;
        }
        assert db == k;
      } else {
        // da > k: pa[k] == pwa[k]
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

  // ---------------------------------------------------------------------------
  // All ra[m] = 0 for m >= k = |a| (prefix case)
  // ---------------------------------------------------------------------------

  lemma SubResultZeroBeyondA(a: Tumbler, w: Tumbler, k: nat, m: nat)
    requires Subtractable(a, w)
    requires k == |a.components|
    requires k <= m < Max(|a.components|, |w.components|)
    ensures TumblerSubtract(a, w).components[m] == 0
  {
    var la := Max(|a.components|, |w.components|);
    var pa := Pad(a.components, la);
    var pwa := Pad(w.components, la);

    assert pa[m] == 0;

    SubComponent(a, w, m);

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

  // ---------------------------------------------------------------------------
  // Prefix case
  // ---------------------------------------------------------------------------

  lemma SubPrefixCase(a: Tumbler, b: Tumbler, w: Tumbler, k: nat)
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
      // la = k (since la >= |a| = k). ra has length k, rb has length lb > k.
      forall i | 0 <= i < k
        ensures ra.components[i] == rb.components[i]
      { SubResultsAgreeAtI(a, b, w, k, i); }
      LessThanIntro(ra, rb, k);
    } else {
      // la > k. Pad ra.components to lb with zeros and compare.
      var rac := ra.components + Zeros(lb - la);
      assert |rac| == lb;
      assert |rb.components| == lb;

      // rac[i] = ra[i] for i < la, rac[i] = 0 for i >= la
      // rac[i] = 0 for i >= k (since ra[i] = 0 for k <= i < la)

      // Prove rac agrees with rb before k
      forall i | 0 <= i < k
        ensures rac[i] == rb.components[i]
      {
        SubResultsAgreeAtI(a, b, w, k, i);
        assert rac[i] == ra.components[i];
      }

      // Prove rac[i] = 0 for i >= k
      forall i | k <= i < lb
        ensures rac[i] == 0
      {
        if i < la {
          SubResultZeroBeyondA(a, w, k, i);
          assert rac[i] == ra.components[i];
        }
      }

      if rac == rb.components {
        // They agree on all lb positions. Since la <= lb:
        if la < lb {
          forall i | 0 <= i < la
            ensures ra.components[i] == rb.components[i]
          {
            assert ra.components[i] == rac[i] == rb.components[i];
          }
          LessThanIntro(ra, rb, la);
        } else {
          // la == lb: ra.components == rac == rb.components, so ra == rb. Contradiction.
          assert ra.components == rb.components;
          assert false;
        }
      } else {
        // Find first difference between rac and rb.components
        var m := FirstDiff(rac, rb.components);
        // m >= k (agree before k) and rac[m] = 0 (m >= k), rb[m] > 0
        assert m >= k by {
          if m < k {
            // rac[m] == rb.components[m] from agreement before k
            assert false;
          }
        }
        assert rac[m] == 0;
        assert rb.components[m] > 0;

        if m < la {
          // m is within ra's length
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
          // m >= la: rac and rb agree on [0, la), so ra is a prefix of rb
          assert la <= m;
          assert la < lb by {
            assert m < lb; // FirstDiff returns m < |rac| = lb
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

  // ---------------------------------------------------------------------------
  // Main lemma
  // ---------------------------------------------------------------------------

  lemma SubtractionWeakOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    ensures LessEqual(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var k: nat :| LessThanAt(a, b, k);
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);

    if ra == rb { return; }

    if k < |a.components| && k < |b.components| {
      // Component case
      forall i | 0 <= i < k
        ensures ra.components[i] == rb.components[i]
      { SubResultsAgreeAtI(a, b, w, k, i); }
      SubResultOrderAtK(a, b, w, k);
      LessThanIntro(ra, rb, k);
    } else {
      // Prefix case
      SubPrefixCase(a, b, w, k);
    }
  }
}

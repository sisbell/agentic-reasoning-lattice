include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubtractionStrictOrder {
  import opened TumblerAlgebra

  // TA3-strict — SubtractionStrictOrder
  // (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)

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
  // Results agree at position i < k (equal-length case)
  // ---------------------------------------------------------------------------

  lemma SubResultsAgreeAtI(a: Tumbler, b: Tumbler, w: Tumbler, k: nat, i: nat)
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

    SubComponent(a, w, i);
    SubComponent(b, w, i);

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
          // Both diverge before k — must be at the same point
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

  // ---------------------------------------------------------------------------
  // Component case: ra[k] < rb[k]
  // ---------------------------------------------------------------------------

  lemma SubResultOrderAtK(a: Tumbler, b: Tumbler, w: Tumbler, k: nat)
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

    SubComponent(a, w, k);
    SubComponent(b, w, k);

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
        // pb[k] == pw[k] but pa[k] < pb[k], so pa[k] < pw[k]
        // Subtractable(a,w) at position da: pa[da] >= pw[da]
        // Since pa[i] == pb[i] == pw[i] for i < k, and da is first diff of pa,pw:
        // da >= k. But pa[k] < pw[k] means da <= k, so da == k. But pa[k] < pw[k]
        // contradicts pa[k] >= pw[k] from Subtractable.
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
            assert pa[k] >= pw[k]; // Subtractable at da == k
            assert false;
          }
          assert db == k;
        } else {
          // da > k: pa[k] == pw[k]
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

  // ---------------------------------------------------------------------------
  // Main lemma
  // ---------------------------------------------------------------------------

  lemma SubtractionStrictOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    requires |a.components| == |b.components|
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w))
  {
    var k: nat :| LessThanAt(a, b, k);
    // With |a| == |b|, the prefix case of LessThan cannot apply — k < |a|.
    assert k < |a.components| && k < |b.components|;

    forall i | 0 <= i < k
      ensures TumblerSubtract(a, w).components[i] ==
              TumblerSubtract(b, w).components[i]
    { SubResultsAgreeAtI(a, b, w, k, i); }

    SubResultOrderAtK(a, b, w, k);
    LessThanIntro(TumblerSubtract(a, w), TumblerSubtract(b, w), k);
  }
}

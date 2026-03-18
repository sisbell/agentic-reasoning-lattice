include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubtractionPreservesOrder {

  import opened TumblerAlgebra

  // Bridge: provide a LessThan witness at a numeric divergence
  lemma LessThanFromWitness(a: Tumbler, b: Tumbler, j: nat)
    requires j < |a.components| && j < |b.components|
    requires a.components[j] < b.components[j]
    requires forall i :: 0 <= i < j ==> a.components[i] == b.components[i]
    ensures LessThan(a, b)
  {
    assert j <= |a.components| && j <= |b.components|;
    assert j < |a.components| && j < |b.components| && a.components[j] < b.components[j];
  }

  // Bridge: LessThan from proper prefix
  lemma LessThanFromPrefix(a: Tumbler, b: Tumbler, n: nat)
    requires n == |a.components|
    requires n < |b.components|
    requires forall i :: 0 <= i < n ==> a.components[i] == b.components[i]
    ensures LessThan(a, b)
  {
    var bn := b.components[n];
    assert n <= |a.components| && n <= |b.components|;
    assert n == |a.components| && n < |b.components|;
  }

  // Helper: Zeros(n) < any non-trivial subtraction result of length n
  lemma ZerosLessThanSubtract(b: Tumbler, w: Tumbler)
    requires Subtractable(b, w)
    requires Pad(b.components, Max(|b.components|, |w.components|)) !=
             Pad(w.components, Max(|b.components|, |w.components|))
    ensures LessThan(Tumbler(Zeros(Max(|b.components|, |w.components|))),
                     TumblerSubtract(b, w))
  {
    var len := Max(|b.components|, |w.components|);
    var pb := Pad(b.components, len);
    var pw := Pad(w.components, len);
    var kb := FirstDiff(pb, pw);
    var rb := TumblerSubtract(b, w);

    // At kb: pb[kb] > pw[kb] (from Subtractable + FirstDiff)
    assert pb[kb] >= pw[kb];
    assert pb[kb] != pw[kb];

    // rb.components[kb] = pb[kb] - pw[kb] > 0
    // Zeros(len)[kb] = 0
    LessThanFromWitness(Tumbler(Zeros(len)), rb, kb);
  }

  // Helper: padded w values agree at positions within both padding lengths
  lemma PadAgreesOnW(w: Tumbler, len_a: nat, len_b: nat, i: nat)
    requires len_a >= |w.components| && len_b >= |w.components|
    requires i < len_a && i < len_b
    ensures Pad(w.components, len_a)[i] == Pad(w.components, len_b)[i]
  {}

  // Case: pa == pw_a (a equals w after padding), pb != pw_b
  lemma SubPreservesOrder_AEqW(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
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

    // ra = Tumbler(Zeros(len_a)), rb has positive at kb
    assert ra == Tumbler(Zeros(len_a));
    assert pb[kb] >= pw_b[kb];
    assert pb[kb] != pw_b[kb];
    assert rb.components[kb] == pb[kb] - pw_b[kb];
    assert rb.components[kb] > 0;

    if kb < len_a {
      // ra[kb] = 0 < rb[kb]
      assert ra.components[kb] == 0;
      LessThanFromWitness(ra, rb, kb);
    } else {
      // ra is shorter, all its components are 0, rb starts with kb zeros
      // so ra is a prefix of rb's initial zeros
      assert len_a <= kb;
      assert len_a < len_b;
      assert forall i :: 0 <= i < len_a ==> ra.components[i] == 0 && rb.components[i] == 0;
      LessThanFromPrefix(ra, rb, len_a);
    }
  }

  // Case: both pa != pw_a and pb != pw_b (general case)
  lemma SubPreservesOrder_General(a: Tumbler, b: Tumbler, w: Tumbler)
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
      // ra[kb] = 0 (since kb < ka), rb[kb] > 0
      assert ra.components[kb] == 0;
      assert rb.components[kb] > 0;
      LessThanFromWitness(ra, rb, kb);
    } else if ka == kb {
      // At position ka: ra[ka] = pa[ka] - pw[ka], rb[ka] = pb[ka] - pw[ka]
      // From LessThan(a, b) with agreement up to ka, pa[ka] <= pb[ka]
      // So ra[ka] <= rb[ka]
      if pa[ka] < pb[ka] {
        assert ra.components[ka] < rb.components[ka];
        LessThanFromWitness(ra, rb, ka);
      } else {
        // pa[ka] == pb[ka], so ra[ka] == rb[ka]
        // Need to find divergence beyond ka in the suffixes
        assert pa[ka] == pb[ka];
        assert ra.components[ka] == rb.components[ka];
        // For i > ka: ra[i] = pa[i], rb[i] = pb[i]
        // From LessThan(a,b), first diff between a and b is beyond ka
        // Extract the LessThan witness
        ghost var j: nat :|
          j <= |a.components| && j <= |b.components| &&
          (forall i :: 0 <= i < j ==> a.components[i] == b.components[i]) &&
          ((j < |a.components| && j < |b.components| && a.components[j] < b.components[j]) ||
           (j == |a.components| && j < |b.components|));
        // j must be > ka (a and b agree up to ka since both agree with w there)
        assert j > ka;
        if j < |a.components| && j < |b.components| {
          // a[j] < b[j], and for ka < i < j: ra[i] = pa[i] = a[i] = b[i] = pb[i] = rb[i]
          assert ra.components[j] == pa[j];
          assert rb.components[j] == pb[j];
          assert j < len_a && j < len_b;
          assert pa[j] == a.components[j];
          assert pb[j] == b.components[j];
          LessThanFromWitness(ra, rb, j);
        } else {
          // j == |a| < |b| (prefix case)
          // ra has len_a components, rb has len_b
          // For ka < i < j=|a|: ra[i] = pa[i] = a[i] = b[i] = pb[i] = rb[i]
          // At j=|a|: if j < len_a, ra[j] = pa[j] = 0, rb[j] = pb[j] = b[j]
          // Need either ra[j] < rb[j] or ra is shorter
          if j < len_a {
            assert ra.components[j] == pa[j];
            assert pa[j] == 0;
            assert rb.components[j] == pb[j];
            if pb[j] > 0 {
              LessThanFromWitness(ra, rb, j);
            } else {
              // Both 0 at j, need to look further
              // ra is all zeros from j onwards (padding), rb has b's values
              // Since ra != rb, they differ somewhere after j
              assert len_a <= len_b;
              if len_a == len_b {
                assert ra.components != rb.components;
                var d := FirstDiff(ra.components, rb.components);
                assert ra.components[d] == pa[d];
                assert pa[d] == 0;
                LessThanFromWitness(ra, rb, d);
              } else {
                assert len_a < len_b;
                if ra.components == rb.components[..len_a] {
                  LessThanFromPrefix(ra, rb, len_a);
                } else {
                  var d := FirstDiff(ra.components, rb.components[..len_a]);
                  assert rb.components[..len_a][d] == rb.components[d];
                  assert ra.components[d] == pa[d];
                  assert pa[d] == 0;
                  LessThanFromWitness(ra, rb, d);
                }
              }
            }
          } else {
            // j = |a| >= len_a, so ra has fewer components
            // ra has len_a components, and all agree with rb up to len_a
            assert len_a <= j;
            assert len_a < len_b;
            LessThanFromPrefix(ra, rb, len_a);
          }
        }
      }
    } else {
      // ka < kb: impossible (a diverges from w earlier than b,
      // but Subtractable makes a >= w there while b == w, contradicting a < b)
      assert false;
    }
  }

  // DIVERGENCE: ASN states strict (<) unconditionally, but the foundation's
  // TumblerSubtract can map distinct tumblers to the same result when both
  // operands equal w after zero-padding (e.g., a=[1,0], b=[1,0,0],
  // w=[1,0,0,0] gives a⊖w = b⊖w = [0,0,0,0]). Proved weak (≤) version.
  lemma SubtractionPreservesOrder(a: Tumbler, b: Tumbler, w: Tumbler)
    requires LessThan(a, b)
    requires Subtractable(a, w)
    requires Subtractable(b, w)
    ensures LessThan(TumblerSubtract(a, w), TumblerSubtract(b, w)) ||
            TumblerSubtract(a, w) == TumblerSubtract(b, w)
  {
    var ra := TumblerSubtract(a, w);
    var rb := TumblerSubtract(b, w);
    if ra == rb {
    } else {
      var len_a := Max(|a.components|, |w.components|);
      var len_b := Max(|b.components|, |w.components|);
      var pa := Pad(a.components, len_a);
      var pw_a := Pad(w.components, len_a);
      var pb := Pad(b.components, len_b);
      var pw_b := Pad(w.components, len_b);

      if pa == pw_a {
        if pb == pw_b {
          // Both zero — ra = Zeros(len_a), rb = Zeros(len_b), ra != rb
          // So len_a != len_b; need len_a < len_b
          assert ra == Tumbler(Zeros(len_a));
          assert rb == Tumbler(Zeros(len_b));
          assert len_a != len_b;
          assert len_a < len_b;
          LessThanFromPrefix(ra, rb, len_a);
        } else {
          SubPreservesOrder_AEqW(a, b, w);
        }
      } else if pb == pw_b {
        // Impossible: a diverges from w (has positive subtraction result)
        // but b equals w after padding — contradicts a < b
        var ka := FirstDiff(pa, pw_a);
        assert pa[ka] >= pw_a[ka];
        assert pa[ka] != pw_a[ka];
        assert false;
      } else {
        SubPreservesOrder_General(a, b, w);
      }
    }
  }

}

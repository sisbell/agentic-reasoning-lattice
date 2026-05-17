// ASN-0034: TA-assoc — AdditionAssociative
// Addition is associative where both compositions are defined:
// (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) whenever both sides are well-defined.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatAdditionAssociative.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatArithmeticClosureAndIdentity.dfy"

module AdditionAssociative {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened WellDefinedAddition
  import opened CanonicalRepresentation
  import opened NatAdditionAssociative
  import opened NatStrictTotalOrder
  import opened NatArithmeticClosureAndIdentity
  import opened NatCarrierSet

  // Uniqueness: if k is a least-positive-witness index for w, then ActionPoint(w) = k.
  // Follows from ActionPoint's least-witness contract by trichotomy on (ActionPoint(w), k).
  lemma ActionPointUniqueness(w: Tumbler, k: nat)
    requires InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires 1 <= k <= Length(w)
    requires Component(w, k) != 0
    requires forall j :: 1 <= j < k ==> Component(w, j) == 0
    ensures ActionPoint.ActionPoint(w) == k
  {
    var ap := ActionPoint.ActionPoint(w);
    if ap < k {
      assert Component(w, ap) != 0;
      assert 1 <= ap < k;
      assert Component(w, ap) == 0;
    } else if ap > k {
      assert 1 <= k < ap;
      assert Component(w, k) == 0;
    }
  }

  // Helper: action point and positivity of b ⊕ c.
  // s = b ⊕ c has Pos(s), and actionPoint(s) = min(k_b, k_c).
  lemma ActionPointOfSum(b: Tumbler, c: Tumbler)
    requires InT(b) && InT(c)
    requires PositiveTumbler.PositiveTumbler(b)
    requires PositiveTumbler.PositiveTumbler(c)
    requires ActionPoint.ActionPoint(c) <= Length(b)
    ensures
      var s := TumblerAdd.TumblerAdd(b, c);
      var kb := ActionPoint.ActionPoint(b);
      var kc := ActionPoint.ActionPoint(c);
      PositiveTumbler.PositiveTumbler(s) &&
      (kb <= kc ==> ActionPoint.ActionPoint(s) == kb) &&
      (kc <= kb ==> ActionPoint.ActionPoint(s) == kc)
  {
    var s := TumblerAdd.TumblerAdd(b, c);
    var kb := ActionPoint.ActionPoint(b);
    var kc := ActionPoint.ActionPoint(c);

    assert Length(s) == Length(c);

    if kb < kc {
      // Witness kb: s_{kb} = b_{kb} (prefix-copy since kb < kc), and b_{kb} != 0.
      assert kb < kc;
      assert Component(s, kb) == Component(b, kb);
      assert Component(b, kb) != 0;
      assert Component(s, kb) != 0;
      // Zeros below kb: for 1 <= i < kb, s_i = b_i = 0 (zeros-below in b).
      forall i | 1 <= i < kb
        ensures Component(s, i) == 0
      {
        assert i < kc;
        assert Component(s, i) == Component(b, i);
      }
      assert PositiveTumbler.PositiveTumbler(s) by {
        assert 1 <= kb <= Length(s) && Component(s, kb) != 0;
      }
      assert kb <= Length(s);
      ActionPointUniqueness(s, kb);
    } else if kb == kc {
      var k := kb;
      assert Component(s, k) == Component(b, k) + Component(c, k);
      assert Component(b, k) != 0;
      // Carrier = nat: b_k != 0 means b_k >= 1, so s_k = b_k + c_k >= 1 > 0.
      assert Component(s, k) != 0;
      forall i | 1 <= i < k
        ensures Component(s, i) == 0
      {
        assert i < kc;
        assert Component(s, i) == Component(b, i);
      }
      assert PositiveTumbler.PositiveTumbler(s) by {
        assert 1 <= k <= Length(s) && Component(s, k) != 0;
      }
      ActionPointUniqueness(s, k);
    } else {
      // kb > kc
      // s_{kc} = b_{kc} + c_{kc}. b_{kc} = 0 (since kc < kb, zeros-below in b).
      // So s_{kc} = c_{kc} != 0.
      assert kc < kb;
      assert Component(s, kc) == Component(b, kc) + Component(c, kc);
      assert Component(b, kc) == 0;
      LeftAdditiveIdentity(Component(c, kc));
      assert Component(s, kc) == Component(c, kc);
      assert Component(c, kc) != 0;
      assert Component(s, kc) != 0;
      // Zeros below kc: for 1 <= i < kc, s_i = b_i = 0 (since i < kc < kb).
      forall i | 1 <= i < kc
        ensures Component(s, i) == 0
      {
        assert Component(s, i) == Component(b, i);
        assert i < kb;
      }
      assert PositiveTumbler.PositiveTumbler(s) by {
        assert 1 <= kc <= Length(s) && Component(s, kc) != 0;
      }
      ActionPointUniqueness(s, kc);
    }
  }

  // Main lemma: tumbler addition is associative.
  lemma AdditionAssociative(a: Tumbler, b: Tumbler, c: Tumbler)
    requires InT(a) && InT(b) && InT(c)
    requires PositiveTumbler.PositiveTumbler(b)
    requires PositiveTumbler.PositiveTumbler(c)
    requires ActionPoint.ActionPoint(b) <= Length(a)
    requires ActionPoint.ActionPoint(c) <= Length(b)
    ensures
      var s := TumblerAdd.TumblerAdd(b, c);
      PositiveTumbler.PositiveTumbler(s) &&
      ActionPoint.ActionPoint(s) <= Length(a) &&
      TumblerAdd.TumblerAdd(TumblerAdd.TumblerAdd(a, b), c) ==
        TumblerAdd.TumblerAdd(a, s) &&
      (ActionPoint.ActionPoint(b) <= ActionPoint.ActionPoint(c) ==>
        ActionPoint.ActionPoint(s) == ActionPoint.ActionPoint(b)) &&
      (ActionPoint.ActionPoint(c) <= ActionPoint.ActionPoint(b) ==>
        ActionPoint.ActionPoint(s) == ActionPoint.ActionPoint(c))
  {
    ActionPointOfSum(b, c);

    var s := TumblerAdd.TumblerAdd(b, c);
    var kb := ActionPoint.ActionPoint(b);
    var kc := ActionPoint.ActionPoint(c);

    // ActionPoint(s) <= Length(a)
    if kb <= kc {
      assert ActionPoint.ActionPoint(s) == kb;
      assert kb <= Length(a);
    } else {
      assert ActionPoint.ActionPoint(s) == kc;
      assert kc < kb <= Length(a);
    }
    assert ActionPoint.ActionPoint(s) <= Length(a);

    // r = a ⊕ b; well-defined since Pos(b) and kb ≤ |a|.
    var r := TumblerAdd.TumblerAdd(a, b);
    assert Length(r) == Length(b);
    // kc ≤ |b| = |r|, so (a ⊕ b) ⊕ c is well-defined.
    assert ActionPoint.ActionPoint(c) <= Length(r);

    var L := TumblerAdd.TumblerAdd(r, c);
    var R := TumblerAdd.TumblerAdd(a, s);

    assert Length(L) == Length(c);
    assert Length(s) == Length(c);
    assert Length(R) == Length(s) == Length(c);

    var ks := ActionPoint.ActionPoint(s);

    forall i | 1 <= i <= Length(c)
      ensures Component(L, i) == Component(R, i)
    {
      if kb < kc {
        // ks = kb
        assert ks == kb;
        if i < kb {
          // L_i = r_i = a_i; R_i = a_i
          assert i < kc;
          assert Component(L, i) == Component(r, i);
          assert Component(r, i) == Component(a, i);
          assert Component(R, i) == Component(a, i);
        } else if i == kb {
          // L_i = r_i = a_i + b_i (since kb < kc, prefix-copy from r)
          // R_i = a_i + s_i = a_i + b_i (since kb < kc, s_{kb} = b_{kb})
          assert i < kc;
          assert Component(L, i) == Component(r, i);
          assert Component(r, kb) == Component(a, kb) + Component(b, kb);
          assert Component(R, kb) == Component(a, kb) + Component(s, kb);
          assert Component(s, kb) == Component(b, kb);
        } else if i < kc {
          // L_i = r_i = b_i (i > kb); R_i = s_i = b_i (i < kc)
          assert kb < i < kc;
          assert Component(L, i) == Component(r, i);
          assert Component(r, i) == Component(b, i);
          assert Component(R, i) == Component(s, i);
          assert Component(s, i) == Component(b, i);
        } else if i == kc {
          // L_i = r_i + c_i = b_i + c_i (kc > kb)
          // R_i = s_i = b_i + c_i (s_{kc} from advance)
          assert Component(L, kc) == Component(r, kc) + Component(c, kc);
          assert Component(r, kc) == Component(b, kc);
          assert Component(R, kc) == Component(s, kc);
          assert Component(s, kc) == Component(b, kc) + Component(c, kc);
        } else {
          // i > kc: L_i = c_i; R_i = s_i = c_i
          assert i > kc;
          assert Component(L, i) == Component(c, i);
          assert Component(R, i) == Component(s, i);
          assert Component(s, i) == Component(c, i);
        }
      } else if kb == kc {
        var k := kb;
        assert ks == k;
        if i < k {
          assert Component(L, i) == Component(r, i) == Component(a, i);
          assert Component(R, i) == Component(a, i);
        } else if i == k {
          // L_k = r_k + c_k = (a_k + b_k) + c_k
          // R_k = a_k + s_k = a_k + (b_k + c_k)
          assert Component(L, k) == Component(r, k) + Component(c, k);
          assert Component(r, k) == Component(a, k) + Component(b, k);
          assert Component(R, k) == Component(a, k) + Component(s, k);
          assert Component(s, k) == Component(b, k) + Component(c, k);
          NatAdditionAssociative.NatAdditionAssociative(
            Component(a, k), Component(b, k), Component(c, k));
        } else {
          assert i > k;
          assert Component(L, i) == Component(c, i);
          assert Component(R, i) == Component(s, i);
          assert Component(s, i) == Component(c, i);
        }
      } else {
        // kb > kc, ks = kc
        assert ks == kc;
        if i < kc {
          // L_i = r_i = a_i (since i < kc < kb); R_i = a_i
          assert i < kb;
          assert Component(L, i) == Component(r, i);
          assert Component(r, i) == Component(a, i);
          assert Component(R, i) == Component(a, i);
        } else if i == kc {
          // L_{kc} = r_{kc} + c_{kc} = a_{kc} + c_{kc} (since kc < kb, r_{kc} = a_{kc})
          // R_{kc} = a_{kc} + s_{kc}; s_{kc} = b_{kc} + c_{kc} = 0 + c_{kc} = c_{kc}
          assert kc < kb;
          assert Component(L, kc) == Component(r, kc) + Component(c, kc);
          assert Component(r, kc) == Component(a, kc);
          assert Component(R, kc) == Component(a, kc) + Component(s, kc);
          assert Component(s, kc) == Component(b, kc) + Component(c, kc);
          assert Component(b, kc) == 0;
          LeftAdditiveIdentity(Component(c, kc));
          assert Component(s, kc) == Component(c, kc);
        } else {
          assert i > kc;
          assert Component(L, i) == Component(c, i);
          assert Component(R, i) == Component(s, i);
          assert Component(s, i) == Component(c, i);
        }
      }
    }

    CanonicalRepresentation.CanonicalRepresentation(L, R);
  }
}

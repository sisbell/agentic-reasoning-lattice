// ASN-0034: TA7a.2 — SubspaceDivergenceResidue
// When the action point is at position 1 and the leading components coincide
// with a strict disagreement later, the subspace-closure guarantee of TA7a
// fails and the residue acquires a leading zero, placing it in T \ S.
include "./SubspaceClosure.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./TumblerSub.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./CanonicalRepresentation.dfy"

module SubspaceDivergenceResidue {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened TumblerSub
  import opened ZeroPaddedDivergence
  import opened CanonicalRepresentation
  import opened SubspaceClosure

  lemma SubspaceDivergenceResidue(o: Tumbler, w: Tumbler)
    requires InT(o) && InT(w)
    requires InSubspaceS(o)
    requires PositiveTumbler.PositiveTumbler(w)
    requires LexicographicOrder.LexicographicOrder(w, o) || w == o
    requires Length(w) <= Length(o)
    requires ActionPoint.ActionPoint(w) == 1
    requires Component(o, 1) == Component(w, 1)
    requires o != w
    ensures InT(TumblerSub.TumblerSub(o, w))
    ensures !InSubspaceS(TumblerSub.TumblerSub(o, w))
  {
    var r := TumblerSub.TumblerSub(o, w);
    var L := if Length(o) >= Length(w) then Length(o) else Length(w);
    var k := ZeroPaddedDivergence.ZeroPaddedDivergence(o, w);

    // Step 1: zpd(o, w) is defined (k != 0).
    if k == 0 {
      assert FirstPaddedMismatch(o, w, 1, L) == L + 1;
      assert forall i :: 1 <= i <= L ==>
        PaddedComponent(o, i) == PaddedComponent(w, i);
      if Length(o) == Length(w) {
        // Sub-case (α): lengths agree → padded = native → T3 → o = w (contradiction).
        forall i | 1 <= i <= Length(o)
          ensures Component(o, i) == Component(w, i)
        {
          assert PaddedComponent(o, i) == Component(o, i);
          assert PaddedComponent(w, i) == Component(w, i);
        }
        CanonicalRepresentation.CanonicalRepresentation(o, w);
        assert o == w;
      } else {
        // Sub-case (γ): Length(w) < Length(o). Mismatch at i = Length(o).
        assert Length(w) < Length(o);
        var i := Length(o);
        assert PaddedComponent(o, i) == Component(o, i);
        assert PaddedComponent(w, i) == 0;
        assert Component(o, i) > 0;
        assert PaddedComponent(o, i) != PaddedComponent(w, i);
      }
    }
    assert k != 0;

    // Step 2: zpd(o, w) > 1.
    // PaddedComponent(o, 1) = PaddedComponent(w, 1), so FPM cannot return 1.
    assert PaddedComponent(o, 1) == Component(o, 1);
    assert PaddedComponent(w, 1) == Component(w, 1);
    if k == 1 {
      assert FirstPaddedMismatch(o, w, 1, L) == 1;
      assert PaddedComponent(o, 1) != PaddedComponent(w, 1);
    }
    assert k >= 2;

    // Step 3: r_1 = 0 via SubComponent.
    TumblerSubComponents(o, w);
    assert Component(r, 1) == SubComponent(o, w, k, 1);
    assert Component(r, 1) == 0;

    // Step 4: !InSubspaceS(r) — Component(r, 1) = 0 violates positivity at index 1.
    assert Length(r) == L;
  }
}

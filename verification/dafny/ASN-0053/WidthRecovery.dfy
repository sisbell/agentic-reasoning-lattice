// ASN-0053: WR — WidthRecovery (DEF/theorem)
// For a level-uniform span σ = (s, ℓ): reach(σ) ⊖ start(σ) = width(σ).
include "./SpanDefs.dfy"
include "../ASN-0034/DisplacementUnique.dfy"
include "../ASN-0034/Divergence.dfy"

module WidthRecovery {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened NatCarrierSet
  import DU = DisplacementUnique
  import DRT = DisplacementRoundTrip
  import D = Divergence
  import TS = TumblerSub

  // Helper: FirstMismatch(a, b, start, m) <= k when components agree for i in [start, k)
  // and differ at k.
  lemma FirstMismatchLEK(a: Tumbler, b: Tumbler, start: nat, k: nat, m: nat)
    requires InT(a) && InT(b)
    requires 1 <= start && start <= k && k <= m
    requires m <= Length(a) && m <= Length(b)
    requires forall i :: start <= i < k ==> Component(a, i) == Component(b, i)
    requires Component(a, k) != Component(b, k)
    ensures D.FirstMismatch(a, b, start, m) <= k
    decreases k - start
  {
    if start == k {
    } else {
      assert Component(a, start) == Component(b, start);
      FirstMismatchLEK(a, b, start + 1, k, m);
    }
  }

  // Divergence(s, r) <= Length(s) when s and r agree at i < k, differ at k,
  // and have equal lengths.
  lemma DivergenceBound(s: Tumbler, r: Tumbler, k: nat)
    requires InT(s) && InT(r)
    requires s != r
    requires 1 <= k && k <= Length(s)
    requires Length(r) == Length(s)
    requires forall i :: 1 <= i < k ==> Component(s, i) == Component(r, i)
    requires Component(s, k) != Component(r, k)
    ensures D.Divergence(s, r) <= Length(s)
  {
    FirstMismatchLEK(s, r, 1, k, Length(s));
  }

  // WR: For a level-uniform valid span σ = (s, ℓ): reach(σ) ⊖ s = ℓ.
  lemma WidthRecovery(sigma: SpanEntry)
    requires ValidSpan(sigma)
    requires Length(sigma.start) == Length(sigma.width)
    ensures TS.TumblerSub(Reach(sigma), sigma.start) == sigma.width
  {
    var s := sigma.start;
    var l := sigma.width;
    var k := ActionPoint.ActionPoint(l);
    var r := TumblerAdd.TumblerAdd(s, l);
    assert r == Reach(sigma);
    // Level-uniform + TumblerAdd ensures: equal lengths
    assert Length(r) == Length(l) == Length(s);
    // TumblerAdd component structure: agree before k, differ at k
    assert forall i :: 1 <= i < k ==> Component(r, i) == Component(s, i);
    assert Component(r, k) == Component(s, k) + Component(l, k);
    assert Component(l, k) != 0;
    assert Component(r, k) != Component(s, k);
    // s != r
    DRT.LexImpliesNotEqual(s, r);
    // Divergence(s, r) <= Length(s)
    DivergenceBound(s, r, k);
    // D2: s ⊕ l = r, Pos(l), AP(l) <= #s => l = r ⊖ s
    DU.DisplacementUnique(s, r, l);
  }
}

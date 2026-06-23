// ASN-0053: S4 — SplitPartition (DEF)
// For a level-uniform span σ = (s, ℓ) and interior point p (s < p < reach(σ), #p = #s),
// defines λ = (s, p⊖s) and ρ = (p, reach(σ)⊖p); proves they partition ⟦σ⟧.
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/DisplacementRoundTrip.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"

module SplitPartition {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import opened NatStrictTotalOrder
  import SWD = SpanWellDefinedness
  import DRT = DisplacementRoundTrip
  import DivModule = Divergence
  import SpanModule = Span
  import IC = IntrinsicComparison

  datatype SpanValue = SpanValue(start: Tumbler, width: Tumbler)
  datatype SplitResult = SplitResult(left: SpanValue, right: SpanValue)

  ghost predicate ValidSpan(sigma: SpanValue) {
    InT(sigma.start) &&
    InT(sigma.width) &&
    PositiveTumbler.PositiveTumbler(sigma.width) &&
    ActionPoint.ActionPoint(sigma.width) <= Length(sigma.start)
  }

  ghost predicate LevelUniform(sigma: SpanValue) {
    Length(sigma.start) == Length(sigma.width)
  }

  ghost function Reach(sigma: SpanValue): Tumbler
    requires ValidSpan(sigma)
    ensures InT(Reach(sigma))
    ensures Length(Reach(sigma)) == Length(sigma.width)
  {
    TumblerAdd.TumblerAdd(sigma.start, sigma.width)
  }

  ghost function SpanSet(sigma: SpanValue): iset<Tumbler>
    requires ValidSpan(sigma)
  {
    SpanModule.Span(sigma.start, sigma.width)
  }

  // When a < b and #a = #b, Div(a,b) ≤ #a (needed for DisplacementRoundTrip)
  lemma EqualLengthDivergenceBound(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires Length(a) == Length(b)
    ensures DivModule.Divergence(a, b) <= Length(a)
  {
    DRT.LexImpliesNotEqual(a, b);
    var m := Length(a);
    var k: nat :| 1 <= k &&
      (forall i :: 1 <= i < k ==>
        i <= Length(a) && i <= Length(b) && Component(a, i) == Component(b, i)) &&
      ((k <= Length(a) && k <= Length(b) && Less(Component(a, k), Component(b, k))) ||
       (k == Length(a) + 1 && k <= Length(b)));
    assert k <= m;
    var fm := DivModule.FirstMismatch(a, b, 1, m);
    assert DivModule.Divergence(a, b) == fm;
    if fm > m {
      assert 1 <= k && k < fm;
      assert Component(a, k) == Component(b, k);
      assert Less(Component(a, k), Component(b, k));
      Irreflexive(Component(a, k));
    }
  }

  // WF: from s < r with equal length, (s, r⊖s) is valid level-uniform with reach r
  lemma WellFormedFromEndpoints(s: Tumbler, r: Tumbler)
    requires InT(s) && InT(r)
    requires LexicographicOrder.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    ensures ValidSpan(SpanValue(s, TumblerSub.TumblerSub(r, s)))
    ensures LevelUniform(SpanValue(s, TumblerSub.TumblerSub(r, s)))
    ensures Reach(SpanValue(s, TumblerSub.TumblerSub(r, s))) == r
  {
    EqualLengthDivergenceBound(s, r);
    DRT.DisplacementRoundTrip(s, r);
  }

  // S4 DEF: λ = (s, p⊖s) and ρ = (p, reach(σ)⊖p)
  ghost function SplitPartition(sigma: SpanValue, p: Tumbler): SplitResult
    requires ValidSpan(sigma) && LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, Reach(sigma))
  {
    SplitResult(
      SpanValue(sigma.start, TumblerSub.TumblerSub(p, sigma.start)),
      SpanValue(p, TumblerSub.TumblerSub(Reach(sigma), p))
    )
  }

  // S4 theorem: WF + adjacency (c) + union (a) + disjoint (b)
  lemma SplitPartitionTheorem(sigma: SpanValue, p: Tumbler)
    requires ValidSpan(sigma) && LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, Reach(sigma))
    // WF:
    ensures ValidSpan(SplitPartition(sigma, p).left) && ValidSpan(SplitPartition(sigma, p).right)
    ensures LevelUniform(SplitPartition(sigma, p).left) && LevelUniform(SplitPartition(sigma, p).right)
    // (c) adjacency: reach(λ) = start(ρ) = p, reach(ρ) = reach(σ)
    ensures Reach(SplitPartition(sigma, p).left) == p
    ensures SplitPartition(sigma, p).right.start == p
    ensures Reach(SplitPartition(sigma, p).right) == Reach(sigma)
    // (a) union:
    ensures SpanSet(SplitPartition(sigma, p).left) + SpanSet(SplitPartition(sigma, p).right) == SpanSet(sigma)
    // (b) disjoint:
    ensures forall t :: !(t in SpanSet(SplitPartition(sigma, p).left) &&
                          t in SpanSet(SplitPartition(sigma, p).right))
  {
    assert Length(Reach(sigma)) == Length(sigma.start);
    WellFormedFromEndpoints(sigma.start, p);
    WellFormedFromEndpoints(p, Reach(sigma));
    var lam := SplitPartition(sigma, p).left;
    var rho := SplitPartition(sigma, p).right;

    // (a) union: SpanSet(lam) + SpanSet(rho) ⊆ SpanSet(sigma)
    forall t | t in SpanSet(lam) + SpanSet(rho)
      ensures t in SpanSet(sigma)
    {
      if t in SpanSet(lam) {
        // lam.start = sigma.start, reach(lam) = p; so sigma.start ≤ t < p < reach(sigma)
        assert sigma.start == t || LexicographicOrder.LexicographicOrder(sigma.start, t);
        assert LexicographicOrder.LexicographicOrder(t, p);
        SWD.LexicographicTransitive(t, p, Reach(sigma));
      } else {
        // rho.start = p, reach(rho) = reach(sigma); so p ≤ t < reach(sigma)
        assert t == p || LexicographicOrder.LexicographicOrder(p, t);
        if t == p {
          assert sigma.start == t || LexicographicOrder.LexicographicOrder(sigma.start, t);
        } else {
          SWD.LexicographicTransitive(sigma.start, p, t);
        }
        assert LexicographicOrder.LexicographicOrder(t, Reach(sigma));
      }
    }

    // (a) union: SpanSet(sigma) ⊆ SpanSet(lam) + SpanSet(rho)
    forall t | t in SpanSet(sigma)
      ensures t in SpanSet(lam) + SpanSet(rho)
    {
      IC.IntrinsicComparison(t, p);
      if IC.Compare(t, p) == IC.LT {
        // t < p: t ∈ ⟦λ⟧ since sigma.start ≤ t < p = reach(λ)
        assert t in SpanSet(lam);
      } else if IC.Compare(t, p) == IC.EQ {
        // t = p = rho.start: t ∈ ⟦ρ⟧
        assert t == p;
        assert t in SpanSet(rho);
      } else {
        // p < t: t ∈ ⟦ρ⟧ since p = rho.start < t < reach(ρ) = reach(σ)
        assert t in SpanSet(rho);
      }
    }

    // (b) disjoint: t < p (from lam) and p ≤ t (from rho) cannot both hold
    forall t | t in SpanSet(lam) && t in SpanSet(rho)
      ensures false
    {
      assert LexicographicOrder.LexicographicOrder(t, p);        // t < reach(lam) = p
      assert t == p || LexicographicOrder.LexicographicOrder(p, t);  // p ≤ t (rho.start = p)
      if t == p {
        IC.IntrinsicComparison(p, p);   // Compare(p,p) = EQ ≠ LT = Compare(t,p); contradiction
      } else {
        SWD.LexicographicTransitive(p, t, p);  // p < t < p gives LexOrder(p,p)
        IC.IntrinsicComparison(p, p);
      }
    }
  }
}

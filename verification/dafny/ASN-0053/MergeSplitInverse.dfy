// ASN-0053: S3b — MergeSplitInverse (DEF / theorem)
// For adjacent level-uniform spans α, β with level_compat(start(α), start(β)),
// merge(α,β) split at the shared boundary recovers {α, β}.
//   Case A (reach(α)=start(β)): split at start(β) yields left=α, right=β.
//   Case B (reach(β)=start(α)): split at start(α) yields left=β, right=α.
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/DisplacementUnique.dfy"

module MergeSplitInverse {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import opened NatStrictTotalOrder
  import SWD = SpanWellDefinedness
  import DivModule = Divergence
  import DRT = DisplacementRoundTrip
  import DU = DisplacementUnique

  datatype SpanValue = SpanValue(start: Tumbler, width: Tumbler)

  ghost predicate ValidSpan(sigma: SpanValue) {
    InT(sigma.start) &&
    InT(sigma.width) &&
    PositiveTumbler.PositiveTumbler(sigma.width) &&
    ActionPoint.ActionPoint(sigma.width) <= Length(sigma.start)
  }

  predicate LevelUniform(sigma: SpanValue) {
    Length(sigma.start) == Length(sigma.width)
  }

  predicate LevelCompat(t1: Tumbler, t2: Tumbler) {
    Length(t1) == Length(t2)
  }

  ghost function Reach(sigma: SpanValue): (r: Tumbler)
    requires ValidSpan(sigma)
    ensures InT(r)
    ensures LexicographicOrder.LexicographicOrder(sigma.start, r)
    ensures Length(r) == Length(sigma.width)
  {
    TumblerAdd.TumblerAdd(sigma.start, sigma.width)
  }

  // Helper: when Length(a) == Length(b) and a < b, Divergence(a,b) <= Length(a).
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
         i <= Length(a) && i <= Length(b) &&
         Component(a, i) == Component(b, i)) &&
      ((k <= Length(a) && k <= Length(b) && Less(Component(a, k), Component(b, k))) ||
       (k == Length(a) + 1 && k <= Length(b)));
    assert k <= m;
    var fm := DivModule.FirstMismatch(a, b, 1, m);
    assert DivModule.Divergence(a, b) == fm;
    if fm > m {
      assert 1 <= k && k < fm;
      assert Component(a, k) == Component(b, k);
      if k <= Length(a) && k <= Length(b) && Less(Component(a, k), Component(b, k)) {
        Irreflexive(Component(a, k));
      }
    }
  }

  // WF: from s < r with Length(s) == Length(r), (s, r⊖s) is a valid span with reach r.
  lemma WFFromEndpoints(s: Tumbler, r: Tumbler)
    requires InT(s) && InT(r)
    requires LexicographicOrder.LexicographicOrder(s, r)
    requires Length(s) == Length(r)
    ensures ValidSpan(SpanValue(s, TumblerSub.TumblerSub(r, s)))
    ensures Length(TumblerSub.TumblerSub(r, s)) == Length(s)
    ensures TumblerAdd.TumblerAdd(s, TumblerSub.TumblerSub(r, s)) == r
  {
    EqualLengthDivergenceBound(s, r);
    DRT.DisplacementRoundTrip(s, r);
  }

  // WR (WidthRecovery): reach(σ) ⊖ start(σ) = width(σ) for level-uniform σ.
  lemma WidthRecovery(sigma: SpanValue)
    requires ValidSpan(sigma) && LevelUniform(sigma)
    ensures TumblerSub.TumblerSub(Reach(sigma), sigma.start) == sigma.width
  {
    var s := sigma.start;
    var w := sigma.width;
    var r := Reach(sigma);
    // Length(s) == Length(r): LevelUniform + Reach ensures
    assert Length(s) == Length(r);
    EqualLengthDivergenceBound(s, r);
    // DisplacementUnique: s<r, Div(s,r)≤#s, #s≤#r, Pos(w), AP(w)≤#s, s⊕w=r → w = r⊖s
    DU.DisplacementUnique(s, r, w);
  }

  // S4 split: left part λ = (start(γ), p ⊖ start(γ))
  ghost function SpanSplitLeft(gamma: SpanValue, p: Tumbler): SpanValue
    requires ValidSpan(gamma) && LevelUniform(gamma)
    requires InT(p) && LevelCompat(gamma.start, p)
    requires LexicographicOrder.LexicographicOrder(gamma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, Reach(gamma))
  {
    SpanValue(gamma.start, TumblerSub.TumblerSub(p, gamma.start))
  }

  // S4 split: right part ρ = (p, reach(γ) ⊖ p)
  ghost function SpanSplitRight(gamma: SpanValue, p: Tumbler): SpanValue
    requires ValidSpan(gamma) && LevelUniform(gamma)
    requires InT(p) && LevelCompat(gamma.start, p)
    requires LexicographicOrder.LexicographicOrder(gamma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, Reach(gamma))
  {
    SpanValue(p, TumblerSub.TumblerSub(Reach(gamma), p))
  }

  // S3b Case A: reach(α) = start(β).
  // Merge gamma = (start(α), reach(β)⊖start(α)); split at p=start(β) recovers α, β.
  // Precondition alpha.start < Reach(beta) is derived from reach(α)=start(β)<reach(β);
  // stated here so TumblerSub in ensures type-checks via short-circuit &&.
  lemma MergeSplitInverseCaseA(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires Reach(alpha) == beta.start
    requires LexicographicOrder.LexicographicOrder(alpha.start, Reach(beta))
    ensures LexicographicOrder.LexicographicOrder(alpha.start, Reach(beta)) &&
      (var gamma := SpanValue(alpha.start, TumblerSub.TumblerSub(Reach(beta), alpha.start));
       var p := beta.start;
       ValidSpan(gamma) && LevelUniform(gamma) &&
       InT(p) && LevelCompat(gamma.start, p) &&
       LexicographicOrder.LexicographicOrder(gamma.start, p) &&
       LexicographicOrder.LexicographicOrder(p, Reach(gamma)) &&
       SpanSplitLeft(gamma, p) == alpha &&
       SpanSplitRight(gamma, p) == beta)
  {
    var p := beta.start;
    // Length equality: Length(alpha.start) == Length(Reach(beta))
    assert Length(alpha.start) == Length(beta.start);   // LevelCompat
    assert Length(beta.start) == Length(beta.width);    // LevelUniform(beta)
    assert Length(Reach(beta)) == Length(beta.width);   // Reach ensures
    assert Length(alpha.start) == Length(Reach(beta));
    // Build gamma = (alpha.start, Reach(beta) ⊖ alpha.start)
    WFFromEndpoints(alpha.start, Reach(beta));
    var gamma := SpanValue(alpha.start, TumblerSub.TumblerSub(Reach(beta), alpha.start));
    assert ValidSpan(gamma);
    assert Length(TumblerSub.TumblerSub(Reach(beta), alpha.start)) == Length(alpha.start);
    assert TumblerAdd.TumblerAdd(alpha.start, TumblerSub.TumblerSub(Reach(beta), alpha.start)) == Reach(beta);
    // Reach(gamma) = Reach(beta)
    assert Reach(gamma) == Reach(beta);
    assert LevelUniform(gamma);
    assert LevelCompat(gamma.start, p);  // Length(alpha.start) == Length(beta.start)
    // p interior: gamma.start = alpha.start < Reach(alpha) = p, and p = beta.start < Reach(beta) = Reach(gamma)
    assert LexicographicOrder.LexicographicOrder(gamma.start, p);
    assert LexicographicOrder.LexicographicOrder(p, Reach(gamma));
    // Split left: TumblerSub(p, gamma.start) = TumblerSub(Reach(alpha), alpha.start) = alpha.width
    WidthRecovery(alpha);
    assert TumblerSub.TumblerSub(p, gamma.start) == alpha.width;
    assert SpanSplitLeft(gamma, p) == alpha;
    // Split right: TumblerSub(Reach(gamma), p) = TumblerSub(Reach(beta), beta.start) = beta.width
    WidthRecovery(beta);
    assert TumblerSub.TumblerSub(Reach(gamma), p) == beta.width;
    assert SpanSplitRight(gamma, p) == beta;
  }

  // S3b Case B: reach(β) = start(α).
  // Merge gamma = (start(β), reach(α)⊖start(β)); split at p=start(α) recovers β, α.
  lemma MergeSplitInverseCaseB(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires Reach(beta) == alpha.start
    requires LexicographicOrder.LexicographicOrder(beta.start, Reach(alpha))
    ensures LexicographicOrder.LexicographicOrder(beta.start, Reach(alpha)) &&
      (var gamma := SpanValue(beta.start, TumblerSub.TumblerSub(Reach(alpha), beta.start));
       var p := alpha.start;
       ValidSpan(gamma) && LevelUniform(gamma) &&
       InT(p) && LevelCompat(gamma.start, p) &&
       LexicographicOrder.LexicographicOrder(gamma.start, p) &&
       LexicographicOrder.LexicographicOrder(p, Reach(gamma)) &&
       SpanSplitLeft(gamma, p) == beta &&
       SpanSplitRight(gamma, p) == alpha)
  {
    var p := alpha.start;
    // Length equality
    assert Length(beta.start) == Length(beta.width);    // LevelUniform(beta)
    assert Length(alpha.start) == Length(beta.start);   // LevelCompat
    assert Length(alpha.start) == Length(alpha.width);  // LevelUniform(alpha)
    assert Length(Reach(alpha)) == Length(alpha.width); // Reach ensures
    assert Length(beta.start) == Length(Reach(alpha));
    // Build gamma = (beta.start, Reach(alpha) ⊖ beta.start)
    WFFromEndpoints(beta.start, Reach(alpha));
    var gamma := SpanValue(beta.start, TumblerSub.TumblerSub(Reach(alpha), beta.start));
    assert ValidSpan(gamma);
    assert Length(TumblerSub.TumblerSub(Reach(alpha), beta.start)) == Length(beta.start);
    assert TumblerAdd.TumblerAdd(beta.start, TumblerSub.TumblerSub(Reach(alpha), beta.start)) == Reach(alpha);
    // Reach(gamma) = Reach(alpha)
    assert Reach(gamma) == Reach(alpha);
    assert LevelUniform(gamma);
    assert LevelCompat(gamma.start, p);  // Length(beta.start) == Length(alpha.start)
    // p interior: gamma.start = beta.start < Reach(beta) = p, and p = alpha.start < Reach(alpha) = Reach(gamma)
    assert LexicographicOrder.LexicographicOrder(gamma.start, p);
    assert LexicographicOrder.LexicographicOrder(p, Reach(gamma));
    // Split left: TumblerSub(p, gamma.start) = TumblerSub(Reach(beta), beta.start) = beta.width
    WidthRecovery(beta);
    assert TumblerSub.TumblerSub(p, gamma.start) == beta.width;
    assert SpanSplitLeft(gamma, p) == beta;
    // Split right: TumblerSub(Reach(gamma), p) = TumblerSub(Reach(alpha), alpha.start) = alpha.width
    WidthRecovery(alpha);
    assert TumblerSub.TumblerSub(Reach(gamma), p) == alpha.width;
    assert SpanSplitRight(gamma, p) == alpha;
  }

  // S3b (MergeSplitInverse): top-level theorem combining both cases.
  // There exist a merged span γ and a boundary point p such that
  // split(γ, p) recovers the original adjacent pair {α, β}.
  lemma MergeSplitInverse(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    requires Reach(alpha) == beta.start || Reach(beta) == alpha.start
    ensures exists gamma: SpanValue, p: Tumbler ::
      ValidSpan(gamma) && LevelUniform(gamma) &&
      InT(p) && LevelCompat(gamma.start, p) &&
      LexicographicOrder.LexicographicOrder(gamma.start, p) &&
      LexicographicOrder.LexicographicOrder(p, Reach(gamma)) &&
      ((SpanSplitLeft(gamma, p) == alpha && SpanSplitRight(gamma, p) == beta) ||
       (SpanSplitLeft(gamma, p) == beta && SpanSplitRight(gamma, p) == alpha))
  {
    if Reach(alpha) == beta.start {
      // Establish beta.start < Reach(beta) and alpha.start < Reach(beta) by transitivity
      SWD.LexicographicTransitive(alpha.start, beta.start, Reach(beta));
      MergeSplitInverseCaseA(alpha, beta);
      var gamma := SpanValue(alpha.start, TumblerSub.TumblerSub(Reach(beta), alpha.start));
      var p := beta.start;
      assert ValidSpan(gamma) && LevelUniform(gamma) &&
             InT(p) && LevelCompat(gamma.start, p) &&
             LexicographicOrder.LexicographicOrder(gamma.start, p) &&
             LexicographicOrder.LexicographicOrder(p, Reach(gamma)) &&
             SpanSplitLeft(gamma, p) == alpha && SpanSplitRight(gamma, p) == beta;
    } else {
      // Reach(beta) == alpha.start (from precondition OR with case A eliminated)
      SWD.LexicographicTransitive(beta.start, alpha.start, Reach(alpha));
      MergeSplitInverseCaseB(alpha, beta);
      var gamma := SpanValue(beta.start, TumblerSub.TumblerSub(Reach(alpha), beta.start));
      var p := alpha.start;
      assert ValidSpan(gamma) && LevelUniform(gamma) &&
             InT(p) && LevelCompat(gamma.start, p) &&
             LexicographicOrder.LexicographicOrder(gamma.start, p) &&
             LexicographicOrder.LexicographicOrder(p, Reach(gamma)) &&
             SpanSplitLeft(gamma, p) == beta && SpanSplitRight(gamma, p) == alpha;
    }
  }
}

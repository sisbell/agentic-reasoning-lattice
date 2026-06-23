// ASN-0053: S11a — DifferenceSeparated (LEMMA)
// SC case (i)/(ii) (separated or adjacent): ⟦α⟧ \ ⟦β⟧ = ⟦α⟧
// Proof: cases (i) and (ii) make ⟦α⟧ ∩ ⟦β⟧ = ∅; set difference = original.
include "IntersectionClosure.dfy"

module DifferenceSeparated {
  import opened IntersectionClosure
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import SpanModule = Span
  import SpanWD = SpanWellDefinedness
  import IC = IntrinsicComparison

  lemma DifferenceSeparated(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires Length(alpha.start) == Length(beta.start)
    // SC case (i): reach(α) < start(β) or reach(β) < start(α)
    // SC case (ii): reach(α) = start(β) or reach(β) = start(α)
    requires (ReachOf(alpha) == beta.start ||
              LexicographicOrder.LexicographicOrder(ReachOf(alpha), beta.start)) ||
             (ReachOf(beta) == alpha.start ||
              LexicographicOrder.LexicographicOrder(ReachOf(beta), alpha.start))
    ensures SpanModule.Span(alpha.start, alpha.length) - SpanModule.Span(beta.start, beta.length) ==
            SpanModule.Span(alpha.start, alpha.length)
  {
    var A := SpanModule.Span(alpha.start, alpha.length);
    var B := SpanModule.Span(beta.start, beta.length);
    // Step 1: show A ∩ B = ∅ by contradiction on any shared element.
    forall t | t in A && t in B
      ensures false
    {
      assert InT(t);
      // t ∈ A: alpha.start ≤ t < reach(alpha)
      assert LexicographicOrder.LexicographicOrder(t, ReachOf(alpha));
      assert t == alpha.start || LexicographicOrder.LexicographicOrder(alpha.start, t);
      // t ∈ B: beta.start ≤ t < reach(beta)
      assert LexicographicOrder.LexicographicOrder(t, ReachOf(beta));
      assert t == beta.start || LexicographicOrder.LexicographicOrder(beta.start, t);
      if ReachOf(alpha) == beta.start ||
         LexicographicOrder.LexicographicOrder(ReachOf(alpha), beta.start) {
        // reach(alpha) ≤ start(beta) ≤ t, but t < reach(alpha) — contradiction
        if ReachOf(alpha) != beta.start {
          SpanWD.LexicographicTransitive(t, ReachOf(alpha), beta.start);
        }
        // Now: LexicographicOrder(t, beta.start) and beta.start ≤ t
        IC.IntrinsicComparison(t, beta.start);
      } else {
        // reach(beta) ≤ start(alpha) ≤ t, but t < reach(beta) — contradiction
        if ReachOf(beta) != alpha.start {
          SpanWD.LexicographicTransitive(t, ReachOf(beta), alpha.start);
        }
        // Now: LexicographicOrder(t, alpha.start) and alpha.start ≤ t
        IC.IntrinsicComparison(t, alpha.start);
      }
    }
    // Step 2: ∅ intersection implies difference equals A.
    assert A * B == iset{};
    assert A - B == A;
  }
}

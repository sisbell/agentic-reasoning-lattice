// ASN-0053: S11d — GeneralDifferenceBound (DEF)
// For level-uniform level-compatible spans α and β, ⟦α⟧ \ ⟦β⟧ is at most 2 spans.
// Covers all SC cases via case analysis on span boundaries.
include "DifferenceBound.dfy"

module GeneralDifferenceBound {
  import opened DifferenceBound
  import opened LexicographicOrder

  ghost function GeneralDifferenceBound(alpha: SpanValue, beta: SpanValue): (result: seq<SpanValue>)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LevelUniform(alpha) && LevelUniform(beta)
    requires LevelCompat(alpha.start, beta.start)
    ensures |result| <= 2
  {
    // SC(i)/(ii): reach(α) ≤ start(β) — separated or adjacent
    if Reach(alpha) == beta.start ||
       LexicographicOrder.LexicographicOrder(Reach(alpha), beta.start)
    then [alpha]
    // SC(i)/(ii): reach(β) ≤ start(α) — separated or adjacent
    else if Reach(beta) == alpha.start ||
            LexicographicOrder.LexicographicOrder(Reach(beta), alpha.start)
    then [alpha]
    // All overlapping cases: left piece (if start(α) < start(β)) + right piece (if reach(β) < reach(α))
    // SC(v) equal → lp=[], rp=[] → 0 spans
    // SC(iv) β⊂α → lp=[λ], rp=[ρ] → ≤2 spans
    // SC(iv) α⊂β → lp=[], rp=[] → 0 spans
    // SC(iii) overlap case 1 → lp=[λ], rp=[] → 1 span
    // SC(iii) overlap case 2 → lp=[], rp=[ρ] → 1 span
    else
      var lp := if LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
                then [LambdaSpan(alpha, beta)] else [];
      var rp := if LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
                then [RhoSpan(alpha, beta)] else [];
      lp + rp
  }
}

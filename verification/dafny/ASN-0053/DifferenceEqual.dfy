// ASN-0053: S11b — DifferenceEqual (DEF/lemma)
// SC case (v) (equal): ⟦α⟧ \ ⟦β⟧ = ∅
// Proof: equal start and reach give equal span sets; X \ X = ∅.
include "IntersectionClosure.dfy"

module DifferenceEqual {
  import opened IntersectionClosure
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import SpanModule = Span

  lemma DifferenceEqual(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires alpha.start == beta.start
    requires ReachOf(alpha) == ReachOf(beta)
    ensures SpanModule.Span(alpha.start, alpha.length) - SpanModule.Span(beta.start, beta.length) == iset{}
  {
  }
}

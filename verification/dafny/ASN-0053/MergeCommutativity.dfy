// ASN-0053: S3a — MergeCommutativity (DEF / corollary)
// Merge(α, β) = ⟦α⟧ ∪ ⟦β⟧; commutativity: ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧
include "Convexity.dfy"

module MergeCommutativity {
  import opened Convexity
  import opened CarrierSetDefinition
  import SpanModule = Span

  // S3 DEF: merge of two spans is the union of their point sets.
  ghost function Merge(alpha: SpanValue, beta: SpanValue): iset<Tumbler>
    requires ValidSpan(alpha) && ValidSpan(beta)
  {
    SpanModule.Span(alpha.start, alpha.length) + SpanModule.Span(beta.start, beta.length)
  }

  // S3a (MergeCommutativity): ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧
  lemma MergeCommutativity(alpha: SpanValue, beta: SpanValue)
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures Merge(alpha, beta) == Merge(beta, alpha)
  { }
}

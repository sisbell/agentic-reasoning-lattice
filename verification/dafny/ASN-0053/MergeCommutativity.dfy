// ASN-0053: S3a — MergeCommutativity — DEF (corollary of set-union commutativity)
// merge(α,β) and merge(β,α) denote the same point set: ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧
include "./SpanDefs.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/CarrierSetDefinition.dfy"

module MergeCommutativity {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import S = Span

  // Definition: ⟦merge(α,β)⟧ = ⟦α⟧ ∪ ⟦β⟧
  ghost function MergeDenotation(alpha: SpanEntry, beta: SpanEntry): iset<Tumbler>
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
  {
    S.Span(alpha.start, alpha.width) + S.Span(beta.start, beta.width)
  }

  // S3a: ⟦merge(α,β)⟧ = ⟦merge(β,α)⟧ — commutativity follows from iset union symmetry
  lemma MergeCommutativity(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    ensures MergeDenotation(alpha, beta) == MergeDenotation(beta, alpha)
  {
  }
}

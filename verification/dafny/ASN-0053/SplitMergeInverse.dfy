// ASN-0053: S4a — SplitMergeInverse (DEF / corollary)
// Corollary of S4: split then merge recovers ⟦σ⟧.
//   SplitMerge(σ, p) := ⟦left(σ,p)⟧ ∪ ⟦right(σ,p)⟧ = ⟦σ⟧
include "SplitPartition.dfy"

module SplitMergeInverse {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import SP = SplitPartition

  // S4a DEF: merge of the two sub-spans produced by splitting σ at p.
  ghost function SplitMerge(sigma: SP.SpanValue, p: Tumbler): iset<Tumbler>
    requires SP.ValidSpan(sigma) && SP.LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, SP.Reach(sigma))
    requires SP.ValidSpan(SP.SplitPartition(sigma, p).left)
    requires SP.ValidSpan(SP.SplitPartition(sigma, p).right)
  {
    SP.SpanSet(SP.SplitPartition(sigma, p).left) +
    SP.SpanSet(SP.SplitPartition(sigma, p).right)
  }

  // S4a corollary: SplitMerge(σ, p) = ⟦σ⟧
  lemma SplitMergeInverse(sigma: SP.SpanValue, p: Tumbler)
    requires SP.ValidSpan(sigma) && SP.LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, SP.Reach(sigma))
    ensures SP.ValidSpan(SP.SplitPartition(sigma, p).left)
    ensures SP.ValidSpan(SP.SplitPartition(sigma, p).right)
    ensures SplitMerge(sigma, p) == SP.SpanSet(sigma)
  {
    SP.SplitPartitionTheorem(sigma, p);
  }
}

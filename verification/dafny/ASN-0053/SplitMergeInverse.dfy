// ASN-0053: S4a — SplitMergeInverse (DEF / corollary)
// Corollary: splitting σ at p (S4) then merging (S3) recovers σ.
//   S3(S4(σ, p)) = σ  where  S3: γ = (start(σ), reach(σ) ⊖ start(σ))
include "SplitPartition.dfy"
include "../ASN-0034/DisplacementUnique.dfy"

module SplitMergeInverse {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import TumblerSub
  import SP = SplitPartition
  import DU = DisplacementUnique

  // WR (WidthRecovery): reach(σ) ⊖ start(σ) = width(σ) for level-uniform σ.
  lemma WidthRecovery(sigma: SP.SpanValue)
    requires SP.ValidSpan(sigma) && SP.LevelUniform(sigma)
    requires LexicographicOrder.LexicographicOrder(sigma.start, SP.Reach(sigma))
    ensures TumblerSub.TumblerSub(SP.Reach(sigma), sigma.start) == sigma.width
  {
    var s := sigma.start;
    var w := sigma.width;
    var r := SP.Reach(sigma);
    assert Length(s) == Length(r) by {
      assert Length(s) == Length(w);  // LevelUniform
      assert Length(r) == Length(w);  // Reach ensures
    }
    SP.EqualLengthDivergenceBound(s, r);
    DU.DisplacementUnique(s, r, w);
  }

  // S4a DEF: S3 merge applied to S4 split outputs.
  // s_m = min(start(λ), start(ρ)) = start(σ); r_m = max(reach(λ), reach(ρ)) = reach(σ)
  // γ = (s_m, r_m ⊖ s_m)
  ghost function SplitMerge(sigma: SP.SpanValue, p: Tumbler): SP.SpanValue
    requires SP.ValidSpan(sigma) && SP.LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, SP.Reach(sigma))
    requires LexicographicOrder.LexicographicOrder(sigma.start, SP.Reach(sigma))
  {
    SP.SpanValue(sigma.start, TumblerSub.TumblerSub(SP.Reach(sigma), sigma.start))
  }

  // S4a corollary: S3(S4(σ, p)) = σ
  lemma SplitMergeInverse(sigma: SP.SpanValue, p: Tumbler)
    requires SP.ValidSpan(sigma) && SP.LevelUniform(sigma)
    requires InT(p) && Length(p) == Length(sigma.start)
    requires LexicographicOrder.LexicographicOrder(sigma.start, p)
    requires LexicographicOrder.LexicographicOrder(p, SP.Reach(sigma))
    requires LexicographicOrder.LexicographicOrder(sigma.start, SP.Reach(sigma))
    ensures SplitMerge(sigma, p) == sigma
  {
    SP.SplitPartitionTheorem(sigma, p);  // S4: λ = (s, p⊖s), ρ = (p, reach(σ)⊖p)
    WidthRecovery(sigma);                // WR: reach(σ) ⊖ start(σ) = width(σ)
  }
}

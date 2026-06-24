// ASN-0053: S4a — SplitMergeInverse (DEF/corollary)
// Splitting σ at interior point p and merging the two halves recovers σ exactly.
// min-start = σ.start (since σ.start < p), max-reach = reach(σ) (since p < reach(σ)),
// so merge = SpanEntry(σ.start, reach(σ) ⊖ σ.start) = σ by WR.
include "./SpanDefs.dfy"
include "./SplitPartition.dfy"
include "./MergeEquivalence.dfy"
include "./WidthRecovery.dfy"
include "./LevelConstraint.dfy"
include "../ASN-0034/TumblerSub.dfy"

module SplitMergeInverse {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import LO = LexicographicOrder
  import S6 = LevelConstraint
  import SP = SplitPartition
  import ME = MergeEquivalence
  import WR = WidthRecovery
  import TS = TumblerSub

  // S4a: split(σ, p) then merge recovers σ.
  lemma SplitMergeInverse(sigma: SpanEntry, p: Tumbler)
    requires ValidSpan(sigma)
    requires S6.LevelUniform(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(sigma.start, p)
    requires LO.LexicographicOrder(p, Reach(sigma))
    requires Length(p) == Length(sigma.start)
    ensures SpanEntry(sigma.start, TS.TumblerSub(Reach(sigma), sigma.start)) == sigma
  {
    WR.WidthRecovery(sigma);
  }
}

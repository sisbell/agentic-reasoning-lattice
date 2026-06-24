// ASN-0053: S3b — MergeSplitInverse (DEF/theorem)
// For adjacent level-uniform spans α and β with level_compat(start(α), start(β)):
// splitting merge(α, β) at the shared boundary recovers {α, β}.
// Case A (reach(α) = start(β)): split at start(β) gives left=α, right=β.
// Case B (reach(β) = start(α)): split at start(α) gives left=β, right=α.
include "./SpanDefs.dfy"
include "./WidthRecovery.dfy"
include "./SplitPartition.dfy"
include "./MergeEquivalence.dfy"
include "./LevelConstraint.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module MergeSplitInverse {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import LO = LexicographicOrder
  import S6 = LevelConstraint
  import ME = MergeEquivalence
  import SP = SplitPartition
  import WR = WidthRecovery
  import TS = TumblerSub
  import IC = IntrinsicComparison
  import SWD = SpanWellDefinedness

  // S3b: merge-split roundtrip for adjacent level-uniform spans.
  // The ensures express LeftSpan/RightSpan field equalities directly,
  // using ME.MergeStart and ME.MergeReach instead of ME.MergeSpan to
  // avoid the LO(MergeStart, MergeReach) precondition in ensures.
  lemma MergeSplitInverse(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    requires Reach(alpha) == beta.start || Reach(beta) == alpha.start
    // Case A: reach(α) = start(β) → split merge(α,β) at start(β) gives (α, β)
    ensures (Reach(alpha) == beta.start ==>
               SpanEntry(ME.MergeStart(alpha, beta),
                         TS.TumblerSub(beta.start, ME.MergeStart(alpha, beta))) == alpha &&
               SpanEntry(beta.start,
                         TS.TumblerSub(ME.MergeReach(alpha, beta), beta.start)) == beta)
    // Case B: reach(β) = start(α) → split merge(α,β) at start(α) gives (β, α)
    ensures (Reach(beta) == alpha.start ==>
               SpanEntry(ME.MergeStart(alpha, beta),
                         TS.TumblerSub(alpha.start, ME.MergeStart(alpha, beta))) == beta &&
               SpanEntry(alpha.start,
                         TS.TumblerSub(ME.MergeReach(alpha, beta), alpha.start)) == alpha)
  {
    ME.StartLtReach(alpha, beta);
    WR.WidthRecovery(alpha);
    WR.WidthRecovery(beta);
    IC.IntrinsicComparison(alpha.start, beta.start);
    IC.IntrinsicComparison(Reach(alpha), Reach(beta));
  }
}

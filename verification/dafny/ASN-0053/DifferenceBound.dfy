// ASN-0053: S11 — DifferenceBound (DEF/theorem)
// For level-uniform spans α and β with level_compat(start(α), start(β)) and ⟦β⟧ ⊆ ⟦α⟧,
// ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.
// λ = (start(α), start(β) ⊖ start(α)) when start(α) < start(β)
// ρ = (reach(β), reach(α) ⊖ reach(β)) when reach(β) < reach(α)
include "./SpanDefs.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "./LevelConstraint.dfy"
include "./EmptyDistinction.dfy"
include "./Convexity.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"

module DifferenceBound {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened PositiveTumbler
  import opened ActionPoint
  import opened NatCarrierSet
  import WF = WellFormedSpanFromEndpoints
  import LC = LevelConstraint
  import S = Span
  import SWD = SpanWellDefinedness
  import TS = TumblerSub
  import C0 = Convexity

  // ≤ on tumblers: equals or strictly less.
  ghost predicate Leq(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
  {
    a == b || LexicographicOrder.LexicographicOrder(a, b)
  }

  // S11: DifferenceBound — constructs the span-set for ⟦α⟧ \ ⟦β⟧.
  // Preconditions express ⟦β⟧ ⊆ ⟦α⟧ via boundary characterization:
  //   start(α) ≤ start(β)  and  reach(β) ≤ reach(α)
  ghost function DifferenceBound(alpha: SpanEntry, beta: SpanEntry): (result: seq<SpanEntry>)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires Leq(alpha.start, beta.start)
    requires Leq(Reach(beta), Reach(alpha))
    ensures |result| <= 2
  {
    var left :=
      if LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
      then [SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start))]
      else [];
    var right :=
      if LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
      then [SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)))]
      else [];
    left + right
  }

  // Left span λ is well-formed when start(α) < start(β).
  lemma LeftSpanValid(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(alpha.start, beta.start)
    ensures ValidSpan(SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start)))
    ensures Reach(SpanEntry(alpha.start, TS.TumblerSub(beta.start, alpha.start))) == beta.start
  {
    WF.WellFormedSpanFromEndpoints(alpha.start, beta.start);
  }

  // Right span ρ is well-formed when reach(β) < reach(α).
  // WF's carrier preconditions reach(β), reach(α) ∈ T come from ValidSpan + Reach's ensures.
  // WF's length precondition #reach(β) = #reach(α) is derived from S6 + LevelCompat.
  lemma RightSpanValid(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    requires LexicographicOrder.LexicographicOrder(Reach(beta), Reach(alpha))
    ensures ValidSpan(SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta))))
    ensures Reach(SpanEntry(Reach(beta), TS.TumblerSub(Reach(alpha), Reach(beta)))) == Reach(alpha)
  {
    LC.LevelConstraint(alpha);
    LC.LevelConstraint(beta);
    WF.WellFormedSpanFromEndpoints(Reach(beta), Reach(alpha));
  }
}

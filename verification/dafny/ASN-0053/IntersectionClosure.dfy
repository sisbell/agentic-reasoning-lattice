// ASN-0053: S1 — IntersectionClosure (DEF/theorem)
// γ = (s', r' ⊖ s'), s' = max(start(α), start(β)), r' = min(reach(α), reach(β)).
// ⟦α⟧ ∩ ⟦β⟧ = {t ∈ T : s' ≤ t < r'}, which is ⟦γ⟧ when non-empty.
include "./SpanDefs.dfy"
include "./LevelConstraint.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"

module IntersectionClosure {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import LO = LexicographicOrder
  import S6 = LevelConstraint
  import WF = WellFormedSpanFromEndpoints
  import S = Span
  import TS = TumblerSub
  import SWD = SpanWellDefinedness
  import IC = IntrinsicComparison

  // s' = max(start(α), start(β)) under LexicographicOrder
  ghost function IntersectionStart(alpha: SpanEntry, beta: SpanEntry): Tumbler
    requires InT(alpha.start) && InT(beta.start)
    ensures InT(IntersectionStart(alpha, beta))
    ensures IntersectionStart(alpha, beta) == alpha.start || IntersectionStart(alpha, beta) == beta.start
  {
    if LO.LexicographicOrder(alpha.start, beta.start) then beta.start else alpha.start
  }

  // r' = min(Reach(α), Reach(β)) under LexicographicOrder
  ghost function IntersectionReach(alpha: SpanEntry, beta: SpanEntry): Tumbler
    requires ValidSpan(alpha) && ValidSpan(beta)
    ensures InT(IntersectionReach(alpha, beta))
    ensures IntersectionReach(alpha, beta) == Reach(alpha) || IntersectionReach(alpha, beta) == Reach(beta)
  {
    if LO.LexicographicOrder(Reach(alpha), Reach(beta)) then Reach(alpha) else Reach(beta)
  }

  // S1 definition: γ = (s', r' ⊖ s') — the intersection span in the non-empty case
  ghost function IntersectionSpan(alpha: SpanEntry, beta: SpanEntry): SpanEntry
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    requires LO.LexicographicOrder(IntersectionStart(alpha, beta), IntersectionReach(alpha, beta))
  {
    SpanEntry(
      IntersectionStart(alpha, beta),
      TS.TumblerSub(IntersectionReach(alpha, beta), IntersectionStart(alpha, beta))
    )
  }

  // All four boundary tumblers share a common length (from S6 and LevelCompat)
  lemma BoundaryLengthsAgree(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    ensures Length(alpha.start) == Length(Reach(alpha))
    ensures Length(alpha.start) == Length(beta.start)
    ensures Length(beta.start) == Length(Reach(beta))
    ensures Length(Reach(alpha)) == Length(Reach(beta))
  {
    S6.LevelConstraint(alpha);
    S6.LevelConstraint(beta);
  }

  // s' and r' have the same length
  lemma StartReachSameLength(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    ensures Length(IntersectionStart(alpha, beta)) == Length(IntersectionReach(alpha, beta))
  {
    BoundaryLengthsAgree(alpha, beta);
  }

  // γ is a valid span with Reach(γ) = r'
  lemma IntersectionSpanValid(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    requires LO.LexicographicOrder(IntersectionStart(alpha, beta), IntersectionReach(alpha, beta))
    ensures ValidSpan(IntersectionSpan(alpha, beta))
    ensures Reach(IntersectionSpan(alpha, beta)) == IntersectionReach(alpha, beta)
  {
    var s' := IntersectionStart(alpha, beta);
    var r' := IntersectionReach(alpha, beta);
    StartReachSameLength(alpha, beta);
    WF.WellFormedSpanFromEndpoints(s', r');
  }

  // S1 (IntersectionClosure): ⟦α⟧ ∩ ⟦β⟧ = {t ∈ T : s' ≤ t < r'}
  lemma IntersectionClosure(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires S6.LevelUniform(alpha) && S6.LevelUniform(beta)
    requires S6.LevelCompat(alpha.start, beta.start)
    ensures
      var s' := IntersectionStart(alpha, beta);
      var r' := IntersectionReach(alpha, beta);
      forall t :: InT(t) ==>
        ((t in S.Span(alpha.start, alpha.width) && t in S.Span(beta.start, beta.width)) <==>
         ((t == s' || LO.LexicographicOrder(s', t)) && LO.LexicographicOrder(t, r')))
  {
    var s' := IntersectionStart(alpha, beta);
    var r' := IntersectionReach(alpha, beta);

    forall t | InT(t)
      ensures (t in S.Span(alpha.start, alpha.width) && t in S.Span(beta.start, beta.width)) <==>
              ((t == s' || LO.LexicographicOrder(s', t)) && LO.LexicographicOrder(t, r'))
    {
      // Forward: membership in both spans → interval membership
      if t in S.Span(alpha.start, alpha.width) && t in S.Span(beta.start, beta.width) {
        // t ≥ s': one of the span starts is s'
        assert t == s' || LO.LexicographicOrder(s', t) by {
          if LO.LexicographicOrder(alpha.start, beta.start) {
            // s' = beta.start; Span(beta) gives t == beta.start || beta.start < t
          } else {
            // s' = alpha.start; Span(alpha) gives t == alpha.start || alpha.start < t
          }
        }
        // t < r': one of the reaches is r'
        assert LO.LexicographicOrder(t, r') by {
          if LO.LexicographicOrder(Reach(alpha), Reach(beta)) {
            // r' = Reach(alpha); Span(alpha) gives t < Reach(alpha)
          } else {
            // r' = Reach(beta); Span(beta) gives t < Reach(beta)
          }
        }
      }

      // Backward: interval membership → membership in both spans
      if (t == s' || LO.LexicographicOrder(s', t)) && LO.LexicographicOrder(t, r') {
        // t ∈ Span(alpha)
        assert t in S.Span(alpha.start, alpha.width) by {
          // Lower bound: t ≥ alpha.start (since t ≥ s' ≥ alpha.start)
          assert t == alpha.start || LO.LexicographicOrder(alpha.start, t) by {
            if LO.LexicographicOrder(alpha.start, beta.start) {
              // s' = beta.start > alpha.start; alpha.start < s' ≤ t
              if t == s' {
                // alpha.start < s' = t
              } else {
                // s' < t; alpha.start < s' < t by transitivity
                SWD.LexicographicTransitive(alpha.start, s', t);
              }
            }
            // else s' = alpha.start and t ≥ s' = alpha.start
          }
          // Upper bound: t < Reach(alpha) (since t < r' ≤ Reach(alpha))
          assert LO.LexicographicOrder(t, Reach(alpha)) by {
            if LO.LexicographicOrder(Reach(alpha), Reach(beta)) {
              // r' = Reach(alpha); t < r' = Reach(alpha)
            } else {
              // r' = Reach(beta); need Reach(beta) ≤ Reach(alpha)
              if Reach(beta) == Reach(alpha) {
                // t < r' = Reach(beta) = Reach(alpha)
              } else {
                // NOT(Reach(alpha) < Reach(beta)) and Reach(beta) ≠ Reach(alpha)
                // → Reach(beta) < Reach(alpha) by total order
                IC.IntrinsicComparison(Reach(alpha), Reach(beta));
                SWD.LexicographicTransitive(t, r', Reach(alpha));
              }
            }
          }
        }

        // t ∈ Span(beta)
        assert t in S.Span(beta.start, beta.width) by {
          // Lower bound: t ≥ beta.start (since t ≥ s' ≥ beta.start)
          assert t == beta.start || LO.LexicographicOrder(beta.start, t) by {
            if LO.LexicographicOrder(alpha.start, beta.start) {
              // s' = beta.start; t ≥ s' = beta.start
            } else {
              // s' = alpha.start; need beta.start ≤ alpha.start
              if beta.start == alpha.start {
                // t ≥ s' = alpha.start = beta.start
              } else {
                // NOT(alpha.start < beta.start) and beta.start ≠ alpha.start
                // → beta.start < alpha.start = s'
                IC.IntrinsicComparison(alpha.start, beta.start);
                assert LO.LexicographicOrder(beta.start, s');
                if t == s' {
                  // beta.start < s' = t
                } else {
                  // s' < t; beta.start < s' < t by transitivity
                  SWD.LexicographicTransitive(beta.start, s', t);
                }
              }
            }
          }
          // Upper bound: t < Reach(beta) (since t < r' ≤ Reach(beta))
          assert LO.LexicographicOrder(t, Reach(beta)) by {
            if LO.LexicographicOrder(Reach(alpha), Reach(beta)) {
              // r' = Reach(alpha) < Reach(beta); t < r' < Reach(beta) by transitivity
              SWD.LexicographicTransitive(t, r', Reach(beta));
            } else {
              // r' = Reach(beta); t < r' = Reach(beta)
            }
          }
        }
      }
    }
  }
}

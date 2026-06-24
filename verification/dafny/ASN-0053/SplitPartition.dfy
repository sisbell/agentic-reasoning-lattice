// ASN-0053: S4 — SplitPartition (DEF/theorem)
// For level-uniform σ = (s, ℓ) and interior point p with level_compat(s, p),
// defines λ = (s, p ⊖ s) and ρ = (p, reach(σ) ⊖ p) satisfying:
// (a) ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧  (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅  (c) reach(λ) = start(ρ) = p.
include "./SpanDefs.dfy"
include "./WellFormedSpanFromEndpoints.dfy"
include "./LevelConstraint.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/TumblerSub.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"

module SplitPartition {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import LO = LexicographicOrder
  import S6 = LevelConstraint
  import WF = WellFormedSpanFromEndpoints
  import S = Span
  import SWD = SpanWellDefinedness
  import TS = TumblerSub
  import IC = IntrinsicComparison

  // S4 DEF: left span λ = (s, p ⊖ s)
  ghost function LeftSpan(sigma: SpanEntry, p: Tumbler): SpanEntry
    requires ValidSpan(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(sigma.start, p)
  {
    SpanEntry(sigma.start, TS.TumblerSub(p, sigma.start))
  }

  // S4 DEF: right span ρ = (p, reach(σ) ⊖ p)
  ghost function RightSpan(sigma: SpanEntry, p: Tumbler): SpanEntry
    requires ValidSpan(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(p, Reach(sigma))
  {
    SpanEntry(p, TS.TumblerSub(Reach(sigma), p))
  }

  // S4 — SplitPartition: the splitting function
  ghost function SplitPartition(sigma: SpanEntry, p: Tumbler): (SpanEntry, SpanEntry)
    requires ValidSpan(sigma)
    requires S6.LevelUniform(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(sigma.start, p)
    requires LO.LexicographicOrder(p, Reach(sigma))
    requires Length(p) == Length(sigma.start)
  {
    (LeftSpan(sigma, p), RightSpan(sigma, p))
  }

  // Both constructed spans are valid with stated reaches.
  lemma SplitValid(sigma: SpanEntry, p: Tumbler)
    requires ValidSpan(sigma)
    requires S6.LevelUniform(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(sigma.start, p)
    requires LO.LexicographicOrder(p, Reach(sigma))
    requires Length(p) == Length(sigma.start)
    ensures ValidSpan(LeftSpan(sigma, p))
    ensures ValidSpan(RightSpan(sigma, p))
    ensures Reach(LeftSpan(sigma, p)) == p
    ensures Reach(RightSpan(sigma, p)) == Reach(sigma)
  {
    WF.WellFormedSpanFromEndpoints(sigma.start, p);
    S6.LevelConstraint(sigma);
    WF.WellFormedSpanFromEndpoints(p, Reach(sigma));
  }

  // S4 theorem: ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧ and ⟦λ⟧ ∩ ⟦ρ⟧ = ∅, via boundary predicates.
  // Left clause = {t : s ≤ t < p} = ⟦λ⟧; right clause = {t : p ≤ t < reach(σ)} = ⟦ρ⟧.
  lemma SplitPartitionTheorem(sigma: SpanEntry, p: Tumbler)
    requires ValidSpan(sigma)
    requires S6.LevelUniform(sigma)
    requires InT(p)
    requires LO.LexicographicOrder(sigma.start, p)
    requires LO.LexicographicOrder(p, Reach(sigma))
    requires Length(p) == Length(sigma.start)
    ensures forall t :: InT(t) ==>
      ((t in S.Span(sigma.start, sigma.width)) <==>
       (((t == sigma.start || LO.LexicographicOrder(sigma.start, t)) &&
          LO.LexicographicOrder(t, p)) ||
        ((t == p || LO.LexicographicOrder(p, t)) &&
          LO.LexicographicOrder(t, Reach(sigma)))))
  {
    forall t | InT(t)
      ensures ((t in S.Span(sigma.start, sigma.width)) <==>
               (((t == sigma.start || LO.LexicographicOrder(sigma.start, t)) &&
                  LO.LexicographicOrder(t, p)) ||
                ((t == p || LO.LexicographicOrder(p, t)) &&
                  LO.LexicographicOrder(t, Reach(sigma)))))
    {
      // forward: split on t vs p
      if t in S.Span(sigma.start, sigma.width) {
        IC.IntrinsicComparison(t, p);
        if IC.Compare(t, p) == IC.LT {
          // t < p: left clause holds
        } else {
          // t >= p: right clause holds
        }
      }
      // backward left: t in [s, p) → t in span(σ)
      if ((t == sigma.start || LO.LexicographicOrder(sigma.start, t)) &&
          LO.LexicographicOrder(t, p))
      {
        SWD.LexicographicTransitive(t, p, Reach(sigma));
      }
      // backward right: t in [p, reach(σ)) → t in span(σ)
      if ((t == p || LO.LexicographicOrder(p, t)) &&
          LO.LexicographicOrder(t, Reach(sigma)))
      {
        if t == p {
          // sigma.start < p = t, so lower bound holds
        } else {
          SWD.LexicographicTransitive(sigma.start, p, t);
        }
      }
    }
  }
}

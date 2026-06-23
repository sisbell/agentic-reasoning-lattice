// ASN-0053: NormalizedSpanSet — LEMMA (definition)
// A span-set Σ = ⟨σ₁,...,σₙ⟩ is normalized iff N1 (sorted starts) and N2 (separated reaches).
// The lemma proves N2 → N1 for well-formed span-sets, showing N1 is implied by N2.
include "../ASN-0034/CarrierSetDefinition.dfy"
include "../ASN-0034/LexicographicOrder.dfy"
include "../ASN-0034/TumblerAdd.dfy"
include "../ASN-0034/PositiveTumbler.dfy"
include "../ASN-0034/ActionPoint.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module NormalizedSpanSet {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened LexicographicOrder
  import opened NatCarrierSet
  import SWD = SpanWellDefinedness

  // A span entry: (start, width), representing σ = (s, ℓ).
  datatype SpanEntry = SpanEntry(start: Tumbler, width: Tumbler)

  // T12 well-formedness: σ is a valid span.
  ghost predicate ValidSpan(sigma: SpanEntry) {
    InT(sigma.start) &&
    InT(sigma.width) &&
    PositiveTumbler.PositiveTumbler(sigma.width) &&
    ActionPoint.ActionPoint(sigma.width) <= Length(sigma.start)
  }

  // reach(σ) = start(σ) ⊕ width(σ).
  function Reach(sigma: SpanEntry): (r: Tumbler)
    requires ValidSpan(sigma)
    ensures InT(r)
    ensures LexicographicOrder.LexicographicOrder(sigma.start, r)
  {
    TumblerAdd.TumblerAdd(sigma.start, sigma.width)
  }

  // Helper: extract InT(start) from ValidSpan — provides a trigger for Z3.
  lemma ValidSpanInT(spans: seq<SpanEntry>, i: nat)
    requires i < |spans|
    requires ValidSpan(spans[i])
    ensures InT(spans[i].start)
  { }

  // NormalizedSpanSet: a span-set satisfies N1 (sorted starts) and N2 (separated reaches).
  // Guarded by explicit ValidSpan hypothesis so LexicographicOrder preconditions are met.
  ghost predicate IsNormalizedSpanSet(spans: seq<SpanEntry>)
  {
    forall i :: 0 <= i < |spans| - 1 ==>
      (ValidSpan(spans[i]) && ValidSpan(spans[i+1]) ==>
        LexicographicOrder.LexicographicOrder(spans[i].start, spans[i+1].start) &&
        LexicographicOrder.LexicographicOrder(Reach(spans[i]), spans[i+1].start))
  }

  // N2 → N1: for well-formed spans, reach(σᵢ) < start(σᵢ₊₁) implies start(σᵢ) < start(σᵢ₊₁).
  // Proof: start(σᵢ) < reach(σᵢ) by TumblerAdd strict-increase; then by transitivity.
  lemma NormalizedSpanSet(spans: seq<SpanEntry>)
    requires forall i :: 0 <= i < |spans| ==> ValidSpan(spans[i])
    requires forall i :: 0 <= i < |spans| - 1 ==>
               (ValidSpan(spans[i]) && ValidSpan(spans[i+1]) ==>
                LexicographicOrder.LexicographicOrder(Reach(spans[i]), spans[i+1].start))
    ensures forall i :: 0 <= i < |spans| - 1 ==>
              (ValidSpan(spans[i]) && ValidSpan(spans[i+1]) ==>
               LexicographicOrder.LexicographicOrder(spans[i].start, spans[i+1].start))
  {
    forall i | 0 <= i < |spans| - 1
      ensures ValidSpan(spans[i]) && ValidSpan(spans[i+1]) ==>
                LexicographicOrder.LexicographicOrder(spans[i].start, spans[i+1].start)
    {
      if ValidSpan(spans[i]) && ValidSpan(spans[i+1]) {
        SWD.LexicographicTransitive(spans[i].start, Reach(spans[i]), spans[i+1].start);
      }
    }
  }
}

// ASN-0053: NormalizedSpanSet — LEMMA (definition)
// N2 → N1: for well-formed span-sets, separated reaches imply sorted starts.
// Proof: start(σᵢ) < reach(σᵢ) by TumblerAdd strict-increase; transitivity closes.
include "./SpanDefs.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module NormalizedSpanSet {
  import opened SpanDefs
  import opened LexicographicOrder
  import SWD = SpanWellDefinedness

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

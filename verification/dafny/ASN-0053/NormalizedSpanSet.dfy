// ASN-0053: NormalizedSpanSet — DEFINITION
// normalized(Σ) iff N1 (Sorted) and N2 (Separated) both hold.
include "./SpanDefs.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"

module NormalizedSpanSet {
  import opened SpanDefs
  import opened LexicographicOrder
  import SWD = SpanWellDefinedness

  ghost predicate Normalized(spans: seq<SpanEntry>)
    requires forall i :: 0 <= i < |spans| ==> ValidSpan(spans[i])
  {
    IsNormalizedSpanSet(spans)
  }
}

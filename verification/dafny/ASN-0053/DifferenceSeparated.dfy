// ASN-0053: S11a — DifferenceSeparated (LEMMA)
include "./SpanClassification.dfy"

module DifferenceSeparated {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import SC = SpanClassification

  lemma DifferenceSeparated(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires SC.SpanClassification(alpha, beta) == SC.Separated ||
             SC.SpanClassification(alpha, beta) == SC.Adjacent
    ensures SC.Denotation(alpha) - SC.Denotation(beta) == SC.Denotation(alpha)
  {
    SC.DisjointCases(alpha, beta);
  }
}

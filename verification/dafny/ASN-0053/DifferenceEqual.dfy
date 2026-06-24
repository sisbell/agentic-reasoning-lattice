// ASN-0053: S11b — DifferenceEqual (DEF/lemma)
include "./SpanClassification.dfy"
include "../ASN-0034/LeftCancellation.dfy"

module DifferenceEqual {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import SC = SpanClassification
  import IC = IntrinsicComparison
  import LC = LeftCancellation

  lemma DifferenceEqual(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires SC.SpanClassification(alpha, beta) == SC.Equal
    ensures SC.Denotation(alpha) - SC.Denotation(beta) == iset{}
  {
    var SA := alpha.start; var SB := beta.start;
    var RA := Reach(alpha); var RB := Reach(beta);
    assert IC.Compare(SA, SB) == IC.EQ;
    assert IC.Compare(RA, RB) == IC.EQ;
    IC.IntrinsicComparison(SA, SB);
    IC.IntrinsicComparison(RA, RB);
    assert SA == SB;
    assert RA == RB;
    LC.LeftCancellation(SA, alpha.width, beta.width);
    assert alpha.width == beta.width;
  }
}

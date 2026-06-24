// ASN-0053: S11d — GeneralDifferenceBound (DEF/lemma)
// For any two valid level-uniform level-compat spans α and β,
// ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.
include "./DifferenceBound.dfy"
include "./DifferenceSeparated.dfy"
include "./DifferenceEqual.dfy"
include "./DifferenceOverlap.dfy"

module GeneralDifferenceBound {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import DB = DifferenceBound
  import SC = SpanClassification
  import DS = DifferenceSeparated
  import DE = DifferenceEqual
  import DO = DifferenceOverlap
  import LC = LevelConstraint
  import IC = IntrinsicComparison
  import SWD = SpanWellDefinedness

  // When β.start ≤ α.start and reach(α) ≤ reach(β), every element of ⟦α⟧
  // lies in ⟦β⟧, so ⟦α⟧ \ ⟦β⟧ = ∅.
  lemma AlphaSubsetBeta(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires beta.start == alpha.start || LexicographicOrder.LexicographicOrder(beta.start, alpha.start)
    requires Reach(alpha) == Reach(beta) || LexicographicOrder.LexicographicOrder(Reach(alpha), Reach(beta))
    ensures SC.Denotation(alpha) - SC.Denotation(beta) == iset{}
  {
    forall t : Tumbler | t in SC.Denotation(alpha)
      ensures t in SC.Denotation(beta)
    {
      if beta.start != alpha.start && alpha.start != t {
        SWD.LexicographicTransitive(beta.start, alpha.start, t);
      }
      if Reach(alpha) != Reach(beta) {
        SWD.LexicographicTransitive(t, Reach(alpha), Reach(beta));
      }
      SC.InSpan(beta, t);
    }
  }

  // S11d: for any two valid level-uniform level-compat spans,
  // ⟦α⟧ \ ⟦β⟧ is representable as at most 2 spans.
  lemma GeneralDifferenceBound(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha) && ValidSpan(beta)
    requires LC.LevelUniform(alpha) && LC.LevelUniform(beta)
    requires LC.LevelCompat(alpha.start, beta.start)
    ensures exists spans: seq<SpanEntry> :: |spans| <= 2 &&
              DB.CollectiveDenotation(spans) == SC.Denotation(alpha) - SC.Denotation(beta)
  {
    var SA := alpha.start; var SB := beta.start;
    var RA := Reach(alpha); var RB := Reach(beta);
    IC.IntrinsicComparison(SA, SB); IC.IntrinsicComparison(SB, SA);
    IC.IntrinsicComparison(RA, RB); IC.IntrinsicComparison(RB, RA);
    IC.IntrinsicComparison(RA, SB); IC.IntrinsicComparison(RB, SA);
    var rel := SC.SpanClassification(alpha, beta);
    if rel == SC.Separated || rel == SC.Adjacent {
      DS.DifferenceSeparated(alpha, beta);
      assert DB.CollectiveDenotation([alpha]) == SC.Denotation(alpha);
    } else if rel == SC.Equal {
      DE.DifferenceEqual(alpha, beta);
      assert DB.CollectiveDenotation([]) == iset{};
    } else if rel == SC.ProperOverlap {
      DO.DifferenceOverlap(alpha, beta);
      var gamma :| ValidSpan(gamma) && SC.Denotation(gamma) == SC.Denotation(alpha) - SC.Denotation(beta);
      assert DB.CollectiveDenotation([gamma]) == SC.Denotation(gamma);
    } else {
      // rel == SC.Containment
      if IC.Compare(SA, SB) != IC.GT && IC.Compare(RB, RA) != IC.GT {
        // α ⊇ β: DifferenceBound gives at most 2 spans
        var spans := DB.DifferenceBound(alpha, beta);
        DB.DifferenceBoundCorrect(alpha, beta);
      } else {
        // β ⊇ α: ⟦α⟧ \ ⟦β⟧ = ∅
        assert IC.Compare(SB, SA) != IC.GT && IC.Compare(RA, RB) != IC.GT;
        AlphaSubsetBeta(alpha, beta);
        assert DB.CollectiveDenotation([]) == iset{};
      }
    }
  }
}

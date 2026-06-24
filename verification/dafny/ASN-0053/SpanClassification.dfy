// ASN-0053: SC — SpanClassification (DEF)
// Defines the span denotation and classifies pairs of spans into five cases.
include "./SpanDefs.dfy"
include "../ASN-0034/Span.dfy"
include "../ASN-0034/SpanWellDefinedness.dfy"
include "../ASN-0034/IntrinsicComparison.dfy"

module SpanClassification {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import S = Span
  import SWD = SpanWellDefinedness
  import IC = IntrinsicComparison

  // ⟦γ⟧ = { p : start(γ) ≤ p < reach(γ) } (reach exclusive)
  ghost function Denotation(gamma: SpanEntry): iset<Tumbler>
    requires ValidSpan(gamma)
  {
    S.Span(gamma.start, gamma.width)
  }

  datatype SpanRelation =
    | Separated     // ⟦α⟧ ∩ ⟦β⟧ = ∅ with a gap
    | Adjacent      // ⟦α⟧ ∩ ⟦β⟧ = ∅ touching at one boundary
    | ProperOverlap // ⟦α⟧ ∩ ⟦β⟧ ≠ ∅, neither contains the other
    | Containment   // one denotation is a proper subset of the other
    | Equal         // denotations are identical

  // SC: classify two spans using their four boundary points under T1.
  // Pre: both spans are valid (each has start < reach, all boundary points in T)
  ghost function SpanClassification(alpha: SpanEntry, beta: SpanEntry): SpanRelation
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
  {
    var SA := alpha.start; var SB := beta.start;
    var RA := Reach(alpha); var RB := Reach(beta);
    if IC.Compare(RA, SB) == IC.LT then Separated      // reach(α) < start(β)
    else if IC.Compare(RB, SA) == IC.LT then Separated // reach(β) < start(α)
    else if IC.Compare(RA, SB) == IC.EQ then Adjacent  // reach(α) = start(β)
    else if IC.Compare(RB, SA) == IC.EQ then Adjacent  // reach(β) = start(α)
    else if IC.Compare(SA, SB) == IC.EQ && IC.Compare(RA, RB) == IC.EQ then Equal
    else if IC.Compare(SA, SB) != IC.GT && IC.Compare(RB, RA) != IC.GT then Containment  // α ⊇ β
    else if IC.Compare(SB, SA) != IC.GT && IC.Compare(RA, RB) != IC.GT then Containment  // β ⊇ α
    else ProperOverlap
  }

  // Helper: LexOrder(a, b) implies a != b and NOT LexOrder(b, a)
  lemma LexOrderExcludes(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures a != b
    ensures !LexicographicOrder.LexicographicOrder(b, a)
  {
    IC.IntrinsicComparison(a, b);
    IC.IntrinsicComparison(b, a);
  }

  // Postcondition: Separated/Adjacent ↔ disjoint denotations
  lemma DisjointCases(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires SpanClassification(alpha, beta) == Separated ||
             SpanClassification(alpha, beta) == Adjacent
    ensures Denotation(alpha) !! Denotation(beta)
  {
    var SA := alpha.start; var SB := beta.start;
    var RA := Reach(alpha); var RB := Reach(beta);
    forall t | t in Denotation(alpha)
      ensures t !in Denotation(beta)
    {
      // t ∈ Span(SA, alpha.width): InT(t), SA ≤ t, t < RA
      assert LexicographicOrder.LexicographicOrder(t, RA);
      if IC.Compare(RA, SB) == IC.LT {
        // Separated: reach(α) < start(β) → t < RA < SB → t ∉ Span(SB, ...)
        IC.IntrinsicComparison(RA, SB);
        SWD.LexicographicTransitive(t, RA, SB);
        LexOrderExcludes(t, SB);
      } else if IC.Compare(RB, SA) == IC.LT {
        // Separated: reach(β) < start(α) → RB < SA ≤ t → NOT LexOrder(t, RB)
        IC.IntrinsicComparison(RB, SA);
        if t == SA {
          IC.IntrinsicComparison(t, RB);
        } else {
          assert LexicographicOrder.LexicographicOrder(SA, t);
          SWD.LexicographicTransitive(RB, SA, t);
          IC.IntrinsicComparison(t, RB);
        }
      } else if IC.Compare(RA, SB) == IC.EQ {
        // Adjacent: reach(α) = start(β) → t < RA = SB → t ∉ Span(SB, ...)
        IC.IntrinsicComparison(RA, SB);
        assert RA == SB;
        assert LexicographicOrder.LexicographicOrder(t, SB);
        LexOrderExcludes(t, SB);
      } else {
        // Adjacent: reach(β) = start(α); t ∈ Span(SA,...) means SA ≤ t, but Span(SB,...) needs t < RB = SA
        assert IC.Compare(RB, SA) == IC.EQ;
        IC.IntrinsicComparison(RB, SA);
        assert RB == SA;
        if t == SA {
          IC.IntrinsicComparison(t, RB);
        } else {
          assert LexicographicOrder.LexicographicOrder(SA, t);
          IC.IntrinsicComparison(t, RB);
        }
      }
    }
  }

  // Helper: t is in Denotation(sigma) given explicit membership conditions
  lemma InSpan(sigma: SpanEntry, t: Tumbler)
    requires ValidSpan(sigma)
    requires InT(t)
    requires sigma.start == t || LexicographicOrder.LexicographicOrder(sigma.start, t)
    requires LexicographicOrder.LexicographicOrder(t, Reach(sigma))
    ensures t in Denotation(sigma)
  { }

  // Helper: start of span is in the span; establishes start < reach
  lemma StartInSpan(sigma: SpanEntry)
    requires ValidSpan(sigma)
    ensures sigma.start in Denotation(sigma)
    ensures LexicographicOrder.LexicographicOrder(sigma.start, Reach(sigma))
  {
    SWD.SpanWellDefinedness(sigma.start, sigma.width);
  }

  // Postcondition: ProperOverlap/Containment/Equal ↔ nonempty intersection
  lemma OverlapCases(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires SpanClassification(alpha, beta) == ProperOverlap ||
             SpanClassification(alpha, beta) == Containment ||
             SpanClassification(alpha, beta) == Equal
    ensures !(Denotation(alpha) !! Denotation(beta))
  {
    var SA := alpha.start; var SB := beta.start;
    var RA := Reach(alpha); var RB := Reach(beta);
    // Not Separated/Adjacent: RA > SB and RB > SA
    assert IC.Compare(RA, SB) != IC.LT && IC.Compare(RA, SB) != IC.EQ;
    assert IC.Compare(RB, SA) != IC.LT && IC.Compare(RB, SA) != IC.EQ;
    IC.IntrinsicComparison(RA, SB);
    IC.IntrinsicComparison(RB, SA);
    assert LexicographicOrder.LexicographicOrder(SB, RA);  // SB < RA
    assert LexicographicOrder.LexicographicOrder(SA, RB);  // SA < RB
    StartInSpan(alpha);
    StartInSpan(beta);
    if SpanClassification(alpha, beta) == Equal {
      // SA == SB: SA is in both spans
      IC.IntrinsicComparison(SA, SB);
      assert SA == SB;
      assert SA in Denotation(alpha);
      InSpan(beta, SA);
    } else if SpanClassification(alpha, beta) == Containment {
      if IC.Compare(SA, SB) != IC.GT && IC.Compare(RB, RA) != IC.GT {
        // α ⊇ β: witness = SB (in β by StartInSpan, in α since SA ≤ SB < RB ≤ RA)
        assert SB in Denotation(beta);
        IC.IntrinsicComparison(SA, SB);
        IC.IntrinsicComparison(RB, RA);
        // SB < RB (from StartInSpan(beta)), RB ≤ RA → SB < RA
        if IC.Compare(RB, RA) == IC.LT {
          SWD.LexicographicTransitive(SB, RB, RA);
        } else {
          assert RB == RA;
        }
        assert LexicographicOrder.LexicographicOrder(SB, RA);
        InSpan(alpha, SB);
      } else {
        // β ⊇ α: witness = SA (in α by StartInSpan, in β since SB ≤ SA < RA ≤ RB)
        assert SA in Denotation(alpha);
        IC.IntrinsicComparison(SB, SA);
        IC.IntrinsicComparison(RA, RB);
        // SA < RA (from StartInSpan(alpha)), RA ≤ RB → SA < RB
        if IC.Compare(RA, RB) == IC.LT {
          SWD.LexicographicTransitive(SA, RA, RB);
        } else {
          assert RA == RB;
        }
        assert LexicographicOrder.LexicographicOrder(SA, RB);
        InSpan(beta, SA);
      }
    } else {
      // ProperOverlap: use start of whichever span comes later as witness
      if IC.Compare(SA, SB) == IC.LT {
        // SA < SB: SB ∈ α (SA < SB < RA) and SB ∈ β (by StartInSpan)
        IC.IntrinsicComparison(SA, SB);
        assert SB in Denotation(beta);
        InSpan(alpha, SB);
      } else {
        // SB ≤ SA (Compare EQ or GT): SA ∈ β (SB ≤ SA and SA < RB)
        IC.IntrinsicComparison(SA, SB);
        assert SA in Denotation(alpha);
        if SA == SB {
          InSpan(beta, SA);
        } else {
          // Compare(SA, SB) == GT → LexOrder(SB, SA)
          assert LexicographicOrder.LexicographicOrder(SB, SA);
          InSpan(beta, SA);
        }
      }
    }
  }
}

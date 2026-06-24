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

  // Postcondition: Separated/Adjacent ↔ disjoint denotations
  lemma DisjointCases(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires SpanClassification(alpha, beta) == Separated ||
             SpanClassification(alpha, beta) == Adjacent
    ensures Denotation(alpha) !! Denotation(beta)
  { }

  // Postcondition: ProperOverlap/Containment/Equal ↔ nonempty intersection
  lemma OverlapCases(alpha: SpanEntry, beta: SpanEntry)
    requires ValidSpan(alpha)
    requires ValidSpan(beta)
    requires SpanClassification(alpha, beta) == ProperOverlap ||
             SpanClassification(alpha, beta) == Containment ||
             SpanClassification(alpha, beta) == Equal
    ensures !(Denotation(alpha) !! Denotation(beta))
  { }
}

// ASN-0053: S2 — EmptyDistinction (DEF/corollary)
include "../ASN-0034/SpanWellDefinedness.dfy"

module EmptyDistinction {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import SpanModule = Span
  import SpanWD = SpanWellDefinedness

  // ⟦s, ℓ⟧ = { p ∈ T : s ≤ p < s ⊕ ℓ }
  ghost function Denote(s: Tumbler, l: Tumbler): iset<Tumbler>
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
  {
    SpanModule.Span(s, l)
  }

  // Corollary: s witnesses non-emptiness — no well-formed span denotes ∅
  lemma EmptyDistinction(s: Tumbler, l: Tumbler)
    requires InT(s) && InT(l)
    requires PositiveTumbler.PositiveTumbler(l)
    requires ActionPoint.ActionPoint(l) <= Length(s)
    ensures s in Denote(s, l)
  {
    SpanWD.SpanWellDefinedness(s, l);
  }
}

// ASN-0053: MutuallyLevelCompatible — LEMMA (definition)
// A span-set Σ is mutually level-compatible when all starts share length L.
// When each span is also level-uniform, all boundary tumblers share L.
// Depends: S6 (LevelConstraint)
include "./LevelConstraint.dfy"

module MutuallyLevelCompatible {
  import opened SpanDefs
  import opened CarrierSetDefinition
  import opened LevelConstraint

  ghost predicate IsMutuallyLevelCompatible(spans: seq<SpanEntry>) {
    forall i, j :: 0 <= i < |spans| && 0 <= j < |spans| ==>
      LevelCompat(spans[i].start, spans[j].start)
  }

  lemma MutuallyLevelCompatible(spans: seq<SpanEntry>)
    requires forall i :: 0 <= i < |spans| ==> ValidSpan(spans[i])
    requires forall i :: 0 <= i < |spans| ==> LevelUniform(spans[i])
    requires IsMutuallyLevelCompatible(spans)
    ensures forall i, j :: 0 <= i < |spans| && 0 <= j < |spans| ==>
      Length(spans[i].start) == Length(spans[j].start) &&
      Length(spans[i].width) == Length(spans[j].start) &&
      Length(Reach(spans[i])) == Length(spans[j].start)
  { }
}

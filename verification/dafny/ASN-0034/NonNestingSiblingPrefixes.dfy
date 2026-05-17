// ASN-0034: T10a.2 — NonNestingSiblingPrefixes (LEMMA, corollary)
// Distinct outputs of a single allocator are prefix-incomparable.
// By T10a.1 all siblings share the same length; a prefix relation
// among equal-length distinct tumblers would force pointwise equality,
// collapsing to identity via T3 (CanonicalRepresentation) — contradiction.
include "./AllocatorDiscipline.dfy"
include "./UniformSiblingLength.dfy"
include "./PrefixRelation.dfy"
include "./CanonicalRepresentation.dfy"

module NonNestingSiblingPrefixes {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened AllocatorDiscipline
  import opened UniformSiblingLength
  import opened PrefixRelation
  import opened CanonicalRepresentation

  lemma NonNestingSiblingPrefixes(a: Allocator, i: nat, j: nat)
    requires AllocatorDiscipline.AllocatorDiscipline(a)
    requires SiblingAt(a, i) != SiblingAt(a, j)
    ensures InT(SiblingAt(a, i)) && InT(SiblingAt(a, j))
    ensures !PrefixOf(SiblingAt(a, i), SiblingAt(a, j))
    ensures !PrefixOf(SiblingAt(a, j), SiblingAt(a, i))
  {
    SiblingInT(a, i);
    SiblingInT(a, j);
    UniformSiblingLength.UniformSiblingLength(a, i);
    UniformSiblingLength.UniformSiblingLength(a, j);
    var ti := SiblingAt(a, i);
    var tj := SiblingAt(a, j);
    if PrefixOf(ti, tj) {
      CanonicalRepresentation.CanonicalRepresentation(ti, tj);
    }
    if PrefixOf(tj, ti) {
      CanonicalRepresentation.CanonicalRepresentation(tj, ti);
    }
  }
}

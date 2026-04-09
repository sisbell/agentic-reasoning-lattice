include "./SyntacticEquivalence.dfy"

module UniqueParse {
  // T4b — UniqueParse
  // Corollary of T3, T4, T4a: fields(t) is well-defined and uniquely determined.
  // T3 (CanonicalRepresentation) holds by Dafny datatype equality — the component
  // sequence is fixed, so scanning for zeros yields determinate separator positions.

  import opened SyntacticEquivalence

  // The zero positions: the only candidate separator positions in any valid parse
  ghost function ZeroPositions(s: seq<nat>): set<nat> {
    set i | 0 <= i < |s| && s[i] == 0
  }

  // A valid parse: separator positions satisfy the T4 bidirectional constraint.
  // Separators have value 0; non-separators have strictly positive value.
  ghost predicate ValidParse(s: seq<nat>, seps: set<nat>) {
    (forall i :: i in seps ==> 0 <= i < |s|) &&
    (forall i :: i in seps ==> s[i] == 0) &&
    (forall i :: 0 <= i < |s| && i !in seps ==> s[i] > 0)
  }

  // Core: the separator set of any valid parse equals the zero positions.
  lemma SeparatorsDetermined(s: seq<nat>, seps: set<nat>)
    requires ValidParse(s, seps)
    ensures seps == ZeroPositions(s)
  { }

  // T4b: any two valid parses of a T4-valid address have identical separators,
  // hence fields(t) — the decomposition at separator positions — is unique.
  lemma UniqueParse(t: Tumbler, seps1: set<nat>, seps2: set<nat>)
    requires ValidTumbler(t)
    requires SyntacticWF(t.components)
    requires ValidParse(t.components, seps1)
    requires ValidParse(t.components, seps2)
    ensures seps1 == seps2
  {
    SeparatorsDetermined(t.components, seps1);
    SeparatorsDetermined(t.components, seps2);
  }
}

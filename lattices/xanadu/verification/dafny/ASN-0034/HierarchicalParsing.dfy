include "./LevelDetermination.dfy"

module HierarchicalParsing {
  // T4 — HierarchicalParsing
  // Axiom: valid address tumblers satisfy field-separator constraints.
  // Postconditions from T3 (canonical representation, structural equality):
  //   (a) Non-empty field constraint <=> syntactic conditions [T4a]
  //   (b) Separator set uniquely determined by t alone [T4b]
  //   (c) zeros(t) determines hierarchical level bijectively [T4c]

  import SE = SyntacticEquivalence
  import UP = UniqueParse
  import LD = LevelDetermination

  // T4 axiom: valid address tumbler constraints
  ghost predicate ValidAddress(t: SE.Tumbler) {
    SE.ValidTumbler(t) &&
    SE.SyntacticWF(t.components) &&
    LD.ZeroCount(t.components) <= 3
  }

  // T4: hierarchical parsing — postconditions (a), (b), and (c)
  lemma HierarchicalParsing(t: SE.Tumbler)
    requires ValidAddress(t)
    // (a) non-empty field constraint <=> syntactic well-formedness
    ensures SE.FieldsNonEmpty(t.components, 0) <==> SE.SyntacticWF(t.components)
    // (b) a valid parse exists and any two valid parses yield identical separator sets
    ensures exists seps: set<nat> :: UP.ValidParse(t.components, seps)
    ensures forall seps1: set<nat>, seps2: set<nat> ::
              UP.ValidParse(t.components, seps1) && UP.ValidParse(t.components, seps2)
              ==> seps1 == seps2
    // (c) zeros(t) determines hierarchical level bijectively
    ensures (LD.ZeroCount(t.components) == 0 <==> LD.LevelOfZeros(LD.ZeroCount(t.components)) == LD.Node)
    ensures (LD.ZeroCount(t.components) == 1 <==> LD.LevelOfZeros(LD.ZeroCount(t.components)) == LD.User)
    ensures (LD.ZeroCount(t.components) == 2 <==> LD.LevelOfZeros(LD.ZeroCount(t.components)) == LD.Document)
    ensures (LD.ZeroCount(t.components) == 3 <==> LD.LevelOfZeros(LD.ZeroCount(t.components)) == LD.Element)
  {
    SE.SyntacticEquivalence(t);
    assert UP.ValidParse(t.components, UP.ZeroPositions(t.components));
  }
}

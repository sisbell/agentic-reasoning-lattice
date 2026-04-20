include "./UniqueParse.dfy"

module LevelDetermination {
  // T4c — LevelDetermination
  // Corollary of T4, T4b: zeros(t) bijectively determines
  // hierarchical level on {0,1,2,3}.

  import opened SyntacticEquivalence

  // Count of zero-valued components
  function ZeroCount(s: seq<nat>): nat
    decreases |s|
  {
    if |s| == 0 then 0
    else (if s[0] == 0 then 1 else 0) + ZeroCount(s[1..])
  }

  // The four hierarchical levels
  datatype HierLevel = Node | User | Document | Element

  // Mapping: zero count -> level
  function LevelOfZeros(n: nat): HierLevel
    requires n <= 3
  {
    if n == 0 then Node
    else if n == 1 then User
    else if n == 2 then Document
    else Element
  }

  // T4 validity: well-formed address with bounded zero count
  ghost predicate T4Valid(t: Tumbler) {
    ValidTumbler(t) &&
    SyntacticWF(t.components) &&
    ZeroCount(t.components) <= 3
  }

  // Injectivity: distinct zero counts yield distinct levels
  lemma LevelOfZerosInjective(n1: nat, n2: nat)
    requires n1 <= 3 && n2 <= 3
    requires LevelOfZeros(n1) == LevelOfZeros(n2)
    ensures n1 == n2
  { }

  // Surjectivity: every level is realized
  lemma LevelOfZerosSurjective(l: HierLevel)
    ensures exists n: nat :: n <= 3 && LevelOfZeros(n) == l
  {
    match l {
      case Node => assert LevelOfZeros(0) == Node;
      case User => assert LevelOfZeros(1) == User;
      case Document => assert LevelOfZeros(2) == Document;
      case Element => assert LevelOfZeros(3) == Element;
    }
  }

  // T4c: zeros(t) determines hierarchical level bijectively
  lemma LevelDetermination(t1: Tumbler, t2: Tumbler)
    requires T4Valid(t1) && T4Valid(t2)
    ensures LevelOfZeros(ZeroCount(t1.components)) ==
            LevelOfZeros(ZeroCount(t2.components))
            <==>
            ZeroCount(t1.components) == ZeroCount(t2.components)
  { }
}

include "./AllocatorDiscipline.dfy"

module NonNestingSiblingPrefixes {
  // T10a.2 — NonNestingSiblingPrefixes (LEMMA)
  // Corollary of T10a.1 (uniform sibling length), T1, TA5:
  // siblings produced by inc(·, 0) have equal length,
  // and equal-length distinct tumblers cannot be prefixes of each other.

  import opened AllocatorDiscipline

  // Iterated sibling increment: n applications of inc(·, 0)
  function IncSiblingN(t: Tumbler, n: nat): Tumbler
    requires ValidTumbler(t)
    ensures ValidTumbler(IncSiblingN(t, n))
    ensures |IncSiblingN(t, n).components| == |t.components|
    decreases n
  {
    if n == 0 then t
    else IncSibling(IncSiblingN(t, n - 1))
  }

  // The last component of IncSiblingN(t, n) is t.last + n
  lemma IncSiblingNLast(t: Tumbler, n: nat)
    requires ValidTumbler(t)
    ensures IncSiblingN(t, n).components[|t.components| - 1] == t.components[|t.components| - 1] + n
    decreases n
  {
    if n == 0 {
    } else {
      IncSiblingNLast(t, n - 1);
    }
  }

  lemma NonNestingSiblingPrefixes(base: Tumbler, i: nat, j: nat)
    requires ValidTumbler(base)
    requires i != j
    ensures var a := IncSiblingN(base, i); var b := IncSiblingN(base, j);
            !IsPrefix(a, b) && !IsPrefix(b, a)
  {
    var a := IncSiblingN(base, i);
    var b := IncSiblingN(base, j);
    // Distinct indices → distinct last components → distinct tumblers
    IncSiblingNLast(base, i);
    IncSiblingNLast(base, j);
    assert a.components[|base.components| - 1] != b.components[|base.components| - 1];
    // Equal length (T10a.1) + distinct → non-nesting (NonNestingSiblings)
    NonNestingSiblings(a, b);
  }
}

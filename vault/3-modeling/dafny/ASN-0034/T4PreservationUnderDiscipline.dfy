include "./AllocatorDiscipline.dfy"
include "./IncrementPreservesT4.dfy"

module T4PreservationUnderDiscipline {
  // T10a.4 — T4PreservationUnderDiscipline (LEMMA)
  // Corollary of T10a (AllocatorDiscipline) and TA5a (IncrementPreservesT4):
  // Under the allocator discipline, every increment operation preserves
  // ValidAddress (T4). The discipline restricts k to {0, 1, 2} with
  // zero-count bounds; TA5a proves preservation holds iff those bounds hold.

  import INC = IncrementPreservesT4
  import HP = HierarchicalParsing
  import SE = SyntacticEquivalence
  import LD = LevelDetermination

  lemma T4PreservationUnderDiscipline(t: SE.Tumbler, k: nat)
    requires HP.ValidAddress(t)
    requires k == 0 || (k == 1 && LD.ZeroCount(t.components) <= 3) || (k == 2 && LD.ZeroCount(t.components) <= 2)
    ensures HP.ValidAddress(INC.Inc(t, k))
  {
    INC.IncrementPreservesT4(t, k);
  }
}

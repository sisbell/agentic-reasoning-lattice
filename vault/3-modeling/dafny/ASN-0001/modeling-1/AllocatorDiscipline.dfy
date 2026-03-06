include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AllocatorDisciplineModule {

  import opened TumblerAlgebra

  // ASN-0001 T10a — AllocatorDiscipline (INV, predicate(State, State))
  // transition invariant

  datatype AllocatorId = AllocatorId(id: nat)

  datatype AllocState = AllocState(streams: map<AllocatorId, seq<Tumbler>>)

  // Last significant position: index of last nonzero component
  function LastSigRec(s: seq<nat>, i: nat): nat
    requires i < |s|
    requires exists j :: 0 <= j <= i && s[j] != 0
    ensures 0 <= LastSigRec(s, i) <= i
    ensures s[LastSigRec(s, i)] != 0
    ensures forall j :: LastSigRec(s, i) < j <= i ==> s[j] == 0
    decreases i
  {
    if s[i] != 0 then i
    else LastSigRec(s, i - 1)
  }

  function LastSig(t: Tumbler): nat
    requires PositiveTumbler(t)
    ensures LastSig(t) < |t.components|
    ensures t.components[LastSig(t)] != 0
    ensures forall j :: LastSig(t) < j < |t.components| ==> t.components[j] == 0
  {
    LastSigRec(t.components, |t.components| - 1)
  }

  // Sibling increment: inc(prev, 0) — same length, only last sig position changes
  ghost predicate IsSiblingInc(prev: Tumbler, next: Tumbler) {
    PositiveTumbler(prev) &&
    |next.components| == |prev.components| &&
    (var s := LastSig(prev);
     next.components[s] == prev.components[s] + 1 &&
     forall i :: 0 <= i < |prev.components| && i != s ==>
       next.components[i] == prev.components[i])
  }

  // Child spawn: inc(parent, k) for some k > 0 — extends parent to create child prefix
  // k is determined by the length difference, so no existential needed
  ghost predicate IsChildSpawn(parent: Tumbler, child_prefix: Tumbler) {
    |child_prefix.components| > |parent.components| &&
    (forall i :: 0 <= i < |parent.components| ==>
      child_prefix.components[i] == parent.components[i]) &&
    (forall i :: |parent.components| <= i < |child_prefix.components| - 1 ==>
      child_prefix.components[i] == 0) &&
    child_prefix.components[|child_prefix.components| - 1] == 1
  }

  // T10a: Allocator discipline
  // Each allocator produces siblings exclusively by inc(·, 0).
  // New allocators arise via child spawning from an existing allocator.
  ghost predicate AllocatorDiscipline(s: AllocState, s': AllocState) {
    // Sibling discipline: consecutive addresses in each stream are sibling increments
    (forall a :: a in s'.streams ==>
      forall i :: 0 <= i < |s'.streams[a]| - 1 ==>
        IsSiblingInc(s'.streams[a][i], s'.streams[a][i+1])) &&
    // Append-only: existing streams are preserved
    (forall a :: a in s.streams ==>
      a in s'.streams &&
      |s'.streams[a]| >= |s.streams[a]| &&
      s'.streams[a][..|s.streams[a]|] == s.streams[a]) &&
    // Provenance: new allocators' first entry is a child spawn from some parent
    (forall a :: a in s'.streams && a !in s.streams && |s'.streams[a]| > 0 ==>
      exists parent :: parent in s.streams && |s.streams[parent]| > 0 &&
        IsChildSpawn(s.streams[parent][|s.streams[parent]| - 1], s'.streams[a][0]))
  }
}

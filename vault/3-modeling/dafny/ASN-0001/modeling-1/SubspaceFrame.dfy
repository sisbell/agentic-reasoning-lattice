include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module SubspaceFrame {

  import opened TumblerAlgebra

  // TA7b — SubspaceFrame (FRAME, ensures on Insert/Delete)
  //
  // An INSERT or DELETE operation within subspace S1 does not modify
  // any position in a distinct subspace S2:
  //   (A b in S2 : post(b) = pre(b))

  type ContentId = nat

  // V-space position: subspace identifier and ordinal within that subspace
  datatype VEntry = VEntry(subspace: nat, ordinal: nat)

  // V-space state: maps content items to their V-positions
  type VState = map<ContentId, VEntry>

  // Frame predicate: every content item outside the target subspace
  // retains its membership and position
  ghost predicate Frame(pre: VState, post: VState, targetSubspace: nat) {
    forall id :: id in pre && pre[id].subspace != targetSubspace ==>
      id in post && post[id] == pre[id]
  }

  // Insert within subspace s at point p, shifting by amount n
  function Insert(st: VState, s: nat, p: nat, n: nat): VState
    requires n > 0
  {
    map id | id in st ::
      if st[id].subspace == s && st[id].ordinal >= p
      then VEntry(s, st[id].ordinal + n)
      else st[id]
  }

  // Delete within subspace s: positions >= p + n shift down by n
  function Delete(st: VState, s: nat, p: nat, n: nat): VState
    requires n > 0
    requires forall id :: id in st && st[id].subspace == s && st[id].ordinal > p ==>
               st[id].ordinal >= p + n
  {
    map id | id in st ::
      if st[id].subspace == s && st[id].ordinal >= p + n
      then VEntry(s, st[id].ordinal - n)
      else st[id]
  }

  // TA7b: Insert preserves positions in other subspaces
  lemma InsertFrame(st: VState, s: nat, p: nat, n: nat)
    requires n > 0
    ensures Frame(st, Insert(st, s, p, n), s)
  { }

  // TA7b: Delete preserves positions in other subspaces
  lemma DeleteFrame(st: VState, s: nat, p: nat, n: nat)
    requires n > 0
    requires forall id :: id in st && st[id].subspace == s && st[id].ordinal > p ==>
               st[id].ordinal >= p + n
    ensures Frame(st, Delete(st, s, p, n), s)
  { }
}

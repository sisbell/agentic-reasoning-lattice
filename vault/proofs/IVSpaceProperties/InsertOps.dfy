
module InsertOps {
  import opened TumblerAlgebra
  import opened Foundation

  // Shared INSERT operation on seq-based V-space.
  // V-space as seq<IAddr>, isomorphic to Foundation's vmap under J1.
  // Position j (1-indexed) corresponds to index j-1.
  function InsertV(v: seq<IAddr>, p: nat, k: nat, newAddrs: seq<IAddr>): (v': seq<IAddr>)
    requires 1 <= p <= |v| + 1
    requires k >= 1
    requires |newAddrs| == k
    ensures |v'| == |v| + k
  {
    v[..p-1] + newAddrs + v[p-1..]
  }

  // Elements of a sequence as a set
  function SetOf(s: seq<IAddr>): set<IAddr> {
    set i | 0 <= i < |s| :: s[i]
  }
}

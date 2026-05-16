module LastSignificantPosition {
  // TA5-SIG — LastSignificantPosition (DEF)
  // sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}) when nonzero exists; #t when all zero
  // 0-based: rightmost nonzero index; last index when all zero

  datatype Tumbler = Tumbler(components: seq<nat>)

  predicate HasNonZero(s: seq<nat>) {
    exists i :: 0 <= i < |s| && s[i] != 0
  }

  function Sig(t: Tumbler): (p: nat)
    requires |t.components| >= 1
    ensures p < |t.components|
    ensures HasNonZero(t.components) ==> t.components[p] != 0
    ensures forall j :: p < j < |t.components| ==> t.components[j] == 0
    ensures !HasNonZero(t.components) ==> p == |t.components| - 1
  {
    FindLastNonZero(t.components, |t.components|)
  }

  function FindLastNonZero(s: seq<nat>, i: nat): (p: nat)
    requires |s| >= 1
    requires 0 < i <= |s|
    ensures p < |s|
    ensures forall j :: p < j < i ==> s[j] == 0
    ensures (exists k :: 0 <= k < i && s[k] != 0) ==> s[p] != 0
    ensures !(exists k :: 0 <= k < i && s[k] != 0) ==> p == |s| - 1
    decreases i
  {
    if s[i - 1] != 0 then i - 1
    else if i == 1 then |s| - 1
    else FindLastNonZero(s, i - 1)
  }
}

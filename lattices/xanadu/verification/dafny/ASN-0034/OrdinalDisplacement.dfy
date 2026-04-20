module OrdinalDisplacement {
  // OrdinalDisplacement — OrdinalDisplacement (DEF)
  // δ(n, m) = [0, ..., 0, n] of length m, action point m

  datatype Tumbler = Tumbler(components: seq<nat>)

  function OrdinalDisplacement(n: nat, m: nat): Tumbler
    requires n >= 1
    requires m >= 1
    ensures |OrdinalDisplacement(n, m).components| == m
    ensures OrdinalDisplacement(n, m).components[m - 1] == n
    ensures forall i :: 0 <= i < m - 1 ==> OrdinalDisplacement(n, m).components[i] == 0
  {
    Tumbler(seq(m - 1, _ => 0) + [n])
  }
}

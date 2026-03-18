include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module OnlyRegistryModified {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Bop (FRAME) — OnlyRegistryModified: Only Σ.B is modified;
  // all other state components are unchanged.

  // DIVERGENCE: The BaptismState used in RegistryGrowth has only field B,
  // making the frame trivially structural. This module models a richer
  // SystemState with an opaque rest component to give the frame condition
  // non-trivial content: baptize preserves rest.

  datatype SystemState<R(==)> = SystemState(B: set<Tumbler>, rest: R)

  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  ghost predicate InStream(t: Tumbler, p: Tumbler, d: nat) {
    d >= 1 &&
    |t.components| == |p.components| + d &&
    t.components[..|p.components|] == p.components &&
    (forall i :: |p.components| <= i < |p.components| + d - 1 ==> t.components[i] == 0) &&
    t.components[|t.components| - 1] >= 1
  }

  ghost function Children(B: set<Tumbler>, p: Tumbler, d: nat): set<Tumbler> {
    set t | t in B && InStream(t, p, d)
  }

  ghost function Next(B: set<Tumbler>, p: Tumbler, d: nat): Tumbler
    requires d >= 1
  {
    StreamElement(p, d, |Children(B, p, d)| + 1)
  }

  ghost predicate ValidBaptism(p: Tumbler, d: nat) {
    TumblerHierarchy.ValidAddress(p) &&
    1 <= d <= 2 &&
    TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
  }

  ghost predicate OnlyRegistryModified_p<R>(s: SystemState<R>, s': SystemState<R>) {
    s'.rest == s.rest
  }

  ghost function Baptize<R>(s: SystemState<R>, p: Tumbler, d: nat): (s': SystemState<R>)
    requires ValidBaptism(p, d)
    ensures OnlyRegistryModified_p(s, s')
    ensures s'.B == s.B + {Next(s.B, p, d)}
  {
    SystemState(s.B + {Next(s.B, p, d)}, s.rest)
  }
}

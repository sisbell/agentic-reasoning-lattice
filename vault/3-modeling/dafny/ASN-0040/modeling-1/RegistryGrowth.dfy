include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module RegistryGrowth {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Bop (POST) — RegistryGrowth: Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}

  datatype BaptismState = BaptismState(B: set<Tumbler>)

  // n-th element of sibling stream S(p, d), 1-indexed
  function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  // Membership in sibling stream S(p, d)
  ghost predicate InStream(t: Tumbler, p: Tumbler, d: nat) {
    d >= 1 &&
    |t.components| == |p.components| + d &&
    t.components[..|p.components|] == p.components &&
    (forall i :: |p.components| <= i < |p.components| + d - 1 ==> t.components[i] == 0) &&
    t.components[|t.components| - 1] >= 1
  }

  // children(B, p, d) = B ∩ S(p, d)
  ghost function Children(B: set<Tumbler>, p: Tumbler, d: nat): set<Tumbler> {
    set t | t in B && InStream(t, p, d)
  }

  // DIVERGENCE: The ASN defines next(B, p, d) as:
  //   if children = ∅ then inc(p, d) else inc(max(children), 0)
  // This model uses the B2-equivalent: next = StreamElement(p, d, |children|+1).
  // Equivalence holds when B1 (ContiguousPrefix) is satisfied.
  ghost function Next(B: set<Tumbler>, p: Tumbler, d: nat): Tumbler
    requires d >= 1
  {
    StreamElement(p, d, |Children(B, p, d)| + 1)
  }

  // B6 — valid baptism precondition
  ghost predicate ValidBaptism(p: Tumbler, d: nat) {
    TumblerHierarchy.ValidAddress(p) &&
    1 <= d <= 2 &&
    TumblerHierarchy.ZeroCount(p.components) + (d - 1) <= 3
  }

  // Bop (POST) — RegistryGrowth
  ghost predicate RegistryGrowth(s: BaptismState, s': BaptismState, p: Tumbler, d: nat)
    requires ValidBaptism(p, d)
  {
    s'.B == s.B + {Next(s.B, p, d)}
  }

  ghost function Baptize(s: BaptismState, p: Tumbler, d: nat): (s': BaptismState)
    requires ValidBaptism(p, d)
    ensures RegistryGrowth(s, s', p, d)
  {
    BaptismState(s.B + {Next(s.B, p, d)})
  }
}

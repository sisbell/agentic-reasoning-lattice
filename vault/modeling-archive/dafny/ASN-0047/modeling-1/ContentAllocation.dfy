include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// K.α — ContentAllocation (POST)
// C' = C ∪ {a ↦ v}, a fresh
module ContentAllocation {
  import opened TumblerAlgebra

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
  )

  // ---------------------------------------------------------------------------
  // K.α — ContentAllocation
  //
  // C' = C ∪ {a ↦ v} where a ∉ dom(C)
  // Frame: E' = E; (A d :: M'(d) = M(d)); R' = R
  // ---------------------------------------------------------------------------

  ghost predicate Post(s: State, s': State, a: Tumbler, v: nat) {
    a !in s.C &&
    s'.C == s.C[a := v] &&
    s'.E == s.E &&
    s'.M == s.M &&
    s'.R == s.R
  }

  // Allocated address maps to the given value
  lemma AllocationMapsCorrectly(s: State, s': State, a: Tumbler, v: nat)
    requires Post(s, s', a, v)
    ensures a in s'.C
    ensures s'.C[a] == v
  { }

  // Existing content preserved
  lemma AllocationPreservesExisting(s: State, s': State, a: Tumbler, v: nat, a2: Tumbler)
    requires Post(s, s', a, v)
    requires a2 in s.C
    ensures a2 in s'.C
    ensures s'.C[a2] == s.C[a2]
  { }

  // Domain grows by exactly {a}
  lemma AllocationExtendsDomain(s: State, s': State, a: Tumbler, v: nat)
    requires Post(s, s', a, v)
    ensures s'.C.Keys == s.C.Keys + {a}
  { }
}

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// J4 — ForkComposite
// Fork of d_src to d_new: K.δ ; K.μ⁺ ; K.ρ (and no other steps)
// Postconditions: dom(C') = dom(C), all ran(M'(d_new)) have provenance in R'
module ForkComposite {
  import opened TumblerAlgebra
  import TumblerHierarchy

  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
  )

  function GetArrangement(M: map<Tumbler, Arr>, d: Tumbler): Arr {
    if d in M then M[d] else map[]
  }

  ghost function ArrRange(m: Arr): set<Tumbler> {
    set v | v in m :: m[v]
  }

  // --- Step 1: K.δ creating d_new ---

  ghost predicate DeltaPost(s: State, s': State, dnew: Tumbler) {
    dnew !in s.E &&
    TumblerHierarchy.ValidAddress(dnew) &&
    TumblerHierarchy.DocumentAddress(dnew) &&
    s'.E == s.E + {dnew} &&
    s'.C == s.C &&
    s'.M == s.M &&
    s'.R == s.R
  }

  // --- Step 2: K.μ⁺ populating d_new from d_src ---

  ghost predicate MuPlusForkPost(s: State, s': State, dnew: Tumbler, dsrc: Tumbler) {
    dnew in s.E &&
    dsrc in s.E &&
    TumblerHierarchy.DocumentAddress(dnew) &&
    TumblerHierarchy.DocumentAddress(dsrc) &&
    ArrRange(GetArrangement(s'.M, dnew)) <= ArrRange(GetArrangement(s.M, dsrc)) &&
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d :: d != dnew ==> GetArrangement(s'.M, d) == GetArrangement(s.M, d))
  }

  // --- Step 3: K.ρ bulk provenance for d_new ---

  ghost predicate RhoBulkPost(s: State, s': State, dnew: Tumbler) {
    dnew in s.E &&
    TumblerHierarchy.DocumentAddress(dnew) &&
    (forall a :: a in ArrRange(GetArrangement(s.M, dnew)) ==> (a, dnew) in s'.R) &&
    s.R <= s'.R &&
    s'.C == s.C &&
    s'.E == s.E &&
    s'.M == s.M
  }

  // --- Fork precondition ---

  ghost predicate ForkPre(s: State, dsrc: Tumbler, dnew: Tumbler) {
    dsrc in s.E &&
    TumblerHierarchy.DocumentAddress(dsrc) &&
    GetArrangement(s.M, dsrc) != map[] &&
    dnew !in s.E &&
    TumblerHierarchy.ValidAddress(dnew) &&
    TumblerHierarchy.DocumentAddress(dnew) &&
    dsrc != dnew
  }

  // J4 — ForkComposite
  lemma ForkComposite(
    s0: State, s1: State, s2: State, s3: State,
    dsrc: Tumbler, dnew: Tumbler
  )
    requires ForkPre(s0, dsrc, dnew)
    requires DeltaPost(s0, s1, dnew)
    requires MuPlusForkPost(s1, s2, dnew, dsrc)
    requires RhoBulkPost(s2, s3, dnew)
    // dom(C') = dom(C) — none of K.δ, K.μ⁺, K.ρ modify C
    ensures s3.C == s0.C
    // (A a ∈ ran(M'(d_new)) :: (a, d_new) ∈ R')
    ensures forall a :: a in ArrRange(GetArrangement(s3.M, dnew)) ==> (a, dnew) in s3.R
  {
  }
}

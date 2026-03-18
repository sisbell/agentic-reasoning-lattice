include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ArrangementMutability {
  import opened TumblerAlgebra

  // P3 — ArrangementMutability
  //
  // Arrangements admit extension, contraction, and reordering.
  // C, E, R are monotonic; only M can shrink or be reordered.
  // Derived from P0 (ContentPermanence), P1 (EntityPermanence),
  // P2 (ProvenancePermanence).

  // Full state: P3 requires all four components to characterize
  // which are monotonic vs mutable.
  type Arr = map<Tumbler, Tumbler>

  datatype State = State(
    C: map<Tumbler, nat>,
    E: set<Tumbler>,
    M: map<Tumbler, Arr>,
    R: set<(Tumbler, Tumbler)>
  )

  function GetArr(s: State, d: Tumbler): Arr {
    if d in s.M then s.M[d] else map[]
  }

  // ---------------------------------------------------------------------------
  // Elementary transitions — effect + frame (ASN-0047 §K)
  // ---------------------------------------------------------------------------

  // K.α — content allocation: C grows; E, M, R in frame
  ghost predicate IsContentAlloc(s: State, s': State) {
    s.C.Keys < s'.C.Keys &&
    (forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]) &&
    s'.E == s.E &&
    s'.M == s.M &&
    s'.R == s.R
  }

  // K.δ — entity creation: E grows; C, M, R in frame
  ghost predicate IsEntityCreate(s: State, s': State) {
    s'.C == s.C &&
    (exists e: Tumbler :: e !in s.E && s'.E == s.E + {e}) &&
    s'.M == s.M &&
    s'.R == s.R
  }

  // K.μ⁺ — arrangement extension: one arrangement grows; C, E, R in frame
  ghost predicate IsArrExtension(s: State, s': State) {
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (exists d: Tumbler :: d in s.E &&
      GetArr(s, d).Keys < GetArr(s', d).Keys &&
      (forall v :: v in GetArr(s, d) ==>
        v in GetArr(s', d) && GetArr(s', d)[v] == GetArr(s, d)[v]) &&
      (forall d' :: d' != d ==> GetArr(s', d') == GetArr(s, d')))
  }

  // K.μ⁻ — arrangement contraction: one arrangement shrinks; C, E, R in frame
  ghost predicate IsArrContraction(s: State, s': State) {
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (exists d: Tumbler :: d in s.E &&
      GetArr(s', d).Keys < GetArr(s, d).Keys &&
      (forall v :: v in GetArr(s', d) ==>
        v in GetArr(s, d) && GetArr(s', d)[v] == GetArr(s, d)[v]) &&
      (forall d' :: d' != d ==> GetArr(s', d') == GetArr(s, d')))
  }

  // K.μ~ — arrangement reordering: one arrangement changed; C, E, R in frame
  // DIVERGENCE: The ASN specifies multiset preservation of I-addresses
  // under reordering (bijection π on V-positions). This model captures
  // only the frame conditions (C, E, R unchanged), which suffice for the
  // monotonicity claim. Full bijection modeling is out of scope for P3.
  ghost predicate IsArrReorder(s: State, s': State) {
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (exists d: Tumbler :: d in s.E &&
      GetArr(s, d) != GetArr(s', d) &&
      (forall d' :: d' != d ==> GetArr(s', d') == GetArr(s, d')))
  }

  // K.ρ — provenance recording: R grows; C, E, M in frame
  ghost predicate IsProvRecord(s: State, s': State) {
    s'.C == s.C &&
    s'.E == s.E &&
    s'.M == s.M &&
    (exists a: Tumbler, d: Tumbler ::
      s'.R == s.R + {(a, d)})
  }

  ghost predicate IsElementary(s: State, s': State) {
    IsContentAlloc(s, s') ||
    IsEntityCreate(s, s') ||
    IsArrExtension(s, s') ||
    IsArrContraction(s, s') ||
    IsArrReorder(s, s') ||
    IsProvRecord(s, s')
  }

  // ---------------------------------------------------------------------------
  // P3 — ArrangementMutability
  //
  // Under any elementary transition, C, E, R are monotonic.
  // Only arrangements (M) can shrink or be reordered.
  // ---------------------------------------------------------------------------

  lemma ArrangementMutability(s: State, s': State)
    requires IsElementary(s, s')
    ensures forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
    ensures s.E <= s'.E
    ensures s.R <= s'.R
  { }
}

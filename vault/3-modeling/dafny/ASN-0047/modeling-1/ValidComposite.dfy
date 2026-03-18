include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// Valid composite — ValidComposite (INV, predicate(State, State))
// A composite transition Σ → Σ' satisfies:
// (1) Each step Σᵢ → Σᵢ₊₁ is an elementary transition whose precondition
//     holds at Σᵢ.
// (2) Coupling constraints J0, J1, J1' hold between Σ and Σ'.
module ValidComposite {
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

  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  function RanM(s: State, d: Tumbler): set<Tumbler> {
    GetArrangement(s.M, d).Values
  }

  // ---------------------------------------------------------------------------
  // Elementary transitions
  //
  // DIVERGENCE: Elementary step predicates omit tumbler-level preconditions
  // (IsElement for K.α, parent(e) ∈ E for K.δ) that constrain which addresses
  // are valid operands. These are orthogonal to the coupling constraints and
  // are modeled in ContentAllocatable and EntityCreatable respectively.
  // ---------------------------------------------------------------------------

  // K.α — content allocation
  ghost predicate KAlphaStep(s: State, s': State, a: Tumbler, v: nat) {
    a !in s.C &&
    s'.C == s.C[a := v] &&
    s'.E == s.E &&
    s'.M == s.M &&
    s'.R == s.R
  }

  ghost predicate KAlpha(s: State, s': State) {
    exists a: Tumbler, v: nat :: KAlphaStep(s, s', a, v)
  }

  // K.δ — entity creation
  ghost predicate KDeltaStep(s: State, s': State, e: Tumbler) {
    e !in s.E &&
    TumblerHierarchy.ValidAddress(e) &&
    !TumblerHierarchy.ElementAddress(e) &&
    s'.E == s.E + {e} &&
    s'.C == s.C &&
    s'.M == s.M &&
    s'.R == s.R
  }

  ghost predicate KDelta(s: State, s': State) {
    exists e: Tumbler :: KDeltaStep(s, s', e)
  }

  // K.μ⁺ — arrangement extension
  ghost predicate KMuPlusStep(s: State, s': State, d: Tumbler) {
    d in E_doc(s) &&
    GetArrangement(s.M, d).Keys < GetArrangement(s'.M, d).Keys &&
    (forall v :: v in GetArrangement(s.M, d) ==>
      v in GetArrangement(s'.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]) &&
    (forall v :: v in GetArrangement(s'.M, d).Keys - GetArrangement(s.M, d).Keys ==>
      GetArrangement(s'.M, d)[v] in s.C) &&
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  ghost predicate KMuPlus(s: State, s': State) {
    exists d: Tumbler :: KMuPlusStep(s, s', d)
  }

  // K.μ⁻ — arrangement contraction
  ghost predicate KMuMinusStep(s: State, s': State, d: Tumbler) {
    d in E_doc(s) &&
    GetArrangement(s'.M, d).Keys < GetArrangement(s.M, d).Keys &&
    (forall v :: v in GetArrangement(s'.M, d) ==>
      v in GetArrangement(s.M, d) &&
      GetArrangement(s'.M, d)[v] == GetArrangement(s.M, d)[v]) &&
    s'.C == s.C &&
    s'.E == s.E &&
    s'.R == s.R &&
    (forall d' :: d' != d ==> GetArrangement(s'.M, d') == GetArrangement(s.M, d'))
  }

  ghost predicate KMuMinus(s: State, s': State) {
    exists d: Tumbler :: KMuMinusStep(s, s', d)
  }

  // K.ρ — provenance recording
  ghost predicate KRhoStep(s: State, s': State, a: Tumbler, d: Tumbler) {
    a in s.C &&
    d in E_doc(s) &&
    s'.R == s.R + {(a, d)} &&
    s'.C == s.C &&
    s'.E == s.E &&
    s'.M == s.M
  }

  ghost predicate KRho(s: State, s': State) {
    exists a: Tumbler, d: Tumbler :: KRhoStep(s, s', a, d)
  }

  // One elementary step (disjunction of all transition kinds)
  ghost predicate Step(s: State, s': State) {
    KAlpha(s, s') || KDelta(s, s') || KMuPlus(s, s') ||
    KMuMinus(s, s') || KRho(s, s')
  }

  // Valid trace: sequence of states where consecutive pairs are elementary steps
  ghost predicate ValidTrace(trace: seq<State>) {
    |trace| >= 1 &&
    forall i :: 0 <= i < |trace| - 1 ==> Step(trace[i], trace[i + 1])
  }

  // ---------------------------------------------------------------------------
  // Coupling constraints (between initial and final states)
  // ---------------------------------------------------------------------------

  // J0 — AllocationRequiresPlacement
  // Every freshly allocated I-address appears in some arrangement in the post-state
  ghost predicate J0(s: State, s': State) {
    forall a :: a in s'.C.Keys - s.C.Keys ==>
      exists d :: d in E_doc(s') && a in RanM(s', d)
  }

  // J1 — ExtensionRecordsProvenance
  // Every I-address freshly placed in a document's arrangement has provenance
  ghost predicate J1(s: State, s': State) {
    forall d :: d in E_doc(s') ==>
      forall a :: a in RanM(s', d) - RanM(s, d) ==>
        (a, d) in s'.R
  }

  // J1' — ProvenanceRequiresExtension
  // Every fresh provenance entry corresponds to a fresh arrangement placement
  ghost predicate J1Prime(s: State, s': State) {
    forall a, d :: d in E_doc(s') && (a, d) in s'.R - s.R ==>
      a in RanM(s', d) - RanM(s, d)
  }

  // ---------------------------------------------------------------------------
  // ValidComposite
  //
  // A composite transition Σ → Σ' is valid iff it decomposes into a finite
  // sequence of elementary steps (condition 1), and the coupling constraints
  // J0, J1, J1' hold between the endpoints (condition 2).
  // ---------------------------------------------------------------------------

  ghost predicate ValidComposite(s: State, s': State) {
    (exists trace: seq<State> ::
      ValidTrace(trace) &&
      trace[0] == s &&
      trace[|trace| - 1] == s') &&
    J0(s, s') &&
    J1(s, s') &&
    J1Prime(s, s')
  }
}

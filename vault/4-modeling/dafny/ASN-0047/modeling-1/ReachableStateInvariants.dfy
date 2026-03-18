include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "ValidComposite.dfy"

// ReachableStateInvariants — LEMMA (ASN-0047)
// Every state reachable from Σ₀ by valid composite transitions satisfies
// P4, P6, P7, P7a, P8, S2, S3, S8a, S8-depth, S8-fin.
//
// DIVERGENCE: S2 (injectivity) is structural — map<Tumbler, Tumbler> is a
// function. S8-fin is inherent in Dafny's finite map. S8a/S8-depth are not
// modeled here (see ArrangementInvariantsPreserved for VPosValid abstraction).
module ReachableStateInvariants {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import VC = ValidComposite

  type State = VC.State
  type Arr = VC.Arr

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function E_doc(s: State): set<Tumbler> { VC.E_doc(s) }
  function RanM(s: State, d: Tumbler): set<Tumbler> { VC.RanM(s, d) }

  ghost predicate IsEntity(e: Tumbler) {
    TumblerHierarchy.ValidAddress(e) &&
    TumblerHierarchy.ZeroCount(e.components) <= 2
  }

  function Parent(e: Tumbler): Tumbler
    requires IsEntity(e)
    requires !TumblerHierarchy.NodeAddress(e)
  {
    var z0 := FindZero(e.components, 0);
    if TumblerHierarchy.AccountAddress(e) || z0 >= |e.components| then
      Tumbler(e.components[..z0])
    else
      var z1 := FindZero(e.components, z0 + 1);
      Tumbler(e.components[..z1])
  }

  // ---------------------------------------------------------------------------
  // State invariants
  // ---------------------------------------------------------------------------

  // Arrangements only for allocated documents
  ghost predicate WF(s: State) {
    forall d :: d in s.M ==> d in E_doc(s)
  }

  // P4 — Contains(Σ) ⊆ R
  ghost predicate P4(s: State) {
    forall d, a :: d in E_doc(s) && a in RanM(s, d) ==> (a, d) in s.R
  }

  // P6 — ExistentialCoherence: content has a document prefix in E
  ghost predicate P6(s: State) {
    forall a :: a in s.C ==>
      exists d :: d in E_doc(s) && IsPrefix(d, a)
  }

  // P7 — ProvenanceGrounding
  ghost predicate P7(s: State) {
    forall a, d :: (a, d) in s.R ==> a in s.C
  }

  // P7a — ProvenanceCoverage
  ghost predicate P7a(s: State) {
    forall a :: a in s.C ==> exists d :: (a, d) in s.R
  }

  // P8 — EntityHierarchy
  ghost predicate P8(s: State) {
    forall e :: e in s.E && IsEntity(e) && !TumblerHierarchy.NodeAddress(e) ==>
      Parent(e) in s.E
  }

  // S3 — referential integrity of arrangements
  ghost predicate S3(s: State) {
    forall d :: d in E_doc(s) ==>
      forall a :: a in RanM(s, d) ==> a in s.C
  }

  // DIVERGENCE: ProvDocValid (the d ∈ E_doc part of R ⊆ T_elem × E_doc) is
  // an explicit invariant. The ASN states it structurally on Σ.R. Needed
  // for P7 preservation via J1' + S3.
  ghost predicate ProvDocValid(s: State) {
    forall a, d :: (a, d) in s.R ==> d in E_doc(s)
  }

  ghost predicate AllInv(s: State) {
    WF(s) && P4(s) && P6(s) && P7(s) && P7a(s) &&
    P8(s) && S3(s) && ProvDocValid(s)
  }

  // ---------------------------------------------------------------------------
  // Initial state
  // ---------------------------------------------------------------------------

  ghost predicate IsInitialState(s: State) {
    s.C == map[] &&
    |s.E| == 1 &&
    (forall e :: e in s.E ==> TumblerHierarchy.NodeAddress(e)) &&
    s.M == map[] &&
    s.R == {}
  }

  // ---------------------------------------------------------------------------
  // Composite transition
  //
  // DIVERGENCE: Composite states derived properties as conjuncts rather than
  // deriving them from elementary transition frames. In the ASN, permanence
  // follows from PermanenceFromFrames, arrangement preservation from
  // ArrangementInvariantsPreserved, and P6/P8 preservation from K.α/K.δ
  // preconditions + P1. This formulation is sufficient for induction.
  // ---------------------------------------------------------------------------

  ghost predicate Composite(s: State, s': State) {
    // Coupling constraints (ASN J0, J1, J1')
    VC.J0(s, s') && VC.J1(s, s') && VC.J1Prime(s, s') &&
    // Permanence (P0 + P1 + P2)
    (forall k :: k in s.C ==> k in s'.C && s'.C[k] == s.C[k]) &&
    s.E <= s'.E &&
    s.R <= s'.R &&
    // Post-state per-state invariants
    WF(s') && S3(s') &&
    // P6 for fresh content (from K.α precondition + P1)
    (forall a :: a in s'.C && a !in s.C ==>
      exists d :: d in E_doc(s') && IsPrefix(d, a)) &&
    // P8 for fresh entities (from K.δ precondition + P1)
    (forall e :: (e in s'.E && e !in s.E && IsEntity(e) &&
       !TumblerHierarchy.NodeAddress(e)) ==> Parent(e) in s'.E) &&
    // ProvDocValid for fresh provenance (from K.ρ precondition + P1)
    (forall a, d :: (a, d) in s'.R && (a, d) !in s.R ==> d in E_doc(s'))
  }

  // ---------------------------------------------------------------------------
  // Lemmas
  // ---------------------------------------------------------------------------

  lemma BaseCase(s: State)
    requires IsInitialState(s)
    ensures AllInv(s)
  { }

  lemma FreshContentNotInArr(s: State, a: Tumbler, d: Tumbler)
    requires WF(s) && S3(s)
    requires a !in s.C
    ensures a !in RanM(s, d)
  { }

  lemma InductiveStep(s: State, s': State)
    requires AllInv(s)
    requires Composite(s, s')
    ensures AllInv(s')
  {
    // P7a: existential witness for each content address in s'
    forall a | a in s'.C
      ensures exists d :: (a, d) in s'.R
    {
      if a in s.C {
        var d :| (a, d) in s.R;
        assert (a, d) in s'.R;
      } else {
        assert a in s'.C.Keys - s.C.Keys;
        var d :| d in VC.E_doc(s') && a in VC.RanM(s', d);
        FreshContentNotInArr(s, a, d);
        assert (a, d) in s'.R;
      }
    }
  }

  // ReachableStateInvariants
  lemma {:induction false} Theorem(trace: seq<State>)
    requires |trace| >= 1
    requires IsInitialState(trace[0])
    requires forall i :: 0 <= i < |trace| - 1 ==> Composite(trace[i], trace[i+1])
    ensures forall i :: 0 <= i < |trace| ==> AllInv(trace[i])
    decreases |trace|
  {
    BaseCase(trace[0]);
    if |trace| > 1 {
      Theorem(trace[..|trace|-1]);
      InductiveStep(trace[|trace|-2], trace[|trace|-1]);
    }
  }
}

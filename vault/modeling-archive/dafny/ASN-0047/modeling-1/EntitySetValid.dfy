include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module EntitySetValid {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection for entity set property
  datatype State = State(E: set<Tumbler>)

  // ---------------------------------------------------------------------------
  // Σ.E — EntitySetValid
  //
  // E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}
  // (A e ∈ E :: ¬IsElement(e))
  // ---------------------------------------------------------------------------

  ghost predicate EntitySetValid(s: State) {
    forall e :: e in s.E ==>
      TumblerHierarchy.ValidAddress(e) &&
      !TumblerHierarchy.ElementAddress(e)
  }

  // Level strata
  function E_node(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.NodeAddress(e)
  }

  function E_account(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.AccountAddress(e)
  }

  function E_doc(s: State): set<Tumbler> {
    set e | e in s.E && TumblerHierarchy.DocumentAddress(e)
  }

  // Partition: the three strata cover E and are pairwise disjoint
  lemma StrataPartition(s: State)
    requires EntitySetValid(s)
    ensures E_node(s) + E_account(s) + E_doc(s) == s.E
    ensures E_node(s) !! E_account(s)
    ensures E_node(s) !! E_doc(s)
    ensures E_account(s) !! E_doc(s)
  { }
}

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressAllocation/HierarchicalParsing.dfy"
include "../../../../proofs/DocumentOntology/DocumentOntology.dfy"

module EmptyCreationModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened HierarchicalParsing
  import opened DocumentOntology

  // --- Helpers ---

  // AccountAddr = {a ∈ T : zeros(a) = 1}
  predicate ValidAccountAddr(t: Tumbler) {
    CountZeros(t.components) == 1
  }

  // parent(d) undefined in the given document set
  ghost predicate ParentUndefined(d: Tumbler, docs: set<DocId>) {
    forall d' :: d' in docs ==> !DocLevelPrefix(d', d)
  }

  // --- D0 — EmptyCreation (POST, ensures) ---
  // Create a fresh empty private document under account a.
  // The existential scopes over both postcondition and frame.
  ghost predicate EmptyCreationSpec(s: DocState, s': DocState, a: Tumbler) {
    // pre: a ∈ AccountAddr ∧ actor(op) = a
    // (actor(op) = a is implicit: a is the requesting account)
    ValidAccountAddr(a) &&
    // post ∧ frame
    (exists d: DocId ::
      // (E d : d ∉ Σ.D ∧ d ∈ Σ'.D ∧ account(d) = a : ...)
      d !in s.base.docs && d in s'.base.docs &&
      ValidDocAddr(d) &&
      HasAccountLevel(d) && AccountPrefix(d) == a &&
      // |Σ'.V(d)| = 0
      d in s'.base.vmap && s'.base.vmap[d].Keys == {} &&
      // Σ'.pub(d) = private
      d in s'.pub && s'.pub[d] == Private &&
      // parent(d) undefined
      ParentUndefined(d, s'.base.docs) &&
      // (A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)
      (forall d' :: (d' in s.base.docs &&
        HasAccountLevel(d') && AccountPrefix(d') == a) ==>
        LessThan(d', d)) &&
      // Σ'.D = Σ.D ∪ {d}
      s'.base.docs == s.base.docs + {d} &&
      // Σ'.I = Σ.I
      s'.base.iota == s.base.iota &&
      // (A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d'))
      (forall d' :: (d' in s.base.docs && d' in s.base.vmap && d' in s.pub) ==>
        d' in s'.base.vmap && s'.base.vmap[d'] == s.base.vmap[d'] &&
        d' in s'.pub && s'.pub[d'] == s.pub[d']))
  }
}

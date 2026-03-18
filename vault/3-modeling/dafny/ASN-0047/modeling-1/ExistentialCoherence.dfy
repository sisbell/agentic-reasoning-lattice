include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// P6 — ExistentialCoherence
// (A a ∈ dom(C) :: origin(a) ∈ E_doc)
// Derived from ContentAllocatable, P0, P1
module ExistentialCoherence {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection: content domain and entity set
  datatype State = State(
    C: set<Tumbler>,       // dom(C) — allocated content addresses
    E: set<Tumbler>        // E — allocated entity addresses
  )

  // ---------------------------------------------------------------------------
  // P6 — ExistentialCoherence
  //
  // (A a ∈ dom(C) :: origin(a) ∈ E_doc)
  //
  // Every content address has an origin document that is an allocated entity.
  // origin(a) is the document-level prefix of element address a — structural,
  // not mutable state — so we express it existentially (consistent with
  // ContentAllocatable).
  // ---------------------------------------------------------------------------

  ghost predicate ExistentialCoherenceInv(s: State) {
    forall a :: a in s.C ==>
      exists d :: d in s.E && TumblerHierarchy.DocumentAddress(d) && IsPrefix(d, a)
  }

  // Base case: Σ₀ has dom(C₀) = ∅
  lemma ExistentialCoherence_Base(s: State)
    requires s.C == {}
    ensures ExistentialCoherenceInv(s)
  { }

  // Inductive step: K.α preserves P6
  // ContentAllocatable requires origin(a) ∈ E_doc; P1 preserves entity membership
  lemma ExistentialCoherence_Alloc(s: State, s': State, a: Tumbler, d: Tumbler)
    requires ExistentialCoherenceInv(s)
    // ContentAllocatable
    requires d in s.E && TumblerHierarchy.DocumentAddress(d) && IsPrefix(d, a)
    // K.α postcondition
    requires s'.C == s.C + {a}
    // P1 — EntityPermanence
    requires s.E <= s'.E
    ensures ExistentialCoherenceInv(s')
  { }

  // Frame: transitions not modifying content preserve P6
  // P0 (ContentPermanence) holds content stable; P1 preserves entities
  lemma ExistentialCoherence_Frame(s: State, s': State)
    requires ExistentialCoherenceInv(s)
    requires s'.C == s.C
    requires s.E <= s'.E
    ensures ExistentialCoherenceInv(s')
  { }
}

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressAllocation/HierarchicalParsing.dfy"

module EmptyCreationModule {
  import opened TumblerAlgebra
  import opened Foundation
  import HierarchicalParsing

  // --- Helpers ---

  // Publication status per ASN-0029 Σ.pub
  datatype PubStatus = Private | Published | Privashed

  // DIVERGENCE: Foundation.State lacks Σ.pub (publication status).
  // DocState extends Foundation's State with a pub map.
  datatype DocState = DocState(
    base: State,
    pub: map<DocId, PubStatus>
  )

  // AccountAddr = {a ∈ T : zeros(a) = 1}
  predicate ValidAccountAddr(t: Tumbler) {
    HierarchicalParsing.CountZeros(t.components) == 1
  }

  // Document address: zeros(d) = 2
  predicate ValidDocAddr(d: Tumbler) {
    HierarchicalParsing.CountZeros(d.components) == 2
  }

  // Find position of first zero starting from index i
  function FirstZeroFrom(s: seq<nat>, i: nat): nat
    requires i <= |s|
    requires exists j :: i <= j < |s| && s[j] == 0
    ensures i <= FirstZeroFrom(s, i) < |s|
    ensures s[FirstZeroFrom(s, i)] == 0
    ensures forall j :: i <= j < FirstZeroFrom(s, i) ==> s[j] != 0
    decreases |s| - i
  {
    if s[i] == 0 then i
    else FirstZeroFrom(s, i + 1)
  }

  // d has at least one zero separator with a component after it
  predicate HasAccountLevel(d: Tumbler) {
    (exists j :: 0 <= j < |d.components| && d.components[j] == 0) &&
    FirstZeroFrom(d.components, 0) + 1 < |d.components|
  }

  // account(d): extract the account prefix (through component after first zero)
  function AccountPrefix(d: DocId): Tumbler
    requires HasAccountLevel(d)
  {
    var z := FirstZeroFrom(d.components, 0);
    Tumbler(d.components[..z+2])
  }

  // Document-level prefix: d_s ≺ d_v
  ghost predicate DocLevelPrefix(ds: Tumbler, dv: Tumbler) {
    IsPrefix(ds, dv) && ds != dv &&
    ValidDocAddr(ds) && ValidDocAddr(dv)
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

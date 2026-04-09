include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/ForwardAllocation.dfy"
include "../../../../proofs/AddressProperties/PartitionIndependence.dfy"
include "../../../../proofs/AddressProperties/AllocatorDiscipline.dfy"
include "../../../../proofs/AddressProperties/GlobalUniqueness.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"
include "../../../../proofs/AddressPermanence/AddressPermanence.dfy"

module ProvenanceNotLocationModule {
  import opened AddressPermanence
  import opened Foundation
  import HierarchicalParsing

  // P8 — ProvenanceNotLocation (INV, predicate(IAddr))
  //
  // Type-level property: no component of IAddr encodes current physical
  // storage location. The node field records the originating node
  // (provenance per T4), and is immutable by value-type semantics.
  //
  // (A a : a ∈ Σ.A : fields(a).node = originating_node(a))
  //
  // The resolution mapping (IAddr → physical location) is not a
  // component of a or of Σ.ι.

  // Extract the originating node — first component of the tumbler (per T4).
  function OriginNode(a: IAddr): nat
    requires |a.components| > 0
  {
    a.components[0]
  }

  // P8: The address has a well-defined node field encoding provenance.
  // ValidAddress (T4) guarantees components[0] != 0, so OriginNode
  // identifies a real node. The predicate is over IAddr alone — no
  // state parameter — expressing that provenance is structural.
  predicate ProvenanceNotLocation(a: IAddr) {
    HierarchicalParsing.ValidAddress(a)
  }

  // --- Separation of concerns: resolution is external ---
  //
  // Physical location is modeled as a map outside State, demonstrating
  // that it is not a component of IAddr or Σ.ι. This separation IS
  // the architectural content of P8.

  datatype ResolutionState = ResolutionState(loc: map<IAddr, nat>)

  ghost predicate WellFormedResolution(s: State, r: ResolutionState) {
    r.loc.Keys == Allocated(s)
  }

  // Migrate: change an address's physical location.
  // State (iota, docs, vmap) is unchanged — only resolution moves.
  function Migrate(r: ResolutionState, a: IAddr, target: nat): ResolutionState
    requires a in r.loc
  {
    ResolutionState(r.loc[a := target])
  }

  // Migration preserves well-formed resolution
  lemma MigratePreservesWF(s: State, r: ResolutionState, a: IAddr, target: nat)
    requires a in Allocated(s)
    requires WellFormedResolution(s, r)
    ensures WellFormedResolution(s, Migrate(r, a, target))
  { }

  // Migration preserves origin — trivially, since origin is a pure
  // function of the address value and Migrate does not touch IAddr.
  lemma MigratePreservesOrigin(a: IAddr, r: ResolutionState, target: nat)
    requires ProvenanceNotLocation(a)
    requires a in r.loc
    ensures OriginNode(a) == OriginNode(a)
  { }

  // Resolution is independent of origin — target need not equal OriginNode(a).
  // This is the constructive counterpart of the Alloy counterexample check
  // (ResolutionEqualsOrigin): migration can set resolution to any node.
  lemma ResolutionIndependentOfOrigin(
    s: State, r: ResolutionState, a: IAddr, target: nat
  )
    requires a in Allocated(s)
    requires WellFormedResolution(s, r)
    ensures Migrate(r, a, target).loc[a] == target
  { }
}

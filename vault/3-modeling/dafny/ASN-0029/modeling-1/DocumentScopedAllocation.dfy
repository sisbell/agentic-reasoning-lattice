include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"

module DocumentScopedAllocationModule {
  import opened TumblerAlgebra
  import opened Foundation
  import HierarchicalParsing

  // ASN-0029 D7a — DocumentScopedAllocation (POST, ensures)
  // INSERT on document d allocates fresh I-addresses under d's tumbler prefix.
  // (A a ∈ fresh : d ≼ a ∧ a_{#d+1} = 0 ∧ zeros(a) = 3)
  // Each fresh address has the form d.0.E₁...Eδ with all Eᵢ > 0 and δ ≥ 1.

  ghost predicate DocumentScopedAllocation(d: DocId, freshAddrs: set<IAddr>) {
    forall a :: a in freshAddrs ==>
      // d ≼ a
      IsPrefix(d, a) &&
      // a strictly extends d by at least separator + one element component
      |a.components| > |d.components| + 1 &&
      // element-field separator immediately follows d
      a.components[|d.components|] == 0 &&
      // exactly three zero separators (element address)
      HierarchicalParsing.CountZeros(a.components) == 3 &&
      // all element-field components are positive (Eᵢ > 0)
      (forall i :: |d.components| + 1 <= i < |a.components| ==>
        a.components[i] > 0)
  }
}

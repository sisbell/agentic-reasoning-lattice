include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/SubspaceDisjointness.dfy"

module OriginTraceabilityModule {
  import opened TumblerAlgebra
  import opened Foundation
  import SubspaceDisjointness

  // ASN-0029 D7 — OriginTraceability (INV, function(IAddr): DocId)
  // home(a) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ a}
  // The unique maximal document-level prefix of an I-address.
  // For address N.0.U.0.D₁...Dₖ.0.E₁...Eₘ, extracts Tumbler([N, 0, U, 0, D₁...Dₖ]).

  // Address has at least 2 zero separators (document level or below)
  predicate HasDocLevel(a: IAddr) {
    SubspaceDisjointness.HasKZeros(a.components, 2, 0)
  }

  // home: extract the maximal document-level prefix
  function Home(a: IAddr): DocId
    requires HasDocLevel(a)
  {
    if !SubspaceDisjointness.HasKZeros(a.components, 3, 0) then
      // a has exactly 2 zeros — it IS a document address
      a
    else
      // a has 3+ zeros — document prefix is everything before the 3rd zero
      var pos := SubspaceDisjointness.KthZero(a.components, 3, 0);
      Tumbler(a.components[..pos])
  }
}

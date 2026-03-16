include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// O5 — SubdivisionAuthority
module SubdivisionAuthority {
  import opened TumblerAlgebra

  datatype Principal = Principal(id: nat)

  datatype OwnershipState = OwnershipState(
    alloc: set<Tumbler>,
    principals: set<Principal>,
    pfx: map<Principal, Tumbler>
  )

  // O5 — SubdivisionAuthority
  // DIVERGENCE: allocated_by is modeled as an explicit allocator map
  // (Tumbler → Principal) rather than embedded in State, since the ASN
  // defines allocated_by_{Σ'} as transition-specific metadata not derivable
  // from states alone. The map assumes at most one allocator per newly
  // allocated address, consistent with O5's most-specific requirement and
  // O1b (prefix injectivity).
  ghost predicate SubdivisionAuthority(
    s: OwnershipState,
    s': OwnershipState,
    allocator: map<Tumbler, Principal>
  ) {
    forall a :: a in s'.alloc && a !in s.alloc && a in allocator ==>
      var pi := allocator[a];
      pi in s.principals && pi in s.pfx &&
      IsPrefix(s.pfx[pi], a) &&
      (forall pi' :: pi' in s.principals && pi' in s.pfx && IsPrefix(s.pfx[pi'], a)
        ==> |s.pfx[pi'].components| <= |s.pfx[pi].components|)
  }
}

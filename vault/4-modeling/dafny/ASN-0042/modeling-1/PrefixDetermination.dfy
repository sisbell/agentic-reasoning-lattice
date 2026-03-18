include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// O1 — PrefixDetermination
// owns(π, a) ≡ pfx(π) ≼ a
module PrefixDetermination {
  import opened TumblerAlgebra

  // Principal identity — distinguished by ownership prefix
  datatype Principal = Principal(prefix: Tumbler)

  // O1: Ownership is prefix containment
  ghost predicate Owns(pi: Principal, a: Tumbler) {
    IsPrefix(pi.prefix, a)
  }
}

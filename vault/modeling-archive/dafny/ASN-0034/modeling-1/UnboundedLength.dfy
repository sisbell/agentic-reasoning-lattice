include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module UnboundedLength {

  import opened TumblerAlgebra

  // T0(b) — UnboundedLength
  // (A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))

  // Constructive witness: build a tumbler of exactly length n
  function TumblerOfLength(n: nat): Tumbler
    requires n >= 1
    ensures |TumblerOfLength(n).components| == n
  {
    Tumbler(seq(n, _ => 1))
  }

  // The tumbler type imposes no upper bound on sequence length
  lemma UnboundedLength(n: nat)
    requires n >= 1
    ensures exists t: Tumbler :: |t.components| >= n
  {
    var t := TumblerOfLength(n);
  }
}

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module StreamExtendsParent {
  import opened TumblerAlgebra

  // S1 — StreamExtendsParent
  // (A n : n >= 1 : p ≼ cₙ) — every stream element extends p as a prefix.
  // Derived from TA5(b): closed form cₙ = [p₁,...,p_{#p}, 0^{d-1}, n].

  ghost function StreamElement(p: Tumbler, d: nat, n: nat): Tumbler
    requires d >= 1
    requires n >= 1
  {
    Tumbler(p.components + Zeros(d - 1) + [n])
  }

  lemma StreamExtendsParent(p: Tumbler, d: nat, n: nat)
    requires d >= 1
    requires n >= 1
    ensures IsPrefix(p, StreamElement(p, d, n))
  { }
}

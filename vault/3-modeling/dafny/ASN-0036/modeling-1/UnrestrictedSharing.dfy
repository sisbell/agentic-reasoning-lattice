include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module UnrestrictedSharing {
  import opened TumblerAlgebra

  // S5 — UnrestrictedSharing

  // Opaque content value type
  type Val(==)

  // Two-space state (content store + arrangements)
  datatype State = State(C: map<Tumbler, Val>, M: map<Tumbler, map<Tumbler, Tumbler>>)

  // S3 — ReferentialIntegrity
  ghost predicate ReferentialIntegrity(s: State) {
    forall d, v :: d in s.M && v in s.M[d] ==> s.M[d][v] in s.C
  }

  // Build arrangement: n V-positions Tumbler([1]) .. Tumbler([n]) all mapping to a
  function WitnessArrangement(a: Tumbler, n: nat): map<Tumbler, Tumbler>
    ensures forall k :: 1 <= k <= n ==> Tumbler([k]) in WitnessArrangement(a, n)
    ensures forall v :: v in WitnessArrangement(a, n) ==>
              WitnessArrangement(a, n)[v] == a
  {
    if n == 0 then map[]
    else WitnessArrangement(a, n - 1)[Tumbler([n]) := a]
  }

  // S5 — For any N, there exists a state satisfying S0–S3 where some
  // I-address is shared by more than N V-positions.
  //
  // S0/S1 (transition invariants) constrain state pairs — any single state
  // is trivially consistent. S2 holds by construction (maps are functions).
  // S3 (ReferentialIntegrity) is verified for the witness.
  //
  // Witness: C = {a ↦ w}, M = {d ↦ {v₁ ↦ a, ..., v_{N+1} ↦ a}}.
  lemma UnrestrictedSharingLemma(N: nat, w: Val)
    ensures var a := Tumbler([1]);
            var d := Tumbler([1]);
            var arr := WitnessArrangement(a, N + 1);
            var s := State(map[a := w], map[d := arr]);
            ReferentialIntegrity(s) &&
            a in s.C &&
            d in s.M &&
            (forall k :: 1 <= k <= N + 1 ==>
              Tumbler([k]) in s.M[d] && s.M[d][Tumbler([k])] == a) &&
            (forall k1, k2 :: 1 <= k1 < k2 <= N + 1 ==>
              Tumbler([k1]) != Tumbler([k2]))
  { }
}

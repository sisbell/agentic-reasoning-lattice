// ASN-0034: TA7a — SubspaceClosure
// Defines the subspace S of ordinals with all positive components:
//   S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.
// Matches T4's positive-component constraint on element fields.
include "./CarrierSetDefinition.dfy"

module SubspaceClosure {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  ghost predicate InSubspaceS(o: Tumbler)
    requires InT(o)
  {
    forall i :: 1 <= i <= Length(o) ==> Component(o, i) > 0
  }

  ghost function SubspaceS(): iset<Tumbler>
  {
    iset o | InT(o) && InSubspaceS(o)
  }
}

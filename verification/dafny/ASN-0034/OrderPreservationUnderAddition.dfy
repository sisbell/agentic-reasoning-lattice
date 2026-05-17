// ASN-0034: TA1 — OrderPreservationUnderAddition
// (A a, b, w : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b :
//   a ⊕ w ≤ b ⊕ w).
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./CanonicalRepresentation.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatAdditionOrderAndSuccessor.dfy"
include "./NatAdditionCancellation.dfy"

module OrderPreservationUnderAddition {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened WellDefinedAddition
  import opened CanonicalRepresentation
  import opened NatStrictTotalOrder
  import opened NatAdditionOrderAndSuccessor
  import opened NatAdditionCancellation
  import opened NatCarrierSet

  // Constructive extraction of the LexicographicOrder witness as a returned
  // ghost value. Wrapping the :| in a small helper sidesteps the issue where
  // the solver cannot establish the existential when the enclosing lemma has
  // a complex existential conclusion of its own.
  lemma LexWitness(a: Tumbler, b: Tumbler) returns (k: nat)
    requires InT(a) && InT(b)
    requires LexicographicOrder.LexicographicOrder(a, b)
    ensures 1 <= k
    ensures forall i :: 1 <= i < k ==>
              i <= Length(a) && i <= Length(b) &&
              Component(a, i) == Component(b, i)
    ensures (k <= Length(a) && k <= Length(b)
             && Less(Component(a, k), Component(b, k)))
            || (k == Length(a) + 1 && k <= Length(b))
  {
    k :| 1 <= k
         && (forall i :: 1 <= i < k ==>
               i <= Length(a) && i <= Length(b) &&
               Component(a, i) == Component(b, i))
         && ((k <= Length(a) && k <= Length(b)
              && Less(Component(a, k), Component(b, k)))
             || (k == Length(a) + 1 && k <= Length(b)));
  }

  lemma OrderPreservationUnderAddition(a: Tumbler, b: Tumbler, w: Tumbler)
    requires InT(a) && InT(b) && InT(w)
    requires LexicographicOrder.LexicographicOrder(a, b)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    requires ActionPoint.ActionPoint(w) <= Length(b)
    ensures
      var r1 := TumblerAdd.TumblerAdd(a, w);
      var r2 := TumblerAdd.TumblerAdd(b, w);
      LexicographicOrder.LexicographicOrder(r1, r2) || r1 == r2
  {
    var j := LexWitness(a, b);

    var r1 := TumblerAdd.TumblerAdd(a, w);
    var r2 := TumblerAdd.TumblerAdd(b, w);
    var k := ActionPoint.ActionPoint(w);

    if j <= Length(a) && j <= Length(b)
       && Less(Component(a, j), Component(b, j)) {
      // Case (i): components first diverge at j with Less(a_j, b_j).
      if j < k {
        // Witness j for LexicographicOrder(r1, r2).
        assert j < k <= Length(w);
        assert Component(r1, j) == Component(a, j);
        assert Component(r2, j) == Component(b, j);
        forall i | 1 <= i < j
          ensures i <= Length(r1) && i <= Length(r2)
                  && Component(r1, i) == Component(r2, i)
        {
          assert i < k;
        }
      } else if j == k {
        // Witness k. Less(a_k + w_k, b_k + w_k) from Less(a_k, b_k) on nat.
        assert Component(r1, k) == Component(a, k) + Component(w, k);
        assert Component(r2, k) == Component(b, k) + Component(w, k);
        assert Less(Component(r1, k), Component(r2, k));
        forall i | 1 <= i < k
          ensures i <= Length(r1) && i <= Length(r2)
                  && Component(r1, i) == Component(r2, i)
        {
        }
      } else {
        // j > k: r1 and r2 coincide componentwise on [1, #w].
        forall i | 1 <= i <= Length(w)
          ensures Component(r1, i) == Component(r2, i)
        {
          if i < k {
            assert i < k < j;
          } else if i == k {
            assert k < j;
          } else {
            assert k < i <= Length(w);
          }
        }
        CanonicalRepresentation.CanonicalRepresentation(r1, r2);
      }
    } else {
      // Case (ii): j == #a + 1 ≤ #b. Components agree on [1, #a]; k ≤ #a < j.
      assert j == Length(a) + 1 && j <= Length(b);
      forall i | 1 <= i <= Length(w)
        ensures Component(r1, i) == Component(r2, i)
      {
        if i < k {
          assert i < k <= Length(a) < j;
        } else if i == k {
          assert k <= Length(a) < j;
        } else {
          assert k < i <= Length(w);
        }
      }
      CanonicalRepresentation.CanonicalRepresentation(r1, r2);
    }
  }
}

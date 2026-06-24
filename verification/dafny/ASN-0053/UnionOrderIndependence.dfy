// ASN-0053: S10 — UnionOrderIndependence (theorem)
// normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)  (commutativity)
// normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))  (associativity)
include "./SpanDefs.dfy"
include "./NormalizationExistence.dfy"
include "./NormalizationUniqueness.dfy"

module UnionOrderIndependence {
  import opened SpanDefs
  import NE = NormalizationExistence
  import NU = NormalizationUniqueness

  // Bridge: NU.Denote agrees with NE.Denote (same body, different module contexts)
  lemma DenoteBridge(spans: seq<SpanEntry>)
    requires NE.AllValid(spans)
    ensures NU.AllValid(spans) && NU.Denote(spans) == NE.Denote(spans)
    decreases |spans|
  {
    if |spans| == 0 {
    } else {
      NE.AllValidTail(spans);
      DenoteBridge(spans[1..]);
    }
  }

  // Bridge: NE.StrictlyNormalized implies NU.StrictlyNormalized (same body)
  lemma StrictlyNormalizedBridge(spans: seq<SpanEntry>)
    requires NE.AllValid(spans) && NE.StrictlyNormalized(spans)
    ensures NU.AllValid(spans) && NU.StrictlyNormalized(spans)
  {
    DenoteBridge(spans);
  }

  // S10 (commutativity): normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)
  // Proof: equal denotations (iset union commutes) + S9 (uniqueness of normalized form)
  lemma UnionOrderIndependence(spans1: seq<SpanEntry>, spans2: seq<SpanEntry>)
    requires NE.AllValid(spans1) && NE.AllValid(spans2)
    requires NE.AllLevelUniform(spans1) && NE.AllLevelUniform(spans2)
    requires NE.MutuallyLevelCompatible(spans1 + spans2)
    ensures forall hat12: seq<SpanEntry>, hat21: seq<SpanEntry> ::
      (NE.AllValid(hat12) && NE.StrictlyNormalized(hat12) && NE.Denote(hat12) == NE.Denote(spans1 + spans2) &&
       NE.AllValid(hat21) && NE.StrictlyNormalized(hat21) && NE.Denote(hat21) == NE.Denote(spans2 + spans1)) ==>
      hat12 == hat21
  {
    NE.AllValidConcat(spans1, spans2);
    NE.AllValidConcat(spans2, spans1);
    NE.DenoteSameMultiset(spans1 + spans2, spans2 + spans1);
    forall hat12: seq<SpanEntry>, hat21: seq<SpanEntry>
      | NE.AllValid(hat12) && NE.StrictlyNormalized(hat12) && NE.Denote(hat12) == NE.Denote(spans1 + spans2) &&
        NE.AllValid(hat21) && NE.StrictlyNormalized(hat21) && NE.Denote(hat21) == NE.Denote(spans2 + spans1)
      ensures hat12 == hat21
    {
      DenoteBridge(hat12);
      DenoteBridge(hat21);
      StrictlyNormalizedBridge(hat12);
      StrictlyNormalizedBridge(hat21);
      assert NU.Denote(hat12) == NU.Denote(hat21);
      NU.NormalizationUniqueness(hat12, hat21);
    }
  }

  // S10 (associativity): normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))
  // Proof: seq concat is associative so denotations are equal, then S9 (uniqueness)
  lemma UnionAssociativity(spans1: seq<SpanEntry>, spans2: seq<SpanEntry>, spans3: seq<SpanEntry>)
    requires NE.AllValid(spans1) && NE.AllValid(spans2) && NE.AllValid(spans3)
    requires NE.AllLevelUniform(spans1) && NE.AllLevelUniform(spans2) && NE.AllLevelUniform(spans3)
    requires NE.MutuallyLevelCompatible(spans1 + spans2 + spans3)
    ensures forall hatL: seq<SpanEntry>, hatR: seq<SpanEntry> ::
      (NE.AllValid(hatL) && NE.StrictlyNormalized(hatL) && NE.Denote(hatL) == NE.Denote((spans1 + spans2) + spans3) &&
       NE.AllValid(hatR) && NE.StrictlyNormalized(hatR) && NE.Denote(hatR) == NE.Denote(spans1 + (spans2 + spans3))) ==>
      hatL == hatR
  {
    assert (spans1 + spans2) + spans3 == spans1 + (spans2 + spans3);
    forall hatL: seq<SpanEntry>, hatR: seq<SpanEntry>
      | NE.AllValid(hatL) && NE.StrictlyNormalized(hatL) && NE.Denote(hatL) == NE.Denote((spans1 + spans2) + spans3) &&
        NE.AllValid(hatR) && NE.StrictlyNormalized(hatR) && NE.Denote(hatR) == NE.Denote(spans1 + (spans2 + spans3))
      ensures hatL == hatR
    {
      DenoteBridge(hatL);
      DenoteBridge(hatR);
      StrictlyNormalizedBridge(hatL);
      StrictlyNormalizedBridge(hatR);
      assert NU.Denote(hatL) == NU.Denote(hatR);
      NU.NormalizationUniqueness(hatL, hatR);
    }
  }
}

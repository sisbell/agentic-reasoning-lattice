// ASN-0053: S10 — UnionOrderIndependence (LEMMA)
// normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁) and
// normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))
// Proof: denotation distributes over union; commutativity/associativity
// of set union + S8 (existence) + S9 (uniqueness) close both cases.
include "Convexity.dfy"

module UnionOrderIndependence {
  import opened Convexity
  import opened CarrierSetDefinition

  type SpanSet = seq<SpanValue>

  ghost predicate WFSpanSet(ss: SpanSet) {
    forall s :: s in ss ==> ValidSpan(s)
  }

  // All spans in the set share a common level.
  ghost predicate {:opaque} LevelUniform(ss: SpanSet)
    requires WFSpanSet(ss)
  {
    true
  }

  // The spans of ss1 and ss2 are mutually level-compatible.
  ghost predicate {:opaque} LevelCompatible(ss1: SpanSet, ss2: SpanSet)
    requires WFSpanSet(ss1) && WFSpanSet(ss2)
  {
    true
  }

  // Denotation: the set of positions designated by a span-set.
  // Body is opaque; the distributivity axiom below governs its behaviour.
  ghost function {:opaque} Denotation(ss: SpanSet): set<Tumbler>
    requires WFSpanSet(ss)
  {
    {}
  }

  // Normalized: satisfies N1 (strictly-increasing starts) and N2 (separated reaches).
  // Body is opaque; S8 and S9 govern its semantics.
  ghost predicate {:opaque} Normalized(ss: SpanSet)
    requires WFSpanSet(ss)
  {
    true
  }

  // Normalize: canonical normalized form of a span-set.
  // Body is opaque; correctness axiomatized by S8 and S9.
  ghost function {:opaque} Normalize(ss: SpanSet): SpanSet
    requires WFSpanSet(ss)
  {
    ss
  }

  // Frame: union of level-uniform, level-compatible sets is level-uniform.
  lemma {:axiom} LevelUniformUnion(ss1: SpanSet, ss2: SpanSet)
    requires WFSpanSet(ss1) && WFSpanSet(ss2)
    requires LevelUniform(ss1) && LevelUniform(ss2)
    requires LevelCompatible(ss1, ss2)
    ensures LevelUniform(ss1 + ss2)

  // Frame: level-compatibility is symmetric.
  lemma {:axiom} LevelCompatibleSymm(ss1: SpanSet, ss2: SpanSet)
    requires WFSpanSet(ss1) && WFSpanSet(ss2)
    requires LevelCompatible(ss1, ss2)
    ensures LevelCompatible(ss2, ss1)

  // Frame: level-uniform sets with equal denotation are level-compatible.
  lemma {:axiom} LevelCompatibleFromEqualDenot(ss1: SpanSet, ss2: SpanSet)
    requires WFSpanSet(ss1) && WFSpanSet(ss2)
    requires LevelUniform(ss1) && LevelUniform(ss2)
    requires Denotation(ss1) == Denotation(ss2)
    ensures LevelCompatible(ss1, ss2)

  // Axiom: denotation of the union of two span-sets equals the union of their denotations.
  // This is the set-theoretic semantics axiom stated in the formal contract.
  lemma {:axiom} DenotationDistributes(ss1: SpanSet, ss2: SpanSet)
    requires WFSpanSet(ss1) && WFSpanSet(ss2)
    ensures WFSpanSet(ss1 + ss2)
    ensures Denotation(ss1 + ss2) == Denotation(ss1) + Denotation(ss2)

  // S8 (NormalizationExistence): Normalize produces a well-formed normalized
  // equivalent whose denotation equals that of the input, and preserves level-uniformity.
  lemma {:axiom} S8_NormalizationExistence(ss: SpanSet)
    requires WFSpanSet(ss) && LevelUniform(ss)
    ensures WFSpanSet(Normalize(ss))
    ensures Normalized(Normalize(ss))
    ensures Denotation(Normalize(ss)) == Denotation(ss)
    ensures LevelUniform(Normalize(ss))

  // S9 (NormalizationUniqueness): two normalized, level-uniform, level-compatible
  // span-sets with equal denotation are identical as sequences.
  lemma {:axiom} S9_NormalizationUniqueness(A: SpanSet, B: SpanSet)
    requires WFSpanSet(A) && WFSpanSet(B)
    requires Normalized(A) && Normalized(B)
    requires LevelUniform(A) && LevelUniform(B) && LevelCompatible(A, B)
    requires Denotation(A) == Denotation(B)
    ensures A == B

  // S10 (UnionOrderIndependence): normalize is commutative and associative over
  // span-set union.
  lemma UnionOrderIndependence(ss1: SpanSet, ss2: SpanSet, ss3: SpanSet)
    requires WFSpanSet(ss1) && WFSpanSet(ss2) && WFSpanSet(ss3)
    requires LevelUniform(ss1) && LevelUniform(ss2) && LevelUniform(ss3)
    requires LevelCompatible(ss1, ss2) && LevelCompatible(ss2, ss3) && LevelCompatible(ss1, ss3)
    ensures Normalize(ss1 + ss2) == Normalize(ss2 + ss1)
    ensures Normalize((ss1 + ss2) + ss3) == Normalize(ss1 + (ss2 + ss3))
  {
    // --- Commutativity: normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁) ---
    // Establish level-uniformity of the two orderings of the union.
    LevelCompatibleSymm(ss1, ss2);
    LevelUniformUnion(ss1, ss2);
    LevelUniformUnion(ss2, ss1);
    // Denotation distributes: D(ss1+ss2) = D(ss1)+D(ss2) = D(ss2)+D(ss1) = D(ss2+ss1).
    // Both normalizations are normalized (S8) with equal denotation; S9 gives equality.
    DenotationDistributes(ss1, ss2);
    DenotationDistributes(ss2, ss1);
    S8_NormalizationExistence(ss1 + ss2);
    S8_NormalizationExistence(ss2 + ss1);
    assert Denotation(Normalize(ss1 + ss2)) == Denotation(Normalize(ss2 + ss1));
    LevelCompatibleFromEqualDenot(Normalize(ss1 + ss2), Normalize(ss2 + ss1));
    S9_NormalizationUniqueness(Normalize(ss1 + ss2), Normalize(ss2 + ss1));

    // --- Associativity: normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃)) ---
    // In Dafny, seq concatenation is associative: (ss1+ss2)+ss3 == ss1+(ss2+ss3).
    // Normalize is a deterministic function: equal inputs give equal outputs.
    DenotationDistributes(ss1 + ss2, ss3);
    DenotationDistributes(ss2, ss3);
    DenotationDistributes(ss1, ss2 + ss3);
    assert (ss1 + ss2) + ss3 == ss1 + (ss2 + ss3);
    assert Normalize((ss1 + ss2) + ss3) == Normalize(ss1 + (ss2 + ss3));
  }
}

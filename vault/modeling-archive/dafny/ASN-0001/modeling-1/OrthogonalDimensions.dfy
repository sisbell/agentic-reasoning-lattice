include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module OrthogonalDimensionsModule {
  import opened TumblerAlgebra

  // TA8 — OrthogonalDimensions (2D enfilade)
  // V-displacements and I-displacements are added, subtracted, minimized,
  // and maximized independently. No cross-dimensional operation.

  datatype Displacement2D = Displacement2D(v: Tumbler, i: Tumbler)

  // add(⟨v₁, i₁⟩, ⟨v₂, i₂⟩) = ⟨v₁ ⊕ v₂, i₁ ⊕ i₂⟩
  function Add2D(a: Displacement2D, w: Displacement2D): Displacement2D
    requires PositiveTumbler(w.v) && PositiveTumbler(w.i)
    requires ActionPoint(w.v) < |a.v.components|
    requires ActionPoint(w.i) < |a.i.components|
  {
    Displacement2D(TumblerAdd(a.v, w.v), TumblerAdd(a.i, w.i))
  }

  function Subtract2D(a: Displacement2D, w: Displacement2D): Displacement2D
    requires Subtractable(a.v, w.v) && Subtractable(a.i, w.i)
  {
    Displacement2D(TumblerSubtract(a.v, w.v), TumblerSubtract(a.i, w.i))
  }

  // min(⟨v₁, i₁⟩, ⟨v₂, i₂⟩) = ⟨min(v₁, v₂), min(i₁, i₂)⟩
  ghost function Min2D(a: Displacement2D, b: Displacement2D): Displacement2D {
    Displacement2D(
      if LessThan(a.v, b.v) then a.v else b.v,
      if LessThan(a.i, b.i) then a.i else b.i
    )
  }

  ghost function Max2D(a: Displacement2D, b: Displacement2D): Displacement2D {
    Displacement2D(
      if LessThan(b.v, a.v) then a.v else b.v,
      if LessThan(b.i, a.i) then a.i else b.i
    )
  }

  // TA8: Orthogonal dimensions — 2D operations decompose into
  // independent per-dimension operations with no cross terms.
  // DIVERGENCE: Proof index says predicate(Displacement); formalized as
  // predicate(Displacement2D, Displacement2D) since the property constrains
  // how operations on pairs decompose.
  ghost predicate OrthogonalDimensions(a: Displacement2D, w: Displacement2D) {
    (PositiveTumbler(w.v) && PositiveTumbler(w.i) &&
     ActionPoint(w.v) < |a.v.components| && ActionPoint(w.i) < |a.i.components|)
    ==>
    (Add2D(a, w).v == TumblerAdd(a.v, w.v) &&
     Add2D(a, w).i == TumblerAdd(a.i, w.i))
  }

  lemma OrthogonalDimensionsHolds(a: Displacement2D, w: Displacement2D)
    ensures OrthogonalDimensions(a, w)
  { }

  // Independence: V-projection of addition doesn't depend on I-inputs
  lemma AddVIndependent(a1: Displacement2D, a2: Displacement2D, w: Displacement2D)
    requires a1.v == a2.v
    requires PositiveTumbler(w.v) && PositiveTumbler(w.i)
    requires ActionPoint(w.v) < |a1.v.components|
    requires ActionPoint(w.i) < |a1.i.components|
    requires ActionPoint(w.i) < |a2.i.components|
    ensures Add2D(a1, w).v == Add2D(a2, w).v
  { }

  // Independence: I-projection of addition doesn't depend on V-inputs
  lemma AddIIndependent(a1: Displacement2D, a2: Displacement2D, w: Displacement2D)
    requires a1.i == a2.i
    requires PositiveTumbler(w.v) && PositiveTumbler(w.i)
    requires ActionPoint(w.v) < |a1.v.components|
    requires ActionPoint(w.v) < |a2.v.components|
    requires ActionPoint(w.i) < |a1.i.components|
    ensures Add2D(a1, w).i == Add2D(a2, w).i
  { }
}

include "Endset.dfy"

// coverage(e) — union of span address sets
module LinkCoverage {
  import opened Endset
  import opened TumblerAlgebra

  // coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
  // Modeled as membership predicate: Coverage(e, t) ≡ t ∈ coverage(e)
  ghost predicate Coverage(e: Endset, t: Tumbler) {
    exists sp :: sp in e && WellFormedSpan(sp) &&
      LessEq(sp.start, t) && LessThan(t, TumblerAdd(sp.start, sp.length))
  }
}

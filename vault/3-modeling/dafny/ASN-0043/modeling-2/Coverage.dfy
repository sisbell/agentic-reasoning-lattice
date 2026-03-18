// coverage(e) — Coverage (DEF, function)
// ASN-0043: coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})

include "Endset.dfy"

module Coverage {
  import opened Endset
  import opened TumblerAlgebra

  ghost predicate InCoverage(e: Endset, t: Tumbler)
    requires WellFormedEndset(e)
  {
    exists sp {:trigger sp in e} :: sp in e && WellFormedSpan(sp) &&
      LessEq(sp.start, t) && LessThan(t, TumblerAdd(sp.start, sp.length))
  }

  // coverage(e) = (∪ (s, ℓ) : (s, ℓ) ∈ e : {t ∈ T : s ≤ t < s ⊕ ℓ})
  ghost function Coverage(e: Endset): iset<Tumbler>
    requires WellFormedEndset(e)
  {
    iset t: Tumbler | InCoverage(e, t)
  }
}

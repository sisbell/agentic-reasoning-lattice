**ord(v)** — *OrdinalExtraction* (DEF, function). For a V-position v with #v = m and subspace(v) = v₁, the *ordinal* is:

`ord(v) = [v₂, ..., vₘ]`

— the tumbler of length m − 1 obtained by stripping the subspace identifier. When v satisfies S8a, every component of v is positive, so every component of [v₂, ..., vₘ] is positive — placing ord(v) in TA7a's domain S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.

*Proof.* We verify the postconditions of the definition.

The precondition requires v ∈ T with #v = m ≥ 2, so v has components v₁, v₂, ..., vₘ — each a natural number by T0 (CarrierSetDefinition, ASN-0034). The construction [v₂, ..., vₘ] selects components at positions 2 through m, yielding a sequence of m − 1 natural numbers. Since m ≥ 2, m − 1 ≥ 1, so [v₂, ..., vₘ] is a non-empty finite sequence of natural numbers, hence ord(v) ∈ T by T0. The length is #ord(v) = m − 1 = #v − 1.

When v satisfies S8a (zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0), every component of v is strictly positive: (A i : 1 ≤ i ≤ m : vᵢ > 0). The components of ord(v) are v₂, ..., vₘ — a subset of v's components — so every component of ord(v) is strictly positive: (A i : 1 ≤ i ≤ m − 1 : ord(v)ᵢ > 0). Combined with ord(v) ∈ T and #ord(v) = m − 1 ≥ 1, this places ord(v) in S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} (TA7a, SubspaceClosure, ASN-0034). ∎

*Formal Contract:*
- *Preconditions:* `v ∈ T`, `#v ≥ 2`.
- *Definition:* `ord(v) = [v₂, ..., vₘ]` where `m = #v`.
- *Postconditions:* `ord(v) ∈ T` (length `m - 1 ≥ 1`, satisfying T0). `#ord(v) = #v - 1`. When `v` satisfies S8a (`zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0`), `ord(v) ∈ S` — every component of `[v₂, ..., vₘ]` is positive since every component of `v` is positive by S8a.
- *Frame:* Pure function on the component sequence of `v` — no state is read or modified.

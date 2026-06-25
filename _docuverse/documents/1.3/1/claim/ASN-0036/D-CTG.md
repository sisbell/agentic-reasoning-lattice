**D-CTG (VContiguity).** For each document d, V_1(d) (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`

In words: within the text subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`.
- *Preconditions:* `subspace(v) = 1`; `zeros(v) = 0` ⟺ S8a positivity, by T0; V-positions share a common depth (S8-depth).
- *Postconditions:* V_1(d) is either empty or occupies every position strictly between its extremes (at the fixed depth).
- *Frame:* D-CTG is a constraint on well-formed text-subspace arrangements.
- *Depends:* S8a (V-position well-formedness); S8-depth (common depth within subspace); T1 (LexicographicOrder, ASN-0034) — defines the order.

For the text subspace at depth m = 2, this is a finite condition: the intermediates between [1, a] and [1, b] are the finitely many [1, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_1(d) occupies a single unbroken block of ordinals.

- *Depends:*
  - S8a (Σ.M(d) domain restriction) — supplies the V-position well-formedness constraint `zeros(v) = 0` used in the axiom's quantifier guard and the S8a positivity precondition
  - T0 (ASN-0034) — supplies the equivalence `zeros(v) = 0` iff every component is positive, invoked in the precondition `zeros(v) = 0 ⟺ S8a positivity, by T0`
  - S8-depth (Fixed-depth V-positions) — supplies the common-depth invariant `#v = #u` used in the axiom's quantifier guard to restrict intermediates to the same tumbler depth
  - T1 (LexicographicOrder, ASN-0034) — defines the strict total order `<` on tumblers used throughout the axiom's ordering guards `u < q`, `u < v < q`
- *Forward References:*
  - S8-fin (Finite arrangement) — combined with D-CTG, yields the corollary that V_1(d) occupies a single unbroken finite block of ordinals; named as a downstream companion, not a dependency of this claim's axiom
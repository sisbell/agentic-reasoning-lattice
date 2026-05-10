# Formalize — ASN-0036 / D-CTG-depth

*2026-04-13 13:03*

**D-CTG-depth (SharedPrefixReduction).** For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

*Proof.* Let V_S(d) be non-empty with common depth m ≥ 3 (S8-depth). Suppose for contradiction that V_S(d) contains two positions v₁ and v₂ with v₁ < v₂ (both depth m) whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1 — that is, (v₁)ᵢ = (v₂)ᵢ for all i < j (in particular, (v₁)₁ = S = (v₂)₁, since both belong to V_S(d)), and (v₁)ⱼ < (v₂)ⱼ (the inequality follows from v₁ < v₂ by T1(i), since j is the first disagreeing component and j ≤ min(m, m)).

We construct infinitely many intermediates. For any natural number n > (v₁)ⱼ₊₁, define w of length m by:

- wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j (agreeing with v₁ on the first j components),
- wⱼ₊₁ = n,
- wᵢ = 1 for j + 2 ≤ i ≤ m (if any such positions exist; since j ≤ m − 1, at least the m-th component exists at position j + 1 or beyond).

Then w has depth m (it has m components by construction), and subspace(w) = w₁ = (v₁)₁ = S (since j ≥ 2, the first component is copied from v₁). We verify v₁ < w < v₂:

- **w > v₁**: w agrees with v₁ on components 1 through j. At component j + 1, wⱼ₊₁ = n > (v₁)ⱼ₊₁. Since j + 1 ≤ m = min(m, m), by T1(i), w > v₁.
- **w < v₂**: w agrees with v₂ on components 1 through j − 1 (since v₁ and v₂ agree on these components by the definition of j). At component j, wⱼ = (v₁)ⱼ < (v₂)ⱼ. Since j ≤ m − 1 < m = min(m, m), by T1(i), w < v₂.

Since v₁ < w < v₂, subspace(w) = S, and #w = m = #v₁, D-CTG requires w ∈ V_S(d). By T0(a) (UnboundedComponentValues, ASN-0034), unboundedly many values of n > (v₁)ⱼ₊₁ exist. Distinct values of n yield distinct tumblers w (they differ at component j + 1, so by T3, CanonicalRepresentation, ASN-0034, they are unequal). This produces infinitely many distinct positions in V_S(d), contradicting S8-fin (dom(M(d)) is finite).

Therefore no two positions in V_S(d) can disagree at any component j with 2 ≤ j ≤ m − 1. All positions share components 2 through m − 1, and contiguity reduces to contiguity of the last component (component m) alone. ∎

Nelson's statement specifies not just contiguity but also the starting ordinal: "addresses 1 through 100," not "42 through 141." All ordinal numbering in the tumbler system starts at 1: the first child is always .1 (LM 4/20), link positions within a document begin at 1 (LM 4/31), and position 0 is structurally unavailable since zero serves as a field separator (T4, ASN-0034). V-positions follow the same convention.

*Formal Contract:*
- *Preconditions:* V_S(d) non-empty; common depth m ≥ 3 (S8-depth); D-CTG (VContiguity); S8-fin (finite arrangement).
- *Postconditions:* `(A v₁, v₂ ∈ V_S(d), j : 2 ≤ j ≤ m − 1 : (v₁)ⱼ = (v₂)ⱼ)`. Contiguity of V_S(d) reduces to contiguity of the m-th (last) component.

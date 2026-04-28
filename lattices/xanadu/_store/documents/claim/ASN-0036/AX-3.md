**AX-3 (Infinite type domains).** The state model `Σ = (C, M)` operates over two carrier sets drawn from the tumbler space `T` (ASN-0034). The *document identifier space* is `Doc = {d ∈ T : zeros(d) = 2}`, comprising all tumblers at document depth (D-DOC). The *V-position space* within subspace `S` is `VPos(S) = {v ∈ T : zeros(v) = 0 ∧ v₁ = S}`, comprising all tumblers satisfying S8a's well-formedness conditions with subspace identifier `S`. Both are countably infinite.

`Doc` is countably infinite because T10a allocation (ASN-0034) can produce arbitrarily many document-level tumblers, each assigned a distinct identifier by GlobalUniqueness (ASN-0034), and `T` is countable — its elements are finite sequences of non-negative rationals: `|Doc| = ℵ₀`.

Each `VPos(S)` is countably infinite because, for any `S ≥ 1`, the tumblers `[S, 1], [S, 2], [S, 3], …` are pairwise distinct elements satisfying `zeros(v) = 0` and `v₁ = S ≥ 1`; since `T` is countable, `|VPos(S)| = ℵ₀`.

These cardinality facts serve two purposes. First, S5 (unrestricted sharing) constructs conforming traces with `N + 1` pairwise-distinct documents or V-positions for arbitrary `N ∈ ℕ`; the constructions succeed only if the carrier sets are unbounded. Second, the set comprehension `{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}` appearing in S5's formal statement is well-defined as a set — not a proper class — because it is a subset of `Doc × T`, a countable product. ∎

*Formal Contract:*
- *Axiom:* `|Doc| = ℵ₀` where `Doc = {d ∈ T : zeros(d) = 2}` — the document identifier space is countably infinite.
- *Axiom:* `(A S ≥ 1 :: |VPos(S)| = ℵ₀)` where `VPos(S) = {v ∈ T : zeros(v) = 0 ∧ v₁ = S}` — the V-position space within each subspace is countably infinite.

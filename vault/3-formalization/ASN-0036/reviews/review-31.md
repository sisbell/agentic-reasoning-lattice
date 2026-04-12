# Formalize — ASN-0036 / S8a

*2026-04-12 15:50*

**S8a (V-position well-formedness).** Every V-position is an element-field tumbler with all components strictly positive:

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`

A V-position represents the element field of a full document-scoped address — the fourth field in the T4 field structure. Its first component `v₁` is the subspace identifier. The conjunct `v₁ ≥ 1` is not a guard but a universally true consequence: V-positions are element-field tumblers, and T4's positive-component constraint requires every component of every field to be strictly positive — so `v₁ ≥ 1` holds for all V-positions without exception. This universality is load-bearing: S8's partition proof requires every V-position to belong to some subspace `S` with `v₁ = S ≥ 1` to invoke T5 and T10 for cross-subspace disjointness. The domain and range of `M(d)` live in structurally different tumbler subsets: `dom(M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ t > 0}` (element-field tumblers), while `ran(M(d)) ⊆ {t ∈ T : zeros(t) = 3}` (full element-level addresses, per S7b). Since all V-positions in subspace `s` extend the single-component prefix `[s]`, T5 (PrefixContiguity, ASN-0034) guarantees they form a contiguous interval under T1 — grounding the application of tumbler ordering properties to V-positions and justifying S8-depth's reference to "within a subspace."

*Remark.* The shared vocabulary identifies a second subspace for links (v₁ = 2, per T4 and LM 4/30). Link-subspace V-positions satisfy the same `zeros(v) = 0` and `v > 0` constraints as text-subspace positions — both are element-field tumblers with strictly positive components. The subspace identifier (1 for text, 2 for links) is the first component of the element field; the `0` in tumbler notation (e.g., `N.0.U.0.D.0.2.1`) is a field separator, not a subspace identifier. Link-subspace arrangement semantics are deferred to a future ASN.

*Proof.* S8a is a design requirement: V-positions are element-field tumblers, and T4 (HierarchicalParsing, ASN-0034) constrains the structure of every field. We show each conjunct follows from this structural commitment.

A full element-level I-address has the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ` where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The arrangement `M(d)` maps V-positions to such I-addresses: by S3 (Referential integrity), every V-reference resolves — `M(d)(v) ∈ dom(Σ.C)` — and by S7b (Element-level I-addresses), every address in `dom(Σ.C)` is element-level — `zeros(M(d)(v)) = 3` — so the target address has all four fields present. A V-position `v` is the element field `E` extracted from the document-scoped address — the fourth field in T4's decomposition. As an isolated field, `v` contains no field separators: the zeros in the full address are inter-field boundaries, not intra-field components. Since T4's positive-component constraint requires `Eₗ > 0` for every component of the element field, no component of `v` equals zero; therefore `zeros(v) = 0`.

The conjunct `v > 0` — every component of `v` is strictly positive — follows directly from T4's positive-component constraint. T4 requires that every non-separator component of every field satisfy `Eₗ > 0` for `1 ≤ l ≤ δ`, where `δ = #v` is the number of components in the element field. Since `zeros(v) = 0`, every component of `v` is a non-separator component, so every component is strictly positive: `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`.

The conjunct `v₁ ≥ 1` is a specialisation of `v > 0` to the first component. T4's non-empty field constraint requires `δ ≥ 1` — the element field has at least one component. Since `v₁` is a component of the element field with `v₁ > 0` (from the positive-component constraint), and tumbler components are natural numbers, the strict inequality `v₁ > 0` entails `v₁ ≥ 1`. This is not an independent condition but a universally true consequence that we state explicitly because it is load-bearing: `v₁` serves as the subspace identifier, and S8's partition proof requires every V-position to belong to some subspace `S = v₁ ≥ 1` to invoke T5 and T10 for cross-subspace disjointness. ∎

*Formal Contract:*
- *Axiom:* V-positions are element-field tumblers — the fourth field in T4's decomposition of element-level addresses.
- *Preconditions:* T4 (HierarchicalParsing, ASN-0034) — every non-separator component is strictly positive, every present field has at least one component; S3 (Referential integrity) — every V-reference resolves, connecting V-positions to addresses in `dom(Σ.C)`; S7b — addresses in `dom(Σ.C)` are element-level tumblers with `zeros(a) = 3`.
- *Postconditions:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`.

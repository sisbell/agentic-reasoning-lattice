## Sharing

The arrangement function `M(d)` need not be injective. This is not a deficiency but a design requirement — it is what makes transclusion work.

**S5 (Unrestricted sharing).** The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement. S0–S3 are consistent with any finite sharing multiplicity — they place no constraint on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|`:

`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ (E a ∈ dom(Σ.C) :: |{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N)))`

To see this, fix any `N`. Construct state `Σ_N` with one I-address `a` where `C(a) = w` for some value `w`, and `N + 1` documents `d₁, ..., d_{N+1}`, each with `M(dᵢ) = {vᵢ ↦ a}` for distinct V-positions `vᵢ`. S0 is vacuous — single state, no transition to check. S2 holds: each `M(dᵢ)` is a function with a single entry. S3 holds: `a ∈ dom(C)`. The sharing multiplicity of `a` is `N + 1 > N`. Since `N` was arbitrary, no finite bound is entailed. The same holds within a single document: for any `N`, construct `Σ'_N` with one I-address `a` where `C(a) = w`, and one document `d` with `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}` for `N + 1` distinct V-positions. S0 and S1 are vacuous as above (single state, no transition to check). S2 holds — each `vᵢ` maps to exactly one I-address (namely `a`). S3 holds — `a ∈ dom(C)`. The within-document sharing multiplicity is `N + 1 > N`.

In any particular state, the sharing multiplicity of each address is a definite finite number — possibly zero for orphaned content (S6). The property is an architectural anti-constraint: the invariants place no finite cap on how many references may accumulate.

Nelson: "The virtual byte stream of a document may include bytes from any other document." And: "A document may have a window to another document, and that one to yet another, indefinitely. Thus A contains part of B, and so on. One document can be built upon another, and yet another document can be built upon that one, indefinitely." Transclusion is recursive and unlimited.

Gregory confirms the unbounded nature at the implementation level. The global index that records which documents reference which I-addresses accumulates entries without cap — "no counter, cap, MAX_TRANSCLUSIONS constant, or any other limiting mechanism anywhere in the code path." Each referential inclusion adds one entry. The only constraints are physical resources (memory and disk), not architectural limits.

The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value. S5 says sharing is unlimited — any number of documents can reference the same content. Together they establish a regime in which quotation is a first-class structural relationship: any number of documents can quote the same passage, and the system knows they are all quoting — not independently writing — because they share I-addresses.

We observe that the state `Σ = (C, M)` makes the sharing relation computable: given any `a ∈ dom(C)`, the set `{d : (E v :: M(d)(v) = a)}` is determined by the state. Nelson requires this to be queryable: "It must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." The state model supports this — the information is present; only the efficiency of its extraction is an implementation concern.

*Proof.* We wish to show that for every `N ∈ ℕ`, there exists a state `Σ` satisfying S0–S3 in which some I-address has sharing multiplicity exceeding `N`. We give two constructions — one for cross-document sharing, one for within-document sharing — each succeeding for arbitrary `N`.

**Cross-document construction.** Fix `N ∈ ℕ`. Define state `Σ_N = (C_N, M_N)` by:

- `C_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- `N + 1` documents `d₁, …, d_{N+1}`, with `M_N(dᵢ) = {vᵢ ↦ a}` for pairwise distinct V-positions `vᵢ`.

We verify each invariant. S0 (content immutability) and S1 (store monotonicity) quantify over state transitions `Σ → Σ'`; we consider `Σ_N` as a single state with no transition, so both hold vacuously. S2 (arrangement functionality): each `M_N(dᵢ)` contains a single entry `{vᵢ ↦ a}` — the domain has one element, so uniqueness of the image is immediate; `M_N(dᵢ)` is a function. S3 (referential integrity): the sole I-address referenced by any arrangement is `a`, and `a ∈ dom(C_N)` by construction.

The sharing multiplicity of `a` in `Σ_N` is `|{(d, v) : v ∈ dom(M_N(d)) ∧ M_N(d)(v) = a}| = N + 1`, since each of the `N + 1` documents contributes exactly one pair `(dᵢ, vᵢ)`. Thus the multiplicity exceeds `N`.

**Within-document construction.** Fix `N ∈ ℕ`. Define state `Σ'_N = (C'_N, M'_N)` by:

- `C'_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`.
- One document `d` with `M'_N(d) = {v₁ ↦ a, v₂ ↦ a, …, v_{N+1} ↦ a}` for `N + 1` pairwise distinct V-positions `v₁, …, v_{N+1}`.

S0 and S1 are vacuous as above — single state, no transition to check. S2 (arrangement functionality): the `vᵢ` are pairwise distinct by hypothesis, so each V-position maps to exactly one I-address (namely `a`); `M'_N(d)` is a well-defined function. S3 (referential integrity): the sole referenced I-address `a` satisfies `a ∈ dom(C'_N)` by construction.

The within-document sharing multiplicity is `|{v : v ∈ dom(M'_N(d)) ∧ M'_N(d)(v) = a}| = N + 1 > N`.

**Conclusion.** Since both constructions succeed for arbitrary `N ∈ ℕ`, the conjunction S0 ∧ S1 ∧ S2 ∧ S3 is consistent with sharing multiplicity exceeding any given finite bound. No finite cap on `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|` is entailed by these invariants — neither across documents nor within a single document. ∎

*Formal Contract:*
- *Preconditions:* `N ∈ ℕ` arbitrary.
- *Postconditions:* There exists a state `Σ` satisfying S0 (content immutability), S1 (store monotonicity), S2 (arrangement functionality), and S3 (referential integrity) such that for some `a ∈ dom(Σ.C)`, `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N`. The construction works both across documents (multiplicity `N + 1` over `N + 1` documents) and within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions).
- *Frame:* S0–S3 are the only invariants checked. The constructions are minimal — single I-address, trivial arrangements — to isolate the consistency claim from other architectural properties.

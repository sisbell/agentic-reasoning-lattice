# Cross-cutting Review — ASN-0036 (cycle 3)

*2026-04-12 18:55*

I've read the full ASN-0036 against its foundation statements, tracing every definition, precondition chain, and citation. I note that several previous findings appear to have been addressed in revision (D-MIN now cites S8a, D-SEQ now cites S8-vdepth, V_S(d) and subspace now have formal definition blocks, S3 is now classified as an axiom, D-MIN postcondition now cites S8-vdepth). Three new findings follow.

---

### S5 existential proof requires Val ≠ ∅ without declaring it

**Foundation**: Σ.C (ContentStore) — "Σ.C : T ⇀ Val — the content store is a partial function from tumblers to content values." Val is described as "an unspecified set of content values, opaque at this level of abstraction."

**ASN**: S5 (Unrestricted sharing), cross-document construction: "Define state Σ_N = (C_N, M_N) by: C_N = {a ↦ w} for a single I-address a and arbitrary value w ∈ Val."

**Issue**: The phrase "arbitrary value w ∈ Val" presupposes Val ≠ ∅. The Σ.C definition characterizes Val as "an unspecified set" — which includes the empty set. If Val = ∅, then dom(Σ.C) = ∅ in every state, and S5's inner existential "(E a ∈ dom(Σ.C) :: ...)" is false in every state, making S5's claimed postcondition — `(A N ∈ ℕ :: (E Σ :: ...))` — false. Both constructions (cross-document and within-document) fail identically. The formal contract lists "N ∈ ℕ arbitrary" as the sole precondition, with no mention of Val. The within-document construction has the same gap: "C'_N = {a ↦ w} for a single I-address a and arbitrary value w ∈ Val."

**What needs resolving**: Either the Σ.C definition must assert Val ≠ ∅ (a natural axiom — the system stores something), or S5's formal contract must add Val ≠ ∅ as a precondition.

---

### S8-fin and S3 inductive proofs rely on an unstated initial-state axiom

**Foundation**: Σ.M(d) (Arrangement) — "Σ.M(d) : T ⇀ T — the arrangement of document d is a partial function." Σ.C (ContentStore) — "Σ.C : T ⇀ Val." Neither definition specifies an initial value.

**ASN**: S8-fin (FiniteArrangement), base case: "In the initial state Σ₀, no operations have been performed. ... For every document d, dom(Σ₀.M(d)) = ∅. The empty set is finite." S3 (Referential integrity), base case: "In the initial state Σ₀, no arrangements have been established: dom(Σ₀.M(d)) = ∅ for every document d."

**Issue**: Both inductive proofs assert `dom(Σ₀.M(d)) = ∅` as a fact, but no property in the ASN axiomatizes the initial state. The Σ.M(d) definition says it is a partial function — which could be empty or non-empty. The claim that the initial arrangement is empty is an appeal to operational intuition ("no operations have been performed"), not a derivation from any stated axiom. In TLA+ formalization, the initial-state predicate `Init` is a distinct axiom (`∀ d : M(d) = ∅ ∧ C = ∅`); its absence leaves both inductive base cases formally ungrounded. The same gap affects dom(Σ₀.C) = ∅, which S3's base case uses implicitly (the universal quantification over dom(Σ₀.M(d)) is vacuous, but S8-fin's base case explicitly depends on the empty initial arrangement).

**What needs resolving**: An initial-state axiom establishing `dom(Σ₀.M(d)) = ∅` for every document d and `dom(Σ₀.C) = ∅` must be stated as a formal property — either as a standalone axiom or as part of the Σ = (C, M) state model definition. Both S8-fin's and S3's formal contracts should cite it.

---

### subspace(v) definition restricts domain to V-positions but is applied to arbitrary tumblers

**Foundation**: subspace(v) (SubspaceIdentifier) — "subspace(v) = v₁ for v ∈ dom(Σ.M(d)). Preconditions: S8a — v₁ ≥ 1."

**ASN**: D-CTG (VContiguity), axiom: `(A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d))`. OrdAddHom postcondition (b): `subspace(v ⊕ w) = subspace(v)`.

**Issue**: D-CTG's inner quantifier ranges over all tumblers v ∈ T satisfying three conditions, then forces the conclusion v ∈ V_S(d). Before the axiom fires, v is an arbitrary tumbler — not a V-position, not in dom(M(d)), and not subject to S8a. The condition "subspace(v) = S" applies the function outside its formal domain. The same mismatch appears in OrdAddHom: v ⊕ w is a tumbler in T that may fail S8a (OrdAddS8a shows S8a compliance is conditional on the displacement's tail components), yet postcondition (b) applies subspace to it. Since subspace(t) = t₁ is a trivial component extraction well-defined on all of T, the results are correct — but the formal definition's domain restriction to dom(Σ.M(d)) with S8a as a precondition makes these applications technically out of scope. D-CTG-depth's proof has the same pattern: "subspace(w) = w₁ = (v₁)₁ = S" applies subspace to a constructed intermediate that is not yet a V-position.

**What needs resolving**: Either extend subspace's formal definition to all tumblers in T (dropping the S8a precondition, since t₁ is defined for any t with #t ≥ 1), or replace "subspace(v) = S" with "v₁ = S" in D-CTG's axiom and restate OrdAddHom postcondition (b) as "(v ⊕ w)₁ = v₁". The V_S(d) definition already uses v₁ = S directly, making either fix consistent with existing conventions.

## Result

Not converged after 3 cycles.

*Elapsed: 5530s*

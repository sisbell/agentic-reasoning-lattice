# Cone Review — ASN-0036/ValidInsertionPosition (cycle 1)

*2026-04-15 00:11*

Now I have the complete picture. Let me trace the cross-cutting chains.

---

### D-CTG-depth's proof asserts T-membership without foundation support

**Foundation**: T0 (ASN-0034), T3 (CanonicalRepresentation, ASN-0034)
**ASN**: D-CTG-depth (SharedPrefixReduction), proof construction of tumbler `r`
**Issue**: The proof constructs `r = [p₁, …, p_{k−1}, pₖ+1, 0, …, 0]` and claims `r ∈ T` by citing "T0 (ASN-0034), T contains finite sequences of natural-number components." But T0 characterizes what components *are* (natural numbers); it does not guarantee that every finite sequence of naturals is a member of T. T3 gives canonical representation (equality is sequence equality) — this tells you how to compare tumblers in T, not which sequences are in T. T0(a) gives unboundedness (you can push any component arbitrarily high) but not that every intermediate value is realized. No foundation axiom provides a set-existence principle of the form "for any `(n₁, …, nₖ)` with each `nᵢ ∈ ℕ`, there exists `t ∈ T` with `#t = k` and `tᵢ = nᵢ`." The proof specifically needs a tumbler with zero-valued trailing components to obtain the contradiction with S8a, and no existing axiom constructs such a tumbler from scratch.
**What needs resolving**: Either ASN-0034 needs a T-construction axiom (e.g., that T contains all finite non-empty sequences of naturals), or D-CTG-depth's proof must construct `r` from existing tumblers using operations whose closure in T is already established (⊕, ⊖, OrdinalShift). Since D-CTG-depth is load-bearing for S8-crun and D-SEQ at depth ≥ 3, the gap propagates to the sequential characterization of V_S(d) at those depths.

---

### D-CTG's "T-resident" caveat contradicts what OrdinalShift establishes

**Foundation**: T0(a) (UnboundedComponentValues, ASN-0034), OrdinalShift (ASN-0034)
**ASN**: D-CTG (VContiguity), body text: "T0(a) guarantees tumblers exceeding any bound at a given component but not at every intermediate value, so some ordinal values between occupied positions may lack a corresponding tumbler in T, and D-CTG imposes no constraint at such absent values."
**Issue**: The body text cites only T0(a) and concludes that T-gaps could weaken the contiguity guarantee. But OrdinalShift's postcondition (`shift(v, n) ∈ T`) constructs exactly the intermediates in question. For a non-empty subspace with base `b = min(V_S(d)) ∈ T`, `shift(b, k) = [S, 1, …, 1+k] ∈ T` for all `k ≥ 1`. At depth 2, this gives `[S, k] ∈ T` for every positive integer `k`. At depth ≥ 3 (given D-CTG-depth's shared prefix), the intermediates between any two V-positions also lie in T by OrdinalShift. So the "T-resident" qualifier is operationally vacuous for every configuration that the invariant system permits — no positive-component intermediate between V-positions is absent from T. The caveat attributes the density question to T0(a) alone, ignoring OrdinalShift's role, and suggests a weakness that the specification as a whole does not have. This matters because D-SEQ and S8-crun derive the sequential characterization of V_S(d) from D-CTG, and their correctness depends on intermediates being present in T — a guarantee OrdinalShift provides but D-CTG's body text denies.
**What needs resolving**: D-CTG's body text should either acknowledge that OrdinalShift (not T0(a)) is the operative guarantee for intermediate T-membership, or remove the caveat about absent values. The formal invariant is correct as stated; the issue is that the body text's reasoning about the invariant's strength is inconsistent with the cross-property picture.

---

### `subspace(v)` used in formal invariant without definition

**Foundation**: T1 (LexicographicOrder, ASN-0034)
**ASN**: D-CTG formal invariant uses `subspace(v) = S` for `v ∈ T`; V_S(d) definition (V-S) uses `v₁ = S` for `v ∈ dom(Σ.M(d))`; D-CTG-depth proof bridges them with `subspace(r) = r₁ = p₁ = S`
**Issue**: D-CTG's formal invariant quantifies over all `v ∈ T` and filters by `subspace(v) = S`. V_S(d) defines subspace membership by `v₁ = S`, restricted to V-positions in `dom(Σ.M(d))`. The function `subspace : T → ℕ` is never formally defined for arbitrary tumblers. For V-positions (where `zeros(v) = 0` by S8a), `subspace(v) = v₁` is unambiguous. For a general tumbler with separators, `v₁` could be a network-field component under T4 parsing, making the semantic loading of "subspace" unclear. D-CTG-depth's proof implicitly resolves this by working directly with `r₁ = p₁ = S`, but this identification should be stated as a definition, not assumed. The two notations — `subspace(v) = S` in D-CTG and `v₁ = S` in V_S — denote the same predicate but are never explicitly equated.
**What needs resolving**: Either define `subspace(v) ≡ v₁` as a vocabulary entry (applicable to all `v ∈ T`), or replace `subspace(v) = S` in D-CTG's formal invariant with `v₁ = S` to match V_S's definition. The equivalence is obvious to a human reader but must be explicit for formalization — a TLA+ or Dafny encoding would need to pick one representation and use it consistently.

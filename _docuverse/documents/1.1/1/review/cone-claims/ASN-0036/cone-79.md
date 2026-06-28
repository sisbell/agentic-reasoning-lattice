## Review

The dependency graph for this ASN is clean: all foundation claims are in scope, D-CTG-depth's premises draw from correctly-stated posits (D-CTG, S8-depth, S8a, S8-fin), and the proof machinery flows from T0/T0(a)/T1/NAT-wellorder in the expected way.

**D-CTG-depth proof walkthrough.** The contradiction is correctly structured. Given u, x ∈ V_1(d) with u < x and first interior disagreement at j (NAT-wellorder applied to a nonempty subset of ℕ), the proof pins T1's existential witness k to j by a two-sided squeeze (k < j contradicts the established agreement on 1..j−1; k > j contradicts j being a disagreement point), reading u_j < x_j off clause (i). The witness w = [u₁,…,u_j, n, 1,…,1] satisfies all of D-CTG's inner guards: w ∈ T by T0 comprehension, subspace(w) = w₁ = u₁ = 1 (j ≥ 2 so the first component is copied from u), #w = m = #u, and zeros(w) = 0 because every component is strictly positive (S8a on u for positions 1..j, n > u_{j+1} ≥ 1, and 1 for trailing positions). T1 clause (i) with k = j+1 gives u < w; clause (i) with k = j gives w < x. D-CTG forces w ∈ V_1(d). T0(a) iterated at (u, j+1) with monotone bounds supplies a strictly-increasing sequence of distinct n values, giving infinitely many pairwise-distinct elements of V_1(d) ⊆ dom(M(d)) by T3. This contradicts S8-fin. The m ≥ 3 scope restriction is correctly justified (interior range 2..m−1 non-empty) and the j = m−1 boundary is handled (trailing clause is empty, w = [u₁,…,u_{m-1}, n]). The proof is sound.

**Terminology is consistent.** `subspace`, `#`, `zeros`, `<` (lex), and V_1(d) carry a single meaning throughout. No definitional drift across sections.

**Precondition chain is unbroken.** V_1(d) ⊆ dom(M(d)) holds by V-sub's set-comprehension definition; dom(M(d)) finite by S8-fin; zeros-free by S8a; same depth m by S8-depth; contiguity posited by D-CTG. All consumed in D-CTG-depth at the points the proof needs them.

---

### dom(Σ.M(d)) used without citing Arrangement in S8-fin, S8a, and S8-depth
**Class**: OBSERVE
**Foundation**: Σ.M(d) (Arrangement) — the claim within this ASN that defines `dom(Σ.M(d))` as the set of active V-positions of d
**ASN**: S8-fin Depends (no Arrangement entry despite the bijection codomain being `dom(Σ.M(d))`); S8a Depends (no Arrangement entry despite the axiom's left-hand side being `dom(Σ.M(d))`); S8-depth Depends (no Arrangement entry despite the formal statement quantifying over `dom(Σ.M(d))`)
**Issue**: V-sub correctly lists `Σ.M(d) (Arrangement)` as a dependency, citing it as the source of `dom(Σ.M(d))`. S8-fin, S8a, and S8-depth each use `dom(Σ.M(d))` as a primary object in their formal statements — S8-fin puts it as the bijection's codomain, S8a restricts it directly, S8-depth quantifies over it — but none list Arrangement in their Depends. A reader following S8-fin's dependency chain finds NAT-carrier, NAT-closure, NAT-order, T0; none of these define `dom(Σ.M(d))`. The Arrangement claim is in the same ASN, so the symbol is not semantically ungrounded, but the citation gap is inconsistent with how V-sub handles the same notation.
**What needs resolving**: Add `Σ.M(d) (Arrangement)` to the Depends of S8-fin, S8a, and S8-depth, with a one-line note citing it as the source of the `dom(Σ.M(d))` notation used in each claim's formal statement — mirroring the citation already present in V-sub.

VERDICT: OBSERVE
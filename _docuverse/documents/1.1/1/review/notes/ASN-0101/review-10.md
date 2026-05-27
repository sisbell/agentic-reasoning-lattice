# Review of ASN-0101

## REVISE

### Issue 1: D8 numerical typo

**ASN-0101, D8 Group (i) Justification**: "The remaining four invariants — S3★, S3★-aux, S8★, CL-OWN, CL-UNIQ — require care because..."

**Problem**: The list contains five invariants (S3★, S3★-aux, S8★, CL-OWN, CL-UNIQ), not four.

**Required**: Change "four" to "five".

### Issue 2: D8 Group (ii) chain-discipline lemma list is selective

**ASN-0101, D8 Group (ii)**: "Likewise the substrate-level chain-discipline lemmas — ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, and FirstEmissionFreshness (ASN-0093) — hold trivially at Σ'..."

**Problem**: ASN-0093 supplies additional chain-discipline lemmas not listed: ChainElementT4Validity, ChainPrefixExtension, ChainMembershipForOrigin, DisjointSubAllocatorChains, StoreT4Validity, and CrossDocDisjointness. Each is preserved by the same frame argument (each is a structural property of `dom(C)`, `dom(L)`, `dom(M)`, all unchanged by D0). The selective list invites the reader to wonder whether the omitted lemmas were considered.

**Required**: Either enumerate all relevant chain-discipline lemmas of ASN-0093, or add a closing phrase such as "and the remaining chain-discipline lemmas of ASN-0093, by identical frame reasoning".

### Issue 3: D8 disjointness-routing prose is dense

**ASN-0101, D8 Group (i) Justification**: "The disjointness `Λ ∩ Q = ∅` discharges along two routes... *Non-vacuous route* (`n < n_S − p + 1`, both endpoints present)... *Vacuous route* (`n = n_S − p + 1`...)"

**Problem**: The bifurcation is mathematically correct but the labels "vacuous route" / "non-vacuous route" describe whether `Q` is non-empty, not whether the disjointness conclusion is vacuous. The two namings are inverted from what the reader might expect, and reading the case names against D0's containment bound (`p + n ≤ n_S + 1`) requires unpacking `n_S − n = p − 1` vs `n_S − n ≥ p`.

**Required**: Rename the routes to track whether `Q` is non-empty (e.g., "`Q` non-empty: integer-range disjointness" vs "`Q` empty: trivially disjoint") or add an explicit one-line note explaining which arithmetic regime each route covers.

### Issue 4: D9 third bullet quantification scope

**ASN-0101, D9 third bullet**: "If `d'' = d`, restricted to subspace `S`: `project(L'(ℓ).eᵢ, d, Σ') ∩ V_S(M'(d)) = (project(L(ℓ).eᵢ, d, Σ) ∩ Λ) ∪ {σ_d(v) : v ∈ project(L(ℓ).eᵢ, d, Σ) ∩ Ρ}`."

**Problem**: The bullet does not say how to recover the full projection `project(L'(ℓ).eᵢ, d, Σ')` from the three bullets. The first bullet handles `d'' ≠ d`; the second restricts to `S' ≠ S` within `d`; the third restricts to `S` within `d`. The full projection for `d'' = d` is the union of the second-bullet and third-bullet contributions, but this composition is left implicit and is used in D11's wp justification ("the post-state projection is the union of three things") without an explicit referent.

**Required**: Add a one-line synthesis after the third bullet stating `project(L'(ℓ).eᵢ, d, Σ') = (second-bullet RHS) ∪ (third-bullet RHS)`, or explicitly fold the synthesis into D11's justification.

### Issue 5: Composite-substitution argument's "observably distinct" digression

**ASN-0101, "The operation" section**: "In typical configurations Σ_mid is in fact observably distinct from Σ_pre. K.μ~ requires π ≠ id, so some v ∈ dom(M(d)) has π(v) ≠ v..."

**Problem**: The sequence-length argument from SequentialAtomicTransitions is sufficient on its own to establish the primitive/composite distinction. The subsequent discussion of when `Σ_mid` is *observationally* distinct (link-subspace via CL-UNIQ, content-subspace generically via S5 unrestricted sharing) adds complexity without strengthening the argument. The closing concession — "the sequence-length argument is what closes the case independently of observational distinctness" — confirms the digression is not load-bearing.

**Required**: Either compress the observational-distinctness paragraph to a single sentence and note that it is corroborative, or remove it entirely and let the sequence-length argument stand alone.

### Issue 6: D11 wp for discoverability — semantic note on what `project ⊆ X` requires

**ASN-0101, D11 first bullet**: "A link becomes undiscoverable from `d` after DELETE iff *every* slot's pre-state projection from `d` is contained entirely within the deleted region."

**Problem**: The condition `project(L(ℓ).eᵢ, d, Σ) ⊆ X` is stronger than it first appears because `project` ranges over all of `dom(M(d))` while `X ⊆ V_S(d)`. The condition therefore requires the projection to have no elements in `V_{S'}(d)` (the other subspace) and no elements in `V_S(d) \ X`. The wp formula is correct, but a reader could mistakenly think the condition only constrains the affected subspace.

**Required**: Add a one-line clarification that `project ⊆ X` implicitly requires the projection to have no elements in the other subspace either (or, equivalently, that the link's coverage does not intersect `ran(M(d)|_{V_{S'}(d)})`).

## OUT_OF_SCOPE

### Topic 1: Versioning and historical reconstruction

The "A note on recoverability and historical reconstruction" section discusses how DELETE plus the J4 ForkComposite supports recoverability. The detailed mechanics of version-based reconstruction belong in a separate ASN on versioning composites; ASN-0101 correctly limits itself to noting that D2 + D5 supply the necessary non-destruction substrate.

### Topic 2: Composite-level J0/J1★/J1'★ obligations for multi-step composites containing DEL

D10's "What this does and does not show" correctly notes that multi-step composites combining DEL with allocation-and-placement steps must be checked at their endpoints, and provides a concrete killer example. A full theory of when such composites are valid — including a possibly weaker form of J0 that admits DEL-as-cleanup — belongs in a future ASN on composite validity rules.

### Topic 3: Auxiliary index maintenance under DELETE

The "Boundaries the abstract specification does not cross" section discusses stale auxiliary indices, permanent tree height, and orphan enumeration as implementation concerns outside DEL's scope. These are correctly out of scope; the abstract specification governs state components, not derived indices.

### Topic 4: Behavior of DEL composed with INSERT, COPY, REARRANGE

The Open Questions section asks about INSERT-after-DEL recovery and DEL-INSERT inverse properties. Per the scope clause, these operations' mechanics are out of scope; their interaction with DELETE belongs in a future composition ASN.

VERDICT: REVISE

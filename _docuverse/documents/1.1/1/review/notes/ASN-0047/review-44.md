# Review of ASN-0047

## REVISE

### Issue 1: K.δ descent case has incorrect zero-count formula

**ASN-0047, K.δ (Entity creation), Descent case**: "the increment introduces one (k = 1) or two (k = 2) zero separators on the way to e: `zeros(e) = zeros(t) + k`."

**Problem**: This contradicts TA5(d), which establishes that `inc(t, k)` for `k > 0` appends `k − 1` zeros and a final `1`. Concretely:
- `inc(t, 1)` appends `[1]` — zero zeros added, `zeros(e) = zeros(t)`
- `inc(t, 2)` appends `[0, 1]` — one zero added, `zeros(e) = zeros(t) + 1`

Worked check: from node `N` (zeros = 0), `inc(N, 2) = [N, 0, 1]` is an account (zeros = 1, not 2). The ASN's K.λ first-link case correctly applies `inc(t, 1)` without claiming a zero is added, confirming K.δ is the inconsistent site.

**Required**: Correct the formula to `zeros(e) = zeros(t) + (k − 1)` for `k ≥ 1`, and reconcile with TA5: `k = 1` introduces no zero separator (same-level extension, not descent); `k = 2` introduces one zero separator (one-level descent). If K.δ's "descent case" is intended to mean strict level-descent (zeros(e) > zeros(t)), `k = 1` should be excluded from the case altogether.

### Issue 2: K.μ~ definition is over-permissive relative to the realizable decomposition

**ASN-0047, K.μ~ precondition and Link-subspace fixity argument**: precondition states "π is subspace-preserving — `(A v ∈ dom(M(d)) :: subspace(π(v)) = subspace(v))`"; later derivation establishes that "no link-subspace positions are removed" under the K.μ⁺ amendment, forcing π to be identity on link-subspace V-positions.

**Problem**: The precondition admits any subspace-preserving bijection, including swaps within the link subspace (e.g., π([s_L,1,1]) = [s_L,1,2], π([s_L,1,2]) = [s_L,1,1] — subspace-preserving, satisfies D-CTG/D-MIN postconditions, CL-OWN unaffected since both addresses have the same origin). But the K.μ⁻ + K.μ⁺ decomposition cannot realize such a swap: K.μ⁻ would remove link-subspace positions and the amended K.μ⁺ (restricted to s_C) cannot restore them. The formal definition advertises flexibility the decomposition cannot deliver, leaving the reader able to specify admissible-looking but unrealizable K.μ~ transitions.

**Required**: Strengthen K.μ~'s precondition with an explicit clause `(A v ∈ dom(M(d)) : subspace(v) = s_L : π(v) = v)`, making link-subspace identity a precondition rather than a derived consequence. The derived-property presentation leaves the contract incoherent.

### Issue 3: T7 invocation in L14 derivation is logically redundant

**ASN-0047, L14 derivation**: "Hence s_C = s_L, contradicting SC-NEQ. By T7, addresses with distinct E₁ values are distinct, so no single a can witness both memberships."

**Problem**: T7 concerns the distinctness of *two* tumblers with different E₁ values. The L14 contradiction is at the level of single-valuedness — `fields(a).E₁` is a function and cannot simultaneously equal two distinct values `s_C` and `s_L`. The contradiction closes at "`s_C = s_L, contradicting SC-NEQ`"; T7 contributes nothing further.

**Required**: Remove the "By T7..." step from the derivation, or specify what T7 supplies that L0's two clauses plus SC-NEQ do not.

### Issue 4: K.δ for root nodes does not specify address allocation

**ASN-0047, K.δ (Entity creation)**: "For root nodes (IsNode(e)), no parent is required; node creation is the bootstrap case that seeds new branches of the hierarchy."

**Problem**: The non-root case anchors uniqueness in `e = inc(t, k)` plus T10a's GlobalUniqueness. For root nodes, no mechanism is given — neither how `e` is chosen nor what ensures `e ∉ E`. Σ₀ fixes one bootstrap `n₀`, but K.δ as written permits further root-node creation without specifying how a fresh, non-colliding root-node address is produced. The phrase "seeds new branches" suggests post-Σ₀ root nodes are intended.

**Required**: Either restrict K.δ so that only the bootstrap `n₀` is admissible as a root node (no post-Σ₀ root-node creation), or specify the allocation mechanism for root-node addresses and the corresponding uniqueness guarantee.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism (tombstoning vs presentational removal)

The ASN flags that D-CTG★ forbids interior link-subspace gaps, so Nelson's tombstoning design (LM 4/9) is not expressible as K.μ⁻ alone. The withdrawal mechanism (status flag, retraction link, etc.) is appropriately deferred and listed in Open Questions.

### Topic 2: Concrete realization strategies for K.μ~ content-subspace permutations

The "n' = 0 clear-and-rebuild" decomposition always works; whether more economical decompositions exist for specific permutations is an implementation concern, not an invariant of the transition model.

### Topic 3: Multi-version document arrangements and version DAG

M(d) is treated as a single arrangement per document. Version lineage, fork-on-version semantics beyond ex-nihilo vs J4 fork, and the version DAG's coupling to arrangement transitions belong to a future ASN.

### Topic 4: Concurrent allocation and serialization model

The ASN is sequential — Σ → Σ' is a single composite. Concurrency, allocator serialization, and inter-server protocol are out of scope.

VERDICT: REVISE

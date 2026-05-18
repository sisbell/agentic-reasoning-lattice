# Review of ASN-0047

## REVISE

### Issue 1: K.δ k=0 maximality precondition fails to isolate t's own allocator at "version of document" and deeper levels

**ASN-0047, Elementary transitions, K.δ case (ii) k = 0 (sibling)**: "`t = max{t' ∈ E : parent(t') = parent(e) ∧ zeros(t') = zeros(t) ∧ #t' = #t}`"

**Problem**: The maximality candidate set conflates sibling T10a allocators emitting at the same T4b-parent and length. Multiple version sub-allocators coexist in the same T4b-parent ∩ length ∩ zeros stratum. Concrete witness:

- Account `A = [1,0,1]`; documents `d₁ = [1,0,1,0,1]` and `d₂ = [1,0,1,0,2]` (both with T4b-parent = A, length #A + 2).
- Versions `v₁ = inc(d₁, 1) = [1,0,1,0,1,1]` and `v₂ = inc(d₂, 1) = [1,0,1,0,2,1]`. Both are documents (zeros = 2), both with T4b-parent = N(v).0.U(v) = [1,0,1] = A, both at length #A + 3.
- `A_v(d₁)` and `A_v(d₂)` are *distinct* T10a sub-allocators (siblings under `A_doc(A)` with different spawnPts), but the candidate set `{t' ∈ E : parent(t') = A ∧ zeros(t') = 2 ∧ #t' = #A + 3}` = `{v₁, v₂}` includes outputs from both.
- Since `d₁ < d₂`, `v₁ < v₂` under T1; max = `v₂`.
- K.δ k=0 with operand `v₁` (to extend `A_v(d₁)` with `v₁' = inc(v₁, 0)`) fails the maximality clause because `v₁ ≠ v₂`.

Once `v₂` enters E, `A_v(d₁)` cannot be extended further via K.δ k=0. The same defect recurs at every "version-of-X" level (versions of versions, etc.) where multiple `A_v(·)` sub-allocators coexist under a common T4b-parent. This contradicts Nelson's CREATENEWVERSION semantics (each document independently extends its own version chain) and the ASN's own text describing per-document version sub-allocators.

**Required**: Either (a) replace the maximality conjunct with a direct freshness predicate `inc(t, 0) ∉ E`, discharged via T10a's per-`(t, 0)` uniqueness on t's own allocator's chain (T10a's GlobalUniqueness covers freshness without needing the maximality framing); or (b) refine the candidate-set scope using a projection that distinguishes the `A_v(d_i)` sub-allocators (e.g., by truncating to the source document, beyond T4b's parent, which collapses to A).

### Issue 2: Logical fallacy in the inference justifying the #t' = #t conjunct

**ASN-0047, K.δ case (ii) k=0 commentary**: "By T10a.1 (UniformSiblingLength, ASN-0034) every T1 sibling-increment on a single allocator preserves length, so length partitions T4b-children-of-parent(e) into per-allocator strata"

**Problem**: The inference is invalid. T10a.1 establishes within-allocator length uniformity (siblings inside one allocator share length). It does not establish between-allocator length distinction. The conclusion "length partitions T4b-children-of-parent(e) into per-allocator strata" requires distinct allocators to have distinct lengths — but T10a tree-siblings (`A_v(d₁)`, `A_v(d₂)` as children of `A_doc(A)`) can have outputs at identical lengths, as Issue 1 demonstrates. T10a.3 (LengthSeparation) separates ancestor-descendant pairs by length, *not* tree-siblings.

The same paragraph says "Within that stratum the maximality conjunct identifies t as the *frontier* — the largest sibling already in E under the unique allocator emitting siblings of length #t with shared T4b-parent." The "unique allocator" claim is directly contradicted by the preceding sentence: "each existing document d under A spawns a version sub-allocator A_v(d)" — multiple sub-allocators, not unique.

**Required**: Remove or rewrite the inference. If the maximality clause is retained (per Issue 1 option b), the justification must accurately identify what the conjunct does and does not isolate. If maximality is replaced by direct freshness (Issue 1 option a), the entire paragraph can be removed.

### Issue 3: Forward-reference accretion in K.δ case (ii) k=0 precondition slot

**ASN-0047, K.δ case (ii) k=0 precondition block**: The paragraph starting "The ¬IsNode(t) conjunct is implied by..." and extending through several conjunct-by-conjunct justifications is essay content in a structural slot.

**Problem**: The precondition slot should state the precondition. This paragraph defensively justifies each conjunct ("required for parent(t) to be defined", "what isolates t's own allocator sub-stream", "supplant t's claim to frontier-ness", etc.), embeds the load-bearing (and incorrect per Issue 2) T10a.1 inference, and runs to many lines explaining the T4b-vs-T10a allocator distinction. This is essay content in a structural slot — defensive justification belongs in a rationale paragraph, not the formal specification of an operation's precondition.

**Required**: Move per-conjunct justification to a separate rationale paragraph or omit it. The precondition definition should be terse enough that a reader can extract the actual obligation without parsing essay-length defensive prose.

### Issue 4: K.μ⁻ effect clause "at least one subspace contracts strictly" treated as derivable, but only verified informally

**ASN-0047, K.μ⁻ amendment, "Per-subspace consequence of the effect clause"**: "`(E S ∈ {s_C, s_L} : V_S(d) ≠ ∅ : n'_S < n_S)` — at least one subspace shrinks strictly. This is a consequence of the whole-arrangement effect clause `dom(M'(d)) ⊂ dom(M(d))` combined with the per-subspace suffix pattern..."

**Problem**: The derivation states the consequence but doesn't show the calculation. Specifically: if both subspaces are empty in the pre-state (`V_{s_C}(d) = V_{s_L}(d) = ∅`), then `dom(M(d)) = ∅`, and `dom(M'(d)) ⊂ ∅` is impossible — K.μ⁻ cannot fire. The pre-state `dom(M(d)) ≠ ∅` is therefore a derived precondition, not stated explicitly. The "at least one subspace non-empty" condition is implicit. This warrants a one-line explicit note: K.μ⁻'s effect clause `dom(M'(d)) ⊂ dom(M(d))` forces `dom(M(d)) ≠ ∅`, which forces at least one `V_S(d) ≠ ∅`, which combined with the per-subspace patterns forces strict contraction on the non-empty subspace(s).

**Required**: State the chain explicitly so the empty-arrangement boundary case is visible, or add `dom(M(d)) ≠ ∅` as an explicit precondition of K.μ⁻.

### Issue 5: ExtendedReachableStateInvariants verification matrix uses "frame" without distinguishing K.μ⁺'s amended form for L

**ASN-0047, Class (a) verification matrix, L-fin row**: `K.α | frame; K.δ | frame; K.μ⁺ | frame; K.μ⁺_L | extends dom(L) by one (finite + 1 = finite); ...`

**Problem**: K.μ⁺'s frame on L is not part of the original K.μ⁺ definition in the four-component-state section — it is introduced only by the K.μ⁺ amendment's extended-state frame clause ("`L' = L`"). The matrix uses "frame" without indicating that this is a property the amendment supplies, not the original transition. A reader cross-checking the matrix against the original K.μ⁺ definition (where L doesn't appear) sees an inconsistency. Same issue for K.μ⁻'s "frame" entry under L0/L-fin/L3/L1 — the original K.μ⁻ predates the link store, and the `L' = L` conjunct is contributed by the K.μ⁻ amendment.

**Required**: Either mark "frame" entries with a footnote indicating which definition supplies the frame conjunct, or rewrite the matrix prose to state that the K.μ⁺ and K.μ⁻ entries refer to the amended forms.

## OUT_OF_SCOPE

The Open Questions appropriately defer topics belonging to future ASNs (forking arrangement structure, link withdrawal mechanisms, transitive transclusion provenance, concurrency, registry protocols, account-level versioning). The Scope section's exclusions are well-aligned with the ASN's claimed scope.

META: [no meta concern — the ASN remains an abstract state/transition specification appropriate to its layer]

VERDICT: REVISE

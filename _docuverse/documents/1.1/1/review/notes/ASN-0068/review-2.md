# Review of ASN-0068

## REVISE

### Issue 1: CV-IN's subspace constraint is informally claimed but not formally enforced

**ASN-0068, CV-IN**: "Every span in `R_a` and every span in `R_b` lies within a single common subspace `S ∈ {s_C, s_L}`, the same `S` for both. ... Every span `σ ∈ R_a` satisfies `start(σ) ∈ V_S(d_a)` and is level-uniform at depth `m_a := m_{d_a, S}`"

**Problem**: The informal "lies within a single common subspace" is strictly stronger than what the formal precondition delivers. Level-uniformity (S6) requires only `#start(σ) = #width(σ)`; it does not constrain `actionPoint(width(σ))`. When `actionPoint(width(σ)) = 1`, by TumblerAdd the first component of `reach(σ)` is `start(σ)₁ + width(σ)₁ > S`, so `⟦σ⟧` extends into subspaces with identifier > S. Concretely, with `m_a = 2`, `start(σ) = [1, 5]` and `width(σ) = [2, 0]` gives `reach(σ) = [3, 5]`, and `⟦σ⟧` denotes positions across subspaces 1 and 2. The relation `corr_{a,b}` happens to filter these out via L0 + L14 (cross-subspace I-addresses can't coincide), but this is a consequence of storage structure, not of the precondition.

**Required**: Either tighten CV-IN to require `actionPoint(width(σ)) ≥ 2` (equivalently, width is an ordinal displacement at depth `m_a`, matching ASN-0058's C0 derivation for content references), or rewrite the informal sentence to acknowledge the precondition only constrains `start(σ)` and the in-subspace property is delivered by the relation's structure.

### Issue 2: Logical error in CV-MAX uniqueness proof's `δ − 1 ≥ 0` step

**ASN-0068, CV-MAX uniqueness, Case δ > 0**: "From `k¹ − k² = δ` and `k¹ < n¹` we get `k² + δ = k¹ < n¹`, hence `δ − 1 < n¹ − k² ≤ n¹`, and since `k² ≥ 0`, also `δ − 1 ≥ 0`."

**Problem**: `k² ≥ 0` does not imply `δ − 1 ≥ 0`. The justification for `δ − 1 ≥ 0` is the case hypothesis `δ > 0` together with `δ ∈ ℤ` (since `δ = j²_a − j¹_a` is a difference of integers), which gives `δ ≥ 1`, hence `δ − 1 ≥ 0`. The current sentence attributes the conclusion to the wrong premise.

**Required**: Replace "since `k² ≥ 0`" with "since `δ > 0` and `δ ∈ ℤ` (as `δ = j²_a − j¹_a` is a difference of natural numbers), so `δ ≥ 1`".

### Issue 3: "Valid V-predecessor" definition is dense and admits two readings

**ASN-0068, Correspondence run maximality**: "(Here 'valid V-predecessor at depth `m`' means the unique tumbler `v'` of depth `m` with `v' + 1 = v`, if such exists at depth `m` within the relevant subspace. ...)"

**Problem**: "Exists at depth `m` within the relevant subspace" is ambiguous: it could mean (a) `v'` exists as a tumbler in T at depth `m` — which is always true for any depth-`m` `v` with a defined OrdinalShift predecessor formula, OR (b) `v'` is a valid V-position (positive components, in V_S(d)). For `v = [S, 1, ..., 1, 1]`, the depth-`m` "predecessor" `[S, 1, ..., 1, 0]` exists as a tumbler in T but is not a V-position (S8a forbids the zero last component). The proof's left-walk relies on interpretation (b); the maximality conditions in the run definition should state this directly.

**Required**: Replace the parenthetical with: "'valid V-predecessor of `v` at depth `m`' is the unique V-position `v'` of depth `m` with `v' + 1 = v`. For `v = [S, 1, ..., 1, k]` in subspace `S`, this is `[S, 1, ..., 1, k − 1]` when `k ≥ 2`, and undefined when `k = 1` (since `[S, 1, ..., 1, 0]` violates S8a)."

### Issue 4: Existence proof's left walk at `i = 0` is vacuous and confusing

**ASN-0068, CV-MAX existence**: "Walking left, let `j ≥ 0` be the largest count of valid backward steps from `(v_a, v_b)` — i.e., such that for all `0 ≤ i ≤ j`, the V-predecessors `(v_a − i, v_b − i)` exist within their restrictions and remain pointwise correspondent."

**Problem**: At `i = 0`, `(v_a − 0, v_b − 0) = (v_a, v_b)` is the starting pair, not a "V-predecessor" of anything; the condition is vacuously satisfied since the pair is given to be in `corr_{a,b}`. The phrasing makes the proof's invariant harder to verify (which step is at the boundary?). Quantifying over `1 ≤ i ≤ j` would be cleaner.

**Required**: Reword as: "let `j ≥ 0` be the largest value such that for all `1 ≤ i ≤ j`, the V-predecessors `v_a − i` and `v_b − i` exist as V-positions within `⟦R_a⟧ ∩ dom(M(d_a))` and `⟦R_b⟧ ∩ dom(M(d_b))` respectively, with `M(d_a)(v_a − i) = M(d_b)(v_b − i)`. (Termination of the walk is forced by S8-fin.)"

### Issue 5: Right- and left-maximality of the constructed run not explicitly tied back to walk termination

**ASN-0068, CV-MAX existence**: "right-maximality holds because extending by one more right step contradicts the choice of `n_R`; left-maximality holds because extending by one more left step contradicts the choice of `j`."

**Problem**: The constructed run starts at `(v_a − j, v_b − j)` with width `j + n_R`, but `n_R` and `j` were chosen relative to `(v_a, v_b)`, not relative to the new start. The reader must perform an offset translation (right-extension of the new run at offset `j + n_R` ≡ right-walk step `n_R` from the original) to confirm the contradiction. Make this translation explicit.

**Required**: Add one sentence stating the index correspondence — e.g., "right-extension of the constructed run to width `j + n_R + 1` is the assertion that the pair `(v_a + n_R, v_b + n_R)` satisfies the run conditions, which is precisely what `n_R`'s maximality denies; symmetrically, left-extension is the pair `(v_a − j − 1, v_b − j − 1)`, denied by `j`'s maximality."

### Issue 6: CV-ATOM, CV-RO, CV-DETERM are stated as separate claims but derived only informally

**ASN-0068, CV-ATOM**: "A correspondence run of width `n = 1` is admissible and is preserved as a maximal element of the result whenever it satisfies maximality..." (No proof.)

**ASN-0068, CV-RO**: "This is structurally guaranteed by the operation's signature: it produces a `Result` value and has no side-effecting clauses in its specification." (Argument by inspection.)

**ASN-0068, CV-DETERM**: "This follows from the uniqueness of the maximal decomposition (CV-MAX)." (One-line derivation.)

**Problem**: Each is a labeled claim suggesting a theorem-grade obligation, but the supporting text is informal description rather than derivation. CV-ATOM in particular makes three negative existence claims ("no minimum-quotation-length cutoff", "no merge-window heuristic", "no block-alignment constraint") that should be derived from the absence of any filtering or aggregation clause in the run definition together with CV-MAX's witnessing property.

**Required**: Either fold each into the text as a remark or note rather than a labeled claim, or supply explicit one-paragraph derivations: CV-ATOM from "the run definition admits `n ≥ 1` and the maximality condition imposes no width threshold, so every isolated pair in `corr_{a,b}` produces a width-1 maximal run by CV-MAX"; CV-RO from "the operation's specification clauses are all of the form `Result := ...` and reference only state, not modify it"; CV-DETERM from "CV-MAX establishes uniqueness of `MaxRuns`, and `MaxRuns` is determined by `M(d_a)`, `M(d_b)`, `R_a`, `R_b`, all of which are determined by state and input."

### Issue 7: Empty input case is a footnote rather than a formal claim

**ASN-0068, after CV-MAX uniqueness**: "*Empty inputs.* The proof and the operation are well-defined on the boundary cases. If either restriction has empty denotation ... then `corr_{a,b} = ∅`, no run conditions can be satisfied, and `MaxRuns(d_a, R_a, d_b, R_b) = ∅`."

**Problem**: This is the most common boundary the operation faces (e.g., fresh forks, never-arranged subspaces), and it is buried as a remark without a label. Worth a named claim or corollary so consumers can cite it.

**Required**: Promote to a labeled claim (e.g., CV-EMPTY) with the form: "When `⟦R_a⟧ ∩ dom(M(d_a)) = ∅` or `⟦R_b⟧ ∩ dom(M(d_b)) = ∅`, `MaxRuns(d_a, R_a, d_b, R_b) = ∅`." Include in the claims table.

### Issue 8: Equivalence `Result ≅ P(Span × Span)` claimed without specifying the dependency

**ASN-0068, "The Input"**: "Equivalently (presentational, not semantic), `Result ≅ P(T × T × ℕ⁺) ≅ P(Span × Span)` via the projection introduced after CV-MAX."

**Problem**: The bijection between `(v_a, v_b, n)` and span-pairs depends on knowing `m_a` and `m_b`, since the projection uses `δ(n, m_a)` and `δ(n, m_b)`. These are determined by `d_a, d_b, S`, but the isomorphism is therefore not universal — it is parameterized by the input. The reader should not have to derive this.

**Required**: Restate as: "Equivalently, given `m_a, m_b` fixed by the input (S8-depth applied to `d_a, d_b` in subspace `S`), `Result` is in bijection with a subset of `Span × Span` via `(v_a, v_b, n) ↔ ((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))`."

### Issue 9: Self-comparison with differing restrictions not explicitly addressed

**ASN-0068, after CV-IN**: "*Self-comparison is admissible.* CV-IN does not exclude `d_a = d_b`. When invoked with both operands referring to the same document ... `corr_{a,a}` contains every pair `(v¹, v²) ∈ (⟦R_a⟧ ∩ dom(M(d))) × (⟦R_b⟧ ∩ dom(M(d)))` with `M(d)(v¹) = M(d)(v²)`."

**Problem**: The discussion treats the self-comparison case as a single configuration but only briefly notes the per-position behaviour. The case `d_a = d_b` with `R_a ≠ R_b` is admissible and produces an asymmetric restriction over the same arrangement; the resulting `MaxRuns` can contain identity pairs only on `⟦R_a⟧ ∩ ⟦R_b⟧` and one-sided self-transclusion pairs elsewhere. Worth stating this explicitly rather than leaving it to the reader.

**Required**: Add a sentence covering `R_a ≠ R_b`: "When `d_a = d_b` and `R_a ≠ R_b`, identity pairs `(v, v)` arise only at `v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ dom(M(d))`; pairs witnessing self-transclusion `(v¹, v²)` with `v¹ ≠ v²` are admitted whenever `v¹ ∈ ⟦R_a⟧`, `v² ∈ ⟦R_b⟧`, and both lie in `dom(M(d))` with `M(d)(v¹) = M(d)(v²)`."

### Issue 10: Result type omits the shared I-address; design choice unstated

**ASN-0068, "The Result"**: `Result := P(T × T × ℕ⁺)` — triples `(v_a, v_b, n)`.

**Problem**: The triple records V-positions and width but not the shared I-address `M(d_a)(v_a + k)`. A consumer needing the I-address must query state. This is a reasonable design (the result is interpreted in conjunction with `M`), but no justification is given. Worth one sentence explaining why the I-address is omitted — e.g., it would duplicate state-derivable information, and the V-position pair is what callers need for rendering. Alternatively, justify the symmetric presentation as `(span_a, span_b)` (after the projection) which similarly omits the I-address.

**Required**: Add a brief justification after the Result definition: e.g., "The shared I-address at offset `k` is derivable as `M(d_a)(v_a + k)` (equivalently `M(d_b)(v_b + k)`); the result triple omits it to avoid duplicating state-derivable information."

## OUT_OF_SCOPE

### Topic 1: Concurrent arrangement modification mid-comparison
**Why out of scope**: First open question explicitly defers this. Concurrency semantics belong in a future ASN governing transition serialization.

### Topic 2: Replication consistency guarantees across docuverse copies
**Why out of scope**: Second open question defers. Replication protocol (BEBE) is explicitly out of scope per review instructions.

### Topic 3: Sub-allocator boundary semantics within a single run
**Why out of scope**: Third open question defers. Whether a run spanning multiple sub-allocator outputs imposes additional invariants is a future investigation.

### Topic 4: Composed multi-document correspondence and history traversal
**Why out of scope**: Sixth and eighth open questions defer. The pairwise scope is asserted and explained; multi-document composition is its own structure.

### Topic 5: Result presentation with bounded total V-width
**Why out of scope**: Tenth open question defers. Performance bounds on the result representation belong with implementation considerations.

VERDICT: REVISE

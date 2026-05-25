# Review of ASN-0068

## REVISE

### Issue 1: CV-EMPTY motivation conflicts with CV-IN admissibility

**ASN-0068, CV-EMPTY justification**: "This boundary is the most common practical input shape: a fresh fork (whose target document's arrangement is empty per K.δ's effect on M), or a comparison restricted to a subspace that one of the documents has never populated. The operation produces the correct result `∅` without exception or special-case handling."

**Problem**: CV-IN requires `start(σ) ∈ V_S(d_a)` for every `σ ∈ R_a`. When `V_S(d_a) = ∅` (fresh fork created by K.δ, or untouched subspace), this clause can be satisfied only vacuously — i.e., by `R_a = ⟨⟩`. Any non-empty `R_a` is inadmissible against an empty subspace, contradicting the "without exception or special-case handling" claim. Additionally, `m_a := m_{d_a, S}` is supplied by S8-depth (ASN-0036) only when `V_S(d_a) ≠ ∅`; for empty subspaces `m_a` is undefined, but the CV-IN per-span clauses reference `m_a` unconditionally.

**Required**: State explicitly that comparisons against an empty subspace require `R_a = ⟨⟩` (and symmetrically for `R_b`), and clarify that `m_a` is well-defined precisely when `V_S(d_a) ≠ ∅` or, when `R_a = ⟨⟩`, is not consulted. Alternatively, relax CV-IN to admit non-empty `R_a` whose starts have the required structural form (depth-`m_σ`, leading components `[S, 1, ..., 1, ...]`) without requiring membership in `V_S(d_a)` — but this relaxation would need to supply `m_σ` operationally rather than from S8-depth, requiring an additional input.

### Issue 2: "Valid V-predecessor" notation introduced inline rather than as a labeled claim

**ASN-0068, definition of maximal correspondence run**: "Here 'valid V-predecessor of `v` at depth `m`' is the unique V-position `v'` of depth `m` with `v' + 1 = v`... We extend the notation to iterated predecessors: for `j ≥ 1`, the *j-th iterated V-predecessor* `v − j` is the unique V-position `v'` of depth `m` with `v' + j = v`..."

**Problem**: The predecessor notation is load-bearing throughout the CV-MAX existence and uniqueness proofs, the maximality definitions, and the worked examples. It is introduced parenthetically rather than as a labeled definition with explicit existence/uniqueness/inverse postconditions. The proof of uniqueness for iterated predecessors is given as "lifts from TS2 via the same induction that grounds existence" without a worked induction; the inverse property `(v − j) + j = v` is stated as "immediate from the defining equation" without the dual step `j + (v − j) = v` (which the proof actually uses via M-aux). Existence at `j = 0` (the convention `v − 0 := v`) is stated but not connected to the j ≥ 1 case, so the M-aux applications in the existence proof at boundary `i = j` or `c = 0` are not explicitly grounded.

**Required**: Promote the predecessor notation to a labeled definition (e.g., **CV-PRED**) with explicit clauses: existence (when `v_m ≥ j + 1`), uniqueness (via TS2 induction), inverse property `(v − j) + j = v`, dual inverse property, and the `j = 0` convention. The proof obligations then have a single citable referent.

### Issue 3: CV-MAX existence proof leans on S8-fin for left-walk termination when D-SEQ★ + S8a give a direct bound

**ASN-0068, CV-MAX existence proof**: "Termination of the walk is forced by S8-fin: `dom(M(d_a))` is finite, so the descending chain of valid predecessors is bounded."

**Problem**: The left walk's termination has a more direct argument than appeal to S8-fin. Each predecessor step decreases the last component of `v_a` by 1 (D-SEQ★, ASN-0047), and the last component is a positive natural number ≥ 1 (S8a, ASN-0036). The chain `v_a, v_a − 1, v_a − 2, ...` therefore has length at most `(v_a)_{m_a} − 1`, a concrete finite bound determined by the starting position alone. The S8-fin appeal is correct but indirect — it bounds termination by global finiteness when local structural bounds suffice. The proof should cite the local argument so the reader can reproduce the bound without reference to global cardinality.

**Required**: Replace "Termination of the walk is forced by S8-fin" with a direct argument from D-SEQ★ + S8a: the last component of the iterated predecessor decreases by 1 at each step, and is bounded below by 1, so the walk terminates in at most `(v_a)_{m_a} − 1` steps.

### Issue 4: CV-ATOM's derivation is structurally a proof-by-absence

**ASN-0068, CV-ATOM derivation**: "The maximality conditions impose no width threshold; they reference only the existence and correspondence of the immediate neighbors `(v_a ± 1, v_b ± 1)`... No clause of the operation's specification mentions a width threshold, a merge window, or a block-alignment offset; the absence of such clauses is what rules them out."

**Problem**: CV-ATOM is established by enumerating what the operation does *not* contain. While this is a valid mode of derivation for an abstract specification, the structure makes the claim fragile: any subsequent ASN that adds a threshold or merge-window clause would silently invalidate CV-ATOM without flagging the dependency. The claim should instead be derived positively from CV-MAX. Specifically: (a) the run definition admits any `n ≥ 1`; (b) CV-MAX guarantees that every pair `(v_a, v_b) ∈ corr_{a,b}` is witnessed by exactly one maximal run; (c) when the immediate neighbors of `(v_a, v_b)` either fail to exist in the restrictions or fail correspondence, the witnessing run has width 1; (d) maximality therefore admits width-1 runs *and* aggregates contiguous matches into wider runs — both behaviors flow from a single uniqueness principle. The current phrasing reads as architectural commentary rather than derivation.

**Required**: Restate CV-ATOM's derivation as positive consequences of the run definition + CV-MAX, rather than as the absence of width-threshold clauses. The byte-granular claim is then a corollary of the existence + uniqueness of width-1 runs whenever the pair has non-correspondent neighbors.

### Issue 5: Result type's bijection with `P(Span × Span)` is unlabeled but referenced

**ASN-0068, operation signature**: "Equivalently, *given a fixed admissible input* `(d_a, R_a, d_b, R_b)` that determines `m_a, m_b` by S8-depth (ASN-0036), `Result` is in bijection with a subset of `P(Span × Span)` via the projection `(v_a, v_b, n) ↔ ((v_a, δ(n, m_a)), (v_b, δ(n, m_b)))` introduced after CV-MAX. The bijection is parameterized by `(m_a, m_b)`; it is not a universal isomorphism on `Result`."

**Problem**: This is a substantive structural claim — that each correspondence run projects to a well-formed pair of level-uniform V-spans — but it is presented without a claim label and without verification that the span pair is admissible (the well-formedness check appears later, in the discussion after CV-MAX, but is not cross-referenced from the signature). The bijection claim depends on `(m_a, m_b)` being well-defined (Issue 1), and the result of the projection must satisfy the level-uniformity and T12 well-formedness conditions of ASN-0053. The claim should be labeled and the verification consolidated.

**Required**: Promote the projection bijection to a labeled corollary (e.g., **CV-SPAN-VIEW**) with explicit postconditions: (a) each run `(v_a, v_b, n)` projects to a pair of well-formed level-uniform spans at depths `m_a, m_b`; (b) the projection is injective on `MaxRuns`; (c) the parameterization by `(m_a, m_b)` makes this an input-dependent presentational equivalence, not a universal isomorphism on the result type.

### Issue 6: Concrete examples do not exercise differing depths

**ASN-0068, worked examples**: All three examples use `m_a = m_b = 2`.

**Problem**: A central CV-IN clause is "We do *not* require `m_a = m_b`." This is a substantive design commitment — the operation handles documents whose V-positions live at structurally different depths. None of the three worked examples exercises `m_a ≠ m_b`. A reader following the verification path against the examples cannot directly check that the walks `v_a + k` (at depth `m_a`) and `v_b + k` (at depth `m_b`) compose correctly when the depths differ. The proof handles this case symbolically, but examples carry the load of grounding the proof's notation against concrete addresses, and the absence is conspicuous.

**Required**: Add an example with `m_a ≠ m_b` (e.g., `m_a = 2`, `m_b = 3`) showing that the walks proceed in lockstep on per-side offsets despite the depth mismatch, and that the projected spans (CV-SPAN-VIEW) have different widths in tumbler form but the same ordinal count `n`.

### Issue 7: Self-comparison discussion lacks a labeled claim

**ASN-0068, Self-comparison paragraph**: "When `R_a = R_b`, every occupied position `v` produces an identity pair `(v, v)`, and each self-transclusion within the restriction produces additional off-diagonal pairs. When `R_a ≠ R_b`, identity pairs `(v, v)` arise only at `v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ dom(M(d))`; pairs witnessing self-transclusion `(v¹, v²)` with `v¹ ≠ v²` are admitted whenever `v¹ ∈ ⟦R_a⟧`, `v² ∈ ⟦R_b⟧`..."

**Problem**: Self-comparison is admitted by CV-IN and exemplified by Example 3, but the structural claim about the relation's shape (identity diagonal + self-transclusion off-diagonal pairs, partitioned by restriction structure) is presented as discussion rather than a labeled claim. CV-LINK-SELF gives the link-subspace specialization, but the content-subspace self-comparison case has no analogous labeled claim, making it harder to invoke this structural property downstream.

**Required**: Add a labeled claim (e.g., **CV-SELF**) characterizing the structure of `corr_{a,a}` for the content subspace: the diagonal `{(v, v) : v ∈ ⟦R_a⟧ ∩ ⟦R_b⟧ ∩ dom(M(d))}` is always included, and additional off-diagonal pairs arise exactly from self-transclusion patterns in `M(d)`.

## OUT_OF_SCOPE

### Topic 1: Concurrent modification during comparison

The open questions section asks about concurrent arrangement modification mid-comparison. The transition model (ASN-0047, SequentialTransitionAxiom) commits to single-event sequential transitions, so concurrency is not formally modeled at this layer. Concurrent semantics belong in a future ASN that extends the transition model.

### Topic 2: Replication and inter-server protocol (BEBE)

Open questions about result identity across replicated copies of the docuverse fall outside the abstract operation's scope. Replication is a separate concern from the operation's structural semantics.

### Topic 3: Cross-allocator-boundary runs

The open question about runs whose I-addresses span sub-allocator boundaries (consecutive V-offsets mapped to I-addresses with different `origin`) is a forward question about the interaction between maximal runs and attribution. The current ASN correctly admits such runs (the correspondence relation does not constrain `origin`); a future ASN may need to specify how renderers attribute such runs.

### Topic 4: Performance bounds and bounded representation

Questions about bounding shared content size without exhaustive enumeration are implementation-relevant performance concerns, not abstract structural claims.

### Topic 5: Multi-document correspondence composition

Open questions about composing multiple pairwise comparisons into multi-document correspondences are deliberately deferred — the operation is pairwise by design, and multi-way generalization is a separate construction.

VERDICT: REVISE

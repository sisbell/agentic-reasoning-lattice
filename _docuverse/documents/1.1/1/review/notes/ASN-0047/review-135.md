# Review of ASN-0047

## REVISE

### Issue 1: FrontierEquivalence lemma proof is informal

**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation***: "**FrontierEquivalence (Lemma).** For every reachable state `Σ` and every operand `t ∈ Σ.E` with `¬IsNode(t)`: `inc(t, 0) ∉ Σ.E ⟺ t is the frontier of its sub-allocator's (t, 0)-branch`"

**Problem**: The lemma is load-bearing — cited by K.δ case (ii) k=0 discharge, by the S4 row of the verification matrix, and indirectly by every K.δ k=0 worked example. Yet the body provides no separated forward (⟹) and reverse (⟸) direction proofs. Instead the text interleaves discussion of T10a.7 versus TA5(c), a counterexample to T4b-based identification, and the three "load-bearing premises," ending with "Together, (i)–(iii) make `inc(t, 0) ∉ E` logically equivalent..." — but the chain of reasoning from premises to biconditional is not explicit.

**Required**: Restructure as two explicit proofs. Forward: assume `inc(t, 0) ∉ E`; by contrapositive on T10a chain-advancement uniqueness at (t, 0) and P1's E-monotonicity, no prior K.δ event has fired (t, 0) on t's sub-allocator chain, hence t is the frontier. Reverse: assume t is the frontier (no prior firing of (t, 0)); by T10a.6 cross-allocator domain disjointness, no other allocator could produce inc(t, 0); hence inc(t, 0) ∉ E.

### Issue 2: K.μ~ admissible π existence is asserted but not constructed

**ASN-0047, *Decomposition of K.μ~***: "the existence of a non-identity bijection at `|dom_C(M(d))| ≥ 2` is itself a sufficiency obligation the operation discharges by exhibiting an admissible `π`"

**Problem**: This is the sufficiency half of the necessary-and-sufficient existence condition (|dom_C(M(d))| ≥ 2 ⟺ admissible π exists). Necessity is proved by ruling out the empty, singleton, and mixed cases. Sufficiency is asserted to be "discharged operationally" but no explicit construction is given. A reader cannot verify the sufficiency claim without performing the construction themselves.

**Required**: Give an explicit construction. For example: given the precondition |dom_C(M(d))| ≥ 2, pick distinct v₁, v₂ ∈ dom_C(M(d)) and define π as the transposition swapping v₁ ↔ v₂ while fixing every other element. Verify admissibility: subspace-preserving (v₁, v₂ both content-subspace); K.μ~-FIX gives dom(M'(d)) = dom(M(d)), so S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, S3★ all transfer from pre-state; π ≠ id since π(v₁) = v₂ ≠ v₁. Existence proved.

### Issue 3: K.δ case (ii) k=2 sub-case A2 induction is implicit

**ASN-0047, *K.δ case (ii) discharge*, sub-case A2**: "The K.δ event that minted `t` was a K.δ case (ii) k = 0 event with operand a prior sibling account `t_prev`... The chain of K.δ k = 0 events back through `t_prev, t_prev_prev, …` is finite (the system history up to the present state is finite) and terminates at the first account under `parent(t)`, dispatched by sub-case A1."

**Problem**: The termination argument relies on well-foundedness of transition history but the induction principle is not stated explicitly. "System history is finite" is correct but doesn't by itself frame the induction structure; the reader has to supply: the natural induction here is on t's position in the A_account(parent(t)) sibling-increment chain (a natural number bounded by transition history). Without stating this, the recursive sub-case dispatch reads as potentially circular.

**Required**: State the induction principle. The argument is induction on the chain position n ≥ 0 of t in A_account(parent(t))'s emission sequence. Base case (n = 0): t is the first emission, placed by K.δ k=2 (sub-case A1). Inductive step (n ≥ 1): t = inc(t_{n-1}, 0) was placed by K.δ k=0 with operand t_{n-1}; by induction on n, the dispatch on t_{n-1} (which has chain position n-1) terminates. Chain position is bounded by the number of K.δ events in the system history, so the induction is well-founded.

### Issue 4: D-SEQ★ derivation - depth-sharing inference step is asserted without proof

**ASN-0047, *Amendments to existing transitions*, D-SEQ★ derivation, m ≥ 3 case, Step 2 (terminal contiguity)**: "S8-depth at Σ' inherits m_S from the surviving V-positions of Σ — restriction cannot alter the depth of any survivor — making V_S(d') and V_S(d) share the same canonical D-SEQ★ shape; set inclusion V_S(d') ⊆ V_S(d) then reduces to comparison of the trailing-component bound, forcing n'_S ≤ n_S."

**Problem**: The step from "V_S(d') ⊆ V_S(d) with both in canonical form" to "n'_S ≤ n_S" is asserted via "comparison of the trailing-component bound" but the comparison is not made explicit. Similarly, in the reverse direction of K.μ⁻ admissible contraction shape, the same inference is invoked.

**Required**: Make the comparison explicit. V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S} and V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S} are both canonical D-SEQ★ shapes of depth m_S. The map k ↦ [S, 1, ..., 1, k] is a bijection between {1, ..., n_S} and V_S(d) (and similarly between {1, ..., n'_S} and V_S(d')). V_S(d') ⊆ V_S(d) translates under this bijection to {1, ..., n'_S} ⊆ {1, ..., n_S}, which forces n'_S ≤ n_S directly.

### Issue 5: K.μ~ dependency chain Steps (A)-(E) lack explicit proofs

**ASN-0047, *Decomposition of K.μ~*, Dependency chain at a glance**: "*Step (A) — S3★(Σ') and admissibility clause (i)*", "*Step (B) — Subspace preservation under π*", etc., with Consumes/Produces relations enumerated.

**Problem**: The dependency chain claims non-circularity by listing what each step consumes and produces, but the actual proofs of Steps (A) and (B) are not separated in the body. The proof of S3★(Σ') under K.μ~ is given in the verification matrix as "preserved via K.μ⁻ restriction + K.μ⁺ amendment alone (link-subspace fixity is downstream, not prerequisite)" — but the substantive derivation is not unpacked. Step (B)'s case-split on `s_C → s_L` and `s_L → s_C` is given, but it relies on Step (A)'s S3★(Σ') without separation.

**Required**: Supply explicit per-step proofs that match the dependency-chain claims. Step (A): show S3★(Σ') from the K.μ⁻ + K.μ⁺ decomposition without invoking subspace preservation. Step (B): given S3★(Σ) and S3★(Σ'), prove subspace preservation. Step (C): given subspace preservation, prove the functional identity M'(d)|_{dom_L} = M(d)|_{dom_L}. Step (D): given the functional identity and CL-UNIQ at Σ, prove pointwise fixity. The current text gives these proofs but interleaved; separating them would make the non-circularity verifiable rather than asserted.

### Issue 6: L14 derivation chain inconsistency across the ASN

**ASN-0047, *Link store and extended system state***: The L14 derivation chain is announced as "L0 + SC-NEQ + T7" with three premises listed. **ASN-0047, the prose paragraph immediately following**: "Chaining: suppose a ∈ dom(C) ∩ dom(L). By L0's C-clause, subspace_I(a) = s_C; by L0's L-clause, subspace_I(a) = s_L. Since subspace_I(a) is a single value for a single tumbler, s_C = s_L, contradicting SC-NEQ."

**Problem**: The actual derivation invokes single-value-ness of subspace_I plus SC-NEQ, not T7. T7's role (as FirstElementFieldDistinction) is to *establish* the partition that L0 records — but L14's contradiction follows from L0's two clauses being incompatible at a single tumbler, not from T7's distinct-tumbler conclusion. Naming T7 in the chain heading but not invoking it in the derivation creates a misleading impression of what's load-bearing.

**Required**: Either drop T7 from the L14 derivation chain (since the contradiction follows from L0 + single-value subspace_I + SC-NEQ alone), or restructure the derivation to actually use T7 (treating dom(C) and dom(L) members as distinct tumblers via T7's distinctness). The current text claims T7 is a premise but the proof doesn't consume it.

### Issue 7: Verification matrix - some cells require non-trivial expansion

**ASN-0047, *Class (a) verification matrix***: For example, the K.μ~ entries reference "Steps 1–3 of the link-subspace fixity proof" (for S8★ and CL-UNIQ), or "inherits via the K.μ⁻ + K.μ⁺ decomposition" (for several invariants). The K.δ entries reference T10a discharge chains spanning sub-cases A1/A2/B/C.

**Problem**: While the matrix-preamble note says "The matrix is a navigational index; each cell summarises the load-bearing argument," several cells reference substantive machinery (multi-step decompositions, case-split chains) that requires the reader to perform non-trivial deductive work. A reader cannot rely on the matrix as a verification artifact without consulting the body prose for each non-trivial cell.

**Required**: Either expand the most non-trivial cells inline (S2 for K.μ⁺, S3★ for K.μ~, S8★ for K.μ~), or add a more visible cross-reference convention (e.g., "[§K.μ~-Step3]") so a reader knows exactly which body paragraph substantiates each cell.

### Issue 8: ASN size and scope coherence

**ASN-0047 (whole document)**: The ASN spans state model definition, seven elementary transitions, multiple named composites, coupling constraints, ~30 invariants, several lemmas (FrontierEquivalence, CrossDocDisjoint, K.μ~ link-subspace fixity, GlobalLineage), multiple worked examples, a 30-row verification matrix, and three Properties Introduced tables.

**Problem**: A single ASN of this size is hard to review systematically. The argument structure is sound in most places, but the density makes it difficult to isolate verification claims. Some sections (the K.μ~ link-subspace fixity proof, the CrossDocDisjoint lemma, the K.δ case (ii) k=2 sub-case discharge tree) are substantial enough to warrant standalone treatment.

**Required**: Consider splitting. Candidates for extraction: (a) K.μ~ admissibility and link-subspace fixity as a standalone lemma ASN; (b) CrossDocDisjoint lemma as a standalone ASN under tumbler algebra; (c) worked examples as a companion ASN; (d) the verification matrix as a verification companion. This is presentation rather than correctness, but the current scope makes thorough review materially harder.

## OUT_OF_SCOPE

### Topic 1: User-facing operations (INSERT, DELETE, COPY, REARRANGE, MAKELINK, CREATENEWVERSION, DELETEVSPAN)

The ASN scope explicitly excludes named operations. The elementary transitions K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ and named composites K.μ~, J4 are the abstract primitives; binding these to user-level operations is downstream work.

### Topic 2: Atomicity at protocol level

SequentialTransitionAxiom posits atomicity of elementary transitions, but the protocol-level atomicity of composites (whether a fork is observable mid-composite by other agents) is explicitly out of scope.

### Topic 3: Authorization model (BERT, ownership, publication state)

Explicitly out of scope. Operations on entities and content are specified without reference to access control.

### Topic 4: Concurrency model

SequentialTransitionAxiom totally orders transitions; multi-agent concurrent execution and serialization protocols are out of scope.

### Topic 5: Interior link withdrawal mechanism

The ASN notes (in Open Questions) that tombstoning of withdrawn links per Nelson (LM 4/9) requires a separate mechanism orthogonal to K.μ⁻'s presentational-removal contract — a per-link status flag, retraction-link convention, or version-scoped membership. This is correctly deferred.

### Topic 6: Node-allocation registry protocol

NodeUniqueAllocation is treated as an axiom abstracting Nelson's hierarchical baptism / Gregory's granfilade; the registry mechanism is correctly left to a future ASN.

VERDICT: REVISE

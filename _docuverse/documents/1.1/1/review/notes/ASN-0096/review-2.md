# Review of ASN-0096

## REVISE

### Issue 1: LP-EXT headline statement is contradicted by the worked example
**ASN-0096, "What Displaces — The Moving Frame" (LP-EXT)**: "For any endset `e`: `proj(e, d, Σ') ⊇ proj(e, d, Σ)`"
**Problem**: The worked example transitions Σ₀ → Σ₁ via INSERT with `proj(e₁, d, Σ₀) = {1.2, 1.3, 1.4}` and `proj(e₁, d, Σ₁) = {1.2, 1.5, 1.6}`. These are not in superset relation: `1.3 ∈ Σ₀ proj` but `1.3 ∉ Σ₁ proj`. The ASN itself admits this immediately after the headline: "The pure LP-EXT statement holds when the new mappings are appended without disturbing existing V-positions." So the headline claim, as cited by LP-MAP / LP-SURV / the claims table, is false for the common case of mid-subspace INSERT.
**Required**: Either restate LP-EXT as the composed form (`proj(e, d, Σ') = π(proj(e, d, Σ)) ∪ new-coverage-positions`), or split into LP-EXT-PURE (subspace-end insertion, precondition stated) and LP-EXT-COMP (mid-subspace insertion). The claims table must list the form that is actually true.

### Issue 2: LP-CONTR breaks under K.μ⁻ with within-subspace shift
**ASN-0096, LP-CONTR**: "`proj(e, d, Σ') = proj(e, d, Σ) ∩ R`"
**Problem**: The worked example invokes "the within-subspace shift moves the surviving V-position 1.7 back by 0.2 to 1.5." Counter-witness: if `proj(e, d, Σ) = {1.7}` and a K.μ⁻ deletion at [1.5, 1.7) shifts surviving V-position 1.7 → 1.5, then `proj ∩ R_ret = {1.7} ∩ {1.1, 1.2, 1.3, 1.4, 1.7} = {1.7}`, but actual `Σ'.M(d)(1.5)` carries the original I-address so actual `proj' = {1.5}`. The headline LP-CONTR is wrong whenever a coverage-mapping V-position is itself shifted.
**Required**: Resolve the inconsistency between the K.μ⁻ effect quoted from ASN-0047 (`Σ'.M(d) = Σ.M(d) ↾ R`, a pure restriction) and the shift invoked in the worked example. Either the example is wrong (no relabeling under pure restriction) or LP-CONTR must elevate the composed form (`π'(proj ∩ R_ret)`) — which currently appears only in prose around the example — to be the claim.

### Issue 3: Atomic decomposition arity contradicts the displacement story
**ASN-0096, LP-MAP table, INSERT row**: "K.α (fresh I-addresses) ∘ K.μ⁺ on d ... | LP-EXT (new V-positions) composed with within-subspace LP-REARR"
**Problem**: The decomposition is named as two atoms (K.α ∘ K.μ⁺), but the displacement is "LP-EXT composed with within-subspace LP-REARR." LP-REARR is the effect of K.μ~, not K.μ⁺. So either (a) the shift is inside K.μ⁺, in which case the headline LP-EXT (superset) is wrong, or (b) the shift requires an additional K.μ~ atom, in which case the decomposition is K.α ∘ K.μ⁺ ∘ K.μ~ not two atoms. Same ambiguity for DELETEVSPAN. The ASN never specifies whether the K.μ family includes within-subspace shifts.
**Required**: Specify precisely whether K.μ⁺ and K.μ⁻ include within-subspace shifts of pre-existing V-positions. Adjust the LP-MAP decompositions and the LP-EXT / LP-CONTR statements consistently.

### Issue 4: LP-MAP completeness is asserted without enumeration
**ASN-0096, LP-MAP**: "Every FEBE editing or document operation that can change `proj(e, d, Σ)` ... decomposes into one of K.μ⁺, K.μ⁺_L, K.μ⁻, or K.μ~..."
**Problem**: The claim asserts surjection over all FEBE operations. The text mentions "seventeen commands" but the table enumerates only eight (INSERT, COPY/VCOPY, DELETEVSPAN, REARRANGE, APPEND, MAKELINK, CREATENEWDOCUMENT, CREATENEWVERSION). The nine missing commands are not analyzed. The closing line ("Every FEBE editing or document operation that can affect a projection does so through one or two of these four modes; nothing else displaces") is a restatement, not a proof.
**Required**: Either enumerate all seventeen commands with explicit decompositions, or narrow LP-MAP's scope to the tabulated subset and identify the unverified commands as an open question.

### Issue 5: LP-CON title and statement misalign; coverage-not-yet-allocated case unaddressed
**ASN-0096, LP-CON**: Title "Content persistence at coverage" but statement is universal: `(A a ∈ dom(Σ.C) :: ...)`.
**Problem**: (a) The title scopes to coverage, the statement scopes to all allocated content — different claims. (b) Coverage may reference addresses never yet allocated (the ASN paraphrases L4 as allowing "future allocations"). LP-CON makes no claim about coverage addresses in `coverage(e) \ dom(Σ.C)`, but reliance clause (c) ("the content at each address in my coverage is permanent") implicitly extends past LP-CON's actual statement. The reliance contract overshoots the proven invariant.
**Required**: Rename LP-CON to match its statement (e.g., "Content allocation persistence"), and address speculative coverage explicitly: state what happens when a later K.α allocates an address already inside an existing endset's coverage (this also intersects open question on "well-behaved endset specifications").

### Issue 6: Projection type signature treats a dependent product as Cartesian
**ASN-0096, "The Projection" (Type signature)**: "`proj : Endset × Σ.E_doc × State → ℘_fin(T)`"
**Problem**: `Σ.E_doc` depends on `Σ`; the valid second argument is determined by the third. The signature is a dependent product, not a Cartesian product. A reader cannot fix the domain without first choosing a state. The codomain similarly: `℘_fin(T)` is fine, but the actual range is bounded by `|dom(Σ.M(d))|`, again state-dependent.
**Required**: Either present as `proj : (Σ : State) → Endset → (d : Σ.E_doc) → ℘_fin(dom(Σ.M(d)))`, or specify `proj(e, d, Σ)` as undefined when `d ∉ Σ.E_doc`, or reorder arguments so the dependence is explicit.

### Issue 7: "Boundary cases test the type signature directly" misclassifies the cases
**ASN-0096, "Boundary Cases"**: "The first six cases test the type signature directly (empty projection, empty endset, zero-width span, exact-coverage deletion, mid-coverage insertion, coverage cluster structure)"
**Problem**: These cases test structural/semantic edge behaviors of projection (degenerate inputs, post-state structure after composed transitions), not the type signature. Testing the signature would mean checking input/output types and totality, not exact-coverage deletion.
**Required**: Rephrase to reflect what is actually being tested (e.g., "structural edge cases of the projection definition").

### Issue 8: `footprint` is used in LP-NOD without being defined alongside `proj` and `render`
**ASN-0096, LP-NOD**: "We call the right-hand-side set the *document footprint* of slot `i` at state Σ, written `footprint(ℓ, i, Σ)`."
**Problem**: `footprint` is introduced mid-claim but is a non-trivial primitive: it appears in LP-NOD's statement, both LP-NOD witnesses, the structural-reason discussion, and the open question on visibility partition. It deserves the same definitional weight as `proj` and `render`.
**Required**: Lift `footprint(ℓ, i, Σ) := {d ∈ Σ.E_doc : proj(Σ.L(ℓ).eᵢ, d, Σ) ≠ ∅}` to a named definition in the state/projection section, before its first use.

### Issue 9: LP-DISC "derivation walk" does not establish the biconditional
**ASN-0096, LP-DISC**: "*Derivation walk.* Forward (from source): ... Reverse (from target): ..."
**Problem**: The walks demonstrate well-definedness of forward and reverse queries (the predicates are computable, the search terminates). They do not derive the iff in the discoverability statement. Since `discoverable` is *defined* by the right-hand side, the iff is by definition — but this is never said. As written, the derivation walk appears to be a proof of something it does not prove.
**Required**: Either state plainly that the iff is by definition (and reframe the walk as a well-definedness argument), or derive the iff from named premises.

## OUT_OF_SCOPE

### Topic 1: Cross-version projection correspondence at fork time
**Why out of scope**: Already an open question. Belongs in a future ASN on version semantics, not a gap here.

### Topic 2: Cross-subspace endset coverage
**Why out of scope**: Coverage spanning text-subspace and link-subspace addresses in one endset is correctly noted as an open question.

### Topic 3: Concurrent state transitions during FOLLOWLINK
**Why out of scope**: Read-consistency across a single operation is a concurrency/transaction concern beyond the current state-and-displacement model.

VERDICT: REVISE

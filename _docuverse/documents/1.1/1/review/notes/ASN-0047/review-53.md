# Review of ASN-0047

## REVISE

### Issue 1: S9 listed in per-state invariants but is structurally per-transition
**ASN-0047, ExtendedReachableStateInvariants**: "Every state reachable from Σ₀ ... satisfies: S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ S9 ∧ D-CTG★ ∧ ..."
**Problem**: S9 (TwoStreamSeparation) in ASN-0036 is quantified `[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: ...)]` — a property of a transition pair (Σ, Σ'), not a single state. The ASN explicitly recognizes this category distinction in the same theorem ("S0 (ContentImmutability) and S1 (StoreMonotonicity) of ASN-0036 are per-transition properties quantified over Σ → Σ', not per-state properties; they appear instead in ExtendedTransitionInvariants below") but fails to apply it to S9. The worked example also lists S9 under "Frame-preserved invariants" for the post-state, perpetuating the type confusion.
**Required**: Move S9 to ExtendedTransitionInvariants alongside S0 and S1, or restate S9 in a per-state form (and adjust the worked-example annotations).

### Issue 2: K.δ case (ii) precondition does not explicitly require t to be in E
**ASN-0047, K.δ case (ii)**: "e = inc(t, k) for some previously allocated t ∈ T, with k ∈ {0, 1, 2}"
**Problem**: "Previously allocated" is informal. For T10a's GlobalUniqueness chain to close `e ∉ E`, t must be in some allocator's domain — for non-node entities, this means t ∈ E. The k=0 sibling case relies on t ∈ E to establish parent(t) = parent(e) ∈ E. The k=2 descent case has t = parent(e), which is required to be in E by an explicit clause. But the k=1 document-version case has t as a previously allocated document; nothing says t ∈ E_doc. A K.δ with t ∉ E would have no allocator-discipline grounding for GlobalUniqueness.
**Required**: State explicitly that t ∈ E (and for k=1, additionally t ∈ E_doc) as preconditions for case (ii).

### Issue 3: K.δ k=1 sub-case restriction to documents is in prose, not in the precondition
**ASN-0047, K.δ case (ii) k=1 sub-case**: "We restrict this sub-case to IsDocument(t) (equivalently, IsDocument(e))..."
**Problem**: The restriction `IsDocument(t)` appears in the explanatory prose but is not folded into the formal precondition list. A reader parsing the precondition list and the case structure could conclude that K.δ with k=1 is admissible whenever t is allocated and parent(e) ∈ E — including account-level t. The "harmless admissibility" verification later assumes the document restriction.
**Required**: Add `k = 1 ⟹ IsDocument(t)` (equivalently, `IsDocument(e)`) explicitly to the formal precondition list for K.δ case (ii).

### Issue 4: K.α precondition does not list `a ∉ dom(C)` as a direct conjunct
**ASN-0047, K.α**: Precondition lists `IsElement(a)`, `origin(a) ∈ E_doc`, `a` produced by sub-allocator, `fields(a).E₁ = s_C`. Then prose: "By the axiom or by GlobalUniqueness (depending on case), a is distinct from every previously allocated content address."
**Problem**: Freshness `a ∉ dom(C)` is the critical condition that makes the effect clause `C' = C ∪ {a ↦ v}` meaningful (non-overwriting). Treating it as a derivation from the sub-allocator clause instead of an explicit precondition makes it easy to lose track during proof chains, and forces the reader to reconstruct the axiom/GlobalUniqueness derivation each time. The parallel K.λ precondition lists `ℓ ∉ dom(L) ∪ dom(C)` directly; K.α should be symmetric.
**Required**: Add `a ∉ dom(C)` (and, for L14 preservation, `a ∉ dom(L)`) as explicit precondition conjuncts, retaining the axiom/GlobalUniqueness derivation as discharging text.

### Issue 5: K.μ⁻ admissibility precondition's derivation duplicates D-SEQ★ structure
**ASN-0047, K.μ⁻ Precondition (Admissible removal)**: Contains a "Local derivation" of the form `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` from D-CTG★/D-MIN★/S8-depth/S8-fin/S8a. The same form is later named D-SEQ★ in the Amendments section and re-derived in fuller detail.
**Problem**: The K.μ⁻ definition is presented before D-SEQ★ is named, so the operator needs the structural form but cannot cite the named result. The chosen workaround — restating the derivation inline with a parenthetical "(Note. This local derivation is reproduced in fuller detail... where the same structural form is named D-SEQ★)" — leaves two near-identical proofs in the document and forces the reader to verify both. The ASN's claim of non-circularity is correct (D-SEQ★'s proof does not consume K.μ⁻ admissibility), but the presentation undermines clarity.
**Required**: Either (a) define D-SEQ★ before K.μ⁻ so the precondition can cite the named invariant directly, or (b) state the K.μ⁻ admissibility precondition as a quantification over inputs that satisfy a structural shape, deferring the proof that reachable states satisfy that shape to the D-SEQ★ derivation.

### Issue 6: K.μ~ link-subspace identity clause justification (Claim A / Claim B) overlaps
**ASN-0047, K.μ~ link-subspace fixity**: Two distinct claims (Claim A: precondition stipulation; Claim B: derivation from S3★ + K.μ⁺ amendment + CL-UNIQ) are kept "logically separate to avoid conflating the definitional content of one with the inductive content of the other."
**Problem**: The separation is principled but the resulting prose runs to multiple paragraphs of dense argument that the precondition is "overdetermined." If Claim A (precondition stipulation) suffices for the K.μ~ contract, Claim B's role is reduced to confirming that the surrounding invariants do not admit a weaker precondition. This is a meta-consistency check rather than a load-bearing derivation, and could be one paragraph rather than an extended treatment with forward references to CL-UNIQ. The current structure also creates a forward reference chain (K.μ~ → CL-UNIQ → S3★) that the reader has to mentally unwind.
**Required**: Either (a) demote Claim B to a brief consistency note (one or two sentences) after Claim A, citing CL-UNIQ as the load-bearing invariant without re-deriving the function-equality step; or (b) make the dependency explicit by stating CL-UNIQ before K.μ~ and citing it as a premise of the precondition.

### Issue 7: ExtendedTransitionInvariants conflates S0/S1 with their subsumer P0
**ASN-0047, ExtendedTransitionInvariants**: "Every valid composite transition Σ → Σ' between reachable states satisfies: S0 ∧ S1 ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P5★ ∧ L12"
**Problem**: The proof body then states "S0 (ContentImmutability) and S1 (StoreMonotonicity) are subsumed by P0. S0 asserts ... — the value-preservation clause of P0. S1 asserts ... — the domain-monotonicity clause of P0." If S0 and S1 are subsumed by P0, listing them as separate conjuncts in the theorem statement is redundant — the conjunction `S0 ∧ S1 ∧ P0` is equivalent to `P0` alone. Including all three suggests they are independent constraints when in fact two are restatements of the third.
**Required**: Either drop S0 and S1 from the conjunction (citing P0 as their unified statement) or replace P0 with `S0 ∧ S1` everywhere and use only the original ASN-0036 names. The current presentation is internally consistent but adds notational redundancy.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism
**Why out of scope**: The ASN explicitly flags this in Open Questions ("What invariants must link withdrawal maintain — must withdrawn links remain arranged, or does withdrawal remove them from M(d)?") and in the Step 5 counterfactual worked example. Nelson's tombstoning design is not expressible as K.μ⁻ under D-CTG★, and the ASN defers the precise mechanism to a future ASN. This is new territory, not a gap in the current transition model.

### Topic 2: Concurrent allocation semantics
**Why out of scope**: The ASN's Open Questions section flags concurrency on the same home document. The transition model is sequential (each composite is a finite sequence of elementary steps); concurrent semantics is a separate refinement layer.

### Topic 3: Version lineage invariants beyond admissibility
**Why out of scope**: The k=1 document-version sub-case admits version-shaped addresses structurally, and the ASN explicitly defers richer version contracts ("what arrangement-transition invariants must hold between successive versions, whether content allocators of base and version are linked, how provenance flows between them") to a future version-management ASN.

### Topic 4: Account-level depth-1 tumbler extension
**Why out of scope**: The Open Questions section flags this directly. The exclusion is structurally harmless and the question of whether to admit it belongs to a future extension governing account-level operations.

VERDICT: REVISE

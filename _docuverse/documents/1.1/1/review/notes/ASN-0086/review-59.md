# Review of ASN-0086

## REVISE

### Issue 1: R7a proof's confused content-store monotonicity reference
**ASN-0086, R7a's proof, final paragraph**: "dom(Σ.C) ⊆ dom(Σ'.C) follows from L12a's underlying content-store monotonicity (S0/S1, ASN-0036) on the original ↝-step."
**Problem**: L12a (ASN-0043) is about *link* store monotonicity, not content. The phrasing "L12a's underlying content-store monotonicity" conflates two distinct invariants. S1 (StoreMonotonicity, ASN-0036) is the appropriate citation for `dom(Σ.C) ⊆ dom(Σ'.C)`.
**Required**: Replace with: "dom(Σ.C) ⊆ dom(Σ'.C) follows from S1 (StoreMonotonicity, ASN-0036) on the original ↝-step."

### Issue 2: R7a's conformance scope is incomplete
**ASN-0086, R7a proof, opening paragraph**: "R7a is stated for layers that conform to L12 and L12a on Σ.L"
**Problem**: The proof relies not only on link store invariants (L12, L12a) but also on content store invariants (S0, S1) via the content monotonicity step in the final paragraph. A layer that violates S0/S1 would also break the content monotonicity claim `dom(Σ.C) ⊆ dom(Σ'.C)`. The conformance scope needs to include the content invariants the proof actually consumes.
**Required**: Broaden conformance scope to something like: "R7a is stated for layers that conform to all substrate invariants on (Σ.C, Σ.M, Σ.L) — specifically L12, L12a on the link store and S0, S1 on the content store."

### Issue 3: Reference to non-foundation ASN-0047
**ASN-0086, Setup paragraph**: "This note's substrate baseline is ASN-0036 + ASN-0043; it has no dependence on ASN-0047 and does not assume the extended state vector (Σ.E, Σ.R, link-subspace V-positions) that ASN-0047 introduces. Citations of S3 throughout refer to ASN-0036's S3 (ReferentialIntegrity), not ASN-0047's S3★."
**Problem**: ASN-0047 is not in the foundation list. Even disclaiming references mention non-foundation ASNs by number and presuppose visibility into ASN-0047's contents (Σ.E, Σ.R, S3★).
**Required**: Remove the ASN-0047 mention. Replace with positive scoping: "This note's substrate baseline is ASN-0036 + ASN-0043. Citations of S3 refer to S3 (ReferentialIntegrity, ASN-0036)."

### Issue 4: Substrate emission primitive lacks formal status
**ASN-0086, Setup section**: "**Substrate emission primitive.** The substrate admits, as its primitive emission for the link store..."
**Problem**: This is asserted as a "substrate commitment" (the ASN's own language) but is not given an explicit label (AXM/COMMITMENT) and has no entry in the Properties Introduced table. It is load-bearing for R0's Step 4 (the invocation that delivers `→`-step existence), R5's emission construction, and R7a's class-(iii) replay. The "Witness-only reading of L1c (substrate commitment)" suffers the same gap. The reader cannot distinguish what is derived from ASN-0043 from what is newly introduced here.
**Required**: (a) Label the substrate emission primitive formally (e.g., "Axiom — SubstrateEmissionPrimitive (AXM)") with explicit precondition/postcondition structure. (b) Label "Witness-only reading of L1c" similarly. (c) Add both as rows in the Properties Introduced table, with status "introduced". (d) Have R0, R5, R7a cite them by label rather than by paragraph reference.

### Issue 5: R7a lacks concrete example
**ASN-0086, R7a**: No concrete worked instance showing the multi-step decomposition.
**Problem**: The worked sketch's Step 1 and Step 2 are single class-(iii) `→`-steps each (R7a with `m = 1`, trivial). The substantive content of R7a — interleaving class-(i) document-allocation prefixes for L1a's home precondition when the home document is itself fresh in the same ↝-step — is never exhibited. A reader has no concrete demonstration of how a composite "create-document-with-initial-link" operation decomposes.
**Required**: Add a concrete example (could be a third step in the Worked Sketch, or a separate sub-section) showing a composite ↝-step that creates a fresh document `d_new` and emits a link homed at `d_new` in the same atomic step, decomposed as `Σ → Σ_1 → Σ_2` with class-(i) at step 1 and class-(iii) at step 2.

### Issue 6: Inconsistent variable naming in R0a Stage 2 induction
**ASN-0086, R0a's Stage 2, class-(iii) sub-cases**: "Sub-case A — a constructed via Step 2 Case A (a = d_new.0.s_L.1)... Sub-case B — a constructed via Step 2 Case B (a = inc^i(b, 0) for the least i ≥ 1 with inc^i(b, 0) ∉ dom(Σ.L), where b ∈ dom(Σ.L) has home(b) = d)."
**Problem**: The variable `d_new` was bound earlier as "the freshly allocated document in class (i)" but is reused in Sub-case A to mean "the home of the class (iii) emission" — which can be any document in `dom(Σ.M)`, not necessarily fresh. Sub-case B then switches to `d`. The notation is inconsistent within a single induction step.
**Required**: Unify to a single name (e.g., `d` throughout the class-(iii) sub-cases) and reserve `d_new` for the class-(i) sub-case only, or introduce a separate symbol for "the home of the class-(iii) emission."

### Issue 7: R6c-Corollary's induction is too brief
**ASN-0086, R6c-Corollary proof**: "Mixed ↦-chains decompose into →-steps (covered by R6c) and arrangement-modifying steps (pointwise-preserving), discharging (a, F, G) ∉ A_K^{Σ''} along the full chain."
**Problem**: This compresses the inductive argument to one sentence. The actual chain-decomposition is straightforward but should be made explicit: the induction is on ↦-chain length, with the inductive step splitting on whether the next ↦-step is a `→`-step (covered by R6c) or an arrangement-modifying step (`A_K^{Σ_{k+1}} = A_K^{Σ_k}` by ASN-0043's L12 + L12a holding Σ.L identical).
**Required**: Expand into a brief explicit induction on ↦-chain length, naming the two cases of the inductive step.

### Issue 8: Definition of nullified — implicit `a ∈ A_rel^Σ` constraint
**ASN-0086, Definition of Nullified**: "nullified(Σ) = {a ∈ A_rel^Σ : (E (b, F', G') ∈ L_R^Σ :: a ∈ coverage(G'))}"
**Problem**: The set-builder restricts `a ∈ A_rel^Σ`, which the existential's witness doesn't imply (a retraction's coverage may include addresses outside `A_rel^Σ` — documents, content, ghosts). This is a substantive design choice: nullified is *only* about tuple addresses. The choice should be motivated, not implicit. Without motivation, a reader cannot tell whether the restriction is a soundness requirement or a layer-naming convention.
**Required**: Add a sentence after the Definition explaining the restriction: "The restriction `a ∈ A_rel^Σ` reflects the substrate's typing — only tuple addresses are eligible for nullification, since `A_K^Σ` (the consumer of nullified) ranges over tuple addresses alone. Retraction-to-document, retraction-to-content, and retraction-to-ghost are excluded by this scope; document removal is performed via classifier tuples (R5 Consequence, retired classification) rather than direct retraction."

### Issue 9: R6b is essentially "by definition" — claim status unclear
**ASN-0086, R6b (SingleDepthRetraction)**: "Deciding `a ∈ nullified(Σ)` reduces to a single-pass existential check over `L_R^Σ`..."
**Problem**: The proof's substance is "this follows from the Definition's quantification over `L_R^Σ` rather than `A_R^Σ`" — i.e., R6b is a tautological consequence of the Definition. The contrast with the alternative (active-subset) reading is useful, but R6b's status as a labeled lemma is unclear: is it a theorem, or is it just a property of the Definition? If it's a definitional consequence, it should be labeled DEF-Consequence or similar, not LEMMA.
**Required**: Clarify status — either (a) re-label R6b as "Consequence of Definition (Nullified)" to reflect its tautological nature, or (b) elevate the content to a genuine theorem (e.g., show that the audit-slice reading is the *unique* reading making R7a's decomposition apply, or some similar non-tautological claim).

### Issue 10: T_ghost referenced but not formally defined
**ASN-0086, R5 generalization paragraph**: "endsets built from L13-admissible canonical spans ({(b, δ(1, #b))} for any b ∈ dom(Σ.L) ∪ dom(Σ.C) ∪ T_ghost)"
**Problem**: `T_ghost` is used as a notational shortcut but is never defined. The reader can guess from context that it means "tumbler-space addresses outside `dom(Σ.C) ∪ dom(Σ.L)`" but the term should be defined explicitly.
**Required**: Either (a) add a Definition: `T_ghost^Σ = T \ (dom(Σ.C) ∪ dom(Σ.L))` and add to the Properties Introduced table, or (b) replace the symbol with the explicit phrase "addresses outside `dom(Σ.C) ∪ dom(Σ.L)`".

### Issue 11: Emit_K signature missing K parameter
**ASN-0086, Definition of Emit_K**: "Emit_K : Σ_D × dom(Σ.M) × Endset × Endset → Σ_D' × A_rel^{Σ_D'}"
**Problem**: The signature shows four argument positions and one return tuple but does not include `K` as an argument despite the Definition's "Given input state Σ ∈ Σ_D, caller-supplied home document d ∈ dom(Σ.M), and finite endsets F, G ∈ Endset, Emit_K(Σ, d, F, G) deposits a fresh tuple under d at an address a..." with `K` left implicit. Is `K` a type parameter (compile-time), an implicit context, or genuinely missing? Nullify's definition `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` reads K as a type-index (subscript), but the signature reads as if K is missing.
**Required**: Either (a) make K explicit in the signature: `Emit : T_admissible × Σ_D × dom(Σ.M) × Endset × Endset → Σ_D' × A_rel^{Σ_D'}`, or (b) keep K as a type-index but state explicitly: "K is a type-index, not a value argument; `Emit_K` is a family of operations indexed by `K ∈ T_admissible`."

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations A_K^{(n)}
**Why out of scope**: The ASN explicitly restricts to standard-triple (arity-3) links and notes this in the Open Questions. Higher-arity treatment is genuinely new territory; the projection-vs-direct-higher-arity tradeoff belongs in a successor ASN.

### Topic 2: Concurrency model and atomicity guarantees
**Why out of scope**: Listed in Open Questions as "Must Emit be atomic with respect to concurrent Observe...". The substrate's transition semantics in this ASN are sequential; concurrent semantics require additional commitments not yet made.

### Topic 3: Cardinality bounds on nullified(Σ)
**Why out of scope**: Listed in Open Questions. The substrate admits unbounded retraction; whether to constrain ratios is a design decision deferred.

### Topic 4: Cross-layer type catalog coordination
**Why out of scope**: Listed in Open Questions. The interaction between layers when both independently extend `T_cat` involves coordination semantics that go beyond the substrate.

### Topic 5: Elevating sibling-frontier discipline to substrate guarantee
**Why out of scope**: Listed in Open Questions as a substantive design question. The current treatment (discipline-conditional R0a, R0a-Cor1, R0a-Cor2) correctly tracks the conditionality; whether to make it unconditional is a future ASN's call.

### Topic 6: L14's native scoped form without Setup hypothesis
**Why out of scope**: Listed in Open Questions. The ASN's globally-s_C-resident hypothesis scopes the disjointness results; a slice-wise reformulation is genuinely separate work.

VERDICT: REVISE

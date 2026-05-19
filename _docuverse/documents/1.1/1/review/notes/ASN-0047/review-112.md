# Review of ASN-0047

## REVISE

### Issue 1: K.α and K.λ precondition framing inconsistency
**ASN-0047, K.α and K.λ sections**: K.α states "The precondition structure — `d ∈ dom(M)` (home document exists)..." (and likewise for K.λ). But the Notation section says "M is a total function with M(d) = ∅ (the empty partial function) when d ∉ E_doc."
**Problem**: Under ASN-0047's totality framing, `dom(M) = T` trivially, so `d ∈ dom(M)` is vacuous. The intent — used consistently in worked examples and in K.μ⁺_L's precondition — is `d ∈ E_doc`. The K.μ⁺ original definition (Elementary transitions) already uses `d ∈ E_doc`. K.α/K.λ break the convention by retaining ASN-0093's `dom(M)` framing.
**Required**: Restate K.α and K.λ preconditions in ASN-0047's framing as `d ∈ E_doc`. The inherited-from-ASN-0093 status can still be preserved (the operations are the same, just expressed in ASN-0047's vocabulary).

### Issue 2: K.σ subsumption implicit
**ASN-0047, Elementary transitions and Allocator hierarchy sections**: ASN-0093 defines K.σ (DocumentRegistration) as a separate primitive that registers `d` into `dom(M)`. ASN-0093's SubAllocatorAxiom activates `A_C(d)` and `A_L(d)` at K.σ events. ASN-0047 absorbs K.σ functionality into K.δ for documents but never says so explicitly.
**Problem**: A reader checking that ASN-0047 covers every foundation primitive will look for K.σ and not find it. The "joint T2-spawn step" reference in *Allocator hierarchy under documents* implicitly identifies K.δ-for-documents with K.σ, but only by inference.
**Required**: Add an explicit statement — at K.δ's definition or in the Allocator hierarchy section — that K.δ for `IsDocument(e)` subsumes ASN-0093's K.σ: the entity-allocation event placing d into E_doc is the same event that registers d into dom(M) and activates A_C(d), A_L(d) per SubAllocatorAxiom.

### Issue 3: "Amendment postcondition" terminology in verification matrix
**ASN-0047, ExtendedReachableStateInvariants verification matrix**: Multiple cells (e.g., D-CTG★/D-MIN★ under K.μ⁺; S2 under K.μ⁺) say "amendment postcondition". But the K.μ⁺ amendment in the *Amendments to existing transitions* section only adds one clause: `subspace(v) = s_C`.
**Problem**: D-CTG★ and D-MIN★ requirements are preconditions on K.μ⁺ that constrain the post-state. They are not part of "the amendment" — they were already preconditions in the original K.μ⁺ definition (carried forward to the extended state). Calling them "amendment postconditions" misnames their origin and their role.
**Required**: Rename matrix entries from "amendment postcondition" to "precondition discharge" (or similar). Acknowledge the original K.μ⁺ definition as the source of the D-CTG/D-MIN obligations.

### Issue 4: "By inheritance" wording for K.α frame
**ASN-0047, K.α section (extended state frame)**: "the `E' = E` and `R' = R` conjuncts inherit from the original K.α frame" / "`E' = E` and `R' = R` extend that frame with the entity and provenance components that ASN-0093 does not name (both are unchanged at K.α by inheritance)."
**Problem**: ASN-0093 has no E or R components, so nothing can be "inherited" for them from ASN-0093. The conjuncts are added by ASN-0047, not inherited.
**Required**: Replace "by inheritance" with phrasing that names the actual source — e.g., "added by this ASN to extend ASN-0093's K.α frame with the entity and provenance components."

### Issue 5: A_doc vs A_↓ notation interchange
**ASN-0047, Sub-allocator names definition and K.δ case (ii) discharge sections**: The Sub-allocator-names section uses `A_doc(parent(d))` and `A_v(d)`. The K.δ case (ii) k=2 discharge uses `A_↓(t)` ("t's next-level sub-allocator") without explicit cross-reference.
**Problem**: A_doc(A) and A_↓(A) (when A is an account) denote the same allocator. The dual notation forces readers to mentally reconcile two names for one concept, especially across K.δ case (ii) sub-cases A, B, C where `A_↓` appears prominently.
**Required**: Unify the notation — either consistently use A_↓ everywhere with a definition table at first use, or use A_doc / A_account / A_v specifically and drop A_↓.

### Issue 6: K.μ~ existence-condition discharge obligation
**ASN-0047, ValidComposite★ definition**: "K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition (per its definition above): admissibility clause (iii) requires `π ≠ id`, whose necessary-and-sufficient existence condition is `|dom_C(M(d))| ≥ 2`."
**Problem**: The existence condition `|dom_C(M(d))| ≥ 2` is stated as a derivation result in *Decomposition of K.μ~*, but ValidComposite★ treats it as something callers verify operationally. The ASN doesn't say whether the existence condition is a *precondition* of K.μ~ (caller-checked) or a *derived obligation* of K.μ~'s definition that the operation must satisfy by exhibiting an admissible π.
**Required**: Make explicit whether `|dom_C(M(d))| ≥ 2` is a K.μ~ precondition or a sufficiency obligation, and add it to K.μ~'s precondition list at the definition site.

## OUT_OF_SCOPE

### Topic 1: Concurrent operation discipline at K.λ
**Why out of scope**: The Open Questions section asks "What must the system guarantee when concurrent operations target the same home document?" The orphan-link semantics and the K.λ subsequent-emission predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅` would interact non-trivially with concurrent allocation against the same A_L(d) frontier. SequentialTransitionAxiom is taken as foundation; concurrency is explicitly deferred per Scope.

### Topic 2: Link-withdrawal mechanism
**Why out of scope**: Per the Open Questions, the reconciliation of Nelson's tombstoning design with D-CTG★/D-MIN★ requires a separate withdrawal mechanism (status flag, tombstone marker, or retraction link). K.μ⁻ admits only suffix-truncation under D-CTG★/D-MIN★, leaving interior withdrawal unaddressed. The ASN correctly identifies this as future work.

### Topic 3: Account-level versioning
**Why out of scope**: Per the Open Questions, the present ASN excludes K.δ k=1 with `IsAccount(t)` at the precondition. Worked examples and consultation evidence reserve versioning to documents. Future extension (account renaming, multi-account identity) would require admitting this — properly deferred.

VERDICT: REVISE

# Review of ASN-0086

## REVISE

### Issue 1: Implementation hypotheses placed inside Setup
**ASN-0086, Setup → Implementation hypotheses**: "Sparse-allocator hypothesis", "Sibling-frontier discipline", "Unit-depth retraction discipline" are introduced as a named "Implementation hypotheses" subsection within Setup.
**Problem**: A specification ASN should not contain "implementation hypotheses" inside its substrate-defining setup. The Sparse-allocator hypothesis is about implementation behavior (whether allocator state is observably tracked); the two disciplines are layer-level constraints on caller behavior, not substrate guarantees. Co-locating them with substrate hypotheses (s_C-residence, subspace distinctness) conflates spec and layer commitments.
**Required**: Relocate the three implementation hypotheses to a separate "Implementation Notes" appendix or remove them. Substrate-level claims (R0–R5, R6a–R6c, R7a) should stand without these. Only the explicitly conditional results (R0a and its corollaries) and the disciplined operations (Emit_K, Nullify single-tuple-scope) reference them, with a sharp boundary marker between substrate-guaranteed and discipline-conditional claims.

### Issue 2: R0a-Cor2's narrowing acknowledged narrower than design intent
**ASN-0086, R0a-Cor2 status note**: "narrower than Nelson's foundational link-model design, which admits deeper-sited sub-links — see Open Questions for relaxation paths"
**Problem**: R0a-Cor2 constrains link addresses to depth-2 (#E = 2) under the discipline. The lemma's own status note flags this as narrower than the design and points to Open Questions for relaxation. A spec lemma whose status note admits the spec is wrong about what the design supports is implementation-driven, not specification-driven.
**Required**: Either (a) supply substrate-level justification for why depth-2-only is the correct spec (and delete the "narrower than design" acknowledgement), or (b) remove R0a-Cor2 entirely as an implementation observation, leaving the depth-narrowing discussion in Open Questions only. The current presentation tries to have it both ways.

### Issue 3: R5's proof lacks substantive derivation
**ASN-0086, R5 Justification**: "By L13 (ReflexiveAddressing, ASN-0043), the unit-depth span `(a, δ(1, #a))` is well-formed; by L4(c) (EndsetGenerality, ASN-0043), endset spans may reference link-subspace addresses; R0 Step 4's invariant-preservation argument admits emissions carrying such spans without restriction on endset target content."
**Problem**: This is three citations stitched together, not a proof. Per Dijkstra's standard, "X follows from Y + Z" is a claim, not a derivation. The substantive question — what self-referencing tuples enable that wasn't already in scope — is deferred entirely to the Consequences section. R5 occupies a load-bearing position (Nullify, R6a/b/c all depend on it) but its proof never engages with what the lemma actually constructs.
**Required**: Show the derivation step by step. At minimum, exhibit one concrete self-targeting tuple construction within the proof, verifying that R0's invariant-preservation argument passes when applied to that endset shape. Currently a downstream reader has to reconstruct the argument themselves.

### Issue 4: Single-tuple scope of Nullify ambiguously specified
**ASN-0086, Definition — Nullify, Single-tuple scope paragraph**: P3 stated as explicit precondition; "Under the sibling-frontier discipline, P3 is automatic at every reachable state; it is stated as an explicit precondition to keep Nullify's contract usable for systems where the discipline is not yet a global guarantee."
**Problem**: The single-tuple scope argument depends on R0a's reachable-state antichain to discharge `a ⊀ b` for the fresh retractor `b`. Under the discipline, R0a fires; without the discipline, P3 explicit but R0a's antichain isn't available — so the substrate emission primitive could place `b` at a strict prefix-extension of `a`, breaking single-tuple scope even with P3 satisfied at the pre-state. The contract's two readings yield genuinely different operational guarantees.
**Required**: Commit Nullify to one regime. Either (a) declare the disciplined regime as the contract (P3 derived, antichain-on-Σ' guaranteed, single-tuple scope absolute), or (b) explicitly state that single-tuple scope requires both P3 and the discipline. The "usable either way" framing hides which guarantees actually hold.

### Issue 5: wp Case 3 (nullifying the retractor) is contrived
**ASN-0086, Weakest-Precondition Analysis, Case 3**: "wp(Nullify(Σ, d_meta, b₁), a₁ ∈ nullified(Σ')) ≡ a₁ ∈ nullified(Σ)"
**Problem**: The wp simplifies to the prior-state predicate alone — no contribution from the Nullify call. This is a sanity check on the Definition's quantifier range (R6b's META content), not wp analysis. It illustrates the absence of state change, not how state changes.
**Required**: Replace with a substantive wp example — e.g., wp(Emit_K composed with Nullify in sequence, some non-trivial postcondition over A_K) or wp(Observe, a coverage-class membership claim) — or remove Case 3 entirely. Three wp examples ought to span three distinct operations or three distinct postcondition shapes; the current set has two informative cases and one trivial.

### Issue 6: R0a Stage 1 reverse-direction argument is redundant
**ASN-0086, R0a Proof, Stage 1**: "The reverse direction `a' ⊀ a` (under `d ≠ d'`) follows by the symmetry of the derivation in `(a, a', d, d')`: every step's conclusion is symmetric under the swap..."
**Problem**: R0a's antichain conclusion is `a ≼ a' ⟹ a = a'`. Showing a ≼ a' contradicts d ≠ d' (forward direction) suffices — antichain is symmetric in (a, a') because the implication is universally quantified. The second paragraph showing a' ⊀ a adds no logical content to antichain.
**Required**: Trim. State the forward direction; if symmetry needs noting, one sentence ("the conclusion is symmetric under the (a, a') swap") suffices instead of a full paragraph.

### Issue 7: Forward-reference accretion in R0a-Cor2's prose
**ASN-0086, R0a-Cor2 prose body**: "(narrower than Nelson's foundational link-model design, which admits deeper-sited sub-links — see Open Questions for relaxation paths)"
**Problem**: The lemma's own prose embeds editorial commentary about future work and points to a downstream section to justify the present narrowness. A reader trying to follow R0a-Cor2's technical content has to skip past meta-commentary. This is forward-reference accretion of the form flagged in this review's anti-bloat classifier.
**Required**: Remove the editorial sentence from R0a-Cor2's statement. The Open Questions relaxation discussion stands on its own; the lemma's prose should focus on what the lemma states, not on what it doesn't.

### Issue 8: R6c Corollary cites unnamed ASN-0036 frame
**ASN-0086, R6c Corollary proof**: "arrangement-modifying transitions hold `Σ.L` identical (arrangement-modification frame above)"
**Problem**: The "arrangement-modification frame" referenced is derived from ASN-0036 invariants but is not cited to specific clauses. A reader cannot easily verify which ASN-0036 provisions establish that arrangement modifications hold Σ.L identical. The "Definition — BroadExtension" paragraph asserts it, but without grounded citations.
**Required**: Cite ASN-0036's specific provisions: P3 (ArrangementMutability) governs `Σ.M` value changes; combined with L12 (LinkImmutability, ASN-0043) and L12a (LinkStoreMonotonicity), this gives `Σ'.L = Σ.L` across arrangement-modifying steps. State the joint provenance explicitly.

## OUT_OF_SCOPE

### Topic 1: Multi-arity link relations
**Why out of scope**: The ASN restricts to standard-triple links and explicitly defers higher-arity relations (`L_K^{(n)}`) to Open Questions. This is appropriate scope-limiting, not an error in this ASN.

### Topic 2: Concurrent access and atomicity of Emit/Observe
**Why out of scope**: Emit/Observe atomicity and consistency model under concurrency are deferred to layer specifications via Open Questions. These belong in a future operations-layer ASN, not here.

### Topic 3: Lifting Setup to non-globally-s_C-resident systems
**Why out of scope**: The slice-wise reformulation under L14's native scoped form is itself an Open Question, properly deferred.

VERDICT: REVISE

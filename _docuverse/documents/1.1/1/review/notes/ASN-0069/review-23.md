# Review of ASN-0069

## REVISE

### Issue 1: V8b's K.μ⁺_L argument elides the load-bearing step

**ASN-0069, V8b non-monotonicity paragraph**: "K.μ⁺_L extends only V_{s_L} of its target document; since F ⊆ V_{s_C}(d_src) by F's definition as a restriction of V_{s_C}(d_src) and the content and link subspaces are partitioned by subspace(v) (with s_C ≠ s_L by SubspaceConventionAxiom, ASN-0047), F ∩ V_{s_L} = ∅, so Π_g = F ∩ Corr_g is unchanged regardless of any link-subspace effect on Corr_g."

**Problem**: The inference from "F ∩ V_{s_L} = ∅" to "Π_g is unchanged" skips the load-bearing step. The set-disjointness establishes only that link-subspace v_ℓ ∉ F — addressing one half of the case analysis. The other half — that for v ∈ F (content-subspace), M(d_src)(v) and M(d_new)(v) are *unchanged* by K.μ⁺_L because the modification targets v_ℓ ≠ v — is the value-invariance claim on which Corr_g restriction to F actually depends. The text leaves this implicit.

V11's analogous K.μ⁺_L handling — "K.μ⁺_L on d^{i-1}_new, which extends only V_{s_L}(d^{i-1}_new) and leaves V_{s_C}(d^{i-1}_new) and its image untouched" — makes exactly this step explicit. V8b should match.

**Required**: Replace the inference with an explicit two-step argument: (i) K.μ⁺_L on any d modifies M(d) only at the single v_ℓ with subspace s_L; (ii) for v ∈ F (subspace s_C), v ≠ v_ℓ, so M'(d_src)(v) = M(d_src)(v) and M'(d_new)(v) = M(d_new)(v); (iii) so Corr_g restricted to F is unchanged; (iv) so Π_g is unchanged.

### Issue 2: V8b's case analysis omits K.μ⁻/K.μ⁺/K.μ~ on non-chain documents

**ASN-0069, V8b non-monotonicity paragraph**: "So Π_g shifts only via K.μ⁻, K.μ⁺, or K.μ~ acting on d_src or d_new; the operational mechanics of removal, re-installation, and remapping are properties of those three transition kinds as defined in ASN-0047, not of the fork operation."

**Problem**: The case analysis explicitly covers K.α, K.λ, K.ρ, K.μ⁺_L, and K.δ but reaches the "shifts only via ... acting on d_src or d_new" conclusion without explicitly invoking the frame conditions for K.μ⁻, K.μ⁺, K.μ~ on documents other than d_src or d_new. Their per-target frame condition `(A d' : d' ≠ d : M'(d') = M(d'))` preserves M(d_src) and M(d_new) when d ≠ d_src, d_new, so Corr_g and Π_g are invariant — but this step is silent.

**Required**: Add a sentence explicitly invoking the frame conditions of K.μ⁻, K.μ⁺, K.μ~ for d ≠ d_src, d ≠ d_new: in each case the per-target frame preserves M(d_src) and M(d_new) entirely, so Corr_g is invariant and Π_g is invariant.

### Issue 3: V2's nested length-induction structure is implicit

**ASN-0069, §"Identity by Sub-Allocation," V2 inductive step**: "We observe that every A_v(d_src) output has length exactly #d_src + 1: the first emission inc(d_src, 1) has length #d_src + 1 by TA5(d) at k = 1 (the base case), and each subsequent emission via inc(·, 0) preserves length by TA5(c)."

**Problem**: This sub-claim is itself an induction on A_v(d_src)'s emission count — base case (first emission has length #d_src + 1 by TA5(d)) plus inductive step (subsequent emission preserves length by TA5(c)). It is nested inside V2's outer induction on the same emission count, but the nesting is not named. A reader must reconstruct the induction structure from the prose. The same proof reuses A_v(d_src)'s emission-count induction twice in the same paragraph without distinguishing the inner and outer induction goals.

**Required**: Either (a) lift "every A_v(d_src) output has length #d_src + 1" to a named sub-lemma proved by a separate emission-count induction, then cite it in V2's inductive step, or (b) explicitly mark the nested induction inside V2's proof — naming the inner base and step distinctly from the outer base and step.

### Issue 4: V11's premise convention at i=1 is unspecified

**ASN-0069, V11 premise**: "for every 1 ≤ i ≤ k, V_{s_C}(d^{i-1}_new) is the same set in the post-state of step i − 1 and the pre-state of step i".

**Problem**: At i=1, "step 0's post-state" does not denote any fork step's post-state — there is no step 0. The natural reading is that this denotes the chain's initial state Σ (= step 1's pre-state), making the premise at i=1 trivially satisfied because the two "states" being compared are the same state. The proof's base case (k=1) bypasses the premise entirely. But the statement of V11 quantifies "for every 1 ≤ i ≤ k", so the convention at i=1 should be spelled out rather than left to interpretation.

**Required**: Add one sentence to V11's premise stating that at i=1, "step 0's post-state" denotes the chain's initial pre-state Σ (= step 1's pre-state), so the premise at i=1 is trivially satisfied.

## OUT_OF_SCOPE

### Topic 1: Tree-structured fork hierarchies

**Why out of scope**: V10 covers sibling forks (multiple forks of one source) and V11 covers chain forks (each fork's source is the prior fork's target). A general tree — siblings combined with chains — is not given a dedicated lemma but is derivable from V10 and V11 composed. A tree-spanning property would be a separate concern, not an error in CREATENEWVERSION's specification.

### Topic 2: Forks of transcluding sources

**Why out of scope**: When d_src's arrangement references I-addresses with origin ≠ d_src (transcluded content), V4's literal inheritance still applies — but the interplay with chain-of-custody discovery, royalty paths across multiple originating documents, and transclude-and-fork composites belongs in a future ASN treating transclusion-aware fork semantics.

### Topic 3: Concurrent fork invocations

**Why out of scope**: SequentialTransitionAxiom (ASN-0047) totally orders state transitions, so concurrent fork invocations resolve to a sequential ordering at the abstract level. Concurrency control at the implementation level — locking, transactional semantics, distributed consensus — belongs in an implementation-mechanics ASN, not in CREATENEWVERSION's abstract specification.

VERDICT: REVISE

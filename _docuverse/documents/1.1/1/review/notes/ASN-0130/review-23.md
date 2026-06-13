# Review of ASN-0130

This is a strong, carefully-built note. I checked the load-bearing arguments — PR2's event-wise acyclicity, PR3a's substitution induction, PR0/PR5a's wp derivations, PR5's bound-constant soundness, and PR-VIEW's view-independence class — and they hold up. The findings below are refinements, dominated by the forward-reference accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: The endorsement-withdrawal point is restated near-verbatim across PR1 and PR3

**ASN-0130, PR1**: "evaluation (PR3) keys on ever-registration, not (iv)-currency — a de-registered referent still resolves and expands, its deposit-state validity proved once and preserved in the audit slice ... What a referent's de-registration withdraws is the endorsement, never the artifact or its standing audit-slice proof."

**ASN-0130, PR3**: "A de-registered definition therefore still evaluates — resolution reads immutable content whose validity the deposit-state validation already proved; what de-registration withdraws is the endorsement (condition (iv) for new registrations), not the artifact or its standing proof in the audit slice."

**Problem**: Two ideas — (a) a de-registered definition still resolves/evaluates with deposit-state validity preserved in the audit slice, and (b) de-registration withdraws the endorsement, not the artifact — are stated in full in both PR1 and PR3, and previewed a third time in the commit bullet ("only the reference-endorsement conjunct is withdrawable, and evaluation does not depend on it (PR3)"). The reader meets the same sentence three times.
**Required**: PR1 is the home (it owns the permanence division across conjuncts). PR3 needs only "evaluate keys on ever-registration, not active registration (PR1)"; drop the re-derivation of what de-registration withdraws.

### Issue 2: Non-predicate rejection is explained at length in both PR5 and PR5a (0)

**ASN-0130, PR5**: "a ℘_fin(T)- or ℕ-valued definition, though registrable and referenceable, is rejected by certification check (0) (PR5a) as a non-predicate and so can never carry pd_stable."

**ASN-0130, PR5a (0)**: "register_pred stores signed terms of any result sort C_D ∈ Codom (PR0, PR-ENC), but only the Boolean-sorted ones are predicates ... so a ℘_fin(T)- or ℕ-valued definition, though a well-formed, registrable, referenceable artifact, has no stability to assert. Failure here is rejection as a non-predicate."

**Problem**: The "℘_fin(T)/ℕ-valued, registrable, referenceable, rejected as non-predicate" content appears twice. PR5a (0) is the definitional home (it *is* the check); PR5's universal-lint passage re-explains it.
**Required**: Let PR5's lint caveat point to PR5a (0) for the non-predicate concept rather than restating it.

### Issue 3: certify_pd_stable's defining check (iii) has no decidability/termination argument

**ASN-0130, PR5a (iii)**: "Class membership: the checker's verdict `expand(a) ∈ ST⁺`, by PD0's rules under PR5's Parameters reading."

**Problem**: The note establishes decidability of every *other* check on these surfaces — PR0 (iii)'s WT pass is "a syntax-directed finite tree walk ... decidable," and PR5a (ii)'s view-independence is "PR-VIEW's syntactic scan, decided by the same finite scan that decides well-typing." But check (iii), the substantive one that gates certification, is stated only as well-*posed* ("ST⁺ membership is well-posed absolutely") — well-posedness is having a truth value, not being computable. An operation must terminate, and ST⁺-classification is a meta-level walk distinct from WT. The decidability is real but unstated, breaking the note's own pattern.
**Required**: One clause: the ST⁺ check is a finite syntax-directed classification over the finite term `expand(a)` (finite by PR2 and PR3a's `expand(a) ∈ PL`), PD0's rules being syntax-directed with the parameter reading adding no unboundedness.

### Issue 4: "What this note commits" bullets restate the PR bodies in full rather than pointing to them

**ASN-0130, commit list (PR3 bullet)**: "Evaluation by reference (PR3): evaluate(a, args, view, Σ) — precondition: a ever-registered; args a signature-respecting environment — resolves content to a term by the self-delimiting parse, expands through the reference DAG into a pure term well-typed at the recorded signature (PR3a), and evaluates per ASN-0129 at the caller's view — references are view-transparent (PR-VIEW) — inheriting purity, termination, and the ceiling unchanged."

**Problem**: This (and the PR0, PR1, PR5 bullets) reproduce the claim's mechanism — precondition, the three layers, view-transparency, inherited properties — at a length that duplicates the body section. Essay content in a structural (summary) slot: the reader reads each mechanism twice. This is exactly the kind of accretion the anti-bloat classifier targets.
**Required**: Reduce the bullets to terse commitments (what is guaranteed), leaving the mechanism to the PR bodies — e.g., "PR3: an ever-registered address evaluates by resolving, DAG-expanding to a pure well-typed term, and evaluating per ASN-0129 at the caller's view, inheriting ASN-0129's purity/termination/ceiling."

## OUT_OF_SCOPE

### Topic 1: Expansion size and structural sharing
PR3 defines `expand(a)` as full inlining and PR2 proves it terminates — the spec requirement. But a diamond reference pattern (a → b, a → c, b → d, c → d) inlines `expand(d)` twice, and nested diamonds blow up exponentially in DAG depth. This affects the *cost* of `evaluate` and the certification check, not any guarantee.
**Why out of scope**: Bounded representation (DAG/hash-consed sharing of `expand`) is an implementation optimization; full inlining is the cleanest *specification* of the denotation. Termination — what the spec owes — is proved.

### Topic 2: Contiguous-run allocation under concurrent allocators
PR0 condition (i) requires `A_def` to be one contiguous `shift`-segment of an origin's K.α chain, rejecting fragmented runs. The worked example notes a run survives "with no other K.α scoped to d_b interleaved," but the question of how a builder *guarantees* a clean run when other allocators target the same document is left to the caller.
**Why out of scope**: This is an allocation-coordination protocol concern. The substrate's contract is correct — present a contiguous run or be rejected — and condition (i) is the right precondition; obtaining one is the builder's affair.

VERDICT: REVISE

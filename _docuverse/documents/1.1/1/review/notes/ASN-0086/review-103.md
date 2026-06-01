# Review of ASN-0086

This note carries the `review-mode.anti-bloat` classifier and explicitly states that prior cycles accumulated meta-prose around forward references. The mathematics is, with one minor exception, sound and well-defended — but several arguments are stated two or three times across the operation definitions, the wp analysis, and the surrounding framing. Those duplications are the substance of this review.

## REVISE

### Issue 1: The P1-necessity argument (fresh emitter / L12a) is stated three times
**ASN-0086, Definition — Nullify; WP Case 1 (Necessity); WP Case 1 (closing)**: the identical chain "the only new key at Σ' is the fresh emitter `b ≠ a`, so by L12a's pointwise agreement `a ∉ dom(Σ'.L)`, hence `a ∉ nullified(Σ')`" appears in all three places:
- Nullify Def: "P1 is required for the postcondition ... without it the fresh emitter `b ≠ a` is the only new key, so by L12a's pointwise agreement `a ∉ dom(Σ'.L)` and hence `a ∉ nullified(Σ')`."
- WP Case 1 Necessity: "dropping P1 admits `a ∉ A_rel^Σ`; the only new key at Σ' is the fresh emitter `b ≠ a`, so by L12a's pointwise agreement `a ∉ dom(Σ'.L) = A_rel^{Σ'}` ..."
- WP Case 1 closing: "P1 because ... without `a ∈ A_rel^Σ` the only new key at Σ' is the fresh emitter `b ≠ a`, leaving `a ∉ A_rel^{Σ'}` ..."

**Problem**: Two paragraphs say the same thing in different words — the precise reader must verify three times that it is the same argument. This is exactly the duplication the anti-bloat classifier targets.
**Required**: State the argument once (the WP Case 1 Necessity slot is the natural home) and replace the other two with a citation, as is already done correctly for the "single-tuple scope, absolute under R0a" derivation ("We cite that derivation here rather than repeat the antichain argument").

### Issue 2: The crafted-span witness `{(d, δ(1, #d))}` is exhibited three times
**ASN-0086, Definition — Unit-depth retraction discipline; WP Case 2 regime (ii); WP Case 2 (Necessity)**:
- Unit-depth discipline: "a crafted broader-coverage retraction such as `Emit_R(Σ, d_retr, ∅, {(d, δ(1, #d))})` is L-invariant-conforming yet violates it."
- WP regime (ii): "e.g. `Emit_R(Σ, d_retr, ∅, {(d, δ(1, #d))})`, whose coverage `{t : d ≼ t}` ... covers every link sited under `d`."
- WP Necessity: "the regime-(ii) crafted-span witness, e.g. an `L_R^Σ` tuple with to-span `{(d, δ(1, #d))}` ..."

**Problem**: The same example construction is re-introduced in three slots. The Necessity paragraph already labels it "the regime-(ii) crafted-span witness," confirming it is a back-reference, yet still restates the span.
**Required**: Introduce the crafted span once (regime (ii)) and reference it by name elsewhere without re-exhibiting the literal endset.

### Issue 3: The active/audit distinction is framed twice in identical terms
**ASN-0086, opening section; "The Active Subset" section opener**:
- Opening: "R6a/R6b/R6c are the substantive lemmas carrying the *active/audit distinction* between `L_K` (audit trail) and `A_K` (operational currently-in-effect set)."
- Section opener: "The conceptual contribution of this section is the *active/audit distinction*: two coherent views over the same link store — `L_K` (audit trail, monotone per R3) and `A_K` (operational currently-in-effect set) ..."

**Problem**: The section opener re-states the framing the introduction already delivered, with the same parenthetical glosses. This is essay content occupying a structural slot.
**Required**: Drop one. The section opener can begin directly with the construction (Definition — Nullified) since the distinction is already announced in the intro.

### Issue 4: Nullify's P0/P1/P2 gating taxonomy is re-explained inside the wp
**ASN-0086, WP Case 1 (closing paragraph)**: "The wp lists P0 and P1 for distinct reasons (Definition of Nullify): P0 because its violation aborts the underlying Emit_R ... P1 because — although its violation does not abort emission — it is load-bearing ... The scope condition P2 ... is neither: it neither gates emission nor bears on single-tuple scope."

**Problem**: The Definition — Nullify already establishes the executing-precondition / postcondition-establishing-condition / scope-condition taxonomy at length. This closing paragraph re-derives the same taxonomy after the necessity argument has already discharged each conjunct. It advances no new reasoning.
**Required**: Delete the closing paragraph; the per-conjunct necessity argument above it already demonstrates why P0 and P1 appear and P2 does not.

### Issue 5: Definition — Nullified restates its own A_rel restriction rationale twice
**ASN-0086, Definition — Nullified**: "The set-builder restriction `a ∈ A_rel^Σ` is intentional: only tuple addresses are eligible for nullification, since `A_K^Σ` ... ranges over tuple addresses alone." ... then: "A retraction's `coverage(G')` may nonetheless target content, documents, or ghost addresses (L9 ...), but the restriction excludes those from `nullified(Σ)`."

**Problem**: The same point — the set-builder restriction confines `nullified` to `A_rel` even though coverage may reach further — is made in two sentences separated by the RetractionDirectionality re-derivation. Combined with the re-statement of Convention RetractionDirectionality ("retraction targets are in `G'` by the layer's adoption"), the definition body is doing explanatory work that belongs in the Convention itself.
**Required**: State the `A_rel` restriction once; fold the Convention reminder into a single citation rather than re-deriving "the existential checks `coverage(G')` only."

### Issue 6: R6a precondition contains a redundant conjunct
**ASN-0086, R6a**: "`(A Σ → Σ', a ∈ A_rel^Σ : a ∈ nullified(Σ) :: a ∈ nullified(Σ'))`"
**Problem**: `nullified(Σ)` is defined with the set-builder restriction `a ∈ A_rel^Σ`, so `a ∈ nullified(Σ)` already entails `a ∈ A_rel^Σ`. The bound `a ∈ A_rel^Σ` is vacuous given the guard.
**Required**: Drop the redundant `a ∈ A_rel^Σ` from the binder, or note explicitly that it is restated for emphasis only.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Observe vs Emit, and cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are correctly deferred to the Open Questions. The single-threaded SequentialAtomicTransitions axiom (ASN-0093) is the operative model here; a consistency model for concurrent Observe/Emit is genuinely new territory, not a defect in this ASN.

### Topic 2: Higher-arity typed relations `L_K^{(n)}` and dynamic type introduction across uncoordinated layers
**Why out of scope**: The note explicitly restricts to standard-triple links and flags both items as open. Neither is an error in the present development.

VERDICT: REVISE

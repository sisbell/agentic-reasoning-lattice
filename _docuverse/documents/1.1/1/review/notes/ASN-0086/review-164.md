# Review of ASN-0086

The mathematical core is sound: R0's branch-by-branch freshness discharge, R0a's two-case antichain argument (cross-home zero-counting; same-home chain + T3), the R-Scope arity-independence proof, and the Case-2 weakest-precondition derivation all hold up under checking, and the worked sketch's tumbler values verify. The findings below are the meta-prose and reviser-drift accretions the `review-mode.anti-bloat` classifier asks me to surface, plus one redundant proof invocation.

## REVISE

### Issue 1: Definition — Nullify elaborates a case its own precondition excludes
**ASN-0086, Definition — Nullify**: "The postcondition `a ∈ nullified(Σ')` thus holds only on the P1 path: off it, when `a ∉ A_rel^{Σ'}` (e.g. `a` a content, document, or ghost address with `a ≠ b`), emission still proceeds but `a ∉ nullified(Σ')`."
**Problem**: P1 (`a ∈ A_rel^Σ`) is a stated precondition of Nullify (also in the Properties table signature). The off-P1 path is a case the precondition rules out, yet a full passage develops its behavior. This is the "paragraph imagines a case the precondition already excludes" drift pattern — the reader must work past it to follow the actual (P1-satisfying) semantics.
**Required**: Drop the off-P1 elaboration. If the point is genuinely that P1 gates only the postcondition and not emission, state that once in a single clause; do not narrate the excluded path.

### Issue 2: Definition — Nullify previews its proof and justifies precondition structure rather than stating it
**ASN-0086, Definition — Nullify**: "The composition below makes precise how these roles play out: only P0 gates emission, while P1 governs the postcondition and P2 the scope." and "P2 is therefore a *scope label*, not an executable gate".
**Problem**: The first sentence is a downstream-preview ("the composition below makes precise"); the second explains *why* P2 is shaped as it is rather than *what* it requires. Both are meta-prose in a structural (definition) slot.
**Required**: State P0/P1/P2 as conditions and let the proof carry the role assignments. Remove the preview sentence and fold any executable content of "P2 is a scope label" into the condition statement itself.

### Issue 3: Unit-depth-discipline definition and relational-layer definition state the same P1-confinement commitment twice
**ASN-0086, Definition — Unit-depth retraction discipline**: "The P1 qualifier is essential: since P1 gates only the postcondition, not emission ... an unqualified Nullify call may deposit a unit-depth to-span rooted at a `b ∉ A_rel^Σ` ..."
**ASN-0086, Definition — relational layer**: "*P1-confinement of Nullify targets:* the layer further commits that every `Nullify(Σ, d_retr, a)` call it issues satisfies P1 (`a ∈ A_rel^Σ`) — the layer never retracts a content, document, or ghost address."
**Problem**: Two paragraphs in different sections carry the same content (P1 must hold for the discipline to be met). The "two paragraphs say the same thing in different words" pattern.
**Required**: State the P1-confinement requirement once (in the discipline definition) and have the relational-layer definition cite it, not re-derive it.

### Issue 4: WP section preamble duplicates Case 1's own "not the weakest precondition" framing
**ASN-0086, Weakest-Precondition Analysis (preamble)**: "Case 1 ... is a *sufficient*-precondition and load-bearingness analysis: it exhibits a conjunction that guarantees the postcondition and shows each conjunct is necessary to the conjunction, but it deliberately does *not* compute a weakest predicate ..."
**ASN-0086, Case 1 body**: "It is **not** the weakest precondition: PC is a *global* conformance condition, while the postcondition is *local* ... so PC is strictly stronger than the postcondition requires."
**Problem**: The section preamble pre-explains what Case 1 is before Case 1 says it itself. Redundant framing across two locations.
**Required**: Keep the substantive distinction in the Case 1 body; reduce the preamble to at most one sentence, or delete it.

### Issue 5: relational-layer reduction corollary invokes R7a and then declares the invocation unnecessary
**ASN-0086, Corollary (reduction to Emit_K), proof**: "That each relational-layer state-affecting operation is a single-step K.λ `→`-step follows directly from the Definition of Emit_K ... so no decomposition is needed. R7a therefore applies at `m = 1`."
**Problem**: The proof both asserts no decomposition is needed (because Emit_K *is* K.λ) and invokes R7a (whose entire purpose is decomposition). The R7a invocation is dead reasoning here. Within this ASN, the corollary is R7a's only stated consumer, so the lemma's placement reads as unearned weight.
**Required**: Either drop the R7a invocation from the corollary (the Emit_K = K.λ observation suffices) or, if R7a is retained for general layers, state that consumer explicitly so the lemma earns its place rather than appearing only to be set aside.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs Observe
The Open Questions raise atomicity of Emit against concurrent Observe and the consistency model for observed `A_K` transitions. These are genuine but belong to a future ASN; this note correctly treats `→` as serialized.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The restriction to standard-triple links is explicit and the n-ary generalization is deferred. That is appropriate scoping, not a gap.

VERDICT: REVISE

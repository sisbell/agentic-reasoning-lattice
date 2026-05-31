# Review of ASN-0086

## REVISE

### Issue 1: The `↦` / `↝` arrangement-transition machinery is inert (or contradicts) the stated ASN-0093 foundation
**ASN-0086, "Broader transition relation `↦`" and "Definition — BroadExtension" / "Lemma — LinkStoreInvarianceUnderArrangement" / "R6c-Corollary"**: "ASN-0036 admits arrangement modifications — extensions of `dom(Σ.M(d))` for existing `d ∈ dom(Σ.M)` — that change `Σ.M`'s pointwise values without extending `dom(Σ.M)`. We write `↦` for the union of `→` with these arrangement-modifying transitions..."

**Problem**: The note opens by declaring "We work in systems satisfying ASN-0093." ASN-0093's M2 (EmptyArrangement) is an invariant: `(A d ∈ dom(M) :: M(d) = ∅)`. Under M2, every document's arrangement is empty at every reachable state, so `dom(Σ.M(d)) = ∅` always and there is *no* arrangement-modifying transition that extends it. Consequently the entire `↦ \ →` class is empty in the stated foundation: `↦` collapses to `→`, `⊑̂` collapses to `⊑`, LinkStoreInvarianceUnderArrangement is vacuously true, and R6c-Corollary adds nothing over R6c. Either the note is silently working in a richer ASN-0036 system with non-empty arrangements (violating "systems satisfying ASN-0093"), or it is shipping a "LEMMA, introduced" (R6c-Corollary) plus a supporting lemma and two extension definitions whose entire subject matter cannot occur. A reader cannot tell which.

**Required**: State precisely which substrate is in force. If ASN-0093 (M2) is the foundation, drop the `↦`/`↝`-vs-`→` distinction, BroadExtension, LinkStoreInvarianceUnderArrangement, and R6c-Corollary as vacuous, and prove R6c against `→` alone. If arrangement modification is genuinely in scope, name the ASN that permits it and reconcile with M2 — do not claim ASN-0093 as the foundation while relying on transitions it forbids.

### Issue 2: R5-Cor (EmitContentUniformity) is a restatement of R0, not a new lemma
**ASN-0086, R5-Cor**: "`(A Σ : dom(Σ.M) ≠ ∅ :: (A d ∈ dom(Σ.M), F, G ∈ Endset, K ∈ T_admissible :: (E Σ' ... a : a ∉ dom(Σ.L) :: a ∈ dom(Σ'.L) ∧ Σ'.L(a) = (F, G, K))))`"

**Problem**: This existential is R0's conclusion verbatim, with the home `d` exposed. R0 already universally quantifies `F, G ∈ Endset` and `K ∈ T_admissible` — that universal *already* covers self-targeting, ghost-targeting, and cross-subspace endsets, since `Endset = 𝒫_fin(Span)` imposes no coverage restriction. "No constraint on `coverage(F)`, `coverage(G)`, `coverage(K)`" is therefore not additional content; it is a property of R0's quantifier. Promoting it to a separate lemma (consumed by R5 Steps 3–4 via "Apply R5-Cor (proved next)") manufactures a forward reference and a proof-by-restatement where a one-sentence remark on R0 would suffice.

**Required**: Demote R5-Cor to a remark inside R0 ("R0's verification inspects only L3 among the endset-content-dependent invariants; all others discharge on the emitter address alone"), and have R5 cite R0 directly. Remove the "proved next" forward reference.

### Issue 3: R6b is stated, re-justified, and then re-derived at length — three times for one claim
**ASN-0086, R6b and Worked Sketch Step 3**: R6b is given as a "DEF-Consequence" with a *Justification* paragraph; the Worked Sketch then devotes all of Step 3 to "exhibiting R6b's non-fixpoint semantics," closing with "This is the substantive content of *R6b*: retraction-of-retraction is not a fixpoint operation..."

**Problem**: The audit-slice-vs-active-subset quantification point is made in R6b's statement, repeated in its Justification, repeated again in the Definition of `nullified` ("Had the Definition quantified over `A_R^Σ`..."), and re-explained across Step 3 and `A_R^{Σ_3}`. This is the "two paragraphs say the same thing in different words" pattern compounded four ways. A worked example is legitimate, but here the example's prose re-states the lemma rather than exercising it.

**Required**: Keep one statement of the quantification-range point (in R6b), let the Definition of `nullified` carry the technical clause without re-arguing it, and let Worked Sketch Step 3 *compute* `nullified(Σ_3)` without re-narrating why the check is single-pass.

### Issue 4: Meta-prose and forward-reference accretion (anti-bloat classifier)
**ASN-0086, multiple sites**:
- After the `↝` definition: "R7a quantifies over `↝` to make its claim categorical... This preservation is automatic for any layer whose only state-affecting operations compose the substrate's K-operations. The conformance assumption is lifted into R7a's precondition, below." — justifies a definition and defers "below."
- "*Per-step substrate-invariant preservation.*" (in R7a): a paragraph whose content is that preservation "needs no per-invariant enumeration" — prose explaining why something is *not* shown.
- R5 proof opening: "The load-bearing content is the admissibility of self-targeting endsets (Steps 1–3); L-invariant verification at the emitted post-state is delegated to R0's verification machinery via R5-Cor." — proof-structure narration plus deferral.
- Unit-depth retraction discipline "*Scope.*" sub-paragraph: explains that the substrate does not enforce the discipline and why a layer must, rather than stating the discipline.

**Problem**: Each makes the reader skip past justification/placement/deferral prose to reach the claim. These are exactly the accretion patterns the `review-mode.anti-bloat` classifier flags.

**Required**: Delete the placement/deferral justifications; state R7a's quantification choice once where `↝` is defined. Replace the "Per-step preservation" paragraph with the single operative sentence ("each replay step is a primitive K-op and preserves the catalog by its ASN-0093 contract; the only step-specific obligation is FreshLinkKeyDisjointness"). Fold the R5 proof-structure preamble into the proof. Reduce the "Scope" sub-paragraph to the substrate-vs-layer distinction in one sentence.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity of Emit vs. Observe, ordering of Observe results, cardinality bound on `nullified(Σ)`
**Why out of scope**: These are listed in Open Questions and concern a consistency model and resource bounds not yet specified; they are new territory, not defects in the present claims.

### Topic 2: Multi-arity active subsets `A_K^{(n)}`
**Why out of scope**: The note explicitly confines `L_K`/`A_K` to standard triples and defers higher-arity relations; Nullify's arity-3 restriction matches that scope correctly.

VERDICT: REVISE

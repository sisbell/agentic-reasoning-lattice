# Review of ASN-0098

## REVISE

### Issue 1: LP11 is a composite-level lemma but the completeness claim treats it as per-step atomic

**ASN-0098, end of "Operation Effects on Projection"**: "The per-step lemmas LP4 through LP14 cover every operation kind of the working frame. Since reachable sequences decompose into finite chains of atomic transitions (SequentialTransitionAxiom of ASN-0093), any multi-step argument is analysed step-by-step, each step governed by one of these lemmas."

**Problem**: K.μ~ is explicitly a *named composite* of K.μ⁻ + K.μ⁺ (ASN-0047: "K.μ~ appearing in the sequence is shorthand for its K.μ⁻ + K.μ⁺ decomposition"), not an atomic transition. When a reachable sequence is decomposed into atomic transitions, a reordering becomes a K.μ⁻ step (governed by LP10, shrink) followed by a K.μ⁺ step (governed by LP9, grow). LP11 is never invoked at the atomic level — it reasons about the composite directly using ASN-0047's bijection equation. So the sentence both (a) lists LP11 among "per-step" lemmas while claiming the steps are "atomic," and (b) asserts step-by-step coverage by lemmas that, for a reordering, are LP9/LP10 rather than LP11. The composite-level result LP11 (`project' = π(project)`) is never reconciled with the atomic LP10-then-LP9 path through the contracted intermediate state.

**Required**: Either classify LP11 explicitly as a composite-level lemma (separate from the atomic per-step set LP4–LP10, LP14) and state that K.μ~ in a sequence is analysed via its K.μ⁻+K.μ⁺ decomposition with LP11 supplying the net-effect characterisation; or derive `project' = π(project)` through the atomic contraction/extension steps and show the intermediate contraction does not break the result. As written, the completeness sentence conflates atomic and composite.

### Issue 2: LP12a labels a postcondition pullback as "the weakest precondition" but omits K.μ⁻ enabledness

**ASN-0098, LP12a**: "the weakest precondition on the pre-state `Σ` under which `discoverable_from(a, d, Σ')` holds in the post-state `Σ' = K.μ⁻[d, R](Σ)` is: `… ≡ (E i : project(a, i, d, Σ) ∩ R ≠ ∅)`"

**Problem**: The derivation presupposes `Σ' = K.μ⁻[d, R](Σ)` exists — i.e., that K.μ⁻ is *enabled* at `Σ` (`d ∈ E_doc`, `dom(M(d)) ≠ ∅`, the strict-shrink admissibility `(E S :: n'_S < n_S)`, and `R` a valid D-SEQ★ prefix set). For a possibly-non-enabled operation, the weakest precondition for total correctness is `enabled(K.μ⁻[d,R]) ∧ (pullback of the postcondition)`; the predicate given is only the second conjunct. At a state where K.μ⁻ is not applicable, the stated predicate can hold while no post-state exists. The lemma overclaims by calling this "the weakest precondition" unconditionally.

**Required**: Either conjoin K.μ⁻'s applicability precondition into the wp, or rename/reframe the result as the *postcondition pullback under the assumption that K.μ⁻ is enabled at `Σ`*, stating that assumption as an explicit hypothesis rather than burying it in the notation `Σ' = K.μ⁻[d,R](Σ)`.

### Issue 3 (anti-bloat): `project` definition carries defensive rationale for its own convention

**ASN-0098, "The Projection Operation"**: "we adopt the convention that `project(e, d, Σ)` is left undefined when `d ∉ dom(Σ.M)`, rather than assigning it a default value, so that every appeal to `project` carries the membership obligation explicitly."

**Problem**: The convention ("left undefined when `d ∉ dom(Σ.M)`") is self-contained. The "rather than assigning a default value, so that every appeal carries the membership obligation explicitly" clause justifies the design choice rather than stating the definition — meta-prose the reader must skip past.

**Required**: Reduce to the convention itself; drop the justification.

### Issue 4 (anti-bloat): LP8 carries a use-site inventory and a claim-consolidation justification

**ASN-0098, LP8**: "*Remark on K.δ.* K.δ-IsNode and K.δ-IsAccount have frame `M' = M`, so LP4 covers them; K.δ-IsDocument is the document-registration case of LP8." and "The two operations are therefore covered by a single claim under the hypothesis above, without requiring a separate displacement claim per operation."

**Problem**: The first is a use-site inventory of which sub-cases land on which lemma; the second is a defense of why one claim suffices rather than two. Neither advances LP8's content — LP8's hypothesis already names the document-registration form, so the consolidation is self-evident from the statement.

**Required**: Remove the consolidation defense; fold any genuinely needed routing of K.δ-IsNode/IsAccount into a single clause if it is load-bearing, otherwise drop it.

### Issue 5 (anti-bloat): LP12a restates its result a second way and then declares the forms interchangeable

**ASN-0098, LP12a**: the "Equivalently, via LP12's coverage-range characterisation …" paragraph, closing with "This is the same wp predicate expressed by intersecting coverage with the V-restricted range, rather than the projection with `R` — the two forms are interchangeable."

**Problem**: This is the same predicate stated in a second notation followed by an explicit "the two forms are interchangeable" — two paragraphs saying the same thing. The reasoning does not advance; the second form is used nowhere downstream that the first would not serve.

**Required**: Keep one form; delete the restatement and the interchangeability note.

### Issue 6 (anti-bloat): the link-canonical class is deferred to future work in two separate locations

**ASN-0098, LP12b table entry**: "The symmetric link-canonical class … is explicitly *OUT_OF_SCOPE* for this ASN — left to future work." and **Open Questions, final bullet**: "What must discoverability preservation guarantee for a link-canonical endset … given that the content-canonical disjointness argument inverts there …"

**Problem**: Both deferrals point at the same downstream/future location for the same omitted class. The LP-Fin introductory paragraph compounds this with forward-reference accretion ("rests on a finitude lemma … established by LP-Fin below; non-canonical spans are excluded … at the type level (see below) …").

**Required**: State the deferral once (the Open Questions bullet is the natural home); strip the duplicate from the LP12b table entry and tighten the LP-Fin intro to state what LP-Fin establishes without the "see below"/"at the type level" forward scaffolding.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive invariants
**Why out of scope**: Given a V-position, returning the links whose projections contain it is a new query primitive; the Open Questions correctly defer it.

### Topic 2: V-order/I-order reflection within a projection under K.μ~
**Why out of scope**: Guarantees about the internal ordering of projected positions are new territory beyond the displacement lemmas this ASN establishes.

VERDICT: REVISE

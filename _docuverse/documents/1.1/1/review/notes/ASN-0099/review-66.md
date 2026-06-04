# Review of ASN-0099

This ASN is mathematically sound on the points I checked: F13's set-additivity chain, F9-λ's disjoint-union increment, the A1a frame discharges against ASN-0047's amended frames, the F2-V∧F3-V factoring equation, and the worked-example evaluations (Queries 1–6) all hold. The findings below are anti-bloat: the reasoning is correct but several passages restate, defend, or narrate rather than advance the argument, and one passage drifts into implementation mechanics.

## REVISE

### Issue 1: A1 block prose and F9 derivation duplicate the same content
**ASN-0099, A1 and F9**: A1 states "Each atomic operation of V ∖ {K.λ} … publishes `L' = L` in its operative frame … K.μ~ is the non-atomic K.μ⁻ + K.μ⁺ composite, so A1 reaches it through its two atomic constituents." F9 then restates verbatim in substance: "Each atomic operation {K.α, K.δ, K.μ⁺, K.μ⁻, K.μ⁺_L, K.ρ} publishes `L' = L` (A1a) … K.μ~ is the non-atomic composite K.μ⁻ + K.μ⁺ … its invariance is the transitive composition of the two atomic equalities."
**Problem**: Two paragraphs in different sections say the same thing in different words — the per-atomic-op `L'=L` publishing and the K.μ~ decomposition argument. The reader follows the same derivation twice.
**Required**: State the per-op publishing and the K.μ~-via-two-atomic-steps argument once (in A1), and have F9 cite it rather than re-derive it.

### Issue 2: Meta-lemma / sub-lemma relationship prose advances no reasoning
**ASN-0099, between ComprehensionInvariantUnderΣL and PerLinkInvarianceUnderValuePreservation**: "We also factor out the per-link primitive that grounds the chain above. It applies under a strictly weaker hypothesis … ComprehensionInvariantUnderΣL is its comprehension-level composition — full `Σ.L = Σ'.L` contributes domain equality, closing the comprehension over a shared index set, and licenses the per-link primitive at every `a` in that shared domain."
**Problem**: This is essay about how the two lemmas relate, not a step in any proof. Both lemmas' statements and proofs stand on their own; the relationship narration is meta-prose the reader must read past.
**Required**: Delete the relationship paragraph; keep the two lemma blocks. If a pointer is needed, one clause ("the per-link case of ComprehensionInvariantUnderΣL") suffices.

### Issue 3: "Empty endsets at non-type slots" drifts into implementation mechanics
**ASN-0099, "Empty endsets at non-type slots"**: "Two distinct short-circuits for an unsatisfied per-constraint conjunct: when `i > |Σ.L(a)|` the slot is structurally absent; when `i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = ∅` the slot exists but its endset carries no spans. Both routes exclude the link; abstract conformance is indifferent to which fires."
**Problem**: "short-circuit," "which fires," and "abstract conformance is indifferent to which fires" describe an evaluator's control flow, not a system guarantee. The only abstract fact is that a structurally-absent slot and an empty-endset slot each fail to witness the constraint — the two "routes" are an implementation distinction.
**Required**: Reduce to the abstract fact: a filter constraint `(i, J)` is unsatisfiable at `a` when `i > |Σ.L(a)|` or `Σ.L(a).eᵢ = ∅`. Drop the short-circuit framing.

### Issue 4: F4 carries accreted design-justification framing
**ASN-0099, F4 (MatchFormulaDesignJustification) and surrounding prose**: "The reader's promise — backlinks returnable without appreciable delay and with overlap-anchored relevance — rests on singleton overlap as F1 states it. Alternative match formulas … are alternative operations, not alternative implementations of FINDLINKS."
**Problem**: The five realizability witnesses are concrete content and should stay — but the (a)/(b) factoring narrative and the rhetorical closers ("the reader's promise rests on…") are defensive justification of why F1 is shaped as it is, accreted around the witnesses. The operative result is simply: any predicate disagreeing with F1 on a realizable pair is a different operation; the witnesses exhibit this.
**Required**: Keep the witnesses; cut the rationale framing to one sentence stating the individuation claim. Flagging placement and volume, not the witnesses' existence.

### Issue 5: Timing non-specification is deferred to in two places
**ASN-0099, "Local Atomicity" and "Open Questions"**: Local Atomicity states "no foundation invariant of this ASN formalises a timing bound beyond 'next query after K.λ commitment reflects the link'," and Open Questions asks "Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance…".
**Problem**: The Local Atomicity sentence pre-answers the Open Question; the same non-specified topic is addressed in two sections.
**Required**: Pick one home for the timing observation (the Open Question) and drop the duplicate pre-answer.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / endset-to-V-position resolution)
**Why out of scope**: The ASN correctly lists this under "What We Have Not Specified"; it is a distinct future operation, not a gap in FINDLINKS.

### Topic 2: Partition tolerance / multi-instance consistency model
**Why out of scope**: Replication and inter-server protocol are excluded by the stated scope; the Open Questions correctly defer these.

VERDICT: REVISE

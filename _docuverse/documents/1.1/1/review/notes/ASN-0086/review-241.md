# Review of ASN-0086

## REVISE

### Issue 1: Nullify's *Rationale* contradicts the self-emit branch of its own precondition P-tgt

**ASN-0086, Definition — Nullify, *Rationale***: "Retraction is a destructive withdrawal, which Nelson scopes to existing, owned material — *'Only the owner has a right to withdraw a document or change it'* — never to addresses no one has yet baptized..."

**Problem**: This rationale justifies only the P1 disjunct, and is flatly contradicted by the other admissible branch of the very precondition it sits under. P-tgt is `P1 ∨ (a = a_emit(Σ, d_retr))`. The self-emit branch is reached *precisely when ¬P1*, i.e. when `a ∉ A_rel^Σ = dom(Σ.L)` — an address **no one has yet baptized**. The worked sketch confirms this in Step 4: "Here P1 (`a ∈ A_rel^Σ`) is false (`a₃ ∉ dom(Σ_3.L)`), but the self-emit disjunct ... holds," and the call deposits the retractor at the fresh `a₃` and nullifies it in the same step. So Nullify *does* retract an as-yet-unbaptized address (baptizing it simultaneously) — exactly what the Rationale asserts it "never" does. The prose justifies a narrower operation than the one specified.

**Required**: Reconcile the Rationale with the self-emit branch. Either (a) qualify it to state that self-emit is a baptize-and-retract-in-one-atomic-step case where the target is owned-at-commit (so "existing owned material" is read at Σ', not Σ), or (b) restrict the Rationale to the P1 branch and explain the self-emit branch's distinct justification. As written, the design grounding (Nelson, `granf2.c:37`) covers P1 only and misdescribes P-tgt.

### Issue 2: The K.λ L3-discharge argument is stated three times in near-identical words

**ASN-0086, R0 *Value-shape consequence***: "The standard triple `(F, G, K)` discharges K.λ's L3 precondition directly ... — arity is 3, both content slots `F, G ∈ Endset`, and `K ∈ T_admissible` forces a non-empty type slot — so the caller discharges no separate value requirement."
**ASN-0086, Definition — Emit_K**: "The typed signature thus discharges K.λ's L3 precondition unconditionally — arity is 3, both content slots `F, G ∈ Endset`, and `K ∈ T_admissible` forces a non-empty type slot — so K.λ's contract carries over with no separate value requirement on the caller."

**Problem**: These are the same sentence twice (the "arity is 3 / both content slots / non-empty type slot" clause is verbatim), and the same point is made a third time in Emit_K's "operationally K.λ ... specializes to N = 3 and e₃ = K" sentence immediately preceding. The note carries the `review-mode.anti-bloat` classifier; "two paragraphs in the same document say the same thing in different words" is a flagged pattern.

**Required**: State the L3-discharge once (it belongs at the Emit_K definition, the operation it characterizes) and have R0 cite it rather than restate it.

### Issue 3: R0's freshness proof re-derives ASN-0093 freshness lemmas instead of citing them, inconsistently with the rest of the note

**ASN-0086, R0 proof** (freshness bullets): the multi-part *cross-home distinctness* / *within-home freshness* / *cross-subspace* re-derivation establishing `a ∉ dom(Σ.L) ∪ dom(Σ.C)`.

**Problem**: ASN-0093's FirstEmissionFreshness and SubsequentEmissionFreshness already prove exactly `a ∉ dom(C) ∪ dom(L)` for the first/subsequent emission, with the same within-document / cross-document (T10) / cross-subspace (T7) case split R0 reconstructs by hand. The note's own worked sketch (Steps 1–4) repeatedly *cites* SubsequentEmissionFreshness for this fact — so R0's from-scratch re-derivation is both redundant against a foundation lemma and inconsistent with how the same fact is discharged elsewhere in the document.

**Required**: Cite FirstEmissionFreshness / SubsequentEmissionFreshness for the `dom(C) ∪ dom(L)` exclusion, and retain only the home(a)=d / on-chain facts that R0 genuinely adds (via FirstEmission / ChainDiscipline). This collapses the freshness bullets to a citation plus the structural postcondition.

## OUT_OF_SCOPE

### Topic 1: Concurrency model for Emit vs Observe
**Why out of scope**: The atomicity/consistency questions (whether `A_K` transitions are observed atomically with respect to concurrent `Observe`) are genuine future territory. ASN-0093's SequentialAtomicTransitions already serializes transitions, so single-state results here stand; a concurrency layer is a separate ASN.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note deliberately restricts every `L_K` to `|Σ.L(a)| = 3` and correctly observes higher-arity links inhabit `A_rel` but index no tuple. Whether to model them as `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is new structure, not a defect in this ASN.

VERDICT: REVISE

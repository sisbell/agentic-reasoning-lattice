# Review of ASN-0040

This note carries the `review-mode.anti-bloat` classifier, and the dominant findings are forward-reference accretion: defensive justifications, repeated rationale, and the same proof written out three or four times. I found no hard correctness bug, but the meta-prose and duplication are extensive enough to warrant REVISE.

## REVISE

### Issue 1: The T4-preservation (TA5a) case analysis is written out four times
**ASN-0040, Bop proof / §B10 / §B6 sufficiency / wp(baptize, B10)**: The identical case split — "d = 1 uses TA5a's `k ∈ {0,1}` branch; d = 2 uses `k = 2 ∧ zeros(t) ≤ 2` (= B6(iii)); m > 0 uses `k = 0` unconditionally" — appears in the Bop "B10 preservation" subsection, again in the §B10 inductive step, again in §B6's (⟸) sufficiency, and again in the wp(baptize, B10) derivation.
**Problem**: Four substantially identical paragraphs. Two paragraphs in the same document saying the same thing is a flagged pattern; this is the same argument quadrupled.
**Required**: Prove "the new element of any baptism satisfies T4" once (it is exactly the content B10 needs), and cite it from §B6, Bop, and the wp section rather than re-deriving.

### Issue 2: B4 is stated twice in full
**ASN-0040, Bop "STRUCTURAL (on Op)" and §B4 (Atomic Baptism)**: Bop carries the full statement "each `baptize(p, d) ∈ Op` is a single atomic edge … `baptize(p, d)(Σ).B = Σ.B ∪ {next(Σ.B, p, d)}`," and §B4 restates the same equation and the no-intermediate-state clause.
**Problem**: Duplicate definitions of one label.
**Required**: State B4 once (in §B4) and have Bop reference it by name.

### Issue 3: B_type proof opening is misplaced and forward-references B_fin
**ASN-0040, B_type proof**: "*Proof.* By induction on the number of state transitions… Case 2 of the inductive step selects max(children(B, p, d)), whose existence requires children to be a finite set — supplied by B_fin (Registry Finiteness)."
**Problem**: This sentence pre-announces Case 2 before the base case is even stated, and forward-references B_fin, which is defined several sections later. B_type sits before B_fin in the document but its proof depends on it — the dependency should at least be visible at the point of use, not as a defensive preamble.
**Required**: Delete the preamble; cite B_fin inline at Case 2 where max is actually taken, or reorder so B_fin precedes B_type.

### Issue 4: Downstream-consumer enumeration in B_type's introduction
**ASN-0040, before B_type**: "We record this preservation as a labelled invariant rather than as informal commentary, since later proofs (B10, B1, B8) appeal to `t ∈ Σ.B ⟹ t ∈ T` and the label makes the citation explicit."
**Problem**: A definition's introduction enumerating its downstream consumers is a flagged pattern; it does not advance the meaning of B_type.
**Required**: Drop the sentence. State the invariant; consumers cite it where they need it.

### Issue 5: Non-circularity / document-ordering justifications around B0a and Bridge1
**ASN-0040, B0a**: "This disjointness is logically prior to, and independent of, Bop's freshness proof: Bop establishes that `next(Σ.B, p, d) ∉ Σ.B` … but the partition itself stands even before that proof — by construction of the two class-defining predicates rather than by their distinct extensional effects." And Bridge1: "The equation `Σ' = baptize(p, d)(Σ)` discharges the *State Space and Transitions* obligation … no informal 'induced by' relation is invoked."
**Problem**: Prose that justifies ordering/non-circularity rather than advancing the claim — a flagged pattern. The partition's disjointness is established by the class-defining predicates; the paragraph defending that against a freshness-proof-circularity worry is noise.
**Required**: Reduce to the one-line construction ("each `op` is in exactly one class by its symbol") and delete the defense.

### Issue 6: "Load-bearing parenthesization" notation gloss
**ASN-0040, B0a**: "The parenthesization of the existential is load-bearing: `(p, d)` is bound by the inner quantifier … so the equation … makes sense only inside the existential's scope."
**Problem**: Meta-prose explaining how to read a quantifier; it does not advance the reasoning.
**Required**: Remove. Correct scoping is the formula's responsibility, not a paragraph's.

### Issue 7: Comparative essay in B8
**ASN-0040, §B8**: "ASN-0034 establishes GlobalUniqueness from the algebraic angle … Here we reach the same conclusion through the set-theoretic lens … The algebraic route answers 'why is each stream collision-free?'; the set-theoretic route answers 'why are different streams collision-free with each other?'"
**Problem**: Essay content comparing two derivation routes. It is rationale, not argument.
**Required**: Cut to at most one sentence noting B8 restates GlobalUniqueness at the namespace level; keep the proof.

### Issue 8: Repeated "B6(iii) is ASN-0040's bridging restatement of TA5a" rationale
**ASN-0040, §B6, §B10, Bop proof**: The same parenthetical — "(B6(iii)'s uniform form is ASN-0040's bridging restatement of TA5a's two d-cases…)" — recurs in §B6 sufficiency, §B10 Case 1, and the Bop proof.
**Problem**: Same clarifying remark restated in three sections (multiple paragraphs deferring to/explaining the same point).
**Required**: State it once at B6's definition; do not repeat at each use.

### Issue 9: Re-lettering of foundation (ASN-0034) notation, with explanation
**ASN-0040, State Space and Transitions**: "This is the same Kripke framework fixed by ASN-0034's AllocatedSet, re-lettered: ASN-0034's Σ (vocabulary) and s (state) are written Op and Σ here."
**Problem**: ASN-0034 (a foundation) uses Σ for the transition vocabulary and `s`/𝒮 for states; ASN-0040 reuses Σ for an individual *state* and renames the vocabulary to Op. Reusing a foundation's symbol for a different object invites collision, and the explanatory sentence is itself accretion. Standard 7 discourages reinventing foundation notation.
**Required**: Either keep ASN-0034's lettering (state `s`, vocabulary Σ) or, if Σ-for-state is wanted for Σ.B, drop the explanatory re-lettering note and simply declare the symbols once.

### Issue 10: Joint-induction framing repeatedly defers to "the proofs below"
**ASN-0040, Bop proof**: "The dedicated §B1, §B10, §B_fin, §B_type proofs below carry the respective single-step preservation arguments…" and "Non-B6 namespaces require additional case analysis — the complete argument … is given in the B1 proof below."
**Problem**: Multiple paragraphs deferring to the same downstream locations (a flagged pattern), while those locations then re-run arguments already partially given in Bop (see Issue 1).
**Required**: Pick one home for each preservation argument (the dedicated §) and have Bop cite it, rather than half-proving and forward-pointing.

## OUT_OF_SCOPE

### Topic 1: Parent-prerequisite (must p ∈ Σ.B before baptizing beneath it)
**Why out of scope**: Explicitly deferred to Tumbler Ownership; the ASN correctly leaves Bop's PRE without `p ∈ Σ.B` and lists it as an Open Question. No action needed.

### Topic 2: Concrete valid seed sets B₀ and the Occupied predicate
**Why out of scope**: B₀ contents are settled by the activation-discipline ASN via Bridge2, and Occupied by a future content-storage ASN. B3/Bridge2 are framed as forward requirements, not current invariants — acceptable.

VERDICT: REVISE

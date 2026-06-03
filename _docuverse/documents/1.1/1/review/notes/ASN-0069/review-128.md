# Review of ASN-0069

I read the full derivation and checked the proofs against the foundation contracts (ASN-0034/0036/0040/0047, all declared dependencies and all foundations, so their use is in-bounds). The correctness core is sound: the K.δ sub-case dispatch (first vs. subsequent fork), the B-Seq/B0a/B1/B2/B4 discharge for B8's same-namespace clause, the empty-source reduction (V7), the V5a frame-composition lemma, the V11 state-stamped induction, and the two ValidComposite★ verifications all hold up under scrutiny. Boundary cases (empty document, fork-of-fork, sibling forks, source with a link subspace, T4 zero-count never exceeded) are covered. I found no proof-by-checkmark and no proof-by-"similarly" — the symmetric uses of V5a are genuine instantiations of a general lemma, not hand-waves.

The remaining issues are the prose-accretion patterns this note's anti-bloat classifier targets.

## REVISE

### Issue 1: Premature φ-detail block quote in §"Sharing, Not Duplication" duplicates the §"The Arrangement Layer" development
**ASN-0069, §"Sharing, Not Duplication"**: the section block-quotes J4's clause (ii) in full — "K.μ⁺ populating `M'(d_new)` via the unique order-preserving bijection `φ : V_{s_C}(d_op) → V_{s_C}(d_new)` ... Derived consequence: `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`" — to support V3 (content-store invariance).

**Problem**: V3's actual derivation uses only the frame conditions (`C' = C` across K.δ + K.μ⁺ + K.ρ); it states this explicitly ("By the conjunction of these elementary frames, the composite preserves `C`"). The φ/bijection/range machinery in the block quote is irrelevant to V3 and is then properly developed — paraphrased again — at the head of §"The Arrangement Layer" ("J4's clause (ii) installs content via the order-preserving bijection `φ : V_{s_C}(d_op) → V_{s_C}(d_new)`, constraining the *range* of `M'(d_new)` to `ran(M(d_op)|_{V_{s_C}(d_op)})`"). So J4(ii) appears twice — once as a premature full block quote, once as the paraphrase that actually sets up the V4 literal-inheritance commitment. A reader following V3 must skip the φ detail to follow the content-invariance claim.

**Required**: In §"Sharing, Not Duplication," reduce the J4 citation to the part V3 needs (content is shared by reference, no K.α step runs — "no new content addresses are introduced"), and let §"The Arrangement Layer" carry the φ/range development, where it is load-bearing for V4. Do not state J4(ii)'s bijection content in both places.

### Issue 2: Process-narration sentences in structural slots
**ASN-0069, §"The Arrangement Layer"** ("We name the commitment as V4 and then derive what follows from it.") and **§"Subspace Selectivity"** ("We derive why this must be so abstractly.").

**Problem**: These sentences narrate the document's own structure rather than advancing the argument — the kind of meta-prose that compounds across cycles. The reasoning that follows stands without them.

**Required**: Delete the narration sentences; begin directly with the substantive claim (the literal-inheritance definition in the first case, the CL-OWN necessity argument in the second).

## OUT_OF_SCOPE

### Topic 1: Edited-chain correspondence, concurrent fork, snapshot-vs-living forks, transcludent sources
**Why out of scope**: The Open Questions section correctly defers these. V11's transitive-identity premise explicitly excludes intermediate-version editing, and the ASN is honest about not claiming same-V-position visibility across later states. These are future-ASN territory, not gaps in this ASN.

### Topic 2: Nelson's "contents of document <doc id>" vs. the d_prev operand on subsequent forks
**Why out of scope**: The subsequent-fork content source `d_op = d_prev` (most recent version, not `d_src`) is fixed by J4's operand-tracking rule in the foundation (ASN-0047), which this ASN must follow. V10a and the worked example surface the consequence. Reconciling J4's operand choice with Nelson's wording would be a question for the foundation, not a revision here.

VERDICT: REVISE

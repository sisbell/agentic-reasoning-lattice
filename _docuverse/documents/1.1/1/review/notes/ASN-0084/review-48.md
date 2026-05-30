# Review of ASN-0084

## REVISE

### Issue 1: Helper lemma relies on ℕ properties absent from the foundation

**ASN-0084, Canonical decomposition, "Existence of a maximum (helper lemma)"**: "NAT-cancel's right-cancellation property (ASN-0034)… NAT-cancel's left-cancellation property (ASN-0034)… NAT-sub's right-inverse property (ASN-0034)… NAT-sub's left-inverse property…"

**Problem**: ASN-0034's natural-number axioms, as extracted, are exactly NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, and NAT-wellorder. There is no `NAT-sub`, no `NAT-cancel`, and no subtraction inverse/cancellation lemma. The entire helper-lemma proof (and every width-arithmetic step that cites `NAT-sub`) is built on foundation properties that do not exist in the cited foundation. Cancellation and the subtraction inverse must either be derived from the five available axioms or the citations are unsupported.

**Required**: Either (a) derive cancellation and the `m − n` inverse properties from NAT-closure/NAT-addcompat/NAT-order/NAT-discrete explicitly within this ASN, or (b) correct the citations to name the axioms that actually carry the steps. The bare appeal "NAT-sub (ASN-0034)" / "NAT-cancel (ASN-0034)" is a claim that ASN-0034 exports these; it does not.

### Issue 2: Phantom foundation labels S7c and S9

**ASN-0084, R-SP and R-NS(NS-inv)**: "S7 (StructuralAttribution, ≡ S7a ∧ S7b ∧ S7c ∧ S7d…)"; "S7b (element-level I-addresses) and S7c (element-field depth)"; "S9 (two-stream separation) — 'no modification to Σ.M(d) can alter Σ.C'."

**Problem**: The ASN-0036 claim statements provided define S7 with preconditions over S7a, S7b, S7d (and T4-family) — there is no S7c and no S9. Yet ASN-0084 repeatedly cites both as load-bearing ASN-0036 invariants and even asserts the decomposition S7 ≡ S7a ∧ S7b ∧ S7c ∧ S7d. These are citations to claims absent from the foundation.

**Required**: Remove the S7c/S9 citations or replace them with the actual foundation claims that supply element-field depth and two-stream separation. If S7 has no S7c sub-clause, the "≡ S7a ∧ S7b ∧ S7c ∧ S7d" expansion is simply wrong and must be corrected.

### Issue 3: Step (b) re-proves a foundation theorem

**ASN-0084, Canonical decomposition, step (b)**: "Two maximal runs sharing a V-position are identical… we show b₁ = b₂ by establishing v₁ = v₂, a₁ = a₂, and n₁ = n₂…" followed by the closing "By (b) — equivalently, by S8's uniqueness of the maximal-run decomposition (ASN-0036)…"

**Problem**: S8 (ASN-0036) already exports that the maximal-run decomposition is unique. The ASN itself concedes the equivalence ("equivalently, by S8's uniqueness"). The multi-paragraph proof of (b) therefore re-establishes a verified foundation result rather than citing it. Only the *operational* connection (termination/confluence of the Split/Merge process — step (c)) is genuinely new. The depth spent re-deriving uniqueness is wasted obligation.

**Required**: Replace step (b)'s standalone re-proof with a citation to S8's uniqueness, retaining only what (c) actually consumes (that every terminal partition is maximal, then S8 closes uniqueness).

### Issue 4: Ordering-justification meta-prose in R-NS and R-SP

**ASN-0084, R-NS "Forward-reference note (on presentation order only)" and R-SP "Forward-reference note"**: "This lemma is stated here… so that subsequent sections cite a single non-S dispatch point rather than re-deriving…"; "The reader who prefers a strictly bottom-up presentation may read… and return to R-SP afterwards."

**Problem**: This is prose that justifies document ordering and argues non-circularity of forward references rather than advancing any claim. Both lemmas carry near-identical notes deferring to the same downstream results (R-BLK, R-COMM). Per the anti-bloat directive, ordering justification and "see X below" deferral chains are findings at source.

**Required**: Delete the presentation-order notes. State the lemma and its dependencies; a forward dependency needs no essay defending its placement.

### Issue 5: REARRANGE_K parameterization essay

**ASN-0084, REARRANGE_K, "Parameterization convention"**: "the subscript K denotes *static* parameterization… Equivalently, one may read REARRANGE_K(Σ, d) as a three-argument operation… The letter K is chosen to disambiguate from the content store Σ.C: the subscript indexes *cut* sequences, not content."

**Problem**: Essay content in a structural slot. The static/dynamic discussion and especially the letter-choice disambiguation ("K is chosen to disambiguate from Σ.C") do not advance the operation's contract. The operation is fully specified by its precondition R-PRE(K) and postcondition; this paragraph is noise the reader must work past.

**Required**: Reduce to the one operative sentence (REARRANGE_K has precondition R-PRE(K) and signature (Σ, d) ↦ Σ'). Drop the notation rationale.

### Issue 6: PermutationDisplacement — self-labeled unused commentary and consumer inventory

**ASN-0084, Displacement Analysis**: "*Informal commentary (not used by downstream lemmas).* … One expects forward and backward magnitudes to balance… making this precise would require defining sums and products on the signed-magnitude carrier, which we deliberately do not do"; and "the lemmas that consume Δ (R-DISP, R-PPERM, R-SPERM, R-BLK) compare Δ-values only by equality."

**Problem**: The first is essay content explicitly tagged as not used by any lemma — it advances no reasoning. The second is a downstream-consumer inventory attached to the definition. Both are the accretion patterns the classifier flags.

**Required**: Remove the informal-commentary paragraph. Drop the consumer enumeration; the equality-only comparison can be stated once where Δ is actually compared, not as a roster.

### Issue 7: CS3 necessity sketch duplicates the R-PRE(iv) sketch in contrast prose

**ASN-0084, R-SP, "Well-typedness argument (R-PRE(iii) — CS3)"**: "*This is not a Q-failing counterexample in the R-PRE(iv) sense.* Where the R-PRE(iv) sketch exhibited a well-typed instance of Q… no such well-typed instance exists here."

**Problem**: A substantial fraction of the CS3 sketch is spent contrasting itself against the R-PRE(iv) sketch ("not a counterexample in the iv sense," "distinct, but equally load-bearing, mode"). The two sketches restate the same well-typed-vs-unsatisfiable distinction in different words across paragraphs. The core CS3 point (cross-subspace cuts leave region widths/β-extent untyped) is sound and worth one short statement; the repeated cross-referencing is redundant.

**Required**: State the CS3 well-typedness failure once and drop the comparative prose that re-explains the iv sketch.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The Open Questions correctly defer generalization beyond 4 cuts and the algebra of composed rearrangements to future work; these are new territory, not defects in the pivot/swap treatment here.

### Topic 2: Which pre-state run pairs produce post-state mergeability
**Why out of scope**: R-BLK explicitly declines to characterize which adjacencies merge after rearrangement, tying it to pre-state I-address arithmetic. That is a separate analysis, legitimately bracketed.

VERDICT: REVISE

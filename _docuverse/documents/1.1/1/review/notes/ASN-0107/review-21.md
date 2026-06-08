# Review of ASN-0107

This note is technically sound. I verified the worked instance end-to-end (zeros-counts, subspace identifiers, `sat` evaluations, the contraction Δ = −2 within R2's `k=3` band, the reorder 3→0) and it holds. P1/P2 correctly pin set-over-address cardinality; E1–E4 and the D-laws are correctly derived; the R6 wp pullback is genuinely *weakest* and consistent with LP12a's `enabled ∧ body` convention; A1b correctly conditions on the no-incoming-links premise to dodge the ghost-reference (LP17) trap. No correctness error found.

The findings are all of the kind the `review-mode.anti-bloat` classifier targets: prose that restates a claim or wanders into performance/essay territory in a structural slot.

## REVISE

### Issue 1: Performance aside in a counting-semantics claim
**ASN-0107, "What Is Counted" (P1 elaboration)**: "The search-scaling guarantee (LM 4/60, 'the quantity of links not satisfying a request does not in principle impede search on others') is the dual observation that non-satisfying links contribute 0; the count is insensitive to them."
**Problem**: Search-scaling is an implementation-performance property ("does not impede search"), not a guarantee about what the count *means*. The substantive content — non-matching links contribute 0 — is already stated by P1 itself. The sentence does not advance the specification of `num`.
**Required**: Delete the search-scaling sentence; P1 already carries the `{0,1}` contribution.

### Issue 2: R1 intro restates E2
**ASN-0107, R1 introduction**: "So `num` is *blind* to any notion of link nullification or retraction: no such notion has a count-visible mechanism, because nothing ever leaves `dom(Σ.L)`, and the existence count (E2) therefore cannot fall."
**Problem**: "the existence count therefore cannot fall" is E2 verbatim; "nothing ever leaves `dom(Σ.L)`" is L12/E2's premise. This paragraph re-derives E2 inside R1's preamble. The reader has to skip the restatement to reach R1's actual content (the minimal-contraction split).
**Required**: Cut the restatement; cite E2 once and proceed to the (P-max)/(P-uniq)/(P-slot)/(P-sole) split.

### Issue 3: Essay duplicating W1
**ASN-0107, "What the Count Does Not Say" (opening)**: "A count is an abstraction in the strict sense: a number standing in for a set, stripped of everything that distinguishes the set's members. The caller who reads `num(Q, Σ) = 47` learns the size of the answer and nothing of its content."
**Problem**: This is essay content occupying the slot immediately before W1, which then states the same thing formally ("`num` … identifies no link's address, owner, endsets, type, or order of arrival"). Two passages, different words, same claim.
**Required**: Drop the essay opening; let W1 carry the claim. The `= 47` numeral adds nothing W1 lacks.

### Issue 4: D3 followup paragraph duplicates D3
**ASN-0107, paragraph following D3**: "A deleted link, in this model, is not removed from `dom(Σ.L)` … but ceases to be reachable through the arrangement the request consults, so it falls out of the discovery count while remaining a permanent member of the store. The archive (the store) and the view (the resolved, discoverable population) diverge exactly here."
**Problem**: D3 already states `num = 0` is "absence *in the view*, not non-existence *in the archive*." The followup restates the archive/view divergence in different words without introducing a new guarantee.
**Required**: Fold any genuinely new content (the L12 "no removal operation" mechanism) into D3's justification and remove the standalone restatement.

### Issue 5: R5 is a synthesis-restatement of E4 + D2
**ASN-0107, R5 (ConservationConditional)**: "Against a fixed permanent `Q`, the existence count's change … equals the number of matching links created on the path, with no subtractive term (E4). Under discovery anchoring this breaks: by D1 arrangement edits move membership … so the net change need not equal the number of matching creations."
**Problem**: The first half is E4 quoted; the second half is D1/D2 quoted. R5 adds the single framing word "conditional," but as written it re-states two prior claims rather than establishing a new one. If the intended new content is "conservation is anchoring-conditional," that is one sentence, not a paragraph re-deriving E4 and D2.
**Required**: Reduce R5 to the one load-bearing sentence (conservation holds against permanent `Q` by E4, fails under discovery by D2) and cite rather than re-state.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored, separately-evolving request parts
The first Open Question (three parts anchored to different documents' arrangements) is correctly deferred — it requires a multi-document coupling model this note does not build. No action needed.

### Topic 2: Count vs. retrieval-cardinality agreement
The third Open Question (staleness between `num` and what FINDLINKS/ASN-0099 would return) belongs with the retrieval operation, which the Scope section places out of bounds. Correctly deferred.

VERDICT: REVISE

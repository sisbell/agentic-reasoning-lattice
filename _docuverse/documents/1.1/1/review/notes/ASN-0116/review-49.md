# Review of ASN-0116

The mathematics here is sound and the operation is genuinely well-specified. INSERT is correctly exhibited as the valid composite `K.α`(×n) → `K.μ⁻` → `K.μ⁺` → `K.ρ`(×n); the clause-1 preconditions are discharged step by step (including the correct First/Subsequent emission split and the strict-contraction bound `J−1 < N`), the clause-2 couplings J0/J1★/J1'★ are driven correctly by the range identity RAN, the block-disjointness interval arithmetic is exact at every boundary (`J=1`, `J=N`, `J=N+1`, empty subspace), the I3-vs-block-fill factoring is handled cleanly (gapped `M'₀` plus I-NEW), and IP6's wp is the genuinely non-trivial *containment* rather than the over-strong emptiness. The worked example checks the right postconditions against concrete numbers, including the re-insertion-after-contraction subtlety. I found no correctness gap, no missing edge case, no invalid cross-ASN reference, and no drift.

The note carries `review-mode.anti-bloat`, so the remaining findings are residual editorial/deferral prose.

## REVISE

### Issue 1: Repeated deferral to the valid-composite section
**ASN-0116, "What is allocated…" + Effect clauses I-ALLOC, I-PROV**: Three paragraphs in different sections announce that preconditions are proved downstream in the same place:
- "…the valid-composite section below settling step by step which lemma governs each emission."
- I-ALLOC: "its per-step preconditions (freshness, and the `w_k ∈ Val` typing…) are discharged in the valid-composite section."
- I-PROV: "(its per-step precondition discharged in the valid-composite section)."

**Problem**: This is the anti-bloat pattern "multiple paragraphs in different sections defer to the same downstream location." The valid-composite section is a real, self-standing proof; the per-clause forward pointers repeat the same navigation note without advancing the clause they sit in.
**Required**: State the deferral once — e.g., a single sentence at the head of the Effect section ("each clause's per-step preconditions are discharged in the valid-composite section below") — and drop the per-clause repetitions, letting I-ALLOC and I-PROV state their postconditions and cite the foundation atomic only.

### Issue 2: Defensive-contrast framing on facts that stand alone
**ASN-0116, several sites**: A recurring "X, not Y" / "X rather than Y" construction editorializes about rigor or necessity rather than conveying content:
- "Its freshness is **proved, not assumed**: K.α's emission lemmas…"
- "Dropping K.μ⁻ here is **forced, not optional**: with J−1 = N…"
- "Gregory's evidence makes this **structural rather than incidental**: the insertion cut is bounded above by the next subspace boundary…"

**Problem**: These match "defensive justifications." In each case the substance that follows the colon is load-bearing and complete on its own (the freshness lemmas; the inapplicability of K.μ⁻ when nothing contracts; the subspace-boundary bound). The contrast clauses pre-empt a critic rather than advance the argument.
**Required**: Drop the contrast framing, keep the substance. (Distinguish from the genuinely technical "intensional (by origin), not extensional (by value)" in IP0, which is a real distinction and should stay.)

## OUT_OF_SCOPE

None to raise. The four Open Questions (shared/transcluded insertion point, concurrent-insertion freshness, transclusion-origin provenance, post-fragmentation contiguity) correctly defer their topics to future ASNs rather than claiming them here, and the note states no claim belonging to COPY/DELETE/REARRANGE/MAKELINK/FINDLINKS/etc. IP4 and IP6 treat link *survival* and *discoverability-preservation as consequences of INSERT* (using only the foundation `discoverable_from`), not link creation or discovery, so they are in scope.

VERDICT: REVISE

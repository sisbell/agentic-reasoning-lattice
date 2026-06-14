# Review of ASN-0131

The mathematics here is sound. I checked every introduced claim against the foundation contracts and the definition, and the proofs hold: RE-ADDR's freshness argument (R0a antichain + unit-depth to-set), RE-UDIST's filter-factoring through the region-independent `Avail(Σ)`, the RE-UDIST-∩ counterexample (non-injective `Σ.M(d)`, distinct V-positions sharing one I-address), the RE-CWP weakest precondition (`Δ`/`I_R` split via the D-CWP bridge), and the RE-RET biconditional (forward via R6a + the Θ hypothesis; backward via R-Scope SingleTupleScope) all check out. The worked instance exercises every distinctive postcondition and computes correctly, including the field-agreement argument for `coverage(e₃) ∩ dom(Σ.C) = ∅`. The Θ-content-disjointness gap and the W⊆s_C scoping are honestly flagged and routed to Open Questions. There are no "by similarly," no bare checkmarks, no missing boundary cases, and no improper non-foundation cross-references.

The findings below are anti-bloat — the classifier this note carries — and one citation precision item.

## REVISE

### Issue 1: Standing-assumption paragraph forward-references RE-RET and pre-states its rationale
**ASN-0131, "The unit of the answer: anchoring without names" (standing-assumption paragraph)**: "The commitment carries more than that to-set shape, and one stronger consequence is load-bearing below: `Nullify` emits its retraction with an *empty from-set* … and the retraction-stability result RE-RET rests on that exclusion: its claim that a retraction emitter's from-set and to-set are content-disjoint *unconditionally* (below) holds precisely because `Nullify`'s from-set is `∅`."

**Problem**: This is forward-reference accretion of two of the listed kinds: a setup paragraph that *enumerates a downstream consumer* of an assumption ("RE-RET rests on that exclusion … (below)") instead of advancing the assumption's meaning, and *explains why the assumption is needed* rather than stating it. The same content — the from-set is empty because the commitment admits only `Nullify`, excluding ASN-0086's attributed retractions, hence content-disjoint — is then restated at the point of use in the retraction section ("the from-set `∅` — empty because the standing commitment admits only `Nullify` retractions, not the attributed ones ASN-0086 otherwise permits"). Two paragraphs in different sections say the same thing.

**Required**: At the adoption site, state the standing assumption and its direct consequences (empty from-set, unit-depth to-set) as facts. Delete the "load-bearing below" / "RE-RET rests on that exclusion … (below)" justification and let RE-RET cite the consequence where it is actually consumed.

### Issue 2: Insert/delete stability paragraph elaborates a case analysis it then declares non-load-bearing
**ASN-0131, "Stability: the answer as the document is edited" (insert/delete paragraph)**: develops the gain/loss/both image characterization, the donor-position mechanics, the "shift **then** backfill" reconstruction, and the tight/non-tight LP19a refinement — then: "The full case split is not needed here — the load-bearing conclusion does not turn on which placement yields gain versus loss".

**Problem**: The load-bearing argument is already complete before this elaboration: the M-only lift establishes that insert/delete write only `Σ.M(d)` and frame `L,E,R`; `Avail(Σ)` is a function of `Σ.L` alone, so only the image moves; the bare-shift gap-state is a non-queryable intermediate by atomicity; therefore RE tracks the image by membership with spans fixed (RE-IDENT). Everything after that — the donor/gap gain-loss mechanics, the backfill reconstruction (which is the note's own composition, not a foundation lemma), and the tight-endset detour — is material the paragraph itself disclaims. A reader must work past it to reach the conclusion. The depth-scoping (insert `#p ≥ 2`, delete `#p = 2`) and the gap/atomicity objection are warranted and should stay; the disclaimed case split and the backfill/tight-endset elaboration are the noise.

**Required**: Keep the depth-scoping, the M-only lift, the population-unmoved fact, and the gap-state/atomicity resolution. State non-monotonicity-as-a-class in one sentence if it is worth keeping. Cut the donor-position gain/loss mechanics, the "shift then backfill" reconstruction, and the LP19a tight-endset refinement that the note flags as not load-bearing.

### Issue 3: Closing summary mis-cites RE-CWP for general image-under-editing
**ASN-0131, final sentence**: "The answer's stability thus reduces to two tracked motions: the region's image under editing (RE-CWP) and the active population under emission and retraction (RE-RET)."

**Problem**: RE-CWP is the contraction weakest-precondition only. The general "image under editing" claim — covering extension, contraction, reordering, and the shift-based insert/delete — is RE-EDIT. Citing RE-CWP alone for "image under editing" drops the claim that actually carries that scope.

**Required**: Cite RE-EDIT for the image-under-editing motion, noting RE-CWP as the exact contraction sub-case.

## OUT_OF_SCOPE

### Topic 1: Type-slot match against a content region (Θ content-disjointness)
**Why out of scope**: RE-RET correctly carries `coverage(Θ) ∩ dom(Σ.C) = ∅` as an explicit, acknowledged construction hypothesis (not a hidden assumption), with the exception routed to Open Question 6. The conditional statement of RE-RET is the right move; resolving when a type-slot match against content is meaningful is future territory.

### Topic 2: Link-subspace regions, rendered answers, intersection-equality, non-co-resident link stores, whole-vs-touching-spans
**Why out of scope**: Open Questions 1, 3, 4, 5, 7 defer these correctly. Each is genuinely new territory (a different region subspace, a V-order-rendered answer mode, an arrangement-restriction refinement of RE-UDIST-∩, a cross-store completeness guarantee, the touching-vs-whole convention), not a gap in the present content-region, content-identity operation. I checked that the note's claims do not silently depend on resolving any of them.

VERDICT: REVISE

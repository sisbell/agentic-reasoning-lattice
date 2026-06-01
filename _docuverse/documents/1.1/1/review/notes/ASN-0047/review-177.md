# Review of ASN-0047

## REVISE

### Issue 1: FrontierEquivalence presupposes every non-node entity is a tracked-allocator emission, with no backing invariant
**ASN-0047, FrontierEquivalence (Lemma)**: "for every reachable state `Σ` and every operand `t ∈ Σ.E` with `¬IsNode(t)`, let `A` denote the allocator whose tracked chain contains `t` — t is one of A's emissions, and A is unique by T10a.6."
**Problem**: The clause "t is one of A's emissions" asserts that *every* `¬IsNode` member of E inhabits some T10a-tracked allocator domain. T10a.6 supplies *uniqueness* of the owning allocator only on the hypothesis that `t` is in some tracked domain — it does not establish that hypothesis. Nothing in ExtendedReachableStateInvariants names an invariant "every non-node entity in E is a tracked-allocator emission." It is true by construction (entities enter only via K.δ `inc` steps), but the lemma consumes it as a given rather than citing or proving it. Since FrontierEquivalence is the sole discharge for K.δ k=0 freshness (`inc(t,0) ∉ E`), the gap propagates into every sibling-document allocation.
**Required**: Either add the membership claim as a named per-state invariant (every `e ∈ E` with `¬IsNode(e)` is an emission of a unique tracked sub-allocator) preserved by K.δ, or have the lemma cite the K.δ discharge that establishes it. "A is unique by T10a.6" must be preceded by an established "A exists."

### Issue 2: K.δ's "M untouched / registration via E" claim is stated three times
**ASN-0047, K.δ (Entity creation)**: the same content appears in *Effect on M* ("K.δ leaves M unchanged... the entity's entry into `E_doc`... is carried solely by `E' = E ∪ {e}`"), in *Subsumption of ASN-0093's K.σ* ("K.δ carries document registration through the entry of `e` into `E_doc`... with `M'(e) = ∅`"), and in *Frame* ("The sole effect of K.δ is `E' = E ∪ {e}`; a document's entry into `E_doc` is registration through the entity set alone, with M untouched").
**Problem**: Three paragraphs in one operation definition restate the identical fact (document registration goes through E, M is framed) in different words — the "two paragraphs say the same thing in different words" pattern, here tripled.
**Required**: State the M-frame and the K.σ-subsumption once. The *Frame* line carries the normative content; *Effect on M* and *Subsumption* should be deleted or collapsed to a single sentence.

### Issue 3: FrontierEquivalence is re-derived at three sites
**ASN-0047**: the lemma is fully proved (forward/reverse directions) at its statement; then re-explained in *K.δ case (ii) discharge*, k=0 bullet ("T10a chain-advancement uniqueness at `(t,0)`... GlobalUniqueness... delivers `e ∉ E`"); then re-walked a third time in *Worked example: entity hierarchy*, Step 4, feature (a).
**Problem**: Forward-reference accretion. The proof is load-bearing once; the two downstream sites restate the mechanism rather than simply citing the lemma's name and conclusion.
**Required**: At the K.δ k=0 bullet and the worked-example step, cite `FrontierEquivalence` and state only its conclusion (`inc(t,0) ∉ E`). Remove the restated forward/reverse mechanics.

### Issue 4: Reviser-drift — K.δ k=1 paragraph reasons about a case its own dispatch excludes
**ASN-0047, K.δ case (ii), k = 1**: "Subsequent versions of t arise from K.δ k = 0 events whose operand is a prior version of t (`inc(prev_version, 0)`); those are sibling-advances on `A_v(t)`'s frontier and are dispatched by the k = 0 case above, not by k = 1."
**Problem**: The k=1 precondition already fires at most once per `(t,1)` (stated one sentence earlier). The added sentences then describe what k=1 does *not* handle and re-route the reader to the k=0 case — meta-prose about case boundaries that does not advance the k=1 discharge. This is the flagged pattern "a paragraph imagines a case the claim's precondition already excludes."
**Required**: Delete the "Subsequent versions..." sentence; the per-`(t,1)` uniqueness sentence already closes the k=1 case.

### Issue 5: Multiple sections defer the same obligations to ExtendedReachableStateInvariants / the K.μ~ fixity proof
**ASN-0047**: P7a (Provenance coverage) states "its proof is given once under Class (b)"; P4a is derived inline at its definition *and* re-discharged in Class (b); S8★ is explained at its definition *and* re-prosed in the Class (a) verification text; the K.μ~ link-subspace fixity result is deferred to ("Steps 1–3 of the link-subspace fixity proof") from the S3★, P4★, CL-OWN, CL-UNIQ, and S8★ matrix cells and again in the worked example.
**Problem**: This is forward-reference accretion across distinct sections all pointing at the same downstream proof — distinct from the previously-declined *matrix-navigation* finding, which concerned only the matrix's index convention. Here the duplication is in prose bodies (P4a derived twice, S8★ prosed twice).
**Required**: For each obligation, give the derivation exactly once and have all other sites cite it by label with no restated argument. In particular, P4a should be derived only under Class (b) (its definition paragraph should state the property and point forward), and S8★'s discharge prose should not appear both at the definition and in Class (a).

### Issue 6: The override is announced with meta-prose about not restating it
**ASN-0047, Typing note (M total — overrides foundation)**: "We state the translation once here; the inherited operations below use `d ∈ E_doc` directly, without restating it." and "The override is not a reinterpretation but a replacement."
**Problem**: The substantive content is the identity `d ∈ dom(M) ⟺ d ∈ E_doc` and the translation rule. The surrounding sentences ("not a reinterpretation but a replacement," "we state the translation once here... without restating it") are essay/defensive framing in a normative slot — they justify the editorial choice rather than advance the override.
**Required**: Keep the identity and the translation rule; delete the self-referential sentences about restatement and the "not-a-reinterpretation-but-a-replacement" framing.

## OUT_OF_SCOPE

### Topic 1: Permanent impossibility of link reordering
The K.μ~ link-subspace fixity theorem entails that a document's link display order is fixed at allocation order forever (no transition can permute it). This is consistent with Nelson's "permanent order of arrival," so it is not an error here, but the *consequences* of irrevocable link order (e.g., interaction with link withdrawal/tombstoning) belong to a future operations ASN — already gestured at in Open Questions.
**Why out of scope**: This is downstream design territory (withdrawal mechanisms), not a defect in the present state/transition model.

VERDICT: REVISE

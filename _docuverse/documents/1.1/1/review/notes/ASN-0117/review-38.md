# Review of ASN-0117

The technical content held up under scrutiny: I verified the K.μ⁻ + K.μ⁺ composite realisation (precondition discharge at the intermediate state, strict-contraction and strict-extension obligations, the `R = ∅` single-step case), the J0/J1★/J1'★ coupling arguments, the range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` (including the SD-disjointness step that makes it exact), the wp's necessity and sufficiency, and all five worked scenarios' arithmetic — no errors found. The remaining findings are all accretion of the kind the anti-bloat classifier flags: duplicated claims, deferral sentences, and review-cycle sediment around the worked examples.

## REVISE

### Issue 1: duplicate deferral and re-announcement of the coupling discharge
**ASN-0117, "What shifts" §Effect, end of *Case `R = ∅`* paragraph**: "Coupling and frame discharge for this single-step realisation is taken up with the composite's, below." — immediately followed by the next paragraph's opener "DELETE's coupling and frame obligations are discharged for both realisations — trivially via J2 for the `R = ∅` single step, explicitly for the `R ≠ ∅` composite."
**Problem**: Two consecutive meta-sentences announce the same discharge; the first exists only to defer to the paragraph that begins one line later. This is the forward-reference deferral pattern compounding — the reader must skip past the announcement to reach the discharge it announces.
**Required**: Delete the deferral sentence; the case paragraph can end at the `n'_{s_C} = 0` specialisation note. The discharge paragraph already covers both realisations.

### Issue 2: pure cross-reference narration inside P5's statement
**ASN-0117, P5 (DocumentIsolation)**: "The per-subspace split here is the same one S3★ forces on `M'(d)` above (§\"The document remains one coherent sequence\")."
**Problem**: The sentence advances nothing — it narrates document structure ("this split is the same as that split"). The substantive justification for the per-subspace reading (the counterexample showing the whole-range form `ran(M'(d)) ⊆ dom(Σ'.C)` fails for documents with links) already lives in the coherent-sequence section. P5's statement is complete without the pointer.
**Required**: Delete the sentence.

### Issue 3: claims inventory states each frame equality twice
**ASN-0117, Frame clauses and Claims Introduced table**: P0 ("`dom(C') = dom(C)` with all values preserved") and DEL-CIMM ("`Σ'.C = Σ.C`") are the same proposition under two labels — the DEL-CIMM clause itself cites "(P0)" in acknowledgment. Likewise DEL-LIMM, DEL-FENT, and DEL-FPROV are verbatim projections of DEL-CFRAME's three conjuncts, each defined as "DEL-CFRAME's … clause" and each given its own table row alongside DEL-CFRAME's row.
**Problem**: This is the accretion shape where a unifying name (DEL-CFRAME, evidently added in a later cycle) was introduced without retiring the per-clause names it subsumes. `Σ'.L = Σ.L` is now asserted in the coupling paragraph, in DEL-LIMM, in P4's prose, and twice in the table. The reader must reconcile five table rows that carry two propositions (the content frame; the extended-state frame).
**Required**: One naming layer. Either fold DEL-CIMM into P0 (moving the ASN-0082 D-I citation onto P0's row) and absorb DEL-LIMM/DEL-FENT/DEL-FPROV into DEL-CFRAME (retargeting the citations in P4, P5, the wp section, and the worked examples), or keep the three per-clause names and demote DEL-CFRAME to the name of the discharge paragraph rather than a separate introduced claim. The auxiliary content (P1/P8 on DEL-FENT, P4★/P4a/P7a on DEL-FPROV) survives either consolidation as a sentence on the retained claim.

### Issue 4: worked-example preambles narrate review-coverage rationale
**ASN-0117, "A worked deletion"**: "The primary scenario moved a lone suffix position, so it never exercised DELETE's signature effect…"; "None of the cases above exercises the most delicate composite interaction…"; "The scenarios above all live inside the single document `d`; none exercises the operation's signature isolation guarantee."
**Problem**: Three example blocks open by explaining what the *preceding* examples failed to cover — the rationale of the prior review findings that prompted each example, retained as preamble. The examples themselves are exactly right and should stay; the coverage narration is sediment. The bold headers ("Boundary — leading-span delete (`J = 1`, `R ≠ ∅`)", "Cross-document transclusion (P5 in the concrete)") already name what each case exercises.
**Required**: Trim each preamble to the case statement itself (one clause identifying what the scenario exercises is fine; the retrospective "none of the above did X" framing is not needed).

### Issue 5: symbols used ahead of their introduction
**ASN-0117, "The problem", closing display**: "`σ(q_k) = q_{k−c}` for `k ≥ J + c`" — `J` is not defined until two sections later (`p = q_J` in "What shifts"); `c` is glossed inline but `J` is not (`σ` and `w_ord` are ASN-0082 foundation notation, so they are fine). Similarly, **"The document remains one coherent sequence", S8★ paragraph**: "the survivors `M'(d)(q_{J−1}) = a_{J−1}` and `M'(d)(q_J) = a_{J+c}`" uses the abbreviation `a_k = M(d)(q_k)`, which is introduced only later in "A worked deletion".
**Problem**: Unbound symbols at point of use. The intro display is flagged as a preview, but a preview must still be readable with what precedes it.
**Required**: Gloss `J` at first use (e.g., "where `q_J` is the first deleted slot") and introduce the `a_k = M(d)(q_k)` abbreviation at its first occurrence in the S8★ paragraph rather than in the worked example.

## OUT_OF_SCOPE

### Topic 1: totalization of DELETE over ill-formed spans
**Why out of scope**: The ASN correctly carries containment as a precondition and records rejection-vs-clipping as an open question; specifying the caller-facing total operation is a separate ASN, not a defect here.

### Topic 2: historical backtrack reconstructibility
**Why out of scope**: P0 establishes the bytes persist, but what additional state (prior arrangements, version snapshots) must persist for exact backtrack is new territory the Open Questions already name.

### Topic 3: concurrent deletions without a serializing authority
**Why out of scope**: SequentialTransitionAxiom makes transitions totally ordered in the present model; relaxing that is a future concurrency ASN.

VERDICT: REVISE

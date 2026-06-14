# Review of ASN-0134

The mathematics here is sound and, in places, exemplary — H1/H2's case splits handle the first-emission boundary explicitly (not "by similar reasoning"), G2 catches a real literal-vs-operative gap in I1a, and §8's strict-implication chain is backed by two concrete converse-witnesses plus a worked trace. I am not asking for re-proofs. The note carries the `review-mode.anti-bloat` classifier and is (per its own history) a tightening pass on converged content, so the findings below are consolidation findings: the same load-bearing claim is asserted and re-derived at three or four sites, and several paragraphs defer to one another in a ring. Each fix is "cut and cite the canonical home," not "argue more."

## REVISE

### Issue 1: "Chain contiguity is model-intrinsic" is proved four times
**ASN-0134, A6 / W3 / §5-closing / G1(i)**: the claim appears at A6 ("*properly stronger* than `C1c`/`L1c` in asserting each home's population fills its sub-allocator chain without gaps"), is fully proved at W3 ("Dense chain contiguity … is *model-intrinsic*, preserved by every valid step"), re-asserted in §5's closing ("the chain-contiguity members … included — is model-intrinsic"), and **re-derived a fourth time inside G1(i)**: "Chain contiguity is no exception — once each step is a valid `→_sh` step it deposits at `inc(max,·)`, so each home's population is a gapless initial segment at every state … carried by A6's step-local reading like every other conjunct (W3)."
**Problem**: W3 is the canonical home (it is the named claim). The G1(i) passage re-runs W3's proof when it only needs to cite it; the §5 closing re-states it; A6 already flags it. This is the "compounds across cycles" pattern — each cycle that worried contiguity might be uncovered added another assertion.
**Required**: Keep the proof at W3 only. In G1(i), cut the re-derivation down to a citation — the G1-specific content is the *next* sentence ("only collision-freedom is bought by serialization"), which should remain. Drop the standalone re-assertion in §5's closing paragraph; A6 listing it in the package and W3 classifying it suffices.

### Issue 2: "A batch is not a single operation / not atomic" stated four times, with A1 deferring forward to A5
**ASN-0134, A1 / post-A1 paragraph / A5**: A1's parenthetical says a batch "is *not* a single operation in this sense: it is realized as *many* steps and is **not** atomic, its decomposition and divisibility A5's subject, not this paragraph's; the degenerate batch sizes `m ∈ {0, 1}` are A5's too." The post-A1 paragraph repeats it ("the batch *as a whole* is the non-atomic composite A5 governs, never a 'single state-changing operation' the one-step clause speaks of"). A5 then states it as its own claim.
**Problem**: A1 names batches three times only to forward everything about them to A5 — textbook forward-reference accretion. The phrases "A5's subject, not this paragraph's" and "the degenerate batch sizes `m ∈ {0,1}` are A5's too" are pure routing, not reasoning.
**Required**: In A1, replace the batch parenthetical and the post-A1 batch sentence with a single clause: "(a multi-step batch is many steps, not one operation — A5)." Let A5 own batch non-atomicity, including the `m ∈ {0,1}` degenerate cases.

### Issue 3: contiguity-vs-atomicity / "reader gap" deferral ring (A5 ↔ §6/W4 ↔ OQ5)
**ASN-0134, post-A5 / W4 / Open Question 5**: the post-A5 paragraph: "contiguity does **not** construct atomicity … we defer it to Open Question 5." W4: "leaving open the reader gap A5 already defers." OQ5: "closing the interior-prefix gap A5 leaves open even for a W4-contiguous run."
**Problem**: Three paragraphs in three sections defer to one another about the same gap — the "multiple paragraphs defer to the same downstream location" pattern. A reader chasing the distinction is bounced A5 → OQ5 → back to A5 via W4.
**Required**: State the contiguity≠atomicity distinction once (it belongs at A5, where both modes of divisibility are defined), with one forward pointer to OQ5. W4 should say only "W4 buys contiguity, not reader-atomicity" without re-deferring; OQ5 states the open problem without re-explaining the gap.

### Issue 4: §1 scope parenthetical duplicates "What this note does not cover"
**ASN-0134, §1**: "The agents, the scheduler that places their proposals, the fairness with which it does so: all of that is upstream of `𝔼` and out of scope here (it is the coordination layer's named hypothesis, the implementer's territory)."
**Problem**: This is restated as the first bullet of "What this note does not cover" ("**The scheduler and its fairness.** … is the implementer's and protocol layer's concern"). The dedicated section is the right home for scope exclusions.
**Required**: In §1, keep at most "(the scheduler that produces `𝔼` is out of scope — see *What this note does not cover*)" and drop the duplicated enumeration of agents/scheduler/fairness.

### Issue 5: soundness-vs-durability stated three times in close succession (§8)
**ASN-0134, §8 (V1 and after)**: V1 states it ("Extending a verdict from 'held at `r`' to 'holds through `r'`' requires an *additional* hypothesis"). The next paragraph restates it as two bullets ("*Soundness* … *Durability* …"). The "The practical reading for a quiescence recognizer" paragraph restates it a third time.
**Problem**: The same dichotomy three times in three consecutive paragraphs. The bulleted version and the "practical reading" version say the same thing in different words.
**Required**: Keep V1's statement and one elaboration (the two bullets are the clearest form). Fold the "practical reading" paragraph's distinct content (recognizer guidance) into one or two sentences without re-stating the soundness/durability split.

### Issue 6: SAFE(b) re-derives the §4 instance (i)/(ii) analysis
**ASN-0134, SAFE proof (b)**: clause (b)(ii) re-explains, at length, that per-home MIC admits the duplicate, that clause 8 fixes it, that dedup consults the active not the audit slice (resurrection-by-reemission), and that instance (ii) "is non-duplicating regardless."
**Problem**: This duplicates §4 (instances (i)/(ii)), G2, and W5/ASN-0128 I2 nearly point-for-point inside the theorem's proof. A theorem proof should cite the established results, not re-run them.
**Required**: Reduce SAFE(b)(ii) to: "under clause 8, I1a applies (G2; §4 instance (i)), so `A_K` holds ≤1 tuple per coverage class; resurrection-after-nullification is by design (W5, ASN-0128 I2), not a duplicate." Move the resurrection mechanics out of the proof — they already live in W5.

### Issue 7: flagged micro-patterns (exhaustiveness claim, defensive justification, "if we'd done it wrong" aside)
**ASN-0134, A1 / A5 / §8**: A1 — "the five together exhaust the zero-step realizations"; A5 — "The bound `m ≥ 2` is essential, not cosmetic"; §8 — "Were `Q`-affecting scoped to the `Observe_{K_i}` constituents alone, that frontier-advancing step would be wrongly certified harmless."
**Problem**: These are the patterns the anti-bloat brief names directly — an exhaustiveness claim, a defensive "X is essential not cosmetic," and a counterfactual "if the definition were wrong" justification. None advances the reasoning; each defends a choice already made by the construction.
**Required**: Cut "the five together exhaust …" (the enumeration speaks for itself). Cut "essential, not cosmetic" (the `m ∈ {0,1}` sentence that follows is the content). In §8, replace the counterfactual with the positive statement: "the quantifier ranges over every `c_i`, frontier constituents included" — and stop there.

### Issue 8: MIC clause 6 restates W6 and is admitted non-load-bearing
**ASN-0134, §9, MIC clause 6 + minimality paragraph**: "Clause 6 is the exception — not load-bearing, since `W6` already makes runtime registry writes nonexistent — kept only so the contract names every obligation an implementer might fear they must discharge."
**Problem**: Clause 6 duplicates W6, and the note itself certifies it carries no weight. In a contract the prose calls "minimal," a self-admittedly-vacuous clause kept "so an implementer might [not] fear" is defensive completeness — exactly what an anti-bloat pass should resolve, not enshrine.
**Required**: Either drop clause 6 (W6 covers it; one sentence in §9 prose can note runtime registry-write-freedom) and call the remaining contract minimal, or keep it but delete the "kept only so the contract names every obligation an implementer might fear" justification. Do not retain both the redundant clause and its meta-justification.

## OUT_OF_SCOPE

(none — every finding is present-but-redundant prose, not missing coverage; the residual order-dependence of §4 instance (ii) is correctly acknowledged in-note as persisting under both disciplines, which is honest, not a gap.)

VERDICT: REVISE

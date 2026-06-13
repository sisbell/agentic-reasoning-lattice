# Review of ASN-0130

This is a strong, carefully-built ASN. I checked the load-bearing proofs and could not find a hole: PR-ENC-uniq follows from prefix-freeness; PR2's DAG argument is airtight in both directions ((a) backward-pointing references, (b) self-reference excluded at every deposit *and* hit); PR3a's expansion-well-typing is a correct capture-avoiding substitution induction with WT-α/WT-W properly discharged; PR1's split of permanence across content-intrinsic conjuncts (ii)/(iii) versus the withdrawable endorsement (iv) is honest and correctly proved per-step; the PR0/PR5a wp case analyses are sound; and PR5's ST⁺ soundness rests correctly on PD0's "fixity of bound values" ground. The worked example exercises the right boundaries (validation-on-hit rejection, self-reference, frontier-ghost, branch-in-supersession). No cross-ASN references outside the foundation set, no reinvented foundation notation.

The findings are all the accretion the `review-mode.anti-bloat` classifier asks me to surface: the front-matter and the de-registration discussion each state the same claims two or three times.

## REVISE

### Issue 1: Front-matter re-derives PR1 and PR2 rather than pointing to them

**ASN-0130, "The design rests on three foundation facts" (intro) + "What this note commits" + PR1**: The PR1 validation-split is stated three times, near-verbatim:
- Intro: "its parse-validity and well-typedness, checked at registration, **are validation forever** (its reference-endorsement, **the one validation conjunct not read off content, is a withdrawable deposit-time fact** — PR1)."
- Commitments: "these content/signature-intrinsic facts **are validation forever, no runtime re-validation needed**. The third validation conjunct ... is **a withdrawable deposit-time endorsement, not permanent** ..."
- PR1 body: "they **are validation forever, no re-validation path needed** ..."

The same doubling hits PR2 (the DAG / "expansion terminates ... without any cycle check" argument appears in the intro three-facts, again in the commitments bullet, and again in PR2). The intro paragraph's legitimate work is naming the three foundation *dependencies* (S0/S1, S4, total ordering); the elaboration of each into its PR's conclusion is what duplicates.

**Problem**: Two preview layers ahead of the body, each mini-proving PR1/PR2, with phrase-level reuse ("validation forever," "withdrawable deposit-time"). This is the "two paragraphs say the same thing in different words" pattern in a structural slot.
**Required**: Reduce the intro three-facts to the three dependencies plus pointers (`PR1`, `PR-ENC`, `PR2`); let "What this note commits" be a one-line-per-PR abstract, not a restatement of each PR's caveats. Keep the argument in the body.

### Issue 2: De-registration narrative and the Open-question-3 deferral repeated across PR1, PR3, and PS2

**ASN-0130, PR1 / PR3 / PS2 ("Retraction interacts ...")**: The "de-registration withdraws the endorsement, not the artifact; evaluation/resolution survive" point is made three times:
- PR1: "What a referent's de-registration withdraws is the endorsement, never the artifact or its standing audit-slice proof ..."
- PR3: "what de-registration withdraws is the *endorsement* (condition (iv) for new registrations), not the artifact or its standing proof in the audit slice."
- PS2: "previously registered referencing definitions validated against their own deposit pre-states, and PR1's proof concerns those states; evaluation likewise survives ..."

And the deferral to Open question 3 appears twice, near-verbatim:
- PR1: "whether a dangling live reference should be surfaced, tolerated, or blocked is Open question 3."
- PS2: "Whether dangling *live* references ... should be surfaced, tolerated, or blocked is genuinely open (Open question 3)."

**Problem**: PR3's statement is in-place (it is PR3's own precondition concern) and PR1's belongs to its (iv) discussion, but the PS2 retraction paragraph recaps both and re-defers to OQ3 — the "multiple paragraphs defer to the same downstream location" pattern, plus a verbatim OQ3 sentence.
**Required**: Drop PR1's trailing OQ3 clause (it previews PS2/OQ3); have PS2's retraction paragraph state only the class-specific retraction effect (a `Nullify_Binary` on a `pdef` tuple de-registers; audit slice retains history) and cite PR1/PR3 for the harmlessness rather than restating it. State the OQ3 deferral once.

## OUT_OF_SCOPE

### Topic 1: Cost/size of expansion
PR2 guarantees that `expand(a)` *terminates*; it does not bound its size, and shared sub-references can make the inlined term exponential in the DAG. Resource bounds on resolution/expansion are an implementation concern, not a state invariant — correctly outside this note (and consistent with "The concrete encoding" being deferred).

META: not applicable — the note defines abstract state (designated `pdef`/`pd_stable` classes, definition-as-content), operations (`register_pred`, `certify_pd_stable`, `evaluate`), and invariants, with the byte encoding explicitly left as a substrate parameter; it has not drifted into implementation mechanics.

VERDICT: REVISE

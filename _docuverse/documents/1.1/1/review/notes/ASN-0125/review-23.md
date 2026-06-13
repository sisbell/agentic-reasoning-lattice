# Review of ASN-0125

I worked the proofs carefully — EL0 through EL16, EL-DM's discipline induction, the supersession-relation definitions, and the worked example. The substance is sound. The reachability discharge for K.λ-only composites is correct; EL4's per-claim SingleTarget (PrefixSpanCoverage + R0a) is airtight; the wp Case 2 invocations in EL6(iii)/EL6(iv)/EL7(iv) correctly discharge ASN-0086's third conjunct via freshness + R0a; EL-DM's induction covers every editing-layer operation with no circularity (EL6(v)/EL7(vi) are independent of EL-DM); the worked example's addresses, succ_o transitions, and currency values all check out; boundary cases (empty store at Σ₀, self-supersession exclusion, fork, the current = ∅ standoff, revert, nullified-successor-in-current at EL14(e), middle-element de-listing at EL9(2), position reuse at EL10) are all handled. Foundation citations are accurate and confined to foundation ASNs.

The findings below are one concrete cross-reference error and three meta-prose items — the latter expected given the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: EL7(ii) cites the wrong Open Question
**ASN-0125, EDITop / EL7(ii)**: "whether some layer should couple edit to listing is the separate question of Open Question 7."
**Problem**: The Open Questions list is unnumbered. Counting it, the 7th question is span-level endset correspondence ("When an edit narrows or reshapes an endset, must the record carry span-level correspondence between the old and new endsets…"). Edit-to-listing coupling is the **8th** (last) question ("What coupling invariant, if any, should bind an edit to the home registry's listing of original and successor…"). So "Open Question 7" points to the wrong question. Compounding this: EL7(ii) is the *only* numbered reference to an unnumbered list, so the pointer is fragile — any reordering breaks it silently.
**Required**: Reference the edit-listing question by content rather than by number (e.g., "the open question of whether a layer should couple edit to listing"), or number the Open Questions list and correct this to 8.

### Issue 2: EL6(iv) opens with structure-announcing meta-prose
**ASN-0125, EL6(iv)**: "Activity splits into a design-bearing half that holds unconditionally and a full-state half that needs the discipline hypothesis."
**Problem**: This sentence previews the shape of the proof rather than advancing it; the reader skips it to reach the two actual frame results (the unconditional `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` and the discipline-conditional full equality). The labels "design-bearing half" / "full-state half" carry no content the two results don't already carry.
**Required**: State the two sub-results directly, dropping the framing sentence.

### Issue 3: EL3's necessity proof closes with design-cost essay
**ASN-0125, EL3, closing remarks**: "Two remarks complete the comparison the question poses. … *The carrier costs nothing in mechanism, something in coordination.* The relation-space carrier requires zero substrate change … Its price is that the class is a convention…"
**Problem**: EL3 is a necessity theorem and the necessity is fully discharged before the remarks. The first remark ("The menu was shorter than it looked") is load-bearing — it answers the question's claim that "a separate supersession link" and "a typed relation" are one object, and should stay. The second remark is a cost/coordination observation: it states no claim and contributes nothing to the necessity argument — essay content in a derivation slot. The "Two remarks complete the comparison" framing is itself meta.
**Required**: Drop or relocate the cost remark. Its substantive germ (refinements under a common prefix stay jointly queryable, "but the root must be agreed") foreshadows the prefix-rooted-subtype-closure Open Question and RQ6 — fold it there rather than into the necessity proof.

### Issue 4: the ASN-0042 principal-resolution deferral is stated twice, with overlay speculation
**ASN-0125, EL8(b) and EL13**: EL8(b) — "resolving a home further to a named owner is the office of an ownership layer (ASN-0042) overlaid on the substrate … an overlay the attribution guarantee neither needs nor invokes." EL13 — "under an ASN-0042 ownership overlay, owner domains span many documents."
**Problem**: The same deferral (named-principal resolution lives in the ASN-0042 overlay, not in `Σ`) appears in two sections — the "multiple paragraphs defer to the same downstream location" pattern. EL13's version additionally asserts overlay behavior ("owner domains span many documents") that is ownership-layer territory, not a substrate fact this ASN establishes; the substrate result EL13 actually owns is the narrower "latest is per-home, not per-principal."
**Required**: State the principal-resolution deferral once. In EL13, keep the substrate fact (per-home/per-document-chain latest is state-recoverable; per-principal is not) and compress or drop the overlay-domain speculation to a bare pointer.

## OUT_OF_SCOPE

### The deferred relation semantics are correctly scoped
The note pushes authority-for-non-asserter-retraction, supersession-of-retraction, claims-targeting-claims (meta-claim stratification), non-empty-currency disciplines, temporal witnesses, endset-level correspondence, and edit↔listing coupling into its Open Questions. These are genuinely new territory (authority/ownership layering, meta-claim well-foundedness, correspondence algebra), not gaps in EL0–EL16. No additional out-of-scope coverage is owed; nothing in scope was wrongly claimed.

VERDICT: REVISE

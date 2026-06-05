# Review of ASN-0100

## REVISE

### Issue 1: Citation to a nonexistent postcondition

**ASN-0100, §Effect Two: Placement**: "TumblerAdd's piecewise rule at action point `m_C` copies the leading `m_C − 1` components of `p`, all strictly positive (position 1 is the subspace identifier `s_C ≥ 1`; the remaining `m_C − 2` are `1`, by ValidInsertionPosition postcondition (d) or **ValidFirstInsertionPosition postcondition (d)**, ASN-0036)..."

**Problem**: ValidFirstInsertionPosition (ASN-0036) has only postconditions (a), (b), (c). There is no postcondition (d). The substance is correct — ValidFirstInsertionPosition's *definition* fixes `v = [s_C, 1, …, 1]`, so the leading components are all `1` — but the cited label does not exist. (The companion citation "ValidInsertionPosition postcondition (d)" is correct; only the empty-case citation is spurious.) A proof that cites a clause that isn't there is not discharged.

**Required**: Replace the empty-case citation with ValidFirstInsertionPosition's definition (`v = [s_C, 1, …, 1]` of depth `m`) or its postcondition (a)/(b).

### Issue 2: Redundant restatement of the uniqueness conclusion

**ASN-0100, §Atomicity and Canonical Order**: The subsection opens with "The post-state Σ' is *uniquely determined* by the operation contract; the substrate decomposition that realises it is not," gives a full component-by-component uniqueness proof and forced-ordering analysis, then closes with the Nelson-quote paragraph: "What INSERT fixes is the post-state Σ': it is uniquely determined by `(Σ, p, content)`. The decomposition that realises it is not — many elementary interleavings reach the same Σ'..."

**Problem**: The closing paragraph restates the opening sentence and the forced-ordering conclusion in different words, adding no new claim. This is the "two paragraphs say the same thing" accretion the anti-bloat classifier flags.

**Required**: Fold the Nelson framing into the opening or drop the closing restatement; keep the uniqueness conclusion stated once.

### Issue 3: Implementation-mechanics tangent in an abstract verification slot

**ASN-0100, §Cross-subspace isolation**: "Gregory's implementation realises this isolation via a two-blade 'knife' whose blades bracket the text subspace; link-subspace crums are classified as outside the shift region and are uniformly left untouched."

**Problem**: The abstract isolation property is already discharged in the same paragraph by the `INS.frame.subspace` frame. The knife description is implementation mechanics that adds no evidential weight to the abstract guarantee and does not advance the verification — it forces the precise reader past a mechanism aside.

**Required**: Remove, or relocate to a brief implementation-grounding aside if it carries evidential value (as the foundation axioms' Gregory commentary does); it does not belong inside the invariant-verification step.

### Issue 4: Forward-reference accretion in the worked example

**ASN-0100, §A Worked Example**: The "Projection-shift correspondence — numeric instantiation of INS.proj" block fully instantiates, and the "non-tight contrast" sub-paragraph pre-proves, the general claim INS.proj — which is not canonically stated or derived until §Coverage and link discoverability. The "non-tight contrast" sub-paragraph additionally invents a second endset `e_1'` (data not in the example) solely to exhibit the opposite regime.

**Problem**: The example forward-depends on a claim stated far below, forcing the reader to jump ahead, and duplicates the framing of the later general derivation. The imagined-`e_1'` sub-paragraph is essay content illustrating a case the example's own data excludes — exactly the forward-reference / imagined-case accretion the classifier flags.

**Required**: Either move the projection instantiation after INS.proj is stated, or have the example illustrate only the three regions and defer the `N_{ℓ,i}` tight/non-tight contrast to INS.proj's own statement. Do not both pre-prove and later prove the same claim.

## OUT_OF_SCOPE

(none — the INSERT-vs-COPY section uses COPY only as a foil for INS.identity and defines no COPY claims; the open questions about self-composition and concurrency are legitimately about INSERT.)

VERDICT: REVISE

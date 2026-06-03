# Review of ASN-0069

I checked the core construction (FORK as the K.δ + K.μ⁺ + K.ρ×n composite, plus the K.δ-alone empty case), the inductions in §"Identity by Sub-Allocation", the ValidComposite★ discharge, and the V10/V11 independence/chain arguments. The logic is sound: the foundation-lemma preconditions (B-Seq, B0a, B1, B2, B4 for B8; ChildSpawnFreshness/FrontierEquivalence for K.δ freshness) are properly discharged, the empty/sibling/chain boundaries are all covered, the worked example exercises V1/V3/V4/V5/V6/V8/V9 against a concrete arrangement, and invariant preservation is correctly delegated to ASN-0047's ExtendedReachableStateInvariants once the fork is shown to be a valid composite. I found no correctness gaps.

The findings below are anti-bloat / forward-reference noise, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: §"Frame: Source Isolation" opens with re-quoted-intro + forward-reference scaffolding
**ASN-0069, §"Frame: Source Isolation"**: "This is Nelson's most emphatically stated commitment — the "without damaging the originals" clause [LM 2/45] quoted at the outset is precisely the source-isolation requirement, and V5 below is what discharges it."

**Problem**: The load-bearing sentence is the first one ("The fork must not modify `d_src`"). The remainder re-quotes the Nelson clause already given verbatim in the opening section and forward-points to V5 ("V5 below is what discharges it"). This is meta-prose wrapped around a forward reference — the reader must skip past a back-citation and a forward-citation to reach the actual content (V5a / V5).

**Required**: Drop the re-quote and the "V5 below is what discharges it" forward pointer. State the source-isolation requirement and proceed to V5a, which discharges it on its own terms.

### Issue 2: V5's trailing sentence is a downstream-consumer inventory
**ASN-0069, V5**: "V5a applies equally in both directions after the fork; V10(b) and V12 carry the two context-specific instantiations."

**Problem**: This is the flagged pattern of a property's statement enumerating its later use-sites ("V10(b) and V12 carry the instantiations"). It adds no reasoning to V5; the instantiations are already made where they are needed (V10(b), V12), and those sites already cite V5a. The sentence will rot as use-sites move.

**Required**: Delete the sentence. Let V10(b) and V12 cite V5a at their point of use, as they already do.

### Issue 3: V8's "perpetual" paragraph re-derives permanence that V12 formally collects
**ASN-0069, V8 (closing paragraph)**: "The intercomparison guarantee is *perpetual*. By T8 (AllocationPermanence, ASN-0034), `d_src` and `d_new` remain in `E_doc` forever; by P0/S0, their I-addresses persist in `dom(C)` forever..."

**Problem**: The permanence machinery (T8 → entities persist; P0/S0 → addresses persist) is stated here and then enumerated again formally in V12(a)/(b). The same premises are walked twice in different sections to reach two phrasings of the same permanence fact.

**Required**: State only the V8-specific conclusion (correspondence survives in every subsequent state where neither side has overwritten the V-positions) and cite the permanence facts once — either lean on the foundations directly without the prose re-derivation, or fold the perpetuity statement into V12 where the same citations live.

## OUT_OF_SCOPE

None. The open questions correctly route concurrency, version-space presentation, link projection, and value-equality correspondence to future ASNs.

VERDICT: REVISE
